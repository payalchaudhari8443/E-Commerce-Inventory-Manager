from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///inventory.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Replace with a secure random key
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            return redirect(url_for('stock_management'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/stock_management', methods=['GET', 'POST'])
def stock_management():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    items = Item.query.all()
    if request.method == 'POST':
        if 'delete_id' in request.form:
            item = Item.query.get_or_404(request.form['delete_id'])
            db.session.delete(item)
            db.session.commit()
            flash('Item deleted successfully!')
        elif 'update_id' in request.form:
            item = Item.query.get_or_404(request.form['update_id'])
            item.name = request.form['name']
            item.price = float(request.form['price'])
            item.quantity = int(request.form['quantity'])
            db.session.commit()
            flash('Item updated successfully!')
        else:
            name = request.form['name']
            price = float(request.form['price'])
            quantity = int(request.form['quantity'])
            new_item = Item(name=name, price=price, quantity=quantity)
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully!')
        return redirect(url_for('stock_management'))  # Force page reload
    return render_template('stock_management.html', items=items)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed = generate_password_hash('admin')
        db.session.add(User(username='admin', password_hash=hashed))
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)