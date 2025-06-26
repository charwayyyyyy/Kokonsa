import pytest
from app import create_app, db
from models import User, Follow

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

def test_user_follow(app):
    with app.app_context():
        u1 = User(username='a', email='a@a.com')
        u2 = User(username='b', email='b@b.com')
        db.session.add_all([u1, u2])
        db.session.commit()
        follow = Follow(follower_id=u1.id, followed_id=u2.id)
        db.session.add(follow)
        db.session.commit()
        assert u2 in [f.followed for f in u1.following]
