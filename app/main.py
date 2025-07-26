from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
import logging
from datetime import datetime

from .models import Base, URL
from .utils import generate_short_code, is_valid_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./urls.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="URL Shortener",
    description="A complete URL shortening service with analytics",
    version="1.0.0"
)

# Middleware & Exception Handlers
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------------------
#          ROUTES BELOW
# --------------------------------

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the URL Shortener API. Visit /docs for Swagger UI or use /shorten to shorten URLs."
    }

@app.get("/favicon.ico")
def favicon():
    return JSONResponse(status_code=204, content=None)

@app.get("/health")
def health_check():
    logger.debug("Health check requested")
    return {"status": "healthy", "service": "URL Shortener"}

@app.post("/shorten")
@limiter.limit("10/minute")
def shorten_url(request: Request, url: str, db: Session = Depends(get_db)):
    logger.info(f"Shortening URL: {url}")
    if not is_valid_url(url):
        logger.warning(f"Invalid URL provided: {url}")
        raise HTTPException(status_code=400, detail="Invalid URL")

    existing = db.query(URL).filter(URL.original_url == url).first()
    if existing:
        short_url = str(request.base_url) + existing.short_code
        logger.info(f"Returning existing short URL: {short_url}")
        return {"short_url": short_url}

    while True:
        code = generate_short_code()
        if not db.query(URL).filter(URL.short_code == code).first():
            break

    new_url = URL(original_url=url, short_code=code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    short_url = str(request.base_url) + code
    logger.info(f"Created new short URL: {short_url} for {url}")
    return {"short_url": short_url}

@app.get("/api/stats/{short_code}")
@limiter.limit("30/minute")
def get_stats(request: Request, short_code: str, db: Session = Depends(get_db)):
    logger.info(f"Stats request for short code: {short_code}")
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        return {
            "url": url.original_url,
            "clicks": url.click_count,
            "created_at": url.created_at.isoformat()
        }
    logger.warning(f"Stats requested for non-existent short code: {short_code}")
    raise HTTPException(status_code=404, detail="URL not found")

@app.get("/{short_code}")
@limiter.limit("100/minute")
def redirect_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    logger.info(f"Redirect request for short code: {short_code}")
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        url.click_count += 1
        db.commit()
        logger.info(f"Redirecting {short_code} to {url.original_url} (clicks: {url.click_count})")

        user_agent = request.headers.get("user-agent", "").lower()
        accept = request.headers.get("accept", "").lower()
        if "swagger" in user_agent or "application/json" in accept:
            return {"message": "Redirect would go to:", "target_url": url.original_url}
        return RedirectResponse(url.original_url)

    logger.warning(f"Short code not found: {short_code}")
    raise HTTPException(status_code=404, detail="URL not found")
