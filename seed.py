from app import app
from models import db, Product

def seed_database():
    with app.app_context():
        # Clear existing to avoid duplicates
        db.drop_all()
        db.create_all()

        products = [
            Product(name="Hybrid Maize Seeds", category="Seeds", price=1200, description="High-yield, drought-resistant hybrid maize.", image_file="maize.jpg"),
            Product(name="DAP Fertilizer", category="Fertilizer", price=3500, description="Essential planting fertilizer for strong roots.", image_file="dap.jpg"),
            Product(name="Broad Spectrum Fungicide", category="Chemicals", price=850, description="Protects against blight and leaf rust.", image_file="fungicide.jpg"),
            Product(name="Organic Tomato Seeds", category="Seeds", price=450, description="Fast-maturing variety with excellent shelf life.", image_file="tomato.jpg"),
            Product(name="Knapsack Sprayer (20L)", category="Equipment", price=4200, description="Durable manual sprayer for farm chemicals.", image_file="sprayer.jpg"),
            Product(name="NPK 17:17:17", category="Fertilizer", price=3800, description="Balanced nutrients for top-dressing crops.", image_file="npk.jpg")
        ]

        db.session.bulk_save_objects(products)
        db.session.commit()
        print("🚀 Database Seeded with Elite Products!")

if __name__ == "__main__":
    seed_database()