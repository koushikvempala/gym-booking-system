from common.helpers import print_header, print_table, pause, print_divider
from common.auth import get_user_id
from common.calculations import (
    display_pricing_breakdown, get_expiry_date, DURATION_LABELS
)
from common.helpers import today_str
from database.queries import (
    get_all_approved_gyms, get_gym_by_id,
    get_slots_by_gym, get_trainers_by_gym,
    get_dietplans_by_gym, get_equipment_by_gym,
    create_booking, create_payment, create_membership,
    get_active_booking_count_for_slot
)

# ─────────────────────────────────────────────
# BROWSE GYMS
# ─────────────────────────────────────────────

def browse_gyms():
    print_header("GYM LIST")
    gyms = get_all_approved_gyms()
    if not gyms:
        print("  No gyms available.")
        pause()
        return None
    print_table(gyms, ["id", "gym_name", "city", "base_price"])
    return gyms

def view_gym_details(gym_id):
    gym = get_gym_by_id(gym_id)
    if not gym:
        print("  Gym not found.")
        pause()
        return
    print_header(f"GYM: {gym['gym_name']}")
    print(f"  Address     : {gym['address']}, {gym['city']}")
    print(f"  Phone       : {gym['phone']}")
    print(f"  Email       : {gym['email']}")
    print(f"  About       : {gym['about']}")
    print(f"  Contact     : {gym['contact_info']}")
    print(f"  Base Price  : Rs. {gym['base_price']} / month")
    print_divider()

    # Slots
    slots = get_slots_by_gym(gym_id)
    print("\n  AVAILABLE SLOTS:")
    if slots:
        print_table(slots, ["slot_name", "start_time", "end_time", "capacity"])
    else:
        print("  No slots available.")

    # Trainers
    trainers = get_trainers_by_gym(gym_id, available_only=True)
    print("\n  TRAINERS:")
    if trainers:
        print_table(trainers, ["id", "full_name", "specialization", "experience_yrs", "monthly_fee"])
    else:
        print("  No trainers available.")

    # Equipment
    equipment = get_equipment_by_gym(gym_id)
    print("\n  EQUIPMENT:")
    if equipment:
        print_table(equipment, ["name", "quantity", "condition"])
    else:
        print("  No equipment listed.")

    # Diet Plans
    diet = get_dietplans_by_gym(gym_id)
    print("\n  DIET PLANS:")
    if diet:
        for d in diet:
            print(f"  - {d['title']} | Goal: {d['goal']}")
    else:
        print("  No diet plans.")
    print_divider()
    pause()

# ─────────────────────────────────────────────
# BOOK GYM
# ─────────────────────────────────────────────

def book_gym():
    print_header("BOOK A GYM")
    customer_id = get_user_id()

    # Step 1: Select Gym
    gyms = get_all_approved_gyms()
    if not gyms:
        print("  No gyms available.")
        pause()
        return
    print_table(gyms, ["id", "gym_name", "city", "base_price"])
    try:
        gym_id = int(input("\n  Enter Gym ID to book (0 to cancel): "))
        if gym_id == 0:
            return
    except ValueError:
        print("  Invalid.")
        pause()
        return
    gym = get_gym_by_id(gym_id)
    if not gym:
        print("  Gym not found.")
        pause()
        return

    print(f"\n  Selected: {gym['gym_name']} - Rs. {gym['base_price']}/month")

    # Step 2: Select Slot
    slots = get_slots_by_gym(gym_id)
    if not slots:
        print("  No slots available for this gym.")
        pause()
        return

    # Calculate available capacity for each slot
    for s in slots:
        active_count = get_active_booking_count_for_slot(s["id"])
        s["available_capacity"] = s["capacity"] - active_count

    print("\n  SELECT SLOT:")
    print_table(slots, ["id", "slot_name", "start_time", "end_time", "available_capacity"])
    try:
        slot_id = int(input("  Enter Slot ID: "))
    except ValueError:
        print("  Invalid.")
        pause()
        return
    slot = next((s for s in slots if s["id"] == slot_id), None)
    if not slot:
        print("  Slot not found.")
        pause()
        return

    if slot["available_capacity"] <= 0:
        print("  [ERROR] This slot is fully booked. Please select another slot.")
        pause()
        return

    # Step 3: Training Type
    print("\n  TRAINING TYPE:")
    print("  1. Self Training")
    print("  2. With Trainer (extra charge)")
    train_choice = input("  Choose (1/2): ").strip()
    if train_choice not in ["1", "2"]:
        print("  Invalid choice.")
        pause()
        return

    with_trainer = train_choice == "2"
    trainer_id = None
    trainer_fee = 0

    if with_trainer:
        trainers = get_trainers_by_gym(gym_id, available_only=True)
        if not trainers:
            print("  No trainers available. Booking as self training.")
            with_trainer = False
        else:
            print("\n  SELECT TRAINER:")
            print_table(trainers, ["id", "full_name", "specialization", "experience_yrs", "monthly_fee"])
            try:
                trainer_id = int(input("  Enter Trainer ID: "))
            except ValueError:
                print("  Invalid.")
                pause()
                return
            trainer = next((t for t in trainers if t["id"] == trainer_id), None)
            if not trainer:
                print("  Trainer not found.")
                pause()
                return
            trainer_fee = trainer["monthly_fee"]

    # Step 4: Select Duration
    print("\n  SELECT DURATION:")
    print("  1. 1 Month")
    print("  2. 6 Months  (10% discount)")
    print("  3. 1 Year    (20% discount)")
    dur_choice = input("  Choose (1/2/3): ").strip()
    duration_map = {"1": "1month", "2": "6month", "3": "1year"}
    if dur_choice not in duration_map:
        print("  Invalid choice.")
        pause()
        return
    duration_key = duration_map[dur_choice]

    # Step 5: Show Cost Breakdown
    result = display_pricing_breakdown(
        gym["base_price"], duration_key, with_trainer, trainer_fee
    )

    # Step 6: Payment
    print("\n  PAYMENT METHOD:")
    print("  1. Cash")
    print("  2. Card")
    print("  3. UPI")
    pay_choice = input("  Choose (1/2/3): ").strip()
    method_map = {"1": "cash", "2": "card", "3": "upi"}
    payment_method = method_map.get(pay_choice, "cash")

    confirm = input(f"\n  Confirm booking for Rs. {result['total']}? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Booking cancelled.")
        pause()
        return

    # Step 7: Create Booking
    today = today_str()
    expiry = get_expiry_date(today, duration_key)
    training_type = "trainer" if with_trainer else "self"

    booking_id = create_booking(
        customer_id, gym_id, slot_id, trainer_id,
        duration_key, training_type, today, expiry
    )
    if not booking_id:
        print("  [ERROR] Booking failed.")
        pause()
        return

    # Step 8: Create Payment
    create_payment(
        booking_id, customer_id, gym_id,
        result["membership_cost"], result["trainer_cost"],
        result["total"], payment_method
    )

    # Step 9: Create Membership
    create_membership(
        customer_id, gym_id, booking_id,
        training_type, today, expiry
    )

    print(f"\n  ✓ BOOKING CONFIRMED!")
    print(f"  Gym       : {gym['gym_name']}")
    print(f"  Slot      : {slot['slot_name']} ({slot['start_time']} - {slot['end_time']})")
    print(f"  Duration  : {result['duration']}")
    print(f"  Type      : {training_type.capitalize()} Training")
    print(f"  Valid     : {today} to {expiry}")
    print(f"  Amount    : Rs. {result['total']} (via {payment_method})")
    print_divider()
    pause()

def customer_gym_menu():
    while True:
        print_header("GYM BOOKING")
        print("  1. Browse Gyms")
        print("  2. View Gym Details")
        print("  3. Book a Gym")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            browse_gyms()
            pause()
        elif choice == "2":
            gyms = browse_gyms()
            if gyms:
                try:
                    gid = int(input("  Enter Gym ID for details: "))
                    view_gym_details(gid)
                except ValueError:
                    print("  Invalid ID.")
        elif choice == "3":
            book_gym()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
