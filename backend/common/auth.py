import hashlib
import os
from common.db_connection import execute_query

# ─────────────────────────────────────────────
# PASSWORD HASHING (SHA-256 with salt)
# ─────────────────────────────────────────────

def hash_password(password):
    """Hash password with a random salt using SHA-256."""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(password, stored_hash):
    """Verify password against stored salt:hash."""
    try:
        salt, hashed = stored_hash.split(":")
        return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
    except Exception:
        return False

# ─────────────────────────────────────────────
# ADMIN AUTH (predefined credentials)
# ─────────────────────────────────────────────

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin@123"  # In real project, change this

def admin_login(username, password):
    """Validates admin credentials. Admin is predefined."""
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"id": 1, "username": "admin", "role": "admin"}
    return None

# ─────────────────────────────────────────────
# CUSTOMER / MANAGER LOGIN
# ─────────────────────────────────────────────

def user_login(username, password):
    """
    Login for both customers and managers.
    Returns user dict with role, or None if invalid.
    """
    user = execute_query(
        "SELECT * FROM users WHERE username = ?",
        (username,), fetchone=True
    )
    if not user:
        print("[AUTH] Username not found.")
        return None
    if not verify_password(password, user["password_hash"]):
        print("[AUTH] Incorrect password.")
        return None
    return user

# ─────────────────────────────────────────────
# SESSION (in-memory, for console app)
# ─────────────────────────────────────────────

_current_session = {}

def set_session(user):
    """Store logged-in user in memory."""
    global _current_session
    _current_session = user

def get_session():
    """Get current logged-in user."""
    return _current_session

def clear_session():
    """Logout."""
    global _current_session
    _current_session = {}

def is_logged_in():
    return bool(_current_session)

def get_role():
    return _current_session.get("role", None)

def get_user_id():
    return _current_session.get("id", None)
