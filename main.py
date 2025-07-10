import tkinter as tk
from tkinter import ttk, messagebox
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

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = load_expenses()

        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.main_frame = ttk.Frame(root, padding=20, relief="ridge")
        self.main_frame.grid(row=1, column=1, sticky='nsew')

        self.main_frame.grid_rowconfigure(6, weight=1)  # make output expand vertically
        self.main_frame.grid_columnconfigure(0, weight=1)

        ttk.Button(self.main_frame, text="Add An Expense", command=self.open_add_expense)\
            .grid(row=0, column=0, sticky='ew', pady=5)
        ttk.Button(self.main_frame, text="View All Expenses", command=self.view_all_expenses)\
            .grid(row=1, column=0, sticky='ew', pady=5)
        ttk.Button(self.main_frame, text="View Expenses by Category", command=self.view_by_category)\
            .grid(row=2, column=0, sticky='ew', pady=5)
        ttk.Button(self.main_frame, text="View Expenses by Date", command=self.view_by_date)\
            .grid(row=3, column=0, sticky='ew', pady=5)
        ttk.Button(self.main_frame, text="Quit", command=root.quit)\
            .grid(row=4, column=0, sticky='ew', pady=5)

        self.output = tk.Text(self.main_frame, height=15, width=70)
        self.output.grid(row=5, column=0, pady=10, sticky='nsew')

    def open_add_expense(self):
        win = tk.Toplevel(self.root)
        win.title("Add Expense")

        labels = ["Name:", "Date (YYYY-MM-DD):", "Category:", "Description:", "Amount (€):"]
        entries = {}

        for i, label in enumerate(labels):
            ttk.Label(win, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=5)
            entry = ttk.Entry(win)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

        def add():
            name = entries["Name:"].get().strip()
            date_str = entries["Date (YYYY-MM-DD):"].get().strip()
            category = entries["Category:"].get().strip().capitalize()
            description = entries["Description:"].get().strip()
            amount_str = entries["Amount (€):"].get().strip()

            if not name or not date_str or not category or not description or not amount_str:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Amount must be a positive number.")
                return

            expense = {
                'name': name,
                'date': date,
                'category': category,
                'description': description,
                'amount': amount
            }

            self.expenses.append(expense)
            save_expenses(self.expenses)
            messagebox.showinfo("Success", f"Expense '{name}' added successfully.")
            win.destroy()

        ttk.Button(win, text="Add Expense", command=add).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def print_expense(self, exp):
        return (
            "--------------------------------------------------\n"
            f"Name       : {exp['name']}\n"
            f"Date       : {exp['date'].strftime('%Y-%m-%d')}\n"
            f"Category   : {exp['category']}\n"
            f"Description: {exp['description']}\n"
            f"Amount     : €{exp['amount']:.2f}\n"
            "--------------------------------------------------\n"
        )

    def view_all_expenses(self):
        self.output.delete(1.0, tk.END)
        if not self.expenses:
            self.output.insert(tk.END, "No expenses recorded yet.\n")
            return
        total = 0
        self.output.insert(tk.END, "All Expenses:\n\n")
        for exp in self.expenses:
            self.output.insert(tk.END, self.print_expense(exp))
            total += exp['amount']
        self.output.insert(tk.END, f"\nTotal Expenses: €{total:.2f}\n")

    def view_by_category(self):
        def search():
            category = entry.get().strip().lower()
            self.output.delete(1.0, tk.END)
            found = False
            for exp in self.expenses:
                if exp['category'].lower() == category:
                    self.output.insert(tk.END, self.print_expense(exp))
                    found = True
            if not found:
                self.output.insert(tk.END, "No expenses found in this category.\n")
            search_win.destroy()

        search_win = tk.Toplevel(self.root)
        search_win.title("View by Category")

        ttk.Label(search_win, text="Enter category:").pack(padx=10, pady=5)
        entry = ttk.Entry(search_win)
        entry.pack(padx=30, pady=5)

        ttk.Button(search_win, text="Search", command=search).pack(pady=10)

    def view_by_date(self):
        def search():
            date_str = entry.get().strip()
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            self.output.delete(1.0, tk.END)
            found = False
            for exp in self.expenses:
                if exp['date'] == date:
                    self.output.insert(tk.END, self.print_expense(exp))
                    found = True
            if not found:
                self.output.insert(tk.END, "No expenses found on this date.\n")
            search_win.destroy()

        search_win = tk.Toplevel(self.root)
        search_win.title("View by Date")

        ttk.Label(search_win, text="Enter date (YYYY-MM-DD):").pack(padx=30, pady=5)
        entry = ttk.Entry(search_win)
        entry.pack(padx=10, pady=5)

        ttk.Button(search_win, text="Search", command=search).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
