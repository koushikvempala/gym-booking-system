from common.helpers import print_header, print_table, pause, confirm_action
from common.auth import get_user_id
from common.validations import is_non_empty, is_positive_number
from database.queries import (
    get_gym_by_manager, get_equipment_by_gym,
    add_equipment, update_equipment, delete_equipment
)
from common.db_connection import execute_query

def _get_gym():
    gym = get_gym_by_manager(get_user_id())
    if not gym:
        print("  [ERROR] No gym enrolled.")
        pause()
    return gym

def view_equipment():
    print_header("GYM EQUIPMENT")
    gym = _get_gym()
    if not gym:
        return
    items = get_equipment_by_gym(gym["id"])
    if not items:
        print("  No equipment listed yet.")
    else:
        print_table(items, ["id", "name", "quantity", "condition", "added_at"])
    pause()

def add_new_equipment():
    print_header("ADD EQUIPMENT")
    gym = _get_gym()
    if not gym:
        return
    while True:
        name = input("  Equipment Name: ").strip()
        if is_non_empty(name, "Name"):
            break
    while True:
        qty = input("  Quantity: ").strip()
        if is_positive_number(qty, "Quantity"):
            break
    condition = input("  Condition (Excellent/Good/Fair): ").strip() or "Good"
    eid = add_equipment(gym["id"], name, int(qty), condition)
    if eid:
        print(f"  [SUCCESS] Equipment '{name}' added.")
    else:
        print("  [ERROR] Failed.")
    pause()

def edit_equipment():
    print_header("EDIT EQUIPMENT")
    gym = _get_gym()
    if not gym:
        return
    items = get_equipment_by_gym(gym["id"])
    if not items:
        print("  No equipment found.")
        pause()
        return
    print_table(items, ["id", "name", "quantity", "condition"])
    try:
        eid = int(input("\n  Enter Equipment ID to edit: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    item = execute_query("SELECT * FROM equipment WHERE id=?", (eid,), fetchone=True)
    if not item or item["gym_id"] != gym["id"]:
        print("  [ERROR] Not found.")
        pause()
        return
    name = input(f"  Name [{item['name']}]: ").strip() or item["name"]
    qty_s = input(f"  Quantity [{item['quantity']}]: ").strip()
    qty = int(qty_s) if qty_s else item["quantity"]
    cond = input(f"  Condition [{item['condition']}]: ").strip() or item["condition"]
    update_equipment(eid, name, qty, cond)
    print("  [SUCCESS] Equipment updated.")
    pause()

def remove_equipment():
    print_header("REMOVE EQUIPMENT")
    gym = _get_gym()
    if not gym:
        return
    items = get_equipment_by_gym(gym["id"])
    if not items:
        print("  No equipment.")
        pause()
        return
    print_table(items, ["id", "name", "quantity"])
    try:
        eid = int(input("\n  Enter Equipment ID to remove: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    item = execute_query("SELECT * FROM equipment WHERE id=?", (eid,), fetchone=True)
    if not item or item["gym_id"] != gym["id"]:
        print("  [ERROR] Not found.")
        pause()
        return
    if confirm_action(f"  Remove '{item['name']}'? (y/n): "):
        delete_equipment(eid)
        print("  [SUCCESS] Removed.")
    pause()

def manage_equipment_menu():
    while True:
        print_header("MANAGE EQUIPMENT")
        print("  1. View Equipment")
        print("  2. Add Equipment")
        print("  3. Edit Equipment")
        print("  4. Remove Equipment")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_equipment()
        elif choice == "2":
            add_new_equipment()
        elif choice == "3":
            edit_equipment()
        elif choice == "4":
            remove_equipment()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
