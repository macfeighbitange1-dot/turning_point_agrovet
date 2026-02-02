import os
from flask import Flask, render_template, url_for, flash, redirect, request, abort, session, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

# Import the db and models
from models import db, Product, User, Review, ConsultancyRequest

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
login_manager.login_message_category = 'info'

# PRODUCTION DATABASE INITIALIZATION
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 2. PUBLIC & AUTH ROUTES
@app.route('/')
def home():
    featured_products = Product.query.order_by(Product.date_added.desc()).limit(6).all()
    customer_reviews = Review.query.filter_by(is_approved=True).order_by(Review.date_posted.desc()).limit(3).all()
    return render_template('index.html', products=featured_products, reviews=customer_reviews, title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles secure authentication for Owner and Buyers"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next') # Redirect to intended page after login
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
            
    return render_template('login.html', title='Login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out. / Umelogout kwa mafanikio.', 'info')
    return redirect(url_for('home'))

@app.route('/submit_review', methods=['POST'])
def submit_review():
    name = request.form.get('name')
    location = request.form.get('location')
    content = request.form.get('review')

    if name and location and content:
        new_review = Review(name=name, location=location, content=content)
        db.session.add(new_review)
        db.session.commit()
        flash('Thank you! Your review has been submitted.', 'success')
    else:
        flash('Please fill in all fields.', 'danger')
    return redirect(url_for('home'))

@app.route('/consultancy', methods=['GET', 'POST'])
def consultancy():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        if name and phone:
            new_lead = ConsultancyRequest(name=name, phone=phone, message=message)
            db.session.add(new_lead)
            db.session.commit()
            flash(f'Thank you {name}! We will call you shortly.', 'success')
            return redirect(url_for('home'))
        flash('Name and Phone are required.', 'danger')
        
    return render_template('consultancy.html', title="Expert Consultancy")

# --- SECURE ADMIN DASHBOARD ---
@app.route('/admin_portal')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403) 
    all_reviews = Review.query.order_by(Review.date_posted.desc()).all()
    all_consultancies = ConsultancyRequest.query.order_by(ConsultancyRequest.date_requested.desc()).all()
    return render_template('admin.html', reviews=all_reviews, consultancies=all_consultancies, title="Admin Panel")

@app.route('/admin/delete_review/<int:id>')
@login_required
def delete_review(id):
    if not current_user.is_admin:
        abort(403)
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'info')
    return redirect(url_for('admin_dashboard'))

# 3. UTILITY ROUTES
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product, title=product.name)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = Product.query.filter(
        (Product.name.icontains(query)) | 
        (Product.category.icontains(query)) |
        (Product.description.icontains(query))
    ).all() if query else []
    return render_template('index.html', products=results, query=query, title="Search Results")

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session: session['cart'] = []
    cart = list(session['cart'])
    cart.append(product_id)
    session['cart'] = cart
    session.modified = True 
    return jsonify({"status": "success", "cart_count": len(session['cart'])})

@app.route('/cart')
def cart():
    product_ids = session.get('cart', [])
    cart_products = [Product.query.get(pid) for pid in product_ids if Product.query.get(pid)]
    total = sum(p.price for p in cart_products)
    return render_template('cart.html', products=cart_products, total=total, title="Shopping Cart")

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

@app.route('/health')
def health_check():
    return "OK", 200

# 4. RUNNER
if __name__ == '__main__':
    app.run(debug=True, port=5001)