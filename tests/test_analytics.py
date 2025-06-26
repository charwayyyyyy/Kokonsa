import pytest
from app import create_app, db
from models import User, Post, PostAnalytics

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

def test_post_analytics(app):
    with app.app_context():
        user = User(username='d', email='d@d.com')
        post = Post(title='T', content='C', author=user)
        db.session.add_all([user, post])
        db.session.commit()
        analytics = PostAnalytics(post_id=post.id, user_id=user.id, views=1)
        db.session.add(analytics)
        db.session.commit()
        a = PostAnalytics.query.filter_by(post_id=post.id, user_id=user.id).first()
        assert a.views == 1
