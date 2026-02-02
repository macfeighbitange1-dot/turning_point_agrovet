from app import app
from models import db, Product

def seed_database():
    with app.app_context():
        # Clear existing to avoid duplicates
        db.drop_all()
        db.create_all()

        products = [
            Product(
                name="Premium Crop Solution", 
                category="Chemicals", 
                price=1500, 
                description="Advanced agricultural treatment for crop protection.", 
                image_file="582667416_1379453987524899_4911843970148037333_n.jpg"
            ),
            Product(
                name="Agrovet Specialty Feed", 
                category="Livestock", 
                price=2400, 
                description="High-nutrient specialized animal feed.", 
                image_file="clean_ecommerce_product_image_of_a_70kg.jpeg"
            ),
            Product(
                name="Elite Growth Formula", 
                category="Fertilizer", 
                price=3200, 
                description="Science-backed formula for accelerated plant growth.", 
                image_file="Gemini_Generated_Image_jx3udojx3udojx3u.png"
            ),
            Product(
                name="Specialized Treatment 50g", 
                category="Chemicals", 
                price=950, 
                description="Concentrated treatment for specific crop ailments.", 
                image_file="high_detail_studio_product_image_of_a_50g.jpeg"
            ),
            Product(
                name="Premium Fertilizer 50kg", 
                category="Fertilizer", 
                price=3600, 
                description="High-resolution industrial grade planting fertilizer.", 
                image_file="high_resolution_ecommerce_product_image_of_a_50kg.jpeg"
            ),
            Product(
                name="Hybrid Seed Selection 2kg", 
                category="Seeds", 
                price=1400, 
                description="Professional grade seeds for maximum yield.", 
                image_file="professional_ecommerce_product_photo_of_a_2kg.jpeg"
            ),
            Product(
                name="Dairy Meal 70kg", 
                category="Livestock", 
                price=2900, 
                description="Optimized nutrition for high-yield dairy cattle.", 
                image_file="ultra_realistic_product_photography_of_a_70kg_dairy.jpeg"
            ),
            Product(
                name="DAP Planting Fertilizer", 
                category="Fertilizer", 
                price=3500, 
                description="Essential root-development fertilizer for planting season.", 
                image_file="ultra_realistic_professional_ecommerce_product_image_of_dap.jpeg"
            ),
            Product(
                name="CAN Top Dressing 50kg", 
                category="Fertilizer", 
                price=3100, 
                description="Pure CAN fertilizer for vigorous leafy growth.", 
                image_file="ultra_realistic_studio_photograph_of_a_50kg_can.jpeg"
            ),
            Product(
                name="Certified Seed Stock 2kg", 
                category="Seeds", 
                price=1250, 
                description="Ultra-sharp studio quality certified seeds.", 
                image_file="ultra_sharp_studio_product_photo_of_a_2kg.jpeg"
            ),
            Product(
                name="Turning Point Essential", 
                category="Equipment", 
                price=4800, 
                description="Core agricultural solution for modern farm management.", 
                image_file="486617515_630626369873061_277230241273628885_n.jpg"
            )
        ]

        db.session.bulk_save_objects(products)
        db.session.commit()
        print("🚀 Turning Point Agrovet: Real Inventory Loaded Successfully!")

if __name__ == "__main__":
    seed_database()