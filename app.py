import os
from flask import Flask, render_template, url_for, flash, redirect, request, abort, session, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

# We import the db and models explicitly to ensure they are registered
from models import db, Product, User

app = Flask(__name__)

# 1. ELITE CONFIGURATION
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'agrovet_secure_77x9'),
    SQLALCHEMY_DATABASE_URI='sqlite:///agrovet.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_HTTPONLY=True
)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# PRODUCTION DATABASE INITIALIZATION
# This ensures tables are created even when running via Gunicorn on Render
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 2. ROUTES
@app.route('/')
def home():
    featured_products = Product.query.order_by(Product.date_added.desc()).limit(6).all()
    return render_template('index.html', products=featured_products, title="Home")

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product, title=product.name)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        results = Product.query.filter(
            (Product.name.icontains(query)) | 
            (Product.category.icontains(query)) |
            (Product.description.icontains(query))
        ).all()
    else:
        results = []
    return render_template('index.html', products=results, query=query, title="Search Results")

# --- FIXED CART LOGIC ---
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    cart = list(session['cart'])
    cart.append(product_id)
    session['cart'] = cart
    session.modified = True 
    
    return jsonify({"status": "success", "cart_count": len(session['cart'])})

@app.route('/cart')
def cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', products=[], total=0, title="Shopping Cart")
    
    product_ids = session['cart']
    cart_products = [Product.query.get(pid) for pid in product_ids if Product.query.get(pid)]
    total = sum(p.price for p in cart_products)
    
    return render_template('cart.html', products=cart_products, total=total, title="Shopping Cart")

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared successfully.', 'success')
    return redirect(url_for('cart'))

# --- THE CONSULTANCY UPDATE ---
@app.route('/consultancy', methods=['GET', 'POST'])
def consultancy():
    if request.method == 'POST':
        name = request.form.get('name')
        flash(f'Thank you {name}! Your consultancy request has been sent. We will call you shortly.', 'success')
        return redirect(url_for('home'))
    return render_template('consultancy.html', title="Expert Consultancy")

# 3. LOCAL DEVELOPMENT RUNNER
if __name__ == '__main__':
    app.run(debug=True, port=5001)