from common.db_connection import execute_query

# ═══════════════════════════════════════════
# USER QUERIES
# ═══════════════════════════════════════════

def get_user_by_username(username):
    return execute_query("SELECT * FROM users WHERE username = ?", (username,), fetchone=True)

def get_user_by_id(user_id):
    return execute_query("SELECT * FROM users WHERE id = ?", (user_id,), fetchone=True)

def get_user_by_email(email):
    return execute_query("SELECT * FROM users WHERE email = ?", (email,), fetchone=True)

def create_user(username, password_hash, full_name, email, phone, role):
    return execute_query(
        "INSERT INTO users (username, password_hash, full_name, email, phone, role) VALUES (?,?,?,?,?,?)",
        (username, password_hash, full_name, email, phone, role), commit=True
    )

def update_user(user_id, full_name, email, phone):
    return execute_query(
        "UPDATE users SET full_name=?, email=?, phone=? WHERE id=?",
        (full_name, email, phone, user_id), commit=True
    )

def get_all_managers():
    return execute_query("SELECT * FROM users WHERE role='manager'", fetchall=True)

def deactivate_user(user_id):
    return execute_query("UPDATE users SET is_active=0 WHERE id=?", (user_id,), commit=True)

def activate_user(user_id):
    return execute_query("UPDATE users SET is_active=1 WHERE id=?", (user_id,), commit=True)

# ═══════════════════════════════════════════
# PLAN QUERIES (admin creates)
# ═══════════════════════════════════════════

def get_all_plans(active_only=True):
    if active_only:
        return execute_query("SELECT * FROM plans WHERE is_active=1", fetchall=True)
    return execute_query("SELECT * FROM plans", fetchall=True)

def get_plan_by_id(plan_id):
    return execute_query("SELECT * FROM plans WHERE id=?", (plan_id,), fetchone=True)

def create_plan(name, description, price, duration_months):
    return execute_query(
        "INSERT INTO plans (plan_name, description, price, duration_months) VALUES (?,?,?,?)",
        (name, description, price, duration_months), commit=True
    )

def update_plan(plan_id, name, description, price, duration_months):
    return execute_query(
        "UPDATE plans SET plan_name=?, description=?, price=?, duration_months=? WHERE id=?",
        (name, description, price, duration_months, plan_id), commit=True
    )

def deactivate_plan(plan_id):
    return execute_query("UPDATE plans SET is_active=0 WHERE id=?", (plan_id,), commit=True)

# ═══════════════════════════════════════════
# GYM QUERIES
# ═══════════════════════════════════════════

def get_all_approved_gyms():
    return execute_query("SELECT * FROM gyms WHERE is_approved=1 AND is_active=1", fetchall=True)

def get_gym_by_id(gym_id):
    return execute_query("SELECT * FROM gyms WHERE id=?", (gym_id,), fetchone=True)

def get_gym_by_manager(manager_id):
    return execute_query("SELECT * FROM gyms WHERE manager_id=?", (manager_id,), fetchone=True)

def get_all_gyms():
    return execute_query("SELECT * FROM gyms", fetchall=True)

def create_gym(manager_id, gym_name, address, city, phone, email, about, contact_info, base_price, plan_id, plan_expiry):
    return execute_query(
        """INSERT INTO gyms (manager_id, gym_name, address, city, phone, email, about, contact_info, base_price, plan_id, plan_expiry)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (manager_id, gym_name, address, city, phone, email, about, contact_info, base_price, plan_id, plan_expiry),
        commit=True
    )

def update_gym_profile(gym_id, gym_name, address, city, phone, email, about, contact_info, base_price):
    return execute_query(
        "UPDATE gyms SET gym_name=?, address=?, city=?, phone=?, email=?, about=?, contact_info=?, base_price=? WHERE id=?",
        (gym_name, address, city, phone, email, about, contact_info, base_price, gym_id), commit=True
    )

def approve_gym(gym_id):
    return execute_query("UPDATE gyms SET is_approved=1 WHERE id=?", (gym_id,), commit=True)

def reject_gym(gym_id):
    return execute_query("UPDATE gyms SET is_approved=0, is_active=0 WHERE id=?", (gym_id,), commit=True)

# ═══════════════════════════════════════════
# MANAGER SUBSCRIPTION QUERIES
# ═══════════════════════════════════════════

def get_manager_subscription(manager_id):
    return execute_query(
        "SELECT ms.*, p.plan_name FROM manager_subscriptions ms JOIN plans p ON ms.plan_id=p.id WHERE ms.manager_id=? AND ms.status='active'",
        (manager_id,), fetchone=True
    )

def create_manager_subscription(manager_id, plan_id, start_date, expiry_date, amount_paid):
    return execute_query(
        "INSERT INTO manager_subscriptions (manager_id, plan_id, start_date, expiry_date, amount_paid) VALUES (?,?,?,?,?)",
        (manager_id, plan_id, start_date, expiry_date, amount_paid), commit=True
    )

# ═══════════════════════════════════════════
# TRAINER QUERIES
# ═══════════════════════════════════════════

def get_trainers_by_gym(gym_id, available_only=False):
    if available_only:
        return execute_query("SELECT * FROM trainers WHERE gym_id=? AND is_available=1", (gym_id,), fetchall=True)
    return execute_query("SELECT * FROM trainers WHERE gym_id=?", (gym_id,), fetchall=True)

def get_trainer_by_id(trainer_id):
    return execute_query("SELECT * FROM trainers WHERE id=?", (trainer_id,), fetchone=True)

def add_trainer(gym_id, full_name, specialization, experience_yrs, monthly_fee):
    return execute_query(
        "INSERT INTO trainers (gym_id, full_name, specialization, experience_yrs, monthly_fee) VALUES (?,?,?,?,?)",
        (gym_id, full_name, specialization, experience_yrs, monthly_fee), commit=True
    )

def update_trainer(trainer_id, full_name, specialization, experience_yrs, monthly_fee):
    return execute_query(
        "UPDATE trainers SET full_name=?, specialization=?, experience_yrs=?, monthly_fee=? WHERE id=?",
        (full_name, specialization, experience_yrs, monthly_fee, trainer_id), commit=True
    )

def delete_trainer(trainer_id):
    return execute_query("DELETE FROM trainers WHERE id=?", (trainer_id,), commit=True)

# ═══════════════════════════════════════════
# SLOT QUERIES
# ═══════════════════════════════════════════

def get_slots_by_gym(gym_id):
    return execute_query("SELECT * FROM slots WHERE gym_id=? AND is_active=1", (gym_id,), fetchall=True)

def get_slot_by_id(slot_id):
    return execute_query("SELECT * FROM slots WHERE id=?", (slot_id,), fetchone=True)

def add_slot(gym_id, slot_name, start_time, end_time, capacity):
    return execute_query(
        "INSERT INTO slots (gym_id, slot_name, start_time, end_time, capacity) VALUES (?,?,?,?,?)",
        (gym_id, slot_name, start_time, end_time, capacity), commit=True
    )

def update_slot(slot_id, slot_name, start_time, end_time, capacity):
    return execute_query(
        "UPDATE slots SET slot_name=?, start_time=?, end_time=?, capacity=? WHERE id=?",
        (slot_name, start_time, end_time, capacity, slot_id), commit=True
    )

def delete_slot(slot_id):
    return execute_query("UPDATE slots SET is_active=0 WHERE id=?", (slot_id,), commit=True)

# ═══════════════════════════════════════════
# EQUIPMENT QUERIES
# ═══════════════════════════════════════════

def get_equipment_by_gym(gym_id):
    return execute_query("SELECT * FROM equipment WHERE gym_id=?", (gym_id,), fetchall=True)

def add_equipment(gym_id, name, quantity, condition):
    return execute_query(
        "INSERT INTO equipment (gym_id, name, quantity, condition) VALUES (?,?,?,?)",
        (gym_id, name, quantity, condition), commit=True
    )

def update_equipment(eq_id, name, quantity, condition):
    return execute_query(
        "UPDATE equipment SET name=?, quantity=?, condition=? WHERE id=?",
        (name, quantity, condition, eq_id), commit=True
    )

def delete_equipment(eq_id):
    return execute_query("DELETE FROM equipment WHERE id=?", (eq_id,), commit=True)

# ═══════════════════════════════════════════
# DIET PLAN QUERIES
# ═══════════════════════════════════════════

def get_dietplans_by_gym(gym_id):
    return execute_query("SELECT * FROM dietplans WHERE gym_id=?", (gym_id,), fetchall=True)

def add_dietplan(gym_id, title, description, goal):
    return execute_query(
        "INSERT INTO dietplans (gym_id, title, description, goal) VALUES (?,?,?,?)",
        (gym_id, title, description, goal), commit=True
    )

def update_dietplan(dp_id, title, description, goal):
    return execute_query(
        "UPDATE dietplans SET title=?, description=?, goal=? WHERE id=?",
        (title, description, goal, dp_id), commit=True
    )

def delete_dietplan(dp_id):
    return execute_query("DELETE FROM dietplans WHERE id=?", (dp_id,), commit=True)

# ═══════════════════════════════════════════
# BOOKING QUERIES
# ═══════════════════════════════════════════

def create_booking(customer_id, gym_id, slot_id, trainer_id, duration_key, training_type, start_date, expiry_date):
    return execute_query(
        """INSERT INTO bookings
           (customer_id, gym_id, slot_id, trainer_id, duration_key, training_type, start_date, expiry_date)
           VALUES (?,?,?,?,?,?,?,?)""",
        (customer_id, gym_id, slot_id, trainer_id, duration_key, training_type, start_date, expiry_date),
        commit=True
    )

def get_bookings_by_customer(customer_id):
    return execute_query(
        """SELECT b.*, g.gym_name, s.slot_name, s.start_time, s.end_time,
                  t.full_name AS trainer_name
           FROM bookings b
           JOIN gyms g ON b.gym_id=g.id
           JOIN slots s ON b.slot_id=s.id
           LEFT JOIN trainers t ON b.trainer_id=t.id
           WHERE b.customer_id=?
           ORDER BY b.created_at DESC""",
        (customer_id,), fetchall=True
    )

def get_bookings_by_gym(gym_id):
    return execute_query(
        """SELECT b.*, u.full_name AS customer_name, s.slot_name,
                  t.full_name AS trainer_name
           FROM bookings b
           JOIN users u ON b.customer_id=u.id
           JOIN slots s ON b.slot_id=s.id
           LEFT JOIN trainers t ON b.trainer_id=t.id
           WHERE b.gym_id=?
           ORDER BY b.created_at DESC""",
        (gym_id,), fetchall=True
    )

def cancel_booking(booking_id):
    return execute_query("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,), commit=True)

def get_active_booking_count_for_slot(slot_id):
    result = execute_query(
        "SELECT COUNT(*) as count FROM bookings WHERE slot_id=? AND status='active'",
        (slot_id,), fetchone=True
    )
    return result['count'] if result else 0

# ═══════════════════════════════════════════
# PAYMENT QUERIES
# ═══════════════════════════════════════════

def create_payment(booking_id, customer_id, gym_id, membership_cost, trainer_cost, total_amount, payment_method):
    return execute_query(
        """INSERT INTO payments
           (booking_id, customer_id, gym_id, membership_cost, trainer_cost, total_amount, payment_method)
           VALUES (?,?,?,?,?,?,?)""",
        (booking_id, customer_id, gym_id, membership_cost, trainer_cost, total_amount, payment_method),
        commit=True
    )

def get_payments_by_customer(customer_id):
    return execute_query(
        "SELECT p.*, g.gym_name FROM payments p JOIN gyms g ON p.gym_id=g.id WHERE p.customer_id=?",
        (customer_id,), fetchall=True
    )

def get_payments_by_gym(gym_id):
    return execute_query(
        "SELECT p.*, u.full_name AS customer_name FROM payments p JOIN users u ON p.customer_id=u.id WHERE p.gym_id=?",
        (gym_id,), fetchall=True
    )

# ═══════════════════════════════════════════
# MEMBERSHIP QUERIES
# ═══════════════════════════════════════════

def create_membership(customer_id, gym_id, booking_id, membership_type, start_date, expiry_date):
    return execute_query(
        "INSERT INTO memberships (customer_id, gym_id, booking_id, membership_type, start_date, expiry_date) VALUES (?,?,?,?,?,?)",
        (customer_id, gym_id, booking_id, membership_type, start_date, expiry_date), commit=True
    )

def get_memberships_by_customer(customer_id):
    return execute_query(
        """SELECT m.*, g.gym_name FROM memberships m JOIN gyms g ON m.gym_id=g.id
           WHERE m.customer_id=? ORDER BY m.start_date DESC""",
        (customer_id,), fetchall=True
    )

def cancel_membership_by_booking(booking_id):
    return execute_query("UPDATE memberships SET is_active=0 WHERE booking_id=?", (booking_id,), commit=True)

# ═══════════════════════════════════════════
# FEEDBACK QUERIES
# ═══════════════════════════════════════════

def submit_feedback(customer_id, gym_id, subject, message, rating):
    return execute_query(
        "INSERT INTO feedback (customer_id, gym_id, subject, message, rating) VALUES (?,?,?,?,?)",
        (customer_id, gym_id, subject, message, rating), commit=True
    )

def get_all_feedback():
    return execute_query(
        """SELECT f.*, u.full_name AS customer_name, g.gym_name
           FROM feedback f
           JOIN users u ON f.customer_id=u.id
           LEFT JOIN gyms g ON f.gym_id=g.id
           ORDER BY f.created_at DESC""",
        fetchall=True
    )

def get_feedback_by_gym(gym_id):
    return execute_query(
        """SELECT f.*, u.full_name AS customer_name
           FROM feedback f JOIN users u ON f.customer_id=u.id
           WHERE f.gym_id=?""",
        (gym_id,), fetchall=True
    )
