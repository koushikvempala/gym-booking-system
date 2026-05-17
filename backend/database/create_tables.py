import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.db_connection import get_connection

TABLES = [

    # ─── USERS (Customers + Managers) ───
    """
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT    NOT NULL UNIQUE,
        password_hash TEXT  NOT NULL,
        full_name   TEXT    NOT NULL,
        email       TEXT    NOT NULL UNIQUE,
        phone       TEXT,
        role        TEXT    NOT NULL CHECK(role IN ('customer', 'manager')),
        is_active   INTEGER NOT NULL DEFAULT 1,
        created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,

    # ─── ADMINS (predefined, seeded at setup) ───
    """
    CREATE TABLE IF NOT EXISTS admins (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT    NOT NULL UNIQUE,
        password    TEXT    NOT NULL,
        email       TEXT
    )
    """,

    # ─── PLANS (created by admin, purchased by manager) ───
    """
    CREATE TABLE IF NOT EXISTS plans (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_name       TEXT    NOT NULL,
        description     TEXT,
        price           REAL    NOT NULL,
        duration_months INTEGER NOT NULL,
        is_active       INTEGER NOT NULL DEFAULT 1,
        created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
    )
    """,

    # ─── GYMS (enrolled by manager after buying a plan) ───
    """
    CREATE TABLE IF NOT EXISTS gyms (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        manager_id      INTEGER NOT NULL,
        gym_name        TEXT    NOT NULL,
        address         TEXT,
        city            TEXT,
        phone           TEXT,
        email           TEXT,
        about           TEXT,
        contact_info    TEXT,
        base_price      REAL    NOT NULL DEFAULT 0,
        plan_id         INTEGER,
        plan_expiry     TEXT,
        is_approved     INTEGER NOT NULL DEFAULT 0,
        is_active       INTEGER NOT NULL DEFAULT 1,
        created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (manager_id) REFERENCES users(id),
        FOREIGN KEY (plan_id) REFERENCES plans(id)
    )
    """,

    # ─── MANAGER PLAN SUBSCRIPTIONS ───
    """
    CREATE TABLE IF NOT EXISTS manager_subscriptions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        manager_id  INTEGER NOT NULL,
        plan_id     INTEGER NOT NULL,
        start_date  TEXT    NOT NULL,
        expiry_date TEXT    NOT NULL,
        amount_paid REAL    NOT NULL,
        status      TEXT    NOT NULL DEFAULT 'active',
        created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (manager_id) REFERENCES users(id),
        FOREIGN KEY (plan_id) REFERENCES plans(id)
    )
    """,

    # ─── TRAINERS ───
    """
    CREATE TABLE IF NOT EXISTS trainers (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        gym_id          INTEGER NOT NULL,
        full_name       TEXT    NOT NULL,
        specialization  TEXT,
        experience_yrs  INTEGER DEFAULT 0,
        monthly_fee     REAL    NOT NULL DEFAULT 0,
        is_available    INTEGER NOT NULL DEFAULT 1,
        created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (gym_id) REFERENCES gyms(id)
    )
    """,

    # ─── SLOTS ───
    """
    CREATE TABLE IF NOT EXISTS slots (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        gym_id      INTEGER NOT NULL,
        slot_name   TEXT    NOT NULL,
        start_time  TEXT    NOT NULL,
        end_time    TEXT    NOT NULL,
        capacity    INTEGER NOT NULL DEFAULT 10,
        is_active   INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (gym_id) REFERENCES gyms(id)
    )
    """,

    # ─── EQUIPMENT ───
    """
    CREATE TABLE IF NOT EXISTS equipment (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        gym_id      INTEGER NOT NULL,
        name        TEXT    NOT NULL,
        quantity    INTEGER NOT NULL DEFAULT 1,
        condition   TEXT    DEFAULT 'Good',
        added_at    TEXT    NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (gym_id) REFERENCES gyms(id)
    )
    """,

    # ─── DIET PLANS ───
    """
    CREATE TABLE IF NOT EXISTS dietplans (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        gym_id      INTEGER NOT NULL,
        title       TEXT    NOT NULL,
        description TEXT,
        goal        TEXT,
        created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (gym_id) REFERENCES gyms(id)
    )
    """,

    # ─── BOOKINGS ───
    """
    CREATE TABLE IF NOT EXISTS bookings (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id     INTEGER NOT NULL,
        gym_id          INTEGER NOT NULL,
        slot_id         INTEGER NOT NULL,
        trainer_id      INTEGER,
        duration_key    TEXT    NOT NULL,
        training_type   TEXT    NOT NULL CHECK(training_type IN ('self', 'trainer')),
        start_date      TEXT    NOT NULL,
        expiry_date     TEXT    NOT NULL,
        status          TEXT    NOT NULL DEFAULT 'active',
        created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (customer_id) REFERENCES users(id),
        FOREIGN KEY (gym_id) REFERENCES gyms(id),
        FOREIGN KEY (slot_id) REFERENCES slots(id),
        FOREIGN KEY (trainer_id) REFERENCES trainers(id)
    )
    """,

    # ─── PAYMENTS ───
    """
    CREATE TABLE IF NOT EXISTS payments (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        booking_id      INTEGER,
        customer_id     INTEGER NOT NULL,
        gym_id          INTEGER NOT NULL,
        membership_cost REAL    NOT NULL,
        trainer_cost    REAL    NOT NULL DEFAULT 0,
        total_amount    REAL    NOT NULL,
        payment_method  TEXT    NOT NULL DEFAULT 'cash',
        payment_status  TEXT    NOT NULL DEFAULT 'paid',
        paid_at         TEXT    NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (booking_id) REFERENCES bookings(id),
        FOREIGN KEY (customer_id) REFERENCES users(id),
        FOREIGN KEY (gym_id) REFERENCES gyms(id)
    )
    """,

    # ─── MEMBERSHIPS ───
    """
    CREATE TABLE IF NOT EXISTS memberships (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id     INTEGER NOT NULL,
        gym_id          INTEGER NOT NULL,
        booking_id      INTEGER NOT NULL,
        membership_type TEXT    NOT NULL,
        start_date      TEXT    NOT NULL,
        expiry_date     TEXT    NOT NULL,
        is_active       INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (customer_id) REFERENCES users(id),
        FOREIGN KEY (gym_id) REFERENCES gyms(id),
        FOREIGN KEY (booking_id) REFERENCES bookings(id)
    )
    """,

    # ─── FEEDBACK ───
    """
    CREATE TABLE IF NOT EXISTS feedback (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        gym_id      INTEGER,
        subject     TEXT    NOT NULL,
        message     TEXT    NOT NULL,
        rating      INTEGER DEFAULT 5 CHECK(rating BETWEEN 1 AND 5),
        created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
        FOREIGN KEY (customer_id) REFERENCES users(id),
        FOREIGN KEY (gym_id) REFERENCES gyms(id)
    )
    """
]

def create_all_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    for sql in TABLES:
        cursor.execute(sql)
    conn.commit()
    conn.close()
    print("[DB] All tables created successfully.")

if __name__ == "__main__":
    create_all_tables()
