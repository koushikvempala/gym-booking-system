from common.helpers import print_header, pause, print_table
from common.auth import get_user_id
from common.validations import is_non_empty
from database.queries import (
    get_all_approved_gyms, submit_feedback, get_feedback_by_gym
)

def submit_customer_feedback():
    print_header("SUBMIT FEEDBACK")
    customer_id = get_user_id()

    # Optional: pick a gym
    gyms = get_all_approved_gyms()
    gym_id = None
    if gyms:
        print("  Which gym are you giving feedback for?")
        print_table(gyms, ["id", "gym_name", "city"])
        try:
            gid = input("\n  Enter Gym ID (0 for general feedback): ").strip()
            if gid != "0":
                gym_id = int(gid)
        except ValueError:
            gym_id = None

    while True:
        subject = input("  Subject: ").strip()
        if is_non_empty(subject, "Subject"):
            break

    while True:
        message = input("  Message: ").strip()
        if is_non_empty(message, "Message"):
            break

    while True:
        try:
            rating = int(input("  Rating (1-5): ").strip())
            if 1 <= rating <= 5:
                break
            print("  Rating must be 1-5.")
        except ValueError:
            print("  Enter a number between 1 and 5.")

    fid = submit_feedback(customer_id, gym_id, subject, message, rating)
    if fid:
        print("\n  [SUCCESS] Feedback submitted. Thank you!")
    else:
        print("  [ERROR] Failed to submit feedback.")
    pause()

def view_gym_feedback():
    print_header("GYM FEEDBACK / REVIEWS")
    gyms = get_all_approved_gyms()
    if not gyms:
        print("  No gyms found.")
        pause()
        return
    print_table(gyms, ["id", "gym_name", "city"])
    try:
        gym_id = int(input("\n  Enter Gym ID: "))
    except ValueError:
        print("  Invalid.")
        pause()
        return
    feedback = get_feedback_by_gym(gym_id)
    if not feedback:
        print("  No feedback for this gym yet.")
    else:
        for fb in feedback:
            print(f"\n  [{fb['rating']}/5] {fb['subject']} - by {fb['customer_name']}")
            print(f"  {fb['message']}")
    pause()

def feedback_menu():
    while True:
        print_header("FEEDBACK")
        print("  1. Submit Feedback")
        print("  2. View Gym Reviews")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            submit_customer_feedback()
        elif choice == "2":
            view_gym_feedback()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
