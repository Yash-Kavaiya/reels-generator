"""
Scalable batch processor for creating multiple reels
"""
import logging
from pathlib import Path
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from modules.retry_handler import retry_with_backoff

logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self, quote_manager, tts_generator, video_creator, max_workers=3):
        self.quote_manager = quote_manager
        self.tts_generator = tts_generator
        self.video_creator = video_creator
        self.max_workers = max_workers
        self.results = []
        self.failed = []
        
    @retry_with_backoff(max_retries=5, initial_delay=2, exceptions=(Exception,))
    def create_single_reel(self, quote):
        """Create a single reel with retry logic"""
        logger.info(f"Processing Quote ID: {quote['id']}")
        logger.info(f"Text: {quote['text'][:50]}...")
        
        # Generate audio
        logger.info("Generating audio...")
        result = self.tts_generator.generate_from_quote(quote)
        
        if isinstance(result, tuple):
            audio_path, speaker = result
            if speaker and speaker != "gTTS":
                logger.info(f"Voice: {speaker}")
        else:
            audio_path = result
        
        if not audio_path:
            raise Exception("Failed to generate audio")
        
        # Create video
        logger.info("Creating video...")
        video_filename = f"reel_quote_{quote['id']}.mp4"
        video_path = self.video_creator.create_video(quote, audio_path, video_filename)
        
        if not video_path:
            raise Exception("Failed to create video")
        
        logger.info(f"✓ Reel created: {video_path}")
        return {
            'quote_id': quote['id'],
            'video_path': video_path,
            'audio_path': audio_path,
            'status': 'success'
        }
    
    def process_batch(self, count, parallel=False):
        """
        Process multiple reels
        
        Args:
            count: Number of reels to create
            parallel: If True, process in parallel (use with caution)
        """
        logger.info(f"Starting batch processing: {count} reels")
        logger.info(f"Parallel processing: {parallel}")
        
        start_time = datetime.now()
        self.results = []
        self.failed = []
        
        if parallel:
            self._process_parallel(count)
        else:
            self._process_sequential(count)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Summary
        success_count = len(self.results)
        failed_count = len(self.failed)
        
        logger.info("=" * 60)
        logger.info("BATCH PROCESSING COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total requested: {count}")
        logger.info(f"Successful: {success_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Average: {duration/count:.2f} seconds per reel")
        logger.info("=" * 60)
        
        # Save report
        self._save_report(count, success_count, failed_count, duration)
        
        return self.results, self.failed
    
    def _process_sequential(self, count):
        """Process reels one by one"""
        for i in range(count):
            logger.info(f"\n--- Reel {i+1}/{count} ---")
            
            try:
                quote = self.quote_manager.get_random_quote()
                result = self.create_single_reel(quote)
                self.results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to create reel {i+1}: {e}")
                self.failed.append({
                    'index': i+1,
                    'error': str(e)
                })
    
    def _process_parallel(self, count):
        """Process reels in parallel (use with caution for API rate limits)"""
        quotes = [self.quote_manager.get_random_quote() for _ in range(count)]
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_quote = {
                executor.submit(self.create_single_reel, quote): quote 
                for quote in quotes
            }
            
            for i, future in enumerate(as_completed(future_to_quote), 1):
                quote = future_to_quote[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    logger.info(f"Completed {i}/{count}")
                    
                except Exception as e:
                    logger.error(f"Failed quote {quote['id']}: {e}")
                    self.failed.append({
                        'quote_id': quote['id'],
                        'error': str(e)
                    })
    
    def _save_report(self, total, success, failed, duration):
        """Save batch processing report"""
        report_dir = Path("output/reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_requested': total,
            'successful': success,
            'failed': failed,
            'duration_seconds': duration,
            'average_per_reel': duration / total if total > 0 else 0,
            'success_rate': (success / total * 100) if total > 0 else 0,
            'results': self.results,
            'failures': self.failed
        }
        
        report_file = report_dir / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Report saved: {report_file}")
