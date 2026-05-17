from common.helpers import print_header, print_table, pause, confirm_action
from common.db_connection import execute_query
from database.queries import get_all_gyms, get_gym_by_id, approve_gym, reject_gym

def get_pending_gyms():
    return execute_query(
        """SELECT g.*, u.full_name AS manager_name, u.email AS manager_email
           FROM gyms g JOIN users u ON g.manager_id=u.id
           WHERE g.is_approved=0 AND g.is_active=1""",
        fetchall=True
    )

def view_pending_approvals():
    print_header("PENDING GYM APPROVALS")
    gyms = get_pending_gyms()
    if not gyms:
        print("  No pending approvals.")
        pause()
        return
    print_table(gyms, ["id", "gym_name", "city", "manager_name", "manager_email", "created_at"])
    pause()

def approve_or_reject_gym():
    print_header("APPROVE / REJECT GYM")
    gyms = get_pending_gyms()
    if not gyms:
        print("  No gyms pending approval.")
        pause()
        return
    print_table(gyms, ["id", "gym_name", "city", "manager_name"])
    try:
        gym_id = int(input("\n  Enter Gym ID: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    gym = get_gym_by_id(gym_id)
    if not gym:
        print("  [ERROR] Gym not found.")
        pause()
        return
    print(f"\n  Gym    : {gym['gym_name']}")
    print(f"  City   : {gym['city']}")
    print(f"  Address: {gym['address']}")
    print("\n  1. Approve")
    print("  2. Reject")
    print("  0. Cancel")
    action = input("  Choice: ").strip()
    if action == "1":
        approve_gym(gym_id)
        print(f"  [SUCCESS] '{gym['gym_name']}' APPROVED.")
    elif action == "2":
        if confirm_action("  Confirm reject? (y/n): "):
            reject_gym(gym_id)
            print(f"  [SUCCESS] '{gym['gym_name']}' REJECTED.")
    pause()

def view_all_gyms_admin():
    print_header("ALL GYMS")
    gyms = execute_query(
        """SELECT g.id, g.gym_name, g.city, g.is_approved, g.is_active,
                  u.full_name AS manager_name
           FROM gyms g JOIN users u ON g.manager_id=u.id""",
        fetchall=True
    )
    if not gyms:
        print("  No gyms found.")
    else:
        print_table(gyms, ["id", "gym_name", "city", "manager_name", "is_approved", "is_active"])
    pause()

def approvals_menu():
    while True:
        print_header("GYM APPROVALS")
        print("  1. View Pending Approvals")
        print("  2. Approve / Reject Gym")
        print("  3. View All Gyms")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_pending_approvals()
        elif choice == "2":
            approve_or_reject_gym()
        elif choice == "3":
            view_all_gyms_admin()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
