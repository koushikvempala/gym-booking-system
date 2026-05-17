from common.helpers import print_header, print_divider
from database.queries import (
    get_all_managers, get_all_gyms, get_all_plans, get_all_feedback
)

def show_admin_dashboard():
    print_header("ADMIN DASHBOARD")
    managers = get_all_managers() or []
    gyms     = get_all_gyms() or []
    plans    = get_all_plans(active_only=False) or []
    feedback = get_all_feedback() or []

    approved = [g for g in gyms if g["is_approved"] == 1]
    pending  = [g for g in gyms if g["is_approved"] == 0 and g["is_active"] == 1]

    print(f"  Total Managers        : {len(managers)}")
    print(f"  Total Gyms Enrolled   : {len(gyms)}")
    print(f"    - Approved          : {len(approved)}")
    print(f"    - Pending Approval  : {len(pending)}")
    print(f"  Total Plans           : {len(plans)}")
    print(f"  Total Feedback        : {len(feedback)}")
    print_divider()
