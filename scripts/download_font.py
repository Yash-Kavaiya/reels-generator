#!/usr/bin/env python3
"""
Download Noto Sans Gujarati font for better text rendering
"""

import urllib.request
import os
from pathlib import Path

def download_gujarati_font():
    """Download Noto Sans Gujarati font from Google Fonts"""
    
    print("Downloading Noto Sans Gujarati font...")
    
    # Create fonts directory
    fonts_dir = Path("assets/fonts")
    fonts_dir.mkdir(parents=True, exist_ok=True)
    
    # Font URL (direct link to the font file)
    font_url = "https://github.com/notofonts/gujarati/raw/main/fonts/NotoSansGujarati/hinted/ttf/NotoSansGujarati-Regular.ttf"
    font_path = fonts_dir / "NotoSansGujarati-Regular.ttf"
    
    try:
        # Download the font
        print(f"Downloading from: {font_url}")
        urllib.request.urlretrieve(font_url, font_path)
        print(f"✓ Font downloaded successfully to: {font_path}")
        print("\nThe font will now be used for better Gujarati text rendering.")
        return True
    except Exception as e:
        print(f"✗ Error downloading font: {e}")
        print("\nAlternative: Download manually from:")
        print("https://fonts.google.com/noto/specimen/Noto+Sans+Gujarati")
        print(f"And save to: {font_path}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Gujarati Font Downloader")
    print("=" * 60)
    print()
    
    success = download_gujarati_font()
    
    if success:
        print("\n✓ Setup complete! You can now create reels with proper Gujarati text.")
    else:
        print("\n⚠ Font download failed. The system will use Windows Shruti font as fallback.")
    
    print("\nPress Enter to continue...")
    input()
