from common.helpers import print_header, pause, print_divider
from common.auth import get_user_id
from common.validations import is_non_empty, is_valid_email, is_valid_phone, is_positive_number
from database.queries import get_gym_by_manager, update_gym_profile

def view_gym_profile():
    print_header("MY GYM PROFILE")
    manager_id = get_user_id()
    gym = get_gym_by_manager(manager_id)
    if not gym:
        print("  No gym enrolled yet.")
        pause()
        return
    print(f"  Gym Name     : {gym['gym_name']}")
    print(f"  Address      : {gym['address']}, {gym['city']}")
    print(f"  Phone        : {gym['phone']}")
    print(f"  Email        : {gym['email']}")
    print(f"  Base Price   : Rs. {gym['base_price']} / month")
    print(f"  About        : {gym['about']}")
    print(f"  Contact Info : {gym['contact_info']}")
    status_text = 'Approved' if gym['is_approved'] else ('Rejected' if gym['is_active'] == 0 else 'Pending Approval')
    print(f"  Status       : {status_text}")
    print(f"  Plan Expiry  : {gym['plan_expiry']}")
    print_divider()
    pause()

def edit_gym_profile():
    print_header("EDIT GYM PROFILE")
    manager_id = get_user_id()
    gym = get_gym_by_manager(manager_id)
    if not gym:
        print("  No gym found.")
        pause()
        return
    print("  (Press Enter to keep current value)\n")
    gym_name = input(f"  Gym Name [{gym['gym_name']}]: ").strip() or gym["gym_name"]
    address = input(f"  Address [{gym['address']}]: ").strip() or gym["address"]
    city = input(f"  City [{gym['city']}]: ").strip() or gym["city"]
    phone = input(f"  Phone [{gym['phone']}]: ").strip() or gym["phone"]
    email = input(f"  Email [{gym['email']}]: ").strip() or gym["email"]
    about = input(f"  About [{gym['about']}]: ").strip() or gym["about"]
    contact = input(f"  Contact Info [{gym['contact_info']}]: ").strip() or gym["contact_info"]
    price_str = input(f"  Base Price [{gym['base_price']}]: ").strip()
    base_price = float(price_str) if price_str else gym["base_price"]

    update_gym_profile(gym["id"], gym_name, address, city, phone, email, about, contact, base_price)
    print("\n  [SUCCESS] Gym profile updated.")
    pause()

def gym_profile_menu():
    while True:
        print_header("GYM PROFILE")
        print("  1. View Gym Profile")
        print("  2. Edit Gym Profile")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_gym_profile()
        elif choice == "2":
            edit_gym_profile()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
