import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.db_connection import execute_query, get_connection
from common.auth import hash_password
from common.helpers import today_str, add_months

def insert_dummy_data():
    print("[SEED] Inserting dummy data...")

    # ─── MANAGER USERS ───
    manager_pass = hash_password("manager@123")
    m1 = execute_query(
        "INSERT OR IGNORE INTO users (username, password_hash, full_name, email, phone, role) VALUES (?,?,?,?,?,?)",
        ("manager1", manager_pass, "Ravi Kumar", "ravi@gym.com", "9876543210", "manager"),
        commit=True
    )
    m2 = execute_query(
        "INSERT OR IGNORE INTO users (username, password_hash, full_name, email, phone, role) VALUES (?,?,?,?,?,?)",
        ("manager2", manager_pass, "Priya Sharma", "priya@gym.com", "9876543211", "manager"),
        commit=True
    )

    # ─── CUSTOMER USERS ───
    cust_pass = hash_password("customer@123")
    c1 = execute_query(
        "INSERT OR IGNORE INTO users (username, password_hash, full_name, email, phone, role) VALUES (?,?,?,?,?,?)",
        ("customer1", cust_pass, "Arun Vel", "arun@mail.com", "9123456789", "customer"),
        commit=True
    )
    c2 = execute_query(
        "INSERT OR IGNORE INTO users (username, password_hash, full_name, email, phone, role) VALUES (?,?,?,?,?,?)",
        ("customer2", cust_pass, "Meena R", "meena@mail.com", "9123456780", "customer"),
        commit=True
    )

    # ─── ADMIN PLANS ───
    p1 = execute_query(
        "INSERT OR IGNORE INTO plans (plan_name, description, price, duration_months) VALUES (?,?,?,?)",
        ("Basic Plan", "List 1 gym, basic features", 999.00, 1),
        commit=True
    )
    p2 = execute_query(
        "INSERT OR IGNORE INTO plans (plan_name, description, price, duration_months) VALUES (?,?,?,?)",
        ("Standard Plan", "List up to 3 gyms, trainer management", 2499.00, 6),
        commit=True
    )
    p3 = execute_query(
        "INSERT OR IGNORE INTO plans (plan_name, description, price, duration_months) VALUES (?,?,?,?)",
        ("Premium Plan", "Unlimited gyms, all features, priority support", 4999.00, 12),
        commit=True
    )

    # ─── MANAGER SUBSCRIPTION ───
    today = today_str()
    expiry = add_months(today, 6)
    sub1 = execute_query(
        """INSERT OR IGNORE INTO manager_subscriptions
           (manager_id, plan_id, start_date, expiry_date, amount_paid, status)
           VALUES (?,?,?,?,?,?)""",
        (1, 2, today, expiry, 2499.00, "active"),
        commit=True
    )

    # ─── GYMS ───
    g1 = execute_query(
        """INSERT OR IGNORE INTO gyms
           (manager_id, gym_name, address, city, phone, email, about, contact_info, base_price, plan_id, plan_expiry, is_approved)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (1, "FitZone Chennai", "123 Anna Salai", "Chennai", "9876543210",
         "fitzone@gym.com", "Premier fitness center in Chennai",
         "Call us: 9876543210 | fitzone@gym.com", 1200.00, 2, expiry, 1),
        commit=True
    )
    g2 = execute_query(
        """INSERT OR IGNORE INTO gyms
           (manager_id, gym_name, address, city, phone, email, about, contact_info, base_price, plan_id, plan_expiry, is_approved)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (2, "PowerHouse Gym", "45 Velachery Road", "Chennai", "9876543211",
         "powerhouse@gym.com", "Heavy lifting and cardio specialists",
         "Call us: 9876543211 | powerhouse@gym.com", 1500.00, 1, add_months(today,1), 1),
        commit=True
    )

    # ─── TRAINERS ───
    execute_query(
        "INSERT OR IGNORE INTO trainers (gym_id, full_name, specialization, experience_yrs, monthly_fee) VALUES (?,?,?,?,?)",
        (1, "Karthik S", "Bodybuilding", 5, 800.00), commit=True
    )
    execute_query(
        "INSERT OR IGNORE INTO trainers (gym_id, full_name, specialization, experience_yrs, monthly_fee) VALUES (?,?,?,?,?)",
        (1, "Divya M", "Yoga & Flexibility", 3, 600.00), commit=True
    )
    execute_query(
        "INSERT OR IGNORE INTO trainers (gym_id, full_name, specialization, experience_yrs, monthly_fee) VALUES (?,?,?,?,?)",
        (2, "Suresh K", "Cardio & HIIT", 4, 700.00), commit=True
    )

    # ─── SLOTS ───
    execute_query(
        "INSERT OR IGNORE INTO slots (gym_id, slot_name, start_time, end_time, capacity) VALUES (?,?,?,?,?)",
        (1, "Morning", "06:00 AM", "08:00 AM", 15), commit=True
    )
    execute_query(
        "INSERT OR IGNORE INTO slots (gym_id, slot_name, start_time, end_time, capacity) VALUES (?,?,?,?,?)",
        (1, "Evening", "05:00 PM", "07:00 PM", 20), commit=True
    )
    execute_query(
        "INSERT OR IGNORE INTO slots (gym_id, slot_name, start_time, end_time, capacity) VALUES (?,?,?,?,?)",
        (2, "Morning", "06:00 AM", "08:00 AM", 10), commit=True
    )
    execute_query(
        "INSERT OR IGNORE INTO slots (gym_id, slot_name, start_time, end_time, capacity) VALUES (?,?,?,?,?)",
        (2, "Night", "08:00 PM", "10:00 PM", 12), commit=True
    )

    # ─── EQUIPMENT ───
    for item in [("Treadmill", 5, "Excellent"), ("Dumbbells Set", 10, "Good"), ("Bench Press", 4, "Good")]:
        execute_query(
            "INSERT OR IGNORE INTO equipment (gym_id, name, quantity, condition) VALUES (?,?,?,?)",
            (1, item[0], item[1], item[2]), commit=True
        )
    for item in [("Barbell", 8, "Good"), ("Pull-up Bar", 3, "Excellent"), ("Rowing Machine", 2, "Fair")]:
        execute_query(
            "INSERT OR IGNORE INTO equipment (gym_id, name, quantity, condition) VALUES (?,?,?,?)",
            (2, item[0], item[1], item[2]), commit=True
        )

    # ─── DIET PLANS ───
    execute_query(
        "INSERT OR IGNORE INTO dietplans (gym_id, title, description, goal) VALUES (?,?,?,?)",
        (1, "Weight Loss Diet", "Low carb, high protein meals with calorie deficit", "Fat Loss"),
        commit=True
    )
    execute_query(
        "INSERT OR IGNORE INTO dietplans (gym_id, title, description, goal) VALUES (?,?,?,?)",
        (1, "Muscle Gain Diet", "High protein, complex carbs, healthy fats", "Muscle Building"),
        commit=True
    )
    execute_query(
        "INSERT OR IGNORE INTO dietplans (gym_id, title, description, goal) VALUES (?,?,?,?)",
        (2, "Endurance Diet", "Carb-rich meals for long-duration workouts", "Stamina"),
        commit=True
    )

    # ─── FEEDBACK ───
    execute_query(
        "INSERT OR IGNORE INTO feedback (customer_id, gym_id, subject, message, rating) VALUES (?,?,?,?,?)",
        (3, 1, "Great Experience", "FitZone is amazing! Trainers are very helpful.", 5),
        commit=True
    )
    execute_query(
        "INSERT OR IGNORE INTO feedback (customer_id, gym_id, subject, message, rating) VALUES (?,?,?,?,?)",
        (4, 2, "Good Gym", "PowerHouse has good equipment but needs more slots.", 4),
        commit=True
    )

    print("[SEED] Dummy data inserted successfully.")
    print("\n  TEST ACCOUNTS:")
    print("  Admin    -> username: admin      | password: admin@123")
    print("  Manager1 -> username: manager1   | password: manager@123")
    print("  Manager2 -> username: manager2   | password: manager@123")
    print("  Customer1-> username: customer1  | password: customer@123")
    print("  Customer2-> username: customer2  | password: customer@123")

if __name__ == "__main__":
    insert_dummy_data()
