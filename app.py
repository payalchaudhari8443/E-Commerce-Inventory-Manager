from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change for production

# Render Postgres config (set via env vars)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://') if os.environ.get('DATABASE_URL') else 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('stock_management'))
        flash('Invalid credentials')
    return render_template('index.html')

@app.route('/stock', methods=['GET', 'POST'])
def stock_management():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        action = request.form['action']
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        
        if action == 'add':
            new_item = Item(name=name, price=price, quantity=quantity)
            db.session.add(new_item)
        elif action == 'update':
            item_id = int(request.form['id'])
            item = Item.query.get(item_id)
            if item:
                item.name = name
                item.price = price
                item.quantity = quantity
        elif action == 'delete':
            item_id = int(request.form['id'])
            item = Item.query.get(item_id)
            if item:
                db.session.delete(item)
        db.session.commit()
        flash('Operation successful!')
    
    items = Item.query.all()
    return render_template('stock.html', items=items)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        # Add default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            hashed = generate_password_hash('admin')
            db.session.add(User(username='admin', password_hash=hashed))
            db.session.commit()
    app.run(host='0.0.0.0', port=5000, debug=True)