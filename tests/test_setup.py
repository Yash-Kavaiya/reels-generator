#!/usr/bin/env python3
"""
Quick test script to verify setup
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...")
    
    packages = {
        'moviepy': 'moviepy',
        'gTTS': 'gtts',
        'Pillow': 'PIL',
        'numpy': 'numpy',
        'schedule': 'schedule'
    }
    
    failed = []
    for name, module in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            failed.append(name)
    
    return len(failed) == 0, failed

def test_files():
    """Test if required files exist"""
    print("\nTesting required files...")
    
    files = [
        'quotes.json',
        'config.json',
        'main.py',
        'scheduler.py',
        'modules/quote_manager.py',
        'modules/tts_generator.py',
        'modules/video_creator.py'
    ]
    
    missing = []
    for file in files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            missing.append(file)
    
    return len(missing) == 0, missing

def test_directories():
    """Test if output directories exist"""
    print("\nTesting output directories...")
    
    dirs = [
        'output/audio',
        'output/videos',
        'assets/fonts'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        if Path(dir_path).exists():
            print(f"  ✓ {dir_path}")
        else:
            print(f"  ✗ {dir_path} - FAILED TO CREATE")
    
    return True

def test_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        from modules.quote_manager import QuoteManager
        print("  ✓ QuoteManager")
        
        from modules.tts_generator import TTSGenerator
        print("  ✓ TTSGenerator")
        
        from modules.video_creator import VideoCreator
        print("  ✓ VideoCreator")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def test_quote_manager():
    """Test quote manager functionality"""
    print("\nTesting quote manager...")
    
    try:
        from modules.quote_manager import QuoteManager
        qm = QuoteManager()
        
        if len(qm.quotes) > 0:
            print(f"  ✓ Loaded {len(qm.quotes)} quotes")
            quote = qm.get_random_quote(mark_used=False)
            print(f"  ✓ Sample quote: {quote['text'][:50]}...")
            return True
        else:
            print("  ✗ No quotes found in quotes.json")
            return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("YouTube Reels Automation - Setup Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test imports
    success, failed = test_imports()
    results.append(("Package imports", success))
    if not success:
        print(f"\n⚠ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
    
    # Test files
    success, missing = test_files()
    results.append(("Required files", success))
    if not success:
        print(f"\n⚠ Missing files: {', '.join(missing)}")
    
    # Test directories
    success = test_directories()
    results.append(("Output directories", success))
    
    # Test modules
    success = test_modules()
    results.append(("Custom modules", success))
    
    # Test quote manager
    success = test_quote_manager()
    results.append(("Quote manager", success))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to create reels.")
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Or run: python scheduler.py (for automation)")
    else:
        print("\n⚠ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install packages: pip install -r requirements.txt")
        print("- Check if all files are present")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
