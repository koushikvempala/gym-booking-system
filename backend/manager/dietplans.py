from common.helpers import print_header, print_table, pause, confirm_action
from common.auth import get_user_id
from common.validations import is_non_empty
from database.queries import (
    get_gym_by_manager, get_dietplans_by_gym,
    add_dietplan, update_dietplan, delete_dietplan
)
from common.db_connection import execute_query

def _get_gym():
    gym = get_gym_by_manager(get_user_id())
    if not gym:
        print("  [ERROR] No gym enrolled.")
        pause()
    return gym

def view_dietplans():
    print_header("DIET PLANS")
    gym = _get_gym()
    if not gym:
        return
    plans = get_dietplans_by_gym(gym["id"])
    if not plans:
        print("  No diet plans yet.")
    else:
        for p in plans:
            print(f"\n  [{p['id']}] {p['title']} | Goal: {p['goal']}")
            print(f"       {p['description']}")
    pause()

def add_new_dietplan():
    print_header("ADD DIET PLAN")
    gym = _get_gym()
    if not gym:
        return
    while True:
        title = input("  Title: ").strip()
        if is_non_empty(title, "Title"):
            break
    description = input("  Description: ").strip()
    goal = input("  Goal (e.g. Fat Loss, Muscle Gain): ").strip()
    did = add_dietplan(gym["id"], title, description, goal)
    if did:
        print(f"  [SUCCESS] Diet plan '{title}' added.")
    else:
        print("  [ERROR] Failed.")
    pause()

def edit_dietplan():
    print_header("EDIT DIET PLAN")
    gym = _get_gym()
    if not gym:
        return
    plans = get_dietplans_by_gym(gym["id"])
    if not plans:
        print("  No diet plans found.")
        pause()
        return
    print_table(plans, ["id", "title", "goal"])
    try:
        did = int(input("\n  Enter Diet Plan ID to edit: "))
    except ValueError:
        print("  Invalid.")
        pause()
        return
    dp = execute_query("SELECT * FROM dietplans WHERE id=?", (did,), fetchone=True)
    if not dp or dp["gym_id"] != gym["id"]:
        print("  [ERROR] Not found.")
        pause()
        return
    title = input(f"  Title [{dp['title']}]: ").strip() or dp["title"]
    desc = input(f"  Description [{dp['description']}]: ").strip() or dp["description"]
    goal = input(f"  Goal [{dp['goal']}]: ").strip() or dp["goal"]
    update_dietplan(did, title, desc, goal)
    print("  [SUCCESS] Updated.")
    pause()

def remove_dietplan():
    print_header("REMOVE DIET PLAN")
    gym = _get_gym()
    if not gym:
        return
    plans = get_dietplans_by_gym(gym["id"])
    if not plans:
        print("  No diet plans.")
        pause()
        return
    print_table(plans, ["id", "title", "goal"])
    try:
        did = int(input("\n  Enter Diet Plan ID to remove: "))
    except ValueError:
        print("  Invalid.")
        pause()
        return
    dp = execute_query("SELECT * FROM dietplans WHERE id=?", (did,), fetchone=True)
    if not dp or dp["gym_id"] != gym["id"]:
        print("  [ERROR] Not found.")
        pause()
        return
    if confirm_action(f"  Remove '{dp['title']}'? (y/n): "):
        delete_dietplan(did)
        print("  [SUCCESS] Removed.")
    pause()

def dietplans_menu():
    while True:
        print_header("DIET PLANS")
        print("  1. View Diet Plans")
        print("  2. Add Diet Plan")
        print("  3. Edit Diet Plan")
        print("  4. Remove Diet Plan")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_dietplans()
        elif choice == "2":
            add_new_dietplan()
        elif choice == "3":
            edit_dietplan()
        elif choice == "4":
            remove_dietplan()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
