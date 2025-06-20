"""Test user credentials for different roles in the Kokonsa blog platform."""

TEST_USERS = {
    'admin': {
        'username': 'admin',
        'email': 'admin@kokonsa.com',
        'password': 'admin123',
        'is_admin': True,
        'is_active': True
    },
    'moderator': {
        'username': 'moderator',
        'email': 'moderator@kokonsa.com',
        'password': 'mod123',
        'is_admin': False,
        'is_active': True,
        'can_moderate': True
    },
    'active_user': {
        'username': 'blogger',
        'email': 'blogger@kokonsa.com',
        'password': 'blog123',
        'is_admin': False,
        'is_active': True
    },
    'inactive_user': {
        'username': 'pending',
        'email': 'pending@kokonsa.com',
        'password': 'pending123',
        'is_admin': False,
        'is_active': False
    }
}

def get_test_user(role):
    """Get test user credentials by role.
    
    Args:
        role (str): The role of the test user ('admin', 'moderator', 'active_user', 'inactive_user')
        
    Returns:
        dict: User credentials and properties
    """
    return TEST_USERS.get(role, None)