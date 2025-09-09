# main.py - Personal Expense Tracker (CSV-based, simple)
import csv
import os
from datetime import date, datetime
from collections import defaultdict

FNAME = "expenses.csv"
HEADERS = ["date", "category", "amount", "note"]

def ensure_file():
    if not os.path.exists(FNAME):
        with open(FNAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)

def add_expense(date_str, category, amount, note=""):
    ensure_file()
    # Validate date
    try:
        _ = datetime.fromisoformat(date_str).date()
    except Exception:
        raise ValueError("date must be YYYY-MM-DD")
    # Validate amount
    amt = float(amount)
    if amt < 0:
        raise ValueError("amount must be non-negative")
    with open(FNAME, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date_str, category, f"{amt:.2f}", note])

def read_expenses():
    ensure_file()
    with open(FNAME, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def print_table(rows):
    if not rows:
        print("No expenses found.")
        return
    print(f"{'Date':10}  {'Category':15}  {'Amount':10}  {'Note'}")
    print("-"*60)
    for r in rows:
        print(f"{r['date']:10}  {r['category'][:15]:15}  {float(r['amount']):10.2f}  {r.get('note','')}")

def total_expenses(start=None, end=None):
    rows = read_expenses()
    total = 0.0
    for r in rows:
        d = r["date"]
        if start and d < start: 
            continue
        if end and d > end:
            continue
        total += float(r["amount"])
    return total

def summary_by_category(start=None, end=None):
    rows = read_expenses()
    agg = defaultdict(float)
    for r in rows:
        d = r["date"]
        if start and d < start:
            continue
        if end and d > end:
            continue
        agg[r["category"]] += float(r["amount"])
    return dict(sorted(agg.items(), key=lambda x: x[1], reverse=True))

def export_csv(path="expenses_export.csv"):
    rows = read_expenses()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date","category","amount","note"])
        for r in rows:
            writer.writerow([r["date"], r["category"], r["amount"], r.get("note","")])
    print(f"Exported {len(rows)} rows to {path}")

def input_date(prompt="Date (YYYY-MM-DD) [default: today]: "):
    s = input(prompt).strip()
    if not s:
        return date.today().isoformat()
    try:
        d = datetime.fromisoformat(s).date()
        return d.isoformat()
    except Exception:
        print("Invalid format, use YYYY-MM-DD.")
        return input_date(prompt)

def input_amount(prompt="Amount: "):
    s = input(prompt).strip()
    try:
        a = float(s)
        if a < 0:
            print("Amount must be non-negative.")
            return input_amount(prompt)
        return a
    except:
        print("Enter a valid number.")
        return input_amount(prompt)

def main():
    ensure_file()
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Show total (optional date range)")
        print("4. Summary by category")
        print("5. Export to CSV")
        print("6. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            d = input_date()
            cat = input("Category: ").strip() or "Misc"
            amt = input_amount()
            note = input("Note (optional): ").strip()
            try:
                add_expense(d, cat, amt, note)
                print("✅ Expense added.")
            except Exception as e:
                print("Error:", e)
        elif choice == "2":
            rows = read_expenses()
            print_table(rows)
        elif choice == "3":
            start = input("Start date (YYYY-MM-DD) or enter to skip: ").strip() or None
            end = input("End date (YYYY-MM-DD) or enter to skip: ").strip() or None
            total = total_expenses(start, end)
            print(f"💰 Total expenses: {total:.2f}")
        elif choice == "4":
            start = input("Start date (YYYY-MM-DD) or enter to skip: ").strip() or None
            end = input("End date (YYYY-MM-DD) or enter to skip: ").strip() or None
            summ = summary_by_category(start, end)
            if not summ:
                print("No data.")
            else:
                print("Category summary:")
                for k, v in summ.items():
                    print(f"  {k:15} → {v:.2f}")
        elif choice == "5":
            path = input("Export path [expenses_export.csv]: ").strip() or "expenses_export.csv"
            export_csv(path)
        elif choice == "6":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
