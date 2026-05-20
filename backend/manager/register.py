from common.helpers import print_header, pause
from common.auth import hash_password
from common.validations import (
    is_valid_username, is_valid_email, is_valid_phone,
    is_valid_password, is_non_empty
)
from database.queries import get_user_by_username, get_user_by_email, create_user

def manager_register():
    print_header("MANAGER REGISTRATION")

    while True:
        username = input("  Choose a Username: ").strip()
        if not is_valid_username(username):
            continue
        if get_user_by_username(username):
            print("  [ERROR] Username already taken.")
            continue
        break

    while True:
        full_name = input("  Full Name: ").strip()
        if is_non_empty(full_name, "Full Name"):
            break

    while True:
        email = input("  Email: ").strip()
        if not is_valid_email(email):
            continue
        if get_user_by_email(email):
            print("  [ERROR] Email already registered.")
            continue
        break

    while True:
        phone = input("  Phone (10 digits): ").strip()
        if is_valid_phone(phone):
            break

    while True:
        password = input("  Password: ").strip()
        if not is_valid_password(password):
            continue
        confirm = input("  Confirm Password: ").strip()
        if password != confirm:
            print("  [ERROR] Passwords do not match.")
            continue
        break

    password_hash = hash_password(password)
    uid = create_user(username, password_hash, full_name, email, phone, "manager")
    if uid:
        print(f"\n  [SUCCESS] Manager Account created! Welcome, {full_name}.")
        print("  You can now login with your username and password.")
    else:
        print("  [ERROR] Registration failed.")
    pause()
