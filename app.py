from flask import Flask, render_template, request, redirect, url_for, request
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense_tracker.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255))
    purpose = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)

db.create_all()

@app.route('/')
@login_user()
@login_required
def index():
    return render_template('index.html')

@app.route('/submit_expense', methods=['POST'])
def submit_expense():
    if request.method == 'POST':
        category = request.form['category']
        amount = float(request.form['amount'])
        expense_date = request.form['expense_date']
        description = request.form['description']
        purpose = request.form['purpose']
        cost = float(request.form['cost'])

        new_expense = Expense(category=category, amount=amount, expense_date=expense_date,
                              description=description, purpose=purpose, cost=cost)
        db.session.add(new_expense)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
