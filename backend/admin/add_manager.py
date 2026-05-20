from common.helpers import print_header, pause
from common.auth import hash_password
from common.validations import (
    is_non_empty, is_valid_email, is_valid_phone, is_valid_password, is_valid_username
)
from database.queries import get_user_by_username, get_user_by_email, create_user

def admin_add_manager():
    print_header("ADD NEW MANAGER")

    # Username
    while True:
        username = input("  Enter username: ").strip()
        if not is_valid_username(username):
            continue
        if get_user_by_username(username):
            print("  [ERROR] Username already exists.")
            continue
        break

    # Full name
    while True:
        full_name = input("  Enter full name: ").strip()
        if is_non_empty(full_name, "Full Name"):
            break

    # Email
    while True:
        email = input("  Enter email: ").strip()
        if not is_valid_email(email):
            continue
        if get_user_by_email(email):
            print("  [ERROR] Email already registered.")
            continue
        break

    # Phone
    while True:
        phone = input("  Enter phone: ").strip()
        if is_valid_phone(phone):
            break

    # Password
    while True:
        password = input("  Enter password: ").strip()
        if is_valid_password(password):
            break

    password_hash = hash_password(password)
    uid = create_user(username, password_hash, full_name, email, phone, "manager")

    if uid:
        print(f"\n  [SUCCESS] Manager '{full_name}' added with ID: {uid}")
    else:
        print("\n  [ERROR] Failed to add manager.")
    pause()
