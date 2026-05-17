from gtts import gTTS
from pathlib import Path
import logging
from modules.retry_handler import retry_with_backoff

logger = logging.getLogger(__name__)

class TTSGenerator:
    def __init__(self, config):
        self.use_sarvam = config['audio'].get('use_sarvam', False)
        self.language = config['audio']['language']
        self.tld = config['audio']['tld']
        self.slow = config['audio']['slow']
        self.output_dir = Path(config['output']['audio_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Sarvam AI if enabled
        if self.use_sarvam:
            try:
                from modules.sarvam_tts import SarvamTTS
                self.sarvam = SarvamTTS(config)
                logger.info("Sarvam AI TTS initialized")
            except Exception as e:
                logger.warning(f"Sarvam AI initialization failed: {e}")
                logger.info("Falling back to gTTS")
                self.use_sarvam = False
                self.sarvam = None
        else:
            self.sarvam = None
    
    @retry_with_backoff(max_retries=5, initial_delay=1, exceptions=(Exception,))
    def _generate_gtts(self, text, filename):
        """Generate audio with gTTS (with retry)"""
        tts = gTTS(text=text, lang=self.language, tld=self.tld, slow=self.slow)
        output_path = self.output_dir / filename.replace('.wav', '.mp3')
        tts.save(str(output_path))
        logger.info(f"Audio generated with gTTS: {output_path}")
        return str(output_path), "gTTS"
    
    def generate_audio(self, text, filename):
        """Generate audio from Gujarati text with fallback"""
        # Try Sarvam AI first
        if self.use_sarvam and self.sarvam:
            try:
                audio_path, speaker = self.sarvam.generate_audio(text, filename)
                if audio_path:
                    return audio_path, speaker
                else:
                    logger.warning("Sarvam AI returned None, falling back to gTTS")
            except Exception as e:
                logger.warning(f"Sarvam AI failed: {e}, falling back to gTTS")
        
        # Fallback to gTTS
        return self._generate_gtts(text, filename)
    
    def generate_from_quote(self, quote):
        """Generate audio from quote object"""
        filename = f"quote_{quote['id']}.wav"
        return self.generate_audio(quote['text'], filename)
