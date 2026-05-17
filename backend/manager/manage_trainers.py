from common.helpers import print_header, print_table, pause, confirm_action
from common.auth import get_user_id
from common.validations import is_non_empty, is_positive_number
from database.queries import (
    get_gym_by_manager, get_trainers_by_gym,
    add_trainer, update_trainer, delete_trainer, get_trainer_by_id
)

def _get_gym_or_exit():
    gym = get_gym_by_manager(get_user_id())
    if not gym:
        print("  [ERROR] No gym enrolled.")
        pause()
    return gym

def view_trainers():
    print_header("MY TRAINERS")
    gym = _get_gym_or_exit()
    if not gym:
        return
    trainers = get_trainers_by_gym(gym["id"])
    if not trainers:
        print("  No trainers added yet.")
    else:
        print_table(trainers, ["id", "full_name", "specialization", "experience_yrs", "monthly_fee", "is_available"])
    pause()

def add_new_trainer():
    print_header("ADD TRAINER")
    gym = _get_gym_or_exit()
    if not gym:
        return
    while True:
        name = input("  Trainer Full Name: ").strip()
        if is_non_empty(name, "Name"):
            break
    specialization = input("  Specialization (e.g. Yoga, HIIT): ").strip()
    while True:
        exp = input("  Experience (years): ").strip()
        if is_positive_number(exp, "Experience"):
            break
    while True:
        fee = input("  Monthly Fee (Rs): ").strip()
        if is_positive_number(fee, "Monthly Fee"):
            break
    tid = add_trainer(gym["id"], name, specialization, int(exp), float(fee))
    if tid:
        print(f"\n  [SUCCESS] Trainer '{name}' added with ID: {tid}")
    else:
        print("  [ERROR] Failed to add trainer.")
    pause()

def edit_trainer():
    print_header("EDIT TRAINER")
    gym = _get_gym_or_exit()
    if not gym:
        return
    trainers = get_trainers_by_gym(gym["id"])
    if not trainers:
        print("  No trainers found.")
        pause()
        return
    print_table(trainers, ["id", "full_name", "specialization", "monthly_fee"])
    try:
        tid = int(input("\n  Enter Trainer ID to edit: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    trainer = get_trainer_by_id(tid)
    if not trainer or trainer["gym_id"] != gym["id"]:
        print("  [ERROR] Trainer not found.")
        pause()
        return
    print("  (Press Enter to keep current value)\n")
    name = input(f"  Name [{trainer['full_name']}]: ").strip() or trainer["full_name"]
    spec = input(f"  Specialization [{trainer['specialization']}]: ").strip() or trainer["specialization"]
    exp_s = input(f"  Experience [{trainer['experience_yrs']}]: ").strip()
    exp = int(exp_s) if exp_s else trainer["experience_yrs"]
    fee_s = input(f"  Monthly Fee [{trainer['monthly_fee']}]: ").strip()
    fee = float(fee_s) if fee_s else trainer["monthly_fee"]
    update_trainer(tid, name, spec, exp, fee)
    print("  [SUCCESS] Trainer updated.")
    pause()

def remove_trainer():
    print_header("REMOVE TRAINER")
    gym = _get_gym_or_exit()
    if not gym:
        return
    trainers = get_trainers_by_gym(gym["id"])
    if not trainers:
        print("  No trainers found.")
        pause()
        return
    print_table(trainers, ["id", "full_name", "specialization"])
    try:
        tid = int(input("\n  Enter Trainer ID to remove: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    trainer = get_trainer_by_id(tid)
    if not trainer or trainer["gym_id"] != gym["id"]:
        print("  [ERROR] Trainer not found.")
        pause()
        return
    if confirm_action(f"  Remove trainer '{trainer['full_name']}'? (y/n): "):
        delete_trainer(tid)
        print("  [SUCCESS] Trainer removed.")
    pause()

def manage_trainers_menu():
    while True:
        print_header("MANAGE TRAINERS")
        print("  1. View Trainers")
        print("  2. Add Trainer")
        print("  3. Edit Trainer")
        print("  4. Remove Trainer")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_trainers()
        elif choice == "2":
            add_new_trainer()
        elif choice == "3":
            edit_trainer()
        elif choice == "4":
            remove_trainer()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
