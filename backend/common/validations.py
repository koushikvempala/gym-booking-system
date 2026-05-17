import re

# ─────────────────────────────────────────────
# STRING VALIDATORS
# ─────────────────────────────────────────────

def is_non_empty(value, field_name="Field"):
    if not value or not str(value).strip():
        print(f"[VALIDATION] {field_name} cannot be empty.")
        return False
    return True

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    if not re.match(pattern, email):
        print("[VALIDATION] Invalid email format.")
        return False
    return True

def is_valid_phone(phone):
    if not re.match(r'^\d{10}$', str(phone)):
        print("[VALIDATION] Phone must be exactly 10 digits.")
        return False
    return True

def is_valid_password(password):
    if len(password) < 6:
        print("[VALIDATION] Password must be at least 6 characters.")
        return False
    return True

def is_valid_username(username):
    if not re.match(r'^[a-zA-Z0-9_]{4,20}$', username):
        print("[VALIDATION] Username must be 4-20 characters (letters, digits, underscore).")
        return False
    return True

# ─────────────────────────────────────────────
# NUMBER VALIDATORS
# ─────────────────────────────────────────────

def is_positive_number(value, field_name="Value"):
    try:
        if float(value) <= 0:
            print(f"[VALIDATION] {field_name} must be a positive number.")
            return False
        return True
    except (ValueError, TypeError):
        print(f"[VALIDATION] {field_name} must be a number.")
        return False

def is_valid_choice(value, choices, field_name="Choice"):
    if str(value) not in [str(c) for c in choices]:
        print(f"[VALIDATION] {field_name} must be one of: {choices}")
        return False
    return True

# ─────────────────────────────────────────────
# DATE VALIDATORS
# ─────────────────────────────────────────────

def is_valid_date(date_str):
    import datetime
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        print("[VALIDATION] Date must be in YYYY-MM-DD format.")
        return False

# ─────────────────────────────────────────────
# INPUT HELPER
# ─────────────────────────────────────────────

def get_input(prompt, validator=None, *args):
    """
    Prompt user for input and optionally validate.
    Keeps asking until valid input is given.
    """
    while True:
        value = input(prompt).strip()
        if validator is None:
            return value
        if validator(value, *args):
            return value
