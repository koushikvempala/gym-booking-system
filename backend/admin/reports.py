from common.helpers import print_header, print_table, print_divider, pause
from common.db_connection import execute_query

def revenue_report():
    print_header("REVENUE REPORT")
    result = execute_query(
        """SELECT g.gym_name,
                  COUNT(p.id) AS total_payments,
                  SUM(p.total_amount) AS total_revenue
           FROM payments p
           JOIN gyms g ON p.gym_id=g.id
           GROUP BY p.gym_id""",
        fetchall=True
    )
    if not result:
        print("  No payment data found.")
    else:
        print_table(result, ["gym_name", "total_payments", "total_revenue"])
        total = sum(r["total_revenue"] or 0 for r in result)
        print(f"\n  PLATFORM TOTAL REVENUE: Rs. {round(total, 2)}")
    pause()

def bookings_report():
    print_header("BOOKINGS REPORT")
    result = execute_query(
        """SELECT g.gym_name,
                  COUNT(b.id) AS total_bookings,
                  SUM(CASE WHEN b.status='active' THEN 1 ELSE 0 END) AS active,
                  SUM(CASE WHEN b.status='cancelled' THEN 1 ELSE 0 END) AS cancelled
           FROM bookings b JOIN gyms g ON b.gym_id=g.id
           GROUP BY b.gym_id""",
        fetchall=True
    )
    if not result:
        print("  No booking data found.")
    else:
        print_table(result, ["gym_name", "total_bookings", "active", "cancelled"])
    pause()

def manager_subscription_report():
    print_header("MANAGER SUBSCRIPTIONS REPORT")
    result = execute_query(
        """SELECT u.full_name AS manager_name, p.plan_name, ms.amount_paid,
                  ms.start_date, ms.expiry_date, ms.status
           FROM manager_subscriptions ms
           JOIN users u ON ms.manager_id=u.id
           JOIN plans p ON ms.plan_id=p.id
           ORDER BY ms.created_at DESC""",
        fetchall=True
    )
    if not result:
        print("  No subscriptions found.")
    else:
        print_table(result, ["manager_name", "plan_name", "amount_paid", "start_date", "expiry_date", "status"])
        total = sum(r["amount_paid"] or 0 for r in result)
        print(f"\n  TOTAL SUBSCRIPTION REVENUE: Rs. {round(total, 2)}")
    pause()

def gym_summary_report():
    print_header("GYM SUMMARY REPORT")
    result = execute_query(
        """SELECT g.gym_name, g.city, g.is_approved,
                  COUNT(DISTINCT b.id) AS bookings,
                  COUNT(DISTINCT t.id) AS trainers,
                  COUNT(DISTINCT s.id) AS slots
           FROM gyms g
           LEFT JOIN bookings b ON b.gym_id=g.id
           LEFT JOIN trainers t ON t.gym_id=g.id
           LEFT JOIN slots s ON s.gym_id=g.id
           GROUP BY g.id""",
        fetchall=True
    )
    if not result:
        print("  No gym data.")
    else:
        print_table(result, ["gym_name", "city", "is_approved", "bookings", "trainers", "slots"])
    pause()

def reports_menu():
    while True:
        print_header("ADMIN REPORTS")
        print("  1. Revenue Report")
        print("  2. Bookings Report")
        print("  3. Manager Subscriptions Report")
        print("  4. Gym Summary Report")
        print("  0. Back")
        choice = input("\n  Enter choice: ").strip()
        if choice == "1":
            revenue_report()
        elif choice == "2":
            bookings_report()
        elif choice == "3":
            manager_subscription_report()
        elif choice == "4":
            gym_summary_report()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")
