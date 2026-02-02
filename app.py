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

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Allows customers to join. Prevents them from becoming admins."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or Email already taken.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password, is_admin=False)
        
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html', title='Join Us')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard' if current_user.is_admin else 'home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('admin_dashboard' if user.is_admin else 'home'))
        else:
            flash('Login Unsuccessful. Please check credentials.', 'danger')
            
    return render_template('login.html', title='Login')

@app.route('/consultancy', methods=['GET', 'POST'])
def consultancy():
    """Handles farmer requests for expert advice."""
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

# --- SECURE RECOVERY SYSTEM ---
@app.route('/recovery/<string:secret_key>')
def secure_recovery(secret_key):
    """Syncs the Master Admin account with Render Environment Variables."""
    master_key = os.environ.get('RECOVERY_KEY')
    
    if not master_key or secret_key != master_key:
        abort(404) 
        
    admin = User.query.filter_by(username='turning_admin').first()
    new_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    hashed_pw = bcrypt.generate_password_hash(new_password).decode('utf-8')
    
    if admin:
        admin.password = hashed_pw
        admin.is_admin = True
    else:
        admin = User(username='turning_admin', email='admin@tp.com', 
                     password=hashed_pw, is_admin=True)
        db.session.add(admin)
        
    db.session.commit()
    return "Admin Credentials Synced Successfully."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

# --- SECURE ADMIN DASHBOARD ---
@app.route('/admin_portal')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403) 
    all_reviews = Review.query.order_by(Review.date_posted.desc()).all()
    all_consultancies = ConsultancyRequest.query.order_by(ConsultancyRequest.date_requested.desc()).all()
    return render_template('admin.html', reviews=all_reviews, consultancies=all_consultancies, title="Admin Panel")

# 3. UTILITY ROUTES
@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = Product.query.filter((Product.name.icontains(query)) | (Product.category.icontains(query))).all() if query else []
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

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)