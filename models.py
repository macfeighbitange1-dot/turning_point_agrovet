from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """
    Top-tier User model for secure authentication.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) 
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', 'Admin: {self.is_admin}')"

class Product(db.Model):
    """
    Enhanced Product model with SEO and Audit features.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True) 
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_featured = db.Column(db.Boolean, default=False) 
    sku = db.Column(db.String(50), unique=True, nullable=True) 

    def __repr__(self):
        return f"Product('{self.name}', '{self.category}', Price: {self.price})"

class Review(db.Model):
    """
    Professional Review model for bilingual social proof.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False) # e.g., 'Mwea, Kirinyaga'
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True) 

    def __repr__(self):
        return f"Review('{self.name}', '{self.location}', '{self.date_posted}')"

class ConsultancyRequest(db.Model):
    """
    Lead generation model for capturing Kirinyaga farmer inquiries.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=True)
    date_requested = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"ConsultancyRequest('{self.name}', '{self.phone}', '{self.date_requested}')"