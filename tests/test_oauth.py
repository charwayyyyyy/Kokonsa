import pytest
from app import create_app

def test_oauth_blueprints_registered():
    app = create_app()
    with app.app_context():
        # Check if OAuth blueprints are registered
        assert 'google' in app.blueprints
        assert 'github' in app.blueprints
        assert 'twitter' in app.blueprints
