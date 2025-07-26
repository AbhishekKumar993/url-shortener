# URL Shortener Service

A complete URL shortening service built with FastAPI and SQLite, similar to bit.ly or tinyurl.

## Features

- **URL Shortening**: Convert long URLs to short codes
- **Redirects**: Automatic redirection to original URLs
- **Analytics**: Track click counts and creation timestamps
- **Swagger UI**: Interactive API documentation
- **Comprehensive Testing**: Full test coverage
- **Production Ready**: Docker support, logging, rate limiting, CORS
- **Health Monitoring**: Health check endpoint

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Run tests
pytest -v
```

## API Endpoints

### 1. Shorten URL
**POST** `/shorten?url=<long_url>`

Shortens a long URL to a 6-character code.

**Rate Limit**: 10 requests per minute

**Example:**
```bash
curl -X POST "http://localhost:8000/shorten?url=https://www.example.com/very/long/url"
```

**Response:**
```json
{
  "short_url": "http://localhost:8000/abc123"
}
```

### 2. Redirect
**GET** `/{short_code}`

Redirects to the original URL. Tracks clicks automatically.

**Rate Limit**: 100 requests per minute

**Example:**
```bash
curl -L "http://localhost:8000/abc123"
```

### 3. Analytics
**GET** `/api/stats/{short_code}`

Returns analytics for a short code.

**Rate Limit**: 30 requests per minute

**Example:**
```bash
curl "http://localhost:8000/api/stats/abc123"
```

**Response:**
```json
{
  "url": "https://www.example.com/very/long/url",
  "clicks": 5,
  "created_at": "2024-01-01T10:00:00"
}
```

### 4. Health Check
**GET** `/health`

Returns service health status for monitoring.

**Example:**
```bash
curl "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "service": "URL Shortener"
}
```

## Technical Features

- **URL Validation**: Ensures valid URLs before shortening
- **6-Character Codes**: Alphanumeric short codes
- **Click Tracking**: Automatic click counting
- **Creation Timestamps**: Track when URLs were created
- **Duplicate Handling**: Same URL returns same short code
- **Swagger UI Compatible**: JSON responses for API testing
- **SQLite Database**: Persistent storage
- **Comprehensive Error Handling**: Proper HTTP status codes
- **Rate Limiting**: Prevents API abuse
- **CORS Support**: Cross-origin request handling
- **Logging**: Comprehensive request and error logging


## Testing

Run the test suite:
```bash
pytest -v
```

**Test Coverage:**
- URL shortening and redirect functionality
- URL validation
- Duplicate URL handling
- Analytics tracking
- Error cases (invalid URLs, non-existent codes)
- Swagger UI compatibility
- Rate limiting

## Implementation Details

### Architecture
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Lightweight database
- **Pydantic**: Data validation
- **SlowAPI**: Rate limiting


### Database Schema
```sql
urls (
  id INTEGER PRIMARY KEY,
  original_url TEXT NOT NULL,
  short_code TEXT UNIQUE NOT NULL,
  click_count INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### Key Features
- **Thread-safe**: Handles concurrent requests
- **Scalable**: Easy to extend with additional features
- **Production-ready**: Proper error handling, validation, and monitoring
- **Developer-friendly**: Interactive API documentation


## Example Usage

```bash
# 1. Shorten a URL
curl -X POST "http://localhost:8000/shorten?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# 2. Use the short URL (redirects to YouTube)
curl -L "http://localhost:8000/abc123"

# 3. Check analytics
curl "http://localhost:8000/api/stats/abc123"

# 4. Check service health
curl "http://localhost:8000/health"
```

## Development

### Running in Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests
```bash
pytest -v
```

### Database
The SQLite database (`urls.db`) is created automatically on first run.


### Environment Variables
- `DATABASE_URL`: Database connection string (default: SQLite)
- `LOG_LEVEL`: Logging level (default: INFO)
- `PORT`: Port for the application (set by Heroku)

### Health Monitoring
The service includes a health check endpoint at `/health` for monitoring systems.

## License
MIT
