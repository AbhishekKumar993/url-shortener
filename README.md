---

<h1 align="center">🔗 URL Shortener</h1>
<p align="center">A simple and fast URL shortening service, like <strong>bit.ly</strong> or <strong>tinyurl</strong>, built with <code>FastAPI</code> + <code>SQLite</code></p>
---

📦 Features

✅ Shorten long URLs
🔁 Redirect to original URLs
📊 Track clicks and created time
🧪 Fully tested
📄 Swagger UI for APIs
🛡️ Rate limiting
⚙️ Health check endpoint
🧳 Production-ready (Docker, CORS, Logging)


---

🛠️ Tech Stack

Tool	Use

FastAPI	Web framework
SQLite	Lightweight local database
SQLAlchemy	ORM for DB models
Pydantic	Input/output validation
SlowAPI	Rate limiting
Uvicorn	ASGI server
Pytest	Testing framework



---

🚀 Getting Started (Local)

🔧 1. Install Dependencies

pip install -r requirements.txt

▶️ 2. Run the Server

uvicorn app.main:app --reload

Now open: http://localhost:8000/docs to see Swagger UI

🧪 3. Run Tests

pytest -v


---

📁 Project Structure

url-shortener/
├── app/
│   ├── main.py          # App entrypoint
│   ├── database.py      # DB connection
│   ├── models.py        # DB Models
│   ├── crud.py          # Core logic
│   ├── schemas.py       # Pydantic schemas
│   └── utils.py         # Helper functions
├── tests/               # Test cases
├── requirements.txt     # Python dependencies
└── README.md            # Project guide


---

🌐 API Endpoints

🔹 1. Shorten a URL

POST /shorten?url=https://example.com

Response:

{
  "short_url": "http://localhost:8000/abc123"
}


---

🔹 2. Redirect

GET /abc123

Redirects to the original URL and tracks the click.


---

🔹 3. Stats

GET /api/stats/abc123

Response:

{
  "url": "https://example.com",
  "clicks": 5,
  "created_at": "2024-01-01T10:00:00"
}


---

🔹 4. Health Check

GET /health

Response:

{
  "status": "healthy",
  "service": "URL Shortener"
}


---

🧪 Testing Coverage

✅ Shorten & Redirect
✅ Duplicate URLs
✅ URL Validation
✅ Analytics
✅ Rate Limiting
✅ Error Handling
✅ Swagger UI Compatibility


---

🧬 Database Schema

urls (
  id INTEGER PRIMARY KEY,
  original_url TEXT NOT NULL,
  short_code TEXT UNIQUE NOT NULL,
  click_count INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)


---

⚙️ Environment Variables

Variable	Description	Default

DATABASE_URL	SQLite database connection	sqlite:///urls.db
LOG_LEVEL	Logging level	INFO
PORT	Server port (e.g. for deployment)	8000



---

💡 Example Commands

# Shorten a URL
curl -X POST "http://localhost:8000/shorten?url=https://youtube.com"

# Use the short URL
curl -L "http://localhost:8000/abc123"

# Check stats
curl "http://localhost:8000/api/stats/abc123"

# Health check
curl "http://localhost:8000/health"


---

📄 License

Licensed under the MIT License — Free to use and modify.


---
