import pytest
from app import create_app, db
from models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_user_profile_fields(app):
    with app.app_context():
        user = User(username='profileuser', email='profile@example.com', bio='Bio', avatar='avatar.png')
        db.session.add(user)
        db.session.commit()
        u = User.query.filter_by(username='profileuser').first()
        assert u.bio == 'Bio'
        assert u.avatar == 'avatar.png'
