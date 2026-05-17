import datetime

# ─────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────

def print_header(title):
    print("\n" + "=" * 50)
    print(f"  {title.upper()}")
    print("=" * 50)

def print_divider():
    print("-" * 50)

def print_table(rows, columns):
    """Simple table printer for console."""
    if not rows:
        print("  [No records found]")
        return
    # Calculate column widths
    col_widths = [max(len(str(col)), max((len(str(row.get(col, ""))) for row in rows), default=0)) for col in columns]
    header = " | ".join(str(col).ljust(w) for col, w in zip(columns, col_widths))
    print(header)
    print("-" * len(header))
    for row in rows:
        line = " | ".join(str(row.get(col, "")).ljust(w) for col, w in zip(columns, col_widths))
        print(line)

def pause():
    input("\nPress Enter to continue...")

def confirm_action(prompt="Are you sure? (y/n): "):
    return input(prompt).strip().lower() == 'y'

# ─────────────────────────────────────────────
# DATE HELPERS
# ─────────────────────────────────────────────

def today_str():
    return datetime.date.today().strftime("%Y-%m-%d")

def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_months(date_str, months):
    """Add months to a date string (YYYY-MM-DD). Returns new date string."""
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, [31,28+int((year%4==0 and (year%100!=0 or year%400==0))),31,30,31,30,31,31,30,31,30,31][month-1])
    return datetime.date(year, month, day).strftime("%Y-%m-%d")

def is_date_past(date_str):
    """Returns True if date is in the past."""
    d = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    return d < datetime.date.today()
