<h1 align="center">🔗 URL Shortener</h1>

<p align="center">
  A clean, minimalist, and functional URL shortening service built with <strong>FastAPI</strong> and <strong>SQLite</strong> — inspired by Bitly and TinyURL.
</p>

---

## 🌟 Features

- 🔗 **Shorten Long URLs** into 6-character short codes
- 🚦 **Redirect** users automatically to the original URL
- 📊 **Analytics Tracking**: Click counts and timestamps
- 🔒 **Rate Limiting** to prevent abuse
- 🧪 **Test Coverage** with `pytest`
- 🧰 **Swagger UI** at `/docs` for API exploration
- 🌍 **CORS** Enabled for cross-origin access

---

## 🛠️ Tech Stack

- 🚀 **FastAPI** – High-performance Python web framework
- 🗃️ **SQLite** – Simple, file-based relational DB
- 🧠 **SQLAlchemy** – ORM for DB management
- 🔐 **SlowAPI** – Per-IP rate limiting
- 🧪 **Pytest** – Testing framework
- ⚡ **Uvicorn** – ASGI server

---

## 💻 Local Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the development server
uvicorn app.main:app --reload

# 3. Run the test suite
pytest -v

## 📁 Directory Structure

url-shortener/
├── app/
│   ├── main.py        # FastAPI application entry point
│   ├── models.py      # SQLAlchemy ORM models
│   └── utils.py       # Helper functions (e.g., short code generator, URL validator)
├── requirements.txt   # Python dependencies
├── urls.db            # SQLite database file (auto-created at runtime)
└── README.md          # Project documentation
