import pytest
from app import create_app, db
from models import User, Role, Permission

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

def test_role_permission_assignment(app):
    with app.app_context():
        role = Role(name='editor')
        perm = Permission(name='edit_post')
        role.permissions.append(perm)
        user = User(username='testuser', email='test@example.com')
        user.roles.append(role)
        db.session.add_all([role, perm, user])
        db.session.commit()
        assert perm in user.roles[0].permissions
