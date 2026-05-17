from common.helpers import print_header, print_table, print_divider, pause, confirm_action
from database.queries import get_all_managers, get_user_by_id, deactivate_user, activate_user, get_gym_by_manager

def view_all_managers():
    print_header("ALL MANAGERS")
    managers = get_all_managers()
    if not managers:
        print("  No managers found.")
        pause()
        return
    print_table(managers, ["id", "username", "full_name", "email", "phone", "is_active"])
    pause()

def toggle_manager_status():
    print_header("ACTIVATE / DEACTIVATE MANAGER")
    managers = get_all_managers()
    if not managers:
        print("  No managers found.")
        pause()
        return
    print_table(managers, ["id", "username", "full_name", "is_active"])
    try:
        manager_id = int(input("\n  Enter Manager ID: "))
    except ValueError:
        print("  [ERROR] Invalid ID.")
        pause()
        return
    manager = get_user_by_id(manager_id)
    if not manager or manager["role"] != "manager":
        print("  [ERROR] Manager not found.")
        pause()
        return
    current = manager["is_active"]
    action = "Deactivate" if current else "Activate"
    if confirm_action(f"  {action} '{manager['full_name']}'? (y/n): "):
        if current:
            deactivate_user(manager_id)
            print(f"  [SUCCESS] Manager deactivated.")
        else:
            activate_user(manager_id)
            print(f"  [SUCCESS] Manager activated.")
    pause()

def view_manager_details():
    print_header("MANAGER DETAILS")
    try:
        manager_id = int(input("  Enter Manager ID: "))
    except ValueError:
        print("  [ERROR] Invalid ID.")
        pause()
        return
    manager = get_user_by_id(manager_id)
    if not manager or manager["role"] != "manager":
        print("  [ERROR] Manager not found.")
        pause()
        return
    print(f"\n  ID         : {manager['id']}")
    print(f"  Username   : {manager['username']}")
    print(f"  Full Name  : {manager['full_name']}")
    print(f"  Email      : {manager['email']}")
    print(f"  Phone      : {manager['phone']}")
    print(f"  Status     : {'Active' if manager['is_active'] else 'Inactive'}")
    print(f"  Joined     : {manager['created_at']}")
    gym = get_gym_by_manager(manager_id)
    if gym:
        print(f"\n  GYM ENROLLED:")
        print(f"    Name     : {gym['gym_name']}")
        print(f"    City     : {gym['city']}")
        print(f"    Approved : {'Yes' if gym['is_approved'] else 'No'}")
    else:
        print("\n  No gym enrolled yet.")
    pause()

def manage_managers_menu():
    while True:
        print_header("MANAGE MANAGERS")
        print("  1. View All Managers")
        print("  2. View Manager Details")
        print("  3. Activate / Deactivate Manager")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_all_managers()
        elif choice == "2":
            view_manager_details()
        elif choice == "3":
            toggle_manager_status()
        elif choice == "0":
            break
        else:
            print("  [ERROR] Invalid choice.")
