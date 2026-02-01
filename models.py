from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    Top-tier User model for secure authentication.
    UserMixin provides default implementations for is_authenticated, is_active, etc.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # Stores the hashed bcrypt string
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', 'Admin: {self.is_admin}')"

class Product(db.Model):
    """
    Enhanced Product model with SEO and Audit features.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True) # Index for faster search
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    
    # New: Professional features
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False) # For highlighting on home page
    sku = db.Column(db.String(50), unique=True, nullable=True) # Stock Keeping Unit

    def __repr__(self):
        return f"Product('{self.name}', '{self.category}', Price: {self.price})"