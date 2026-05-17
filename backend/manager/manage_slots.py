from common.helpers import print_header, print_table, pause, confirm_action
from common.auth import get_user_id
from common.validations import is_non_empty, is_positive_number
from database.queries import (
    get_gym_by_manager, get_slots_by_gym,
    add_slot, update_slot, delete_slot, get_slot_by_id
)

def _get_gym():
    gym = get_gym_by_manager(get_user_id())
    if not gym:
        print("  [ERROR] No gym enrolled.")
        pause()
    return gym

def view_slots():
    print_header("GYM SLOTS")
    gym = _get_gym()
    if not gym:
        return
    slots = get_slots_by_gym(gym["id"])
    if not slots:
        print("  No slots configured yet.")
    else:
        print_table(slots, ["id", "slot_name", "start_time", "end_time", "capacity"])
    pause()

def add_new_slot():
    print_header("ADD SLOT")
    gym = _get_gym()
    if not gym:
        return
    while True:
        name = input("  Slot Name (e.g. Morning): ").strip()
        if is_non_empty(name, "Slot Name"):
            break
    start = input("  Start Time (e.g. 06:00 AM): ").strip()
    end = input("  End Time (e.g. 08:00 AM): ").strip()
    while True:
        cap = input("  Capacity (number of members): ").strip()
        if is_positive_number(cap, "Capacity"):
            break
    sid = add_slot(gym["id"], name, start, end, int(cap))
    if sid:
        print(f"  [SUCCESS] Slot '{name}' added.")
    else:
        print("  [ERROR] Failed.")
    pause()

def edit_slot():
    print_header("EDIT SLOT")
    gym = _get_gym()
    if not gym:
        return
    slots = get_slots_by_gym(gym["id"])
    if not slots:
        print("  No slots.")
        pause()
        return
    print_table(slots, ["id", "slot_name", "start_time", "end_time", "capacity"])
    try:
        sid = int(input("\n  Enter Slot ID to edit: "))
    except ValueError:
        print("  Invalid.")
        pause()
        return
    slot = get_slot_by_id(sid)
    if not slot or slot["gym_id"] != gym["id"]:
        print("  [ERROR] Slot not found.")
        pause()
        return
    name = input(f"  Name [{slot['slot_name']}]: ").strip() or slot["slot_name"]
    start = input(f"  Start [{slot['start_time']}]: ").strip() or slot["start_time"]
    end = input(f"  End [{slot['end_time']}]: ").strip() or slot["end_time"]
    cap_s = input(f"  Capacity [{slot['capacity']}]: ").strip()
    cap = int(cap_s) if cap_s else slot["capacity"]
    update_slot(sid, name, start, end, cap)
    print("  [SUCCESS] Slot updated.")
    pause()

def remove_slot():
    print_header("REMOVE SLOT")
    gym = _get_gym()
    if not gym:
        return
    slots = get_slots_by_gym(gym["id"])
    if not slots:
        print("  No slots.")
        pause()
        return
    print_table(slots, ["id", "slot_name", "start_time", "end_time"])
    try:
        sid = int(input("\n  Enter Slot ID to remove: "))
    except ValueError:
        print("  Invalid.")
        pause()
        return
    slot = get_slot_by_id(sid)
    if not slot or slot["gym_id"] != gym["id"]:
        print("  [ERROR] Slot not found.")
        pause()
        return
    if confirm_action(f"  Remove slot '{slot['slot_name']}'? (y/n): "):
        delete_slot(sid)
        print("  [SUCCESS] Slot removed.")
    pause()

def manage_slots_menu():
    while True:
        print_header("MANAGE SLOTS")
        print("  1. View Slots")
        print("  2. Add Slot")
        print("  3. Edit Slot")
        print("  4. Remove Slot")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_slots()
        elif choice == "2":
            add_new_slot()
        elif choice == "3":
            edit_slot()
        elif choice == "4":
            remove_slot()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
