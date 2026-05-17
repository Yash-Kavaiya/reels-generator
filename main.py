#!/usr/bin/env python3
"""
YouTube Reels Automation - Gujarati Quotes
Production-ready script with retry logic and scalability
"""

import json
import sys
from pathlib import Path
from modules.quote_manager import QuoteManager
from modules.tts_generator import TTSGenerator
from modules.batch_processor import BatchProcessor
from modules.logger import setup_logger
from modules.retry_handler import retry_with_backoff

# Setup logging
logger = setup_logger()

def load_config(config_file='config.json'):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in config file: {e}")
        sys.exit(1)

@retry_with_backoff(max_retries=5, initial_delay=2, exceptions=(Exception,))
def create_reel(quote_id=None):
    """Create a single reel with retry logic"""
    logger.info("=" * 60)
    logger.info("YouTube Reels Automation - Gujarati Quotes")
    logger.info("=" * 60)
    
    # Load configuration
    config = load_config()
    
    # Initialize modules
    quote_manager = QuoteManager()
    tts_generator = TTSGenerator(config)
    
    # Choose video creator based on config
    use_manim = config.get('animation', {}).get('use_manim', False)
    
    if use_manim:
        try:
            from modules.manim_video_creator import ManimVideoCreator
            video_creator = ManimVideoCreator(config)
            logger.info("Using Manim for video creation")
        except Exception as e:
            logger.warning(f"Manim not available: {e}")
            logger.info("Falling back to MoviePy")
            from modules.video_creator import VideoCreator
            video_creator = VideoCreator(config)
    else:
        from modules.video_creator import VideoCreator
        video_creator = VideoCreator(config)
        logger.info("Using MoviePy for video creation")
    
    # Get quote
    if quote_id:
        quote = quote_manager.get_quote_by_id(quote_id)
        if not quote:
            logger.error(f"Quote with ID {quote_id} not found")
            return None
    else:
        quote = quote_manager.get_random_quote()
    
    logger.info(f"Selected Quote (ID: {quote['id']})")
    logger.info(f"Text: {quote['text']}")
    logger.info(f"Author: {quote['author']}")
    logger.info(f"Category: {quote['category']}")
    
    # Generate audio
    logger.info("[1/2] Generating audio...")
    result = tts_generator.generate_from_quote(quote)
    
    if isinstance(result, tuple):
        audio_path, speaker = result
        if speaker and speaker != "gTTS":
            logger.info(f"Voice: {speaker}")
    else:
        audio_path = result
    
    if not audio_path:
        raise Exception("Failed to generate audio")
    
    # Create video
    logger.info("[2/2] Creating video...")
    video_filename = f"reel_quote_{quote['id']}.mp4"
    video_path = video_creator.create_video(quote, audio_path, video_filename)
    
    if not video_path:
        raise Exception("Failed to create video")
    
    logger.info("=" * 60)
    logger.info("✓ Reel created successfully!")
    logger.info(f"Video: {video_path}")
    logger.info("=" * 60)
    
    return video_path

def create_batch(count=5, parallel=False):
    """Create multiple reels with batch processor"""
    logger.info(f"Creating batch of {count} reels...")
    
    # Load configuration
    config = load_config()
    
    # Initialize modules
    quote_manager = QuoteManager()
    tts_generator = TTSGenerator(config)
    
    # Choose video creator
    use_manim = config.get('animation', {}).get('use_manim', False)
    
    if use_manim:
        try:
            from modules.manim_video_creator import ManimVideoCreator
            video_creator = ManimVideoCreator(config)
        except Exception as e:
            logger.warning(f"Manim not available: {e}, using MoviePy")
            from modules.video_creator import VideoCreator
            video_creator = VideoCreator(config)
    else:
        from modules.video_creator import VideoCreator
        video_creator = VideoCreator(config)
    
    # Create batch processor
    processor = BatchProcessor(
        quote_manager, 
        tts_generator, 
        video_creator,
        max_workers=3  # Adjust based on your system
    )
    
    # Process batch
    results, failed = processor.process_batch(count, parallel=parallel)
    
    return results, failed

def main():
    """Main entry point"""
    logger.info("YouTube Reels Automation - Production Mode")
    print("\n" + "=" * 60)
    print("YouTube Reels Automation")
    print("=" * 60)
    print("1. Create single reel (random quote)")
    print("2. Create single reel (specific quote ID)")
    print("3. Create batch of reels (sequential)")
    print("4. Create batch of reels (parallel - faster but use with caution)")
    print("5. Create 1000 reels (sequential)")
    print("6. Exit")
    print("=" * 60)
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    try:
        if choice == '1':
            create_reel()
            
        elif choice == '2':
            quote_id = int(input("Enter quote ID: "))
            create_reel(quote_id)
            
        elif choice == '3':
            count = int(input("How many reels to create? "))
            create_batch(count, parallel=False)
            
        elif choice == '4':
            count = int(input("How many reels to create? "))
            print("\n⚠ Warning: Parallel processing may hit API rate limits")
            confirm = input("Continue? (yes/no): ").strip().lower()
            if confirm == 'yes':
                create_batch(count, parallel=True)
            else:
                print("Cancelled")
                
        elif choice == '5':
            print("\n🚀 Creating 1000 reels...")
            print("This will take several hours. Progress will be logged.")
            confirm = input("Continue? (yes/no): ").strip().lower()
            if confirm == 'yes':
                create_batch(1000, parallel=False)
            else:
                print("Cancelled")
                
        elif choice == '6':
            logger.info("Exiting...")
            sys.exit(0)
            
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
