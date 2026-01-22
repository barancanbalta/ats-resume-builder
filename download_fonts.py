#!/usr/bin/env python3
"""
Download DejaVu fonts and install them to the fonts/ directory
"""
import urllib.request
import zipfile
import os
import shutil

def download_fonts():
    url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
    zip_path = "dejavu-fonts.zip"
    extract_path = "dejavu-fonts"
    fonts_dir = "fonts"

    try:
        print("📥 Downloading DejaVu fonts...")
        urllib.request.urlretrieve(url, zip_path)
        print("✓ Download complete")

        print("📂 Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print("✓ Extraction complete")

        print("📋 Creating fonts directory...")
        os.makedirs(fonts_dir, exist_ok=True)

        source_dir = os.path.join(extract_path, "dejavu-fonts-ttf-2.37", "ttf")
        fonts_to_copy = [
            "DejaVuSans.ttf",
            "DejaVuSans-Bold.ttf",
            "DejaVuSans-Italic.ttf",
            "DejaVuSans-BoldItalic.ttf"
        ]

        print("📝 Copying fonts...")
        for font in fonts_to_copy:
            src = os.path.join(source_dir, font)
            dst = os.path.join(fonts_dir, font)
            if os.path.exists(src):
                shutil.copy(src, dst)
                print(f"  ✓ {font}")
            else:
                print(f"  ✗ {font} not found!")

        # Cleanup
        print("🧹 Cleaning up...")
        os.remove(zip_path)
        shutil.rmtree(extract_path)

        print("\n✅ Done! Fonts installed successfully.")

        # Verify
        installed = os.listdir(fonts_dir)
        print(f"\n📦 Installed fonts: {len(installed)} files")
        for f in sorted(installed):
            if 'DejaVu' in f:
                print(f"  • {f}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    download_fonts()
