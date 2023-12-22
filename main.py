import streamlit as st
from utility import DatabaseManager, read_config

class ExpenseTracker:
    def __init__(self):
        # Read configuration from config.yaml
        self.config = read_config()

        # Initialize database manager
        db_name = self.config["database"]["name"]
        self.db_manager = DatabaseManager(db_name)

        # Initialize Streamlit app
        self.root = st
        self.root.set_page_config(page_title=self.config["streamlit"]["title"])

        # Initialize variables
        self.category_options = ["Health", "Fashion", "Travel", "Education", "Other"]
        self.selected_category = self.root.selectbox("Category:", self.category_options)
        self.expense_purpose = self.root.text_input("Purpose:")
        self.expense_cost = self.root.number_input("Cost:", value=0.0, step=0.01)
        self.expenses = []

        # Create Streamlit elements
        self.create_add_button()
        self.create_expense_list()

    def create_add_button(self):
        if self.root.button("Add Expense"):
            self.add_expense()
            self.load_expenses()

    def create_expense_list(self):
        self.root.subheader("Expenses:")

        # Load existing expenses from the database
        self.load_expenses()

    def add_expense(self):
        category = self.selected_category
        purpose = self.expense_purpose
        cost = self.expense_cost

        if category and purpose and cost:
            self.db_manager.save_expense(category, purpose, cost)

    def load_expenses(self):
        self.expenses = self.db_manager.load_expenses()

        for row in self.expenses:
            category, purpose, cost = row
            expense_str = f"{category} - {purpose}: ${cost:.2f}"
            self.root.write(expense_str)

    def __del__(self):
        self.db_manager.close_connection()


if __name__ == "__main__":
    app = ExpenseTracker()
