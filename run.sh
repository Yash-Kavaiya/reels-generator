#!/bin/bash
# Quick launcher for YouTube Reels Automation

echo "========================================"
echo "YouTube Reels Automation - Gujarati Quotes"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Select an option:"
echo "1. Run setup test"
echo "2. Create a single reel"
echo "3. Run main program (interactive)"
echo "4. Run scheduler (automation)"
echo "5. Install dependencies"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        python3 test_setup.py
        ;;
    2)
        python3 -c "from main import create_reel; create_reel()"
        ;;
    3)
        python3 main.py
        ;;
    4)
        python3 scheduler.py
        ;;
    5)
        pip3 install -r requirements.txt
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

echo ""
