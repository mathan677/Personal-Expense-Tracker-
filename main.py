import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

FILE_NAME = "expenses.csv"

# -------------------------------
# Utility functions
# -------------------------------
def init_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "category", "amount", "description"])

def add_expense(date, category, amount, description=""):
    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount, description])

def read_expenses():
    rows = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    return rows

def print_table(rows):
    if not rows:
        print("No expenses found.")
        return
    print("-" * 60)
    for row in rows:
        print(f"{row['date']:12} {row['category']:10} {row['amount']:10} {row['description']}")
    print("-" * 60)

def total_expenses(start=None, end=None):
    rows = read_expenses()
    total = 0.0
    for row in rows:
        date = datetime.strptime(row["date"], "%Y-%m-%d")
        if start and date < datetime.strptime(start, "%Y-%m-%d"):
            continue
        if end and date > datetime.strptime(end, "%Y-%m-%d"):
            continue
        total += float(row["amount"])
    return total

def summary_by_category(start=None, end=None):
    rows = read_expenses()
    summary = {}
    for row in rows:
        date = datetime.strptime(row["date"], "%Y-%m-%d")
        if start and date < datetime.strptime(start, "%Y-%m-%d"):
            continue
        if end and date > datetime.strptime(end, "%Y-%m-%d"):
            continue
        cat = row["category"]
        summary[cat] = summary.get(cat, 0) + float(row["amount"])
    return summary

def export_csv(path="expenses_export.csv"):
    rows = read_expenses()
    if not rows:
        print("No data to export.")
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Exported {len(rows)} rows to {path}")

# -------------------------------
# New Features
# -------------------------------
def export_excel(path="expenses.xlsx"):
    rows = read_expenses()
    if not rows:
        print("No data to export.")
        return
    df = pd.DataFrame(rows)
    df["amount"] = df["amount"].astype(float)
    df.to_excel(path, index=False)
    print(f"Exported {len(df)} rows to {path}")

def plot_summary(start=None, end=None, kind="bar"):
    rows = read_expenses()
    if not rows:
        print("No data to plot.")
        return
    
    df = pd.DataFrame(rows)
    df["amount"] = df["amount"].astype(float)
    df["date"] = pd.to_datetime(df["date"])

    # Apply filters
    if start:
        df = df[df["date"] >= pd.to_datetime(start)]
    if end:
        df = df[df["date"] <= pd.to_datetime(end)]

    if df.empty:
        print("No data in given range.")
        return

    plt.figure(figsize=(8, 5))

    if kind == "pie":
        data = df.groupby("category")["amount"].sum()
        plt.pie(data, labels=data.index, autopct="%1.1f%%", startangle=140)
        plt.title("Expenses by Category (Pie)")

    elif kind == "bar":
        data = df.groupby("category")["amount"].sum()
        plt.bar(data.index, data.values)
        plt.title("Expenses by Category (Bar)")
        plt.ylabel("Amount")
        plt.xticks(rotation=45, ha="right")

    elif kind == "line":
        data = df.groupby("date")["amount"].sum()
        plt.plot(data.index, data.values, marker="o")
        plt.title("Daily Expenses (Line Chart)")
        plt.ylabel("Amount")
        plt.xticks(rotation=45, ha="right")

    elif kind == "stacked":
        data = df.pivot_table(index="date", columns="category", values="amount", aggfunc="sum", fill_value=0)
        data.plot(kind="bar", stacked=True, figsize=(10,6))
        plt.title("Expenses by Category (Stacked Bar)")
        plt.ylabel("Amount")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.show()
        return  # pandas plotting already shows

    plt.tight_layout()
    plt.show()

# -------------------------------
# Main Menu
# -------------------------------
def main():
    init_file()
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Show total (optional date range)")
        print("4. Summary by category")
        print("5. Export to CSV")
        print("6. Exit")
        print("7. Plot summary (bar/pie/line/stacked)")
        print("8. Export to Excel (xlsx)")
        choice = input("Choose: ").strip()

        if choice == "1":
            try:
                date = input("Date (YYYY-MM-DD): ").strip()
                category = input("Category: ").strip()
                amount = float(input("Amount: ").strip())
                description = input("Description (optional): ").strip()
                add_expense(date, category, amount, description)
                print("Expense added successfully!")
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
                    print(f"{k:15} = {v:.2f}")

        elif choice == "5":
            path = input("Export path [expenses_export.csv]: ").strip() or "expenses_export.csv"
            export_csv(path)

        elif choice == "6":
            print("Goodbye 👋")
            break

        elif choice == "7":
            start = input("Start date (YYYY-MM-DD) or enter to skip: ").strip() or None
            end = input("End date (YYYY-MM-DD) or enter to skip: ").strip() or None
            print("Choose visualization type:")
            print("  bar     - Bar chart")
            print("  pie     - Pie chart")
            print("  line    - Line chart (expenses over time)")
            print("  stacked - Stacked bar by category over time")
            kind = input("Enter choice [bar/pie/line/stacked]: ").strip().lower()
            if kind not in ["pie","bar","line","stacked"]:
                kind = "bar"
            plot_summary(start, end, kind)

        elif choice == "8":
            path = input("Excel path [expenses.xlsx]: ").strip() or "expenses.xlsx"
            export_excel(path)

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
