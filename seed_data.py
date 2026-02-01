from app import app
from models import db, Product

def seed_products():
    products = [
        # FEEDS & DAIRY
        Product(name="Dairy Meal (70kg)", category="Feed", price=3200.0, stock_quantity=40, 
                image_file="ultra_realistic_product_photography_of_a_70kg_dairy.jpeg",
                description="Premium high-yield dairy meal for maximum milk production and livestock health."),
        
        Product(name="Standard Livestock Feed (70kg)", category="Feed", price=2900.0, stock_quantity=30, 
                image_file="clean_ecommerce_product_image_of_a_70kg.jpeg",
                description="Balanced nutritional diet designed for general livestock maintenance."),

        # FERTILIZERS
        Product(name="DAP Fertilizer (50kg)", category="Fertilizer", price=6500.0, stock_quantity=20, 
                image_file="ultra_realistic_professional_ecommerce_product_image_of_dap.jpeg",
                description="Diammonium Phosphate: The essential foundation for strong root development during planting."),
        
        Product(name="CAN Fertilizer (50kg)", category="Fertilizer", price=5800.0, stock_quantity=25, 
                image_file="ultra_realistic_studio_photograph_of_a_50kg_can.jpeg",
                description="Calcium Ammonium Nitrate: Top-tier nitrogen supplement for explosive leafy growth."),
        
        Product(name="Cereal Fertilizer (50kg)", category="Fertilizer", price=6100.0, stock_quantity=15, 
                image_file="high_resolution_ecommerce_product_image_of_a_50kg.jpeg",
                description="Specialized high-resolution nutrient blend for high-yield cereal crops."),

        # SEEDS
        Product(name="Hybrid Maize (2kg)", category="Seeds", price=950.0, stock_quantity=100, 
                image_file="ultra_sharp_studio_product_photo_of_a_2kg.jpeg",
                description="Certified ultra-sharp hybrid maize seeds, drought-resistant and optimized for high output."),
        
        Product(name="Sorghum Seeds (2kg)", category="Seeds", price=850.0, stock_quantity=60, 
                image_file="professional_ecommerce_product_photo_of_a_2kg.jpeg",
                description="Professional grade sorghum seeds, excellent for arid and semi-arid climatic conditions."),
        
        Product(name="Vegetable Seed Mix", category="Seeds", price=300.0, stock_quantity=150, 
                image_file="486617515_630626369873061_277230241273628885_n.jpg",
                description="High-germination vegetable seed variety pack for kitchen gardens and commercial use."),

        # SUPPLEMENTS & CHEMICALS
        Product(name="Mineral Supplement (50g)", category="Animal Health", price=450.0, stock_quantity=200, 
                image_file="high_detail_studio_product_image_of_a_50g.jpeg",
                description="Concentrated mineral salts essential for livestock bone density and productivity."),
        
        Product(name="Growth Booster Elite", category="Chemicals", price=1200.0, stock_quantity=50, 
                image_file="Gemini_Generated_Image_jx3udojx3udojx3u.png",
                description="Advanced liquid growth booster for accelerated crop development and pest resistance.")
    ]

    with app.app_context():
        print("Cleaning database for a fresh start...")
        db.drop_all()   
        db.create_all() 
        
        db.session.add_all(products)
        db.session.commit()
        print("🚀 Success: Turning Point Agrovet database updated with 10 high-resolution products!")

if __name__ == "__main__":
    seed_products()