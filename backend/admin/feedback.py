from common.helpers import print_header, print_table, pause
from database.queries import get_all_feedback, get_feedback_by_gym
from database.queries import get_all_approved_gyms

def view_all_feedback():
    print_header("ALL CUSTOMER FEEDBACK")
    feedbacks = get_all_feedback()
    if not feedbacks:
        print("  No feedback found.")
        pause()
        return
    print_table(feedbacks, ["id", "customer_name", "gym_name", "subject", "rating", "created_at"])
    print("\n  --- FEEDBACK DETAILS ---")
    try:
        fid = int(input("  Enter Feedback ID to view details (0 to skip): "))
        if fid != 0:
            fb = next((f for f in feedbacks if f["id"] == fid), None)
            if fb:
                print(f"\n  From    : {fb['customer_name']}")
                print(f"  Gym     : {fb.get('gym_name', 'General')}")
                print(f"  Subject : {fb['subject']}")
                print(f"  Rating  : {fb['rating']}/5")
                print(f"  Message : {fb['message']}")
                print(f"  Date    : {fb['created_at']}")
    except ValueError:
        pass
    pause()

def view_feedback_by_gym():
    print_header("FEEDBACK BY GYM")
    gyms = get_all_approved_gyms()
    if not gyms:
        print("  No gyms found.")
        pause()
        return
    print_table(gyms, ["id", "gym_name", "city"])
    try:
        gym_id = int(input("\n  Enter Gym ID: "))
    except ValueError:
        print("  Invalid ID.")
        pause()
        return
    feedbacks = get_feedback_by_gym(gym_id)
    if not feedbacks:
        print("  No feedback for this gym.")
    else:
        print_table(feedbacks, ["id", "customer_name", "subject", "rating", "created_at"])
        for fb in feedbacks:
            print(f"\n  [{fb['rating']}/5] {fb['subject']} - {fb['customer_name']}")
            print(f"  {fb['message']}")
    pause()

def feedback_menu():
    while True:
        print_header("FEEDBACK SYSTEM")
        print("  1. View All Feedback")
        print("  2. View Feedback by Gym")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            view_all_feedback()
        elif choice == "2":
            view_feedback_by_gym()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
