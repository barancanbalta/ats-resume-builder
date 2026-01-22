from cv_generator import get_generator
from user_data import user_profile
import os

templates = ["Klasik", "Modern", "Akademik"]

print("Starting verification for templates...")

for t_name in templates:
    try:
        print(f"Testing {t_name}...")
        gen = get_generator(t_name)
        # Generate raw string/bytes
        output = gen.generate(user_profile)
        
        # Save to disk to verify file creation
        filename = f"test_cv_{t_name}.pdf"
        with open(filename, "wb") as f:
            f.write(output)
            
        file_size = os.path.getsize(filename)
        print(f"SUCCESS: {t_name} generated. Size: {file_size} bytes")
        
    except Exception as e:
        print(f"FAILED: {t_name} - {str(e)}")
