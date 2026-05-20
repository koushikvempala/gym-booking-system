from common.helpers import print_header, print_table, pause
from common.auth import get_user_id
from database.queries import (
    get_bookings_by_customer, get_payments_by_customer,
    get_memberships_by_customer, cancel_booking,
    cancel_membership_by_booking
)
from common.helpers import is_date_past
from datetime import datetime, timezone

def view_booking_history():
    print_header("MY BOOKING HISTORY")
    customer_id = get_user_id()
    bookings = get_bookings_by_customer(customer_id)
    if not bookings:
        print("  No bookings found.")
        pause()
        return
    print_table(bookings, [
        "id", "gym_name", "slot_name", "training_type",
        "trainer_name", "duration_key", "start_date", "expiry_date", "status"
    ])
    pause()

def view_payment_history():
    print_header("MY PAYMENT HISTORY")
    customer_id = get_user_id()
    payments = get_payments_by_customer(customer_id)
    if not payments:
        print("  No payments found.")
        pause()
        return

    for p in payments:
        if p.get("paid_at"):
            try:
                dt_utc = datetime.strptime(p["paid_at"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
                dt_local = dt_utc.astimezone()
                p["paid_at"] = dt_local.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass

    total = sum(p["total_amount"] or 0 for p in payments)
    print(f"  Total Spent: Rs. {round(total, 2)}\n")
    print_table(payments, [
        "id", "gym_name", "membership_cost", "trainer_cost",
        "total_amount", "payment_method", "paid_at"
    ])
    pause()

def view_memberships():
    print_header("MY MEMBERSHIPS")
    customer_id = get_user_id()
    memberships = get_memberships_by_customer(customer_id)
    if not memberships:
        print("  No memberships found.")
        pause()
        return
    for m in memberships:
        expired = is_date_past(m["expiry_date"])
        if m.get("is_active") == 0:
            status = "CANCELLED"
        elif expired:
            status = "EXPIRED"
        else:
            status = "ACTIVE"
        print(f"\n  [{m['id']}] {m['gym_name']}")
        print(f"       Type    : {m['membership_type'].capitalize()} Training")
        print(f"       From    : {m['start_date']}  To: {m['expiry_date']}")
        print(f"       Status  : {status}")
    pause()

def cancel_my_booking():
    print_header("CANCEL BOOKING")
    customer_id = get_user_id()
    bookings = get_bookings_by_customer(customer_id)
    active = [b for b in bookings if b["status"] == "active"]
    if not active:
        print("  No active bookings to cancel.")
        pause()
        return
    print_table(active, ["id", "gym_name", "slot_name", "start_date", "expiry_date"])
    try:
        bid = int(input("\n  Enter Booking ID to cancel: "))
    except ValueError:
        print("  Invalid.")
        pause()
        return
    booking = next((b for b in active if b["id"] == bid), None)
    if not booking:
        print("  Booking not found.")
        pause()
        return
    confirm = input(f"  Cancel booking at {booking['gym_name']}? (y/n): ").strip().lower()
    if confirm == "y":
        cancel_booking(bid)
        cancel_membership_by_booking(bid)
        print("  [SUCCESS] Booking cancelled.")
    pause()

def history_menu():
    while True:
        print_header("MY HISTORY")
        print("  1. Booking History")
        print("  2. Payment History")
        print("  3. My Memberships")
        print("  4. Cancel a Booking")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_booking_history()
        elif choice == "2":
            view_payment_history()
        elif choice == "3":
            view_memberships()
        elif choice == "4":
            cancel_my_booking()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
