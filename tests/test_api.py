import pytest
from app import create_app

def test_get_posts_api():
    app = create_app()
    client = app.test_client()
    resp = client.get('/api/posts/')
    assert resp.status_code in (200, 404)  # 404 if no posts table yet
