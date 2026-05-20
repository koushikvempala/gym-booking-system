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
    if not re.match(r'^[6-9]\d{9}$', str(phone)):
        print("[VALIDATION] Phone must be exactly 10 digits and start with 6, 7, 8, or 9.")
        return False
    return True

def is_valid_password(password):
    if len(password) < 8:
        print("[VALIDATION] Password must be at least 8 characters.")
        return False
    if not re.search(r'[A-Z]', password):
        print("[VALIDATION] Password must contain at least 1 uppercase letter.")
        return False
    if not re.search(r'[a-z]', password):
        print("[VALIDATION] Password must contain at least 1 lowercase letter.")
        return False
    if not re.search(r'\d', password):
        print("[VALIDATION] Password must contain at least 1 number.")
        return False
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;\':",./<>?]', password):
        print("[VALIDATION] Password must contain at least 1 special character.")
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

# ─────────────────────────────────────────────
# PAYMENT HELPER
# ─────────────────────────────────────────────

def process_payment(amount=None):
    if amount is not None:
        print(f"\n  PAYMENT - Amount: Rs. {amount}")
    else:
        print("\n  PAYMENT METHOD:")
        
    print("  1. Card")
    print("  2. UPI")
    print("  3. Wallet")
    
    while True:
        pay_choice = input("  Choose (1/2/3): ").strip()
        if pay_choice in ["1", "2", "3"]:
            break
        print("  Invalid choice.")

    if pay_choice == "1":
        method = "Card"
        print("\n  --- Card Payment ---")
        while True:
            card_no = input("  Card Number (16 digits): ").strip()
            if re.match(r'^\d{16}$', card_no):
                break
            print("  [ERROR] Invalid Card Number. Must be exactly 16 digits.")
            
        while True:
            validity = input("  Validity (MM/YY): ").strip()
            if re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', validity):
                import datetime
                month, year = map(int, validity.split('/'))
                now = datetime.datetime.now()
                current_year = now.year % 100
                current_month = now.month
                if year < current_year or (year == current_year and month < current_month):
                    print("  [ERROR] Card has expired. Please enter a valid future date.")
                else:
                    break
            else:
                print("  [ERROR] Invalid format. Must be MM/YY (Month 01-12).")
            
        while True:
            cvv = input("  CVV (3 digits): ").strip()
            if re.match(r'^\d{3}$', cvv):
                break
            print("  [ERROR] Invalid CVV. Must be exactly 3 digits.")
            
    elif pay_choice == "2":
        method = "UPI"
        print("\n  --- UPI Payment ---")
        while True:
            upi_id = input("  UPI ID (e.g. name@bank): ").strip()
            if re.match(r'^[\w\.-]+@[a-zA-Z]+$', upi_id):
                break
            print("  [ERROR] Invalid UPI ID format.")
            
    elif pay_choice == "3":
        method = "Wallet"
        print("\n  --- Wallet Payment ---")
        while True:
            wallet_no = input("  Wallet Mobile Number (10 digits): ").strip()
            if re.match(r'^\d{10}$', wallet_no):
                break
            print("  [ERROR] Invalid Number. Must be exactly 10 digits.")
            
    print(f"\n  [SUCCESS] Payment details verified for {method}.")
    return method

