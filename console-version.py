from datetime import datetime
import json

FILENAME = "expenses.json"

def save_expenses(expenses):
    with open(FILENAME, 'w') as f:
        json.dump([{
            **exp, 'date': exp['date'].strftime('%Y-%m-%d')
        } for exp in expenses], f, indent=4)

def load_expenses():
    try:
        with open(FILENAME, 'r') as f:
            expenses = json.load(f)
            for exp in expenses:
                exp['date'] = datetime.strptime(exp['date'], "%Y-%m-%d").date()
            return expenses
    except FileNotFoundError:
        return []

def main_menu():
    expenses = load_expenses()
    while True:
        print("Welcome to the Expense Tracker")
        print("Please select an option:")
        print("1. Add Expense")
        print("2. View Expense")
        print("3. Delete Expense")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number (1-4).")
            continue

        if choice == 1:
            add_expense(expenses)
        elif choice == 2:
            view_expense(expenses)
        elif choice == 3:
            expenses = delete_expense(expenses)
        elif choice == 4:
            print("Thank you for using Expense Tracker")
            return
        else:
            print("Invalid choice. Please try again.")

def add_expense(expenses):
    name = input("Enter expense name: ")
    if not name:
        print("Name cannot be empty.")
        return
    while True:
        date = input("Enter expense date: ")
        try:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    category = input("Enter expense category: ")
    description = input("Enter expense description: ")
    while True:
        try:
            amount = float(input("Enter expense amount: "))
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

def view_expense(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    print("Would you like to View by Name, Date or Category?")
    print("1. View by Name")
    print("2. View by Date")
    print("3. View by Category")
    print("4. Back")

    try:
        view_choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid choice. Please enter a number (1-4).")
        return

    if view_choice == 1:
        view_name = input("Enter the name of the expense you want to view: ").strip().lower()
        found = False
        for expense in expenses:
            if expense['name'].lower() == view_name:
                print_expense(expense)
                found = True
        if not found:
            print("No expenses found in this category.")

    elif view_choice == 2:
        view_date = input("Enter the date of the expense you want to view (YYYY-MM-DD): ").strip()
        try:
            view_date = datetime.strptime(view_date, "%Y-%m-%d").date()
            found = False
            for expense in expenses:
                if expense['date'] == view_date:
                    print_expense(expense)
                    found = True
            if not found:
                print("No expenses found for this date.")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    elif view_choice == 3:
        view_category = input("Enter the category of the expense you want to view: ").strip().lower()
        found = False
        for expense in expenses:
            if expense['category'].lower() == view_category:
                print_expense(expense)
                found = True
        if not found:
            print("No expenses found in this category.")

    elif view_choice == 4:
        return

def delete_expense(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return expenses

    delete_name = input("Enter the name of the expense you want to delete: ").strip().lower()
    original_len = len(expenses)
    updated_expenses = [expense for expense in expenses if expense['name'].lower() != delete_name]

    if len(updated_expenses) < original_len:
        confirm = input(f"Are you sure you want to delete all expenses named '{delete_name}' (y/n): ").lower()
        if confirm == 'y':
            save_expenses(updated_expenses)
            print(f"Expense(s) named '{delete_name}' deleted successfully.")
        else:
            print("Deletion cancelled.")

    return updated_expenses

def print_expense(expense):
    print("-" * 50)
    print(f"Name       : {expense['name']}")
    print(f"Date       : {expense['date'].strftime('%Y-%m-%d')}")
    print(f"Category   : {expense['category']}")
    print(f"Description: {expense['description']}")
    print(f"Amount     : €{expense['amount']:.2f}")
    print("-" * 50)

if __name__ == '__main__':
    main_menu()
