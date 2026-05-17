from sarvamai import SarvamAI
from pathlib import Path
import random
import logging
from modules.retry_handler import retry_with_backoff

logger = logging.getLogger(__name__)

class SarvamTTS:
    def __init__(self, config):
        self.api_key = config['audio'].get('sarvam_api_key', '')
        self.speakers = config['audio'].get('sarvam_speakers', ['shubh', 'anushka', 'abhilash', 'manisha'])
        self.model = config['audio'].get('sarvam_model', 'bulbul:v3')
        self.pace = config['audio'].get('pace', 1.0)
        self.sample_rate = config['audio'].get('speech_sample_rate', 48000)
        self.language = config['audio'].get('language', 'gu')
        self.output_dir = Path(config['output']['audio_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.last_speaker = None
        
        # Initialize Sarvam AI client
        if not self.api_key:
            raise ValueError("Sarvam AI API key not configured")
        
        self.client = SarvamAI(api_subscription_key=self.api_key)
        logger.info("Sarvam AI client initialized")
    
    def get_random_speaker(self):
        """Get a random speaker different from the last one"""
        available_speakers = [s for s in self.speakers if s != self.last_speaker]
        if not available_speakers:
            available_speakers = self.speakers
        speaker = random.choice(available_speakers)
        self.last_speaker = speaker
        return speaker
    
    @retry_with_backoff(max_retries=5, initial_delay=2, exceptions=(Exception,))
    def generate_audio(self, text, filename, speaker=None):
        """Generate audio using Sarvam AI SDK with retry logic"""
        try:
            # Select speaker
            if not speaker:
                speaker = self.get_random_speaker()
            
            logger.info(f"Generating audio with Sarvam AI voice: {speaker}")
            
            # Generate speech using SDK
            response = self.client.text_to_speech.convert(
                text=text,
                target_language_code=f"{self.language}-IN",
                speaker=speaker,
                pace=self.pace,
                speech_sample_rate=self.sample_rate,
                enable_preprocessing=True,
                model=self.model
            )
            
            # Save audio file
            output_path = self.output_dir / filename
            
            # The SDK returns base64 encoded audio in response.audios[0]
            if hasattr(response, 'audios') and len(response.audios) > 0:
                import base64
                audio_data = base64.b64decode(response.audios[0])
                
                with open(output_path, 'wb') as f:
                    f.write(audio_data)
                
                logger.info(f"Audio generated successfully: {output_path}")
                return str(output_path), speaker
            else:
                raise Exception("No audio data in response")
        
        except Exception as e:
            logger.error(f"Sarvam AI error: {e}")
            raise
    
    def generate_from_quote(self, quote):
        """Generate audio from quote object"""
        filename = f"quote_{quote['id']}_sarvam.wav"
        return self.generate_audio(quote['text'], filename)
