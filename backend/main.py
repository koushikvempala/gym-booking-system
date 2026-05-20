import sys
import os

# ─── Path Setup (so all imports work from any directory) ───
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# ─── DB Init ───
from database.create_tables import create_all_tables
from database.insert_dummy_data import insert_dummy_data
from common.db_connection import DB_PATH

def setup_database():
    """First-run setup: create tables and seed data if DB doesn't exist."""
    is_new = not os.path.exists(DB_PATH)
    create_all_tables()
    if is_new:
        print("[SETUP] New database detected. Inserting dummy data...")
        insert_dummy_data()

# ─── Auth ───
from common.auth import (
    admin_login, user_login, set_session, clear_session,
    get_role, is_logged_in, get_session
)
from common.helpers import print_header, pause

# ─── Admin Modules ───
from admin.dashboard import show_admin_dashboard
from admin.add_manager import admin_add_manager
from admin.manage_managers import manage_managers_menu
from admin.manage_plans import manage_plans_menu
from admin.approvals import approvals_menu
from admin.feedback import feedback_menu as admin_feedback_menu
from admin.reports import reports_menu

# ─── Manager Modules ───
from manager.enroll_gym import enroll_menu
from manager.gym_profile import gym_profile_menu
from manager.manage_trainers import manage_trainers_menu
from manager.manage_equipment import manage_equipment_menu
from manager.manage_slots import manage_slots_menu
from manager.bookings import bookings_menu
from manager.dietplans import dietplans_menu
from manager.register import manager_register

# ─── Customer Modules ───
from customer.register import customer_register
from customer.booking import customer_gym_menu
from customer.history import history_menu
from customer.feedback import feedback_menu as customer_feedback_menu
from customer.profile import profile_menu

# ═══════════════════════════════════════════════════════════
# LOGIN SCREENS
# ═══════════════════════════════════════════════════════════

def admin_login_screen():
    print_header("ADMIN LOGIN")
    username = input("  Username: ").strip()
    password = input("  Password: ").strip()
    user = admin_login(username, password)
    if user:
        set_session(user)
        print(f"\n  [SUCCESS] Welcome, Admin!")
        return True
    print("  [ERROR] Invalid admin credentials.")
    pause()
    return False

def user_login_screen():
    print_header("LOGIN (Customer / Manager)")
    username = input("  Username: ").strip()
    password = input("  Password: ").strip()
    user = user_login(username, password)
    if user:
        if not user.get("is_active", 1):
            print("  [ERROR] Your account is deactivated. Contact admin.")
            pause()
            return False
        set_session(user)
        print(f"\n  [SUCCESS] Welcome, {user['full_name']}!")
        return True
    pause()
    return False

# ═══════════════════════════════════════════════════════════
# ADMIN DASHBOARD MENU
# ═══════════════════════════════════════════════════════════

def admin_main_menu():
    while True:
        show_admin_dashboard()
        print("  1. Manage Managers")
        print("  2. Add Manager")
        print("  3. Manage Plans")
        print("  4. Gym Approvals")
        print("  5. View Feedback")
        print("  6. Reports")
        print("  0. Logout")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            manage_managers_menu()
        elif choice == "2":
            admin_add_manager()
        elif choice == "3":
            manage_plans_menu()
        elif choice == "4":
            approvals_menu()
        elif choice == "5":
            admin_feedback_menu()
        elif choice == "6":
            reports_menu()
        elif choice == "0":
            clear_session()
            print("  Logged out.")
            break
        else:
            print("  Invalid choice.")

# ═══════════════════════════════════════════════════════════
# MANAGER DASHBOARD MENU
# ═══════════════════════════════════════════════════════════

def manager_main_menu():
    user = get_session()
    while True:
        print_header(f"MANAGER DASHBOARD | {user.get('full_name', '')}")
        print("  1. Gym Enrollment & Plans")
        print("  2. Gym Profile")
        print("  3. Manage Trainers")
        print("  4. Manage Equipment")
        print("  5. Manage Slots")
        print("  6. Diet Plans")
        print("  7. View Bookings & Payments")
        print("  0. Logout")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            enroll_menu()
        elif choice == "2":
            gym_profile_menu()
        elif choice == "3":
            manage_trainers_menu()
        elif choice == "4":
            manage_equipment_menu()
        elif choice == "5":
            manage_slots_menu()
        elif choice == "6":
            dietplans_menu()
        elif choice == "7":
            bookings_menu()
        elif choice == "0":
            clear_session()
            print("  Logged out.")
            break
        else:
            print("  Invalid choice.")

# ═══════════════════════════════════════════════════════════
# CUSTOMER DASHBOARD MENU
# ═══════════════════════════════════════════════════════════

def customer_main_menu():
    user = get_session()
    while True:
        print_header(f"CUSTOMER HOME | {user.get('full_name', '')}")
        print("  1. Browse & Book Gyms")
        print("  2. My Bookings & History")
        print("  3. My Profile")
        print("  4. Feedback / Reviews")
        print("  0. Logout")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            customer_gym_menu()
        elif choice == "2":
            history_menu()
        elif choice == "3":
            profile_menu()
        elif choice == "4":
            customer_feedback_menu()
        elif choice == "0":
            clear_session()
            print("  Logged out.")
            break
        else:
            print("  Invalid choice.")

# ═══════════════════════════════════════════════════════════
# MAIN ENTRY
# ═══════════════════════════════════════════════════════════

def main():
    print("\n" + "=" * 50)
    print("   GYM BOOKING SYSTEM")
    print("   Powered by Python + SQLite3")
    print("=" * 50)
    setup_database()

    while True:
        print_header("MAIN MENU")
        print("  1. Admin Login")
        print("  2. Manager / Customer Login")
        print("  3. New Customer? Register Here")
        print("  4. New Manager? Register Here")
        print("  0. Exit")
        choice = input("\n  Enter choice: ").strip()

        if choice == "1":
            if admin_login_screen():
                admin_main_menu()

        elif choice == "2":
            if user_login_screen():
                role = get_role()
                if role == "manager":
                    manager_main_menu()
                elif role == "customer":
                    customer_main_menu()
                else:
                    print("  Unknown role. Logging out.")
                    clear_session()

        elif choice == "3":
            customer_register()

        elif choice == "4":
            manager_register()

        elif choice == "0":
            print("\n  Goodbye! See you at the gym!\n")
            break

        else:
            print("  Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
