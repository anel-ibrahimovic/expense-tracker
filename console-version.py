from datetime import datetime
import json

def save_expenses(expenses):
    with open('expenses.json', 'w') as f:
        json.dump([{
            **exp, 'date': exp['date'].strftime('%Y-%m-%d')
        } for exp in expenses], f, indent=4)

def load_expenses():
    try:
        with open('expenses.json', 'r') as f:
            expenses = json.load(f)
            for exp in expenses:
                exp['date'] = datetime.strptime(exp['date'], "%Y-%m-%d").date()
            return expenses
    except FileNotFoundError:
        return []

def expense_tracker():
    expenses = load_expenses()
    print("Welcome to Expense Tracker!")

    while True:
        print("\n1. Add Expense")
        print("2. View All Expenses")
        print("3. View Expenses by Category")
        print("4. View Expenses by Date")
        print("5. Quit")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            name = input("Enter an expense you want to add: ")
            while True:
                date = input("Enter the date of the expense (YYYY-MM-DD): ")
                try:
                    date = datetime.strptime(date, "%Y-%m-%d").date()
                    break
                except ValueError:
                    print("Invalid date format. Please use YYYY-MM-DD.")
            category = input("Enter the category of the expense: ").strip().capitalize()
            description = input("Enter the description of the expense: ")
            while True:
                try:
                    amount = float(input("Enter the amount of the expense: "))
                    if amount <= 0:
                        print("Amount must be greater than zero.")
                        continue
                    break
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")

            expense = {
                'name': name,
                'date': date,
                'category': category,
                'description': description,
                'amount': amount
            }
            expenses.append(expense)
            save_expenses(expenses)
            print(f"Expense '{name}' added successfully.")

        elif choice == 2:
            if not expenses:
                print("No expenses recorded yet.")
            else:
                print("\nAll Expenses:")
                for expense in expenses:
                    print_expense(expense)
                total = sum(exp['amount'] for exp in expenses)
                print(f"\nTotal Expenses: €{total:.2f}")

        elif choice == 3:
            if not expenses:
                print("No expenses recorded yet.")
            else:
                view_category = input("Enter the category of the expense you want to view: ").strip().lower()
                found = False
                for expense in expenses:
                    if expense['category'].lower() == view_category:
                        print_expense(expense)
                        found = True
                if not found:
                    print("No expenses found in this category.")

        elif choice == 4:
            if not expenses:
                print("No expenses recorded yet.")
            else:
                view_date = input("Enter the date of the expense you want to view (YYYY-MM-DD): ")
                try:
                    view_date = datetime.strptime(view_date, "%Y-%m-%d").date()
                except ValueError:
                    print("Invalid date format. Please enter a valid date.")
                    continue

                found = False
                for expense in expenses:
                    if expense['date'] == view_date:
                        print_expense(expense)
                        found = True
                if not found:
                    print("No expenses found on this date.")

        elif choice == 5:
            print("Thank you for using Expense Tracker. Goodbye!")
            break

def print_expense(expense):
    print("-" * 50)
    print(f"Name       : {expense['name']}")
    print(f"Date       : {expense['date'].strftime('%Y-%m-%d')}")
    print(f"Category   : {expense['category']}")
    print(f"Description: {expense['description']}")
    print(f"Amount     : €{expense['amount']:.2f}")
    print("-" * 50)

expense_tracker()
