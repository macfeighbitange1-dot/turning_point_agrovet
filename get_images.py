import urllib.request
import os

# Ensure the directory exists
IMAGE_DIR = os.path.join('static', 'img')
os.makedirs(IMAGE_DIR, exist_ok=True)

# A mapping of our database 'image_file' names to professional high-res sources
# We use source.unsplash.com to pull specific high-quality farming topics
agro_images = {
    "maize.jpg": "https://images.unsplash.com/photo-1551730459-92db2a308d6a?w=800",
    "cabbage.jpg": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=800",
    "tomato.jpg": "https://images.unsplash.com/photo-1592841200221-a6898f307baa?w=800",
    "dap.jpg": "https://images.unsplash.com/photo-1628352081506-83c43123ed6d?w=800",
    "can.jpg": "https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?w=800",
    "npk.jpg": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=800",
    "fungicide.jpg": "https://images.unsplash.com/photo-1592982537447-7440770cbfc9?w=800",
    "insecticide.jpg": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800",
    "sprayer.jpg": "https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=800",
    "phmeter.jpg": "https://images.unsplash.com/photo-1516253593875-bd7ba052fbc5?w=800"
}

def download_assets():
    print(f"🚀 Initializing Top 0.1% Image Sync for Turning Point Agrovet...")
    for filename, url in agro_images.items():
        path = os.path.join(IMAGE_DIR, filename)
        try:
            print(f"📥 Downloading {filename}...")
            urllib.request.urlretrieve(url, path)
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")
    print("\n✅ All professional assets loaded to static/img/")

if __name__ == "__main__":
    download_assets()