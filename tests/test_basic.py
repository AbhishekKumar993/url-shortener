import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_shorten_and_redirect():
    """Test basic URL shortening and redirect functionality"""
    url = "https://www.example.com"
    response = client.post("/shorten", params={"url": url})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    short_url = data["short_url"]
    code = short_url.rsplit("/", 1)[-1]
    # Test redirect
    resp = client.get(f"/{code}", follow_redirects=False)
    assert resp.status_code == 307 or resp.status_code == 302
    assert resp.headers["location"] == url

def test_invalid_url():
    """Test URL validation"""
    response = client.post("/shorten", params={"url": "not-a-url"})
    assert response.status_code == 400
    assert "Invalid URL" in response.json()["detail"]

def test_duplicate_url():
    """Test that same URL returns same short code"""
    url = "https://www.example.com/duplicate"
    # First request
    response1 = client.post("/shorten", params={"url": url})
    assert response1.status_code == 200
    data1 = response1.json()
    
    # Second request with same URL
    response2 = client.post("/shorten", params={"url": url})
    assert response2.status_code == 200
    data2 = response2.json()
    
    # Should return same short URL
    assert data1["short_url"] == data2["short_url"]

def test_analytics():
    """Test analytics endpoint"""
    url = "https://www.example.com/analytics"
    # Create short URL
    response = client.post("/shorten", params={"url": url})
    assert response.status_code == 200
    data = response.json()
    code = data["short_url"].rsplit("/", 1)[-1]
    
    # Get initial stats
    stats_response = client.get(f"/api/stats/{code}")
    assert stats_response.status_code == 200
    stats = stats_response.json()
    assert stats["url"] == url
    initial_clicks = stats["clicks"]  # Get the current click count
    assert "created_at" in stats
    
    # Visit the URL to increment clicks
    client.get(f"/{code}")
    
    # Check updated stats
    updated_stats = client.get(f"/api/stats/{code}").json()
    assert updated_stats["clicks"] >= initial_clicks + 1

def test_nonexistent_short_code():
    """Test handling of non-existent short codes"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert "URL not found" in response.json()["detail"]
    
    # Test analytics for non-existent code
    stats_response = client.get("/api/stats/nonexistent")
    assert stats_response.status_code == 404
    assert "URL not found" in stats_response.json()["detail"]

def test_swagger_ui_compatibility():
    """Test that Swagger UI gets JSON response instead of redirect"""
    url = "https://www.example.com/swagger"
    response = client.post("/shorten", params={"url": url})
    assert response.status_code == 200
    data = response.json()
    code = data["short_url"].rsplit("/", 1)[-1]
    
    # Simulate Swagger UI request with Accept: application/json
    headers = {"accept": "application/json"}
    resp = client.get(f"/{code}", headers=headers)
    assert resp.status_code == 200
    json_data = resp.json()
    assert "message" in json_data
    assert "target_url" in json_data
    assert json_data["target_url"] == url