from common.helpers import print_header, print_table, pause, confirm_action
from common.validations import is_non_empty, is_positive_number
from database.queries import (
    get_all_plans, get_plan_by_id, create_plan, update_plan, deactivate_plan
)

def view_all_plans():
    print_header("ALL ADMIN PLANS")
    plans = get_all_plans(active_only=False)
    if not plans:
        print("  No plans found.")
    else:
        print_table(plans, ["id", "plan_name", "description", "price", "duration_months", "is_active"])
    pause()

def add_plan():
    print_header("ADD NEW PLAN")
    while True:
        name = input("  Plan Name: ").strip()
        if is_non_empty(name, "Plan Name"):
            break
    description = input("  Description: ").strip()
    while True:
        price_str = input("  Price (Rs): ").strip()
        if is_positive_number(price_str, "Price"):
            break
    while True:
        dur = input("  Duration (months): ").strip()
        if is_positive_number(dur, "Duration"):
            break
    pid = create_plan(name, description, float(price_str), int(dur))
    if pid:
        print(f"\n  [SUCCESS] Plan '{name}' created with ID: {pid}")
    else:
        print("  [ERROR] Failed to create plan.")
    pause()

def edit_plan():
    print_header("EDIT PLAN")
    view_all_plans()
    try:
        plan_id = int(input("  Enter Plan ID to edit: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    plan = get_plan_by_id(plan_id)
    if not plan:
        print("  [ERROR] Plan not found.")
        pause()
        return
    print(f"  Editing: {plan['plan_name']} | Price: {plan['price']} | Duration: {plan['duration_months']} months")
    name = input(f"  New Name [{plan['plan_name']}]: ").strip() or plan["plan_name"]
    description = input(f"  New Description [{plan['description']}]: ").strip() or plan["description"]
    price_str = input(f"  New Price [{plan['price']}]: ").strip()
    price = float(price_str) if price_str else plan["price"]
    dur_str = input(f"  New Duration months [{plan['duration_months']}]: ").strip()
    duration = int(dur_str) if dur_str else plan["duration_months"]
    update_plan(plan_id, name, description, price, duration)
    print("  [SUCCESS] Plan updated.")
    pause()

def delete_plan():
    print_header("DELETE (DEACTIVATE) PLAN")
    view_all_plans()
    try:
        plan_id = int(input("  Enter Plan ID to deactivate: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    plan = get_plan_by_id(plan_id)
    if not plan:
        print("  [ERROR] Plan not found.")
        pause()
        return
    if confirm_action(f"  Deactivate plan '{plan['plan_name']}'? (y/n): "):
        deactivate_plan(plan_id)
        print("  [SUCCESS] Plan deactivated.")
    pause()

def manage_plans_menu():
    while True:
        print_header("MANAGE PLANS")
        print("  1. View All Plans")
        print("  2. Add New Plan")
        print("  3. Edit Plan")
        print("  4. Deactivate Plan")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_all_plans()
        elif choice == "2":
            add_plan()
        elif choice == "3":
            edit_plan()
        elif choice == "4":
            delete_plan()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
