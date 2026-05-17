#!/usr/bin/env python3
"""
Scheduler for automated reel creation
Run this script to automatically create reels at scheduled times
"""

import schedule
import time
from datetime import datetime
from main import create_reel

def scheduled_job():
    """Job to run at scheduled time"""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled reel creation...")
    try:
        video_path = create_reel()
        if video_path:
            print(f"✓ Scheduled reel created successfully at {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"✗ Failed to create scheduled reel")
    except Exception as e:
        print(f"✗ Error in scheduled job: {e}")

def main():
    """Main scheduler"""
    print("=" * 60)
    print("YouTube Reels Automation Scheduler")
    print("=" * 60)
    print("\nSchedule Options:")
    print("1. Every day at specific time")
    print("2. Every X hours")
    print("3. Every X minutes (for testing)")
    print("4. Custom schedule")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        time_str = input("Enter time (HH:MM format, e.g., 09:00): ").strip()
        schedule.every().day.at(time_str).do(scheduled_job)
        print(f"\n✓ Scheduled to run every day at {time_str}")
    
    elif choice == '2':
        hours = int(input("Enter hours interval: "))
        schedule.every(hours).hours.do(scheduled_job)
        print(f"\n✓ Scheduled to run every {hours} hours")
    
    elif choice == '3':
        minutes = int(input("Enter minutes interval: "))
        schedule.every(minutes).minutes.do(scheduled_job)
        print(f"\n✓ Scheduled to run every {minutes} minutes")
    
    elif choice == '4':
        print("\nCustom schedule examples:")
        print("- schedule.every().monday.at('10:00').do(scheduled_job)")
        print("- schedule.every().hour.at(':30').do(scheduled_job)")
        print("\nEdit scheduler.py to add custom schedule")
        return
    
    else:
        print("Invalid choice")
        return
    
    print("\nScheduler is running... Press Ctrl+C to stop")
    print(f"Next run: {schedule.next_run()}")
    
    # Run scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")

if __name__ == "__main__":
    main()
