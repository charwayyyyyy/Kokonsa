import pytest
from app import create_app, db
from models import User, Post, Comment, CommentUpvote

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

def test_comment_upvote(app):
    with app.app_context():
        user = User(username='c', email='c@c.com')
        post = Post(title='T', content='C', author=user)
        db.session.add_all([user, post])
        db.session.commit()
        comment = Comment(content='Nice', author=user, post=post)
        db.session.add(comment)
        db.session.commit()
        upvote = CommentUpvote(user_id=user.id, comment_id=comment.id)
        db.session.add(upvote)
        db.session.commit()
        assert upvote in comment.comment_upvotes
