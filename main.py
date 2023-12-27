
import streamlit as st
import sqlite3

class ExpenseTracker:
    def __init__(self):
        # Initialize SQLite database
        self.conn = sqlite3.connect("expenses.db")
        self.create_expenses_table()

        # Set Streamlit app title
        st.title("Personal Expense Tracker - Parameter Insertion")

        # Initialize variables
        self.category_options = ["Health", "Fashion", "Travel", "Education", "Other"]
        self.selected_category = st.selectbox("Category:", self.category_options)
        self.expense_purpose = st.text_input("Purpose:")
        self.expense_cost = st.number_input("Cost:", value=0.0, step=0.01)
        self.parameter_type_options = ["Numerical", "Text"]
        self.selected_parameter_type = st.radio("Parameter Type:", self.parameter_type_options)

        # Create Streamlit elements
        self.create_add_button()
        self.create_expense_list()

    def create_expenses_table(self):
        cursor = self.conn.cursor()
        # Drop the existing "expenses" table if it exists
        cursor.execute("DROP TABLE IF EXISTS expenses")
        # Recreate the "expenses" table with the updated schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                purpose TEXT NOT NULL,
                cost REAL NOT NULL,
                parameter_type TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_add_button(self):
        if st.button("Add Expense"):
            self.add_expense()
            self.load_expenses()

    def add_expense(self):
        category = self.selected_category
        purpose = self.expense_purpose
        cost = self.expense_cost
        parameter_type = self.selected_parameter_type

        if category and purpose and cost and parameter_type:
            self.save_expense(category, purpose, cost, parameter_type)

    def save_expense(self, category, purpose, cost, parameter_type):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO expenses (category, purpose, cost, parameter_type) VALUES (?, ?, ?, ?)",
                       (category, purpose, cost, parameter_type))
        self.conn.commit()

    def create_expense_list(self):
        st.subheader("Expenses:")

        # Load existing expenses from the database
        self.load_expenses()

    def load_expenses(self):
        self.expenses = []
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, purpose, cost, parameter_type FROM expenses")
        rows = cursor.fetchall()
        for row in rows:
            category, purpose, cost, parameter_type = row
            expense_str = f"{category} - {purpose}: ${cost:.2f}, Parameter Type: {parameter_type}"
            self.expenses.append(expense_str)

        self.update_expense_list()

    def update_expense_list(self):
        for expense in self.expenses:
            st.write(expense)

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    app = ExpenseTracker()
