from common.helpers import print_header, pause, print_divider
from common.auth import get_user_id
from common.validations import is_valid_email, is_valid_phone, is_non_empty
from database.queries import get_user_by_id, update_user

def view_profile():
    print_header("MY PROFILE")
    user = get_user_by_id(get_user_id())
    if not user:
        print("  User not found.")
        pause()
        return
    print(f"  Username   : {user['username']}")
    print(f"  Full Name  : {user['full_name']}")
    print(f"  Email      : {user['email']}")
    print(f"  Phone      : {user['phone']}")
    print(f"  Member Since: {user['created_at']}")
    print_divider()
    pause()

def edit_profile():
    print_header("EDIT PROFILE")
    user = get_user_by_id(get_user_id())
    if not user:
        print("  User not found.")
        pause()
        return
    print("  (Press Enter to keep current value)\n")
    full_name = input(f"  Full Name [{user['full_name']}]: ").strip() or user["full_name"]
    while True:
        email = input(f"  Email [{user['email']}]: ").strip() or user["email"]
        if is_valid_email(email):
            break
    while True:
        phone = input(f"  Phone [{user['phone']}]: ").strip() or user["phone"]
        if is_valid_phone(phone):
            break
    update_user(user["id"], full_name, email, phone)
    print("  [SUCCESS] Profile updated.")
    pause()

def profile_menu():
    while True:
        print_header("MY PROFILE")
        print("  1. View Profile")
        print("  2. Edit Profile")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_profile()
        elif choice == "2":
            edit_profile()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
