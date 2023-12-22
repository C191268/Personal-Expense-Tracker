import sqlite3
import yaml

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.create_expenses_table()

    def create_expenses_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                purpose TEXT NOT NULL,
                cost REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def save_expense(self, category, purpose, cost):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO expenses (category, purpose, cost) VALUES (?, ?, ?)", (category, purpose, cost))
        self.conn.commit()

    def load_expenses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, purpose, cost FROM expenses")
        rows = cursor.fetchall()
        return rows

    def close_connection(self):
        self.conn.close()

def read_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config
