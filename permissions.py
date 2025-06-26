from flask_login import current_user
from functools import wraps
from flask import abort

# Usage: @permission_required('edit_post')
def permission_required(permission_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if not current_user_has_permission(permission_name):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Helper to check if user has a permission

def current_user_has_permission(permission_name):
    if current_user.is_admin:
        return True
    for role in getattr(current_user, 'roles', []):
        for perm in getattr(role, 'permissions', []):
            if perm.name == permission_name:
                return True
    return False
