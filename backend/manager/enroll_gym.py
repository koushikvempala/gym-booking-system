from common.helpers import print_header, pause, print_table
from common.auth import get_user_id
from common.validations import is_non_empty, is_valid_email, is_valid_phone, is_positive_number
from common.helpers import today_str, add_months
from database.queries import (
    get_all_plans, get_plan_by_id, get_gym_by_manager,
    create_gym, create_manager_subscription, get_manager_subscription
)

def view_admin_plans():
    print_header("AVAILABLE PLANS FROM ADMIN")
    plans = get_all_plans(active_only=True)
    if not plans:
        print("  No plans available.")
    else:
        print_table(plans, ["id", "plan_name", "description", "price", "duration_months"])
    pause()

def subscribe_to_plan():
    print_header("SUBSCRIBE TO ADMIN PLAN")
    manager_id = get_user_id()
    existing = get_manager_subscription(manager_id)
    if existing:
        print(f"  [INFO] You already have an active subscription: {existing['plan_name']}")
        print(f"         Expires: {existing['expiry_date']}")
        pause()
        return

    plans = get_all_plans(active_only=True)
    if not plans:
        print("  No plans available.")
        pause()
        return
    print_table(plans, ["id", "plan_name", "description", "price", "duration_months"])
    try:
        plan_id = int(input("\n  Select Plan ID: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    plan = get_plan_by_id(plan_id)
    if not plan:
        print("  [ERROR] Plan not found.")
        pause()
        return

    print(f"\n  Plan    : {plan['plan_name']}")
    print(f"  Price   : Rs. {plan['price']}")
    print(f"  Duration: {plan['duration_months']} months")
    print("\n  Payment Methods: 1.Cash  2.Card  3.UPI")
    method = input("  Choose payment method (1/2/3): ").strip()
    method_map = {"1": "cash", "2": "card", "3": "upi"}
    pay_method = method_map.get(method, "cash")

    today = today_str()
    expiry = add_months(today, plan["duration_months"])
    sub_id = create_manager_subscription(manager_id, plan_id, today, expiry, plan["price"])
    if sub_id:
        print(f"\n  [SUCCESS] Subscribed to '{plan['plan_name']}' via {pay_method}.")
        print(f"  Valid from {today} to {expiry}.")
    else:
        print("  [ERROR] Subscription failed.")
    pause()

def enroll_gym():
    print_header("ENROLL GYM")
    manager_id = get_user_id()

    # Check subscription
    sub = get_manager_subscription(manager_id)
    if not sub:
        print("  [ERROR] You must subscribe to a plan before enrolling your gym.")
        print("  Please go to 'Subscribe to Plan' first.")
        pause()
        return

    # Check if already enrolled
    existing = get_gym_by_manager(manager_id)
    if existing:
        print(f"  [INFO] You have already enrolled '{existing['gym_name']}'.")
        print(f"         Status: {'Approved' if existing['is_approved'] else 'Pending Approval'}")
        pause()
        return

    print("  Fill in your gym details:\n")
    while True:
        gym_name = input("  Gym Name: ").strip()
        if is_non_empty(gym_name, "Gym Name"):
            break
    while True:
        address = input("  Address: ").strip()
        if is_non_empty(address, "Address"):
            break
    while True:
        city = input("  City: ").strip()
        if is_non_empty(city, "City"):
            break
    while True:
        phone = input("  Gym Phone (10 digits): ").strip()
        if is_valid_phone(phone):
            break
    while True:
        email = input("  Gym Email: ").strip()
        if is_valid_email(email):
            break
    about = input("  About Your Gym: ").strip()
    contact_info = input("  Contact Info (shown to customers): ").strip()
    while True:
        price_str = input("  Base Monthly Membership Price (Rs): ").strip()
        if is_positive_number(price_str, "Base Price"):
            break

    gym_id = create_gym(
        manager_id, gym_name, address, city, phone, email, about,
        contact_info, float(price_str), sub["plan_id"], sub["expiry_date"]
    )
    if gym_id:
        print(f"\n  [SUCCESS] Gym '{gym_name}' enrolled with ID: {gym_id}")
        print("  Awaiting admin approval.")
    else:
        print("  [ERROR] Enrollment failed.")
    pause()

def enroll_menu():
    while True:
        print_header("GYM ENROLLMENT")
        print("  1. View Admin Plans")
        print("  2. Subscribe to a Plan")
        print("  3. Enroll My Gym")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_admin_plans()
        elif choice == "2":
            subscribe_to_plan()
        elif choice == "3":
            enroll_gym()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
