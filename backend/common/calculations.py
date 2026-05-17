# ─────────────────────────────────────────────
# MEMBERSHIP DURATION MAP
# ─────────────────────────────────────────────

DURATION_MONTHS = {
    "1month": 1,
    "6month": 6,
    "1year": 12
}

DURATION_LABELS = {
    "1month": "1 Month",
    "6month": "6 Months",
    "1year": "1 Year"
}

# ─────────────────────────────────────────────
# MEMBERSHIP PRICING
# ─────────────────────────────────────────────

def calculate_membership_cost(base_price, duration_key):
    """
    Calculate total membership cost based on duration.
    - 1 month  = base_price * 1
    - 6 months = base_price * 6 * 0.90 (10% discount)
    - 1 year   = base_price * 12 * 0.80 (20% discount)
    """
    if duration_key == "1month":
        return round(base_price * 1, 2)
    elif duration_key == "6month":
        return round(base_price * 6 * 0.90, 2)
    elif duration_key == "1year":
        return round(base_price * 12 * 0.80, 2)
    return 0.0

def calculate_trainer_fee(trainer_monthly_fee, duration_key):
    """Calculate trainer fee for the duration."""
    months = DURATION_MONTHS.get(duration_key, 1)
    return round(trainer_monthly_fee * months, 2)

def calculate_total_booking_cost(base_price, duration_key, with_trainer=False, trainer_monthly_fee=0):
    """
    Final booking cost calculation.
    Returns dict with breakdown.
    """
    membership_cost = calculate_membership_cost(base_price, duration_key)
    trainer_cost = 0.0
    if with_trainer and trainer_monthly_fee:
        trainer_cost = calculate_trainer_fee(trainer_monthly_fee, duration_key)
    total = membership_cost + trainer_cost
    return {
        "membership_cost": membership_cost,
        "trainer_cost": trainer_cost,
        "total": round(total, 2),
        "duration": DURATION_LABELS.get(duration_key, duration_key)
    }

def get_expiry_date(start_date, duration_key):
    """Returns expiry date string given start date and duration key."""
    from common.helpers import add_months
    months = DURATION_MONTHS.get(duration_key, 1)
    return add_months(start_date, months)

# ─────────────────────────────────────────────
# PLAN PRICING DISPLAY
# ─────────────────────────────────────────────

def display_pricing_breakdown(base_price, duration_key, with_trainer=False, trainer_fee=0):
    """Print a clear cost breakdown to console."""
    result = calculate_total_booking_cost(base_price, duration_key, with_trainer, trainer_fee)
    print("\n--- COST BREAKDOWN ---")
    print(f"  Duration        : {result['duration']}")
    print(f"  Membership Cost : Rs. {result['membership_cost']}")
    if with_trainer:
        print(f"  Trainer Fee     : Rs. {result['trainer_cost']}")
    print(f"  TOTAL           : Rs. {result['total']}")
    print("----------------------")
    return result
