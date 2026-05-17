from common.helpers import print_header, print_table, pause
from common.auth import get_user_id
from database.queries import get_gym_by_manager, get_bookings_by_gym, get_payments_by_gym

def view_bookings():
    print_header("GYM BOOKINGS")
    gym = get_gym_by_manager(get_user_id())
    if not gym:
        print("  No gym enrolled.")
        pause()
        return
    bookings = get_bookings_by_gym(gym["id"])
    if not bookings:
        print("  No bookings yet.")
    else:
        print(f"  Total Bookings: {len(bookings)}\n")
        print_table(bookings, [
            "id", "customer_name", "slot_name", "training_type",
            "trainer_name", "duration_key", "start_date", "expiry_date", "status"
        ])
    pause()

def view_payments():
    print_header("GYM PAYMENTS")
    gym = get_gym_by_manager(get_user_id())
    if not gym:
        print("  No gym enrolled.")
        pause()
        return
    payments = get_payments_by_gym(gym["id"])
    if not payments:
        print("  No payments yet.")
    else:
        total = sum(p["total_amount"] or 0 for p in payments)
        print(f"  Total Revenue: Rs. {round(total, 2)}\n")
        print_table(payments, [
            "id", "customer_name", "membership_cost",
            "trainer_cost", "total_amount", "payment_method", "paid_at"
        ])
    pause()

def bookings_menu():
    while True:
        print_header("BOOKINGS & PAYMENTS")
        print("  1. View All Bookings")
        print("  2. View Payments / Revenue")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_bookings()
        elif choice == "2":
            view_payments()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
