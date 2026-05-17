from moviepy import ImageClip, AudioFileClip
from moviepy.video.fx.FadeIn import FadeIn
from moviepy.video.fx.FadeOut import FadeOut
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path
import textwrap

class VideoCreator:
    def __init__(self, config):
        self.width = config['video']['width']
        self.height = config['video']['height']
        self.fps = config['video']['fps']
        self.bg_color = config['video']['background_color']
        self.text_color = config['video']['text_color']
        self.font_size = config['video']['font_size']
        self.output_dir = Path(config['output']['video_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Try to load Gujarati font, fallback to default
        self.font_path = config['fonts'].get('gujarati', None)
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_text_image(self, text, author):
        """Create an image with text overlay"""
        # Create background
        img = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(self.bg_color))
        draw = ImageDraw.Draw(img)
        
        # Load font - try multiple Gujarati fonts
        font = None
        author_font = None
        
        # List of possible Gujarati fonts to try
        gujarati_fonts = [
            self.font_path,  # User specified
            'C:\\Windows\\Fonts\\NotoSansGujarati-Regular.ttf',
            'C:\\Windows\\Fonts\\NotoSansGujarati.ttf',
            'C:\\Windows\\Fonts\\shruti.ttf',  # Windows default Gujarati
            'C:\\Windows\\Fonts\\Shruti.ttf',
            '/usr/share/fonts/truetype/noto/NotoSansGujarati-Regular.ttf',  # Linux
            '/System/Library/Fonts/Supplemental/NotoSansGujarati.ttf'  # Mac
        ]
        
        for font_path in gujarati_fonts:
            if font_path and Path(font_path).exists():
                try:
                    font = ImageFont.truetype(font_path, self.font_size)
                    author_font = ImageFont.truetype(font_path, self.font_size // 2)
                    print(f"Using font: {font_path}")
                    break
                except:
                    continue
        
        # If no Gujarati font found, use default (will show boxes)
        if not font:
            print("Warning: No Gujarati font found. Text may not display correctly.")
            print("Please download Noto Sans Gujarati font.")
            font = ImageFont.truetype("arial.ttf", self.font_size) if Path("C:\\Windows\\Fonts\\arial.ttf").exists() else ImageFont.load_default()
            author_font = ImageFont.truetype("arial.ttf", self.font_size // 2) if Path("C:\\Windows\\Fonts\\arial.ttf").exists() else ImageFont.load_default()
        
        # Wrap text
        max_chars = 20
        wrapped_text = textwrap.fill(text, width=max_chars)
        
        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2 - 100
        
        # Draw main text
        draw.text((x, y), wrapped_text, fill=self.text_color, font=font, align='center')
        
        # Draw author
        author_text = f"- {author}"
        author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
        author_width = author_bbox[2] - author_bbox[0]
        author_x = (self.width - author_width) // 2
        author_y = y + text_height + 50
        
        draw.text((author_x, author_y), author_text, fill=self.text_color, font=author_font)
        
        return np.array(img)
    
    def create_video(self, quote, audio_path, output_filename):
        """Create video with quote text and audio"""
        try:
            # Load audio to get duration
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            
            # Ensure minimum 10 seconds duration
            duration = max(audio_duration, 10.0)
            
            print(f"Audio duration: {audio_duration:.2f}s, Video duration: {duration:.2f}s")
            
            # Create text image
            text_img = self.create_text_image(quote['text'], quote['author'])
            
            # Create video clip from image (moviepy 2.x compatible)
            video_clip = ImageClip(text_img, duration=duration)
            
            # Add audio (loop if needed to match video duration)
            if audio_duration < duration:
                # Add silence at the end if audio is shorter
                from moviepy import concatenate_audioclips, AudioClip
                silence_duration = duration - audio_duration
                silence = AudioClip(lambda t: 0, duration=silence_duration, fps=audio_clip.fps)
                extended_audio = concatenate_audioclips([audio_clip, silence])
                video_clip = video_clip.with_audio(extended_audio)
            else:
                video_clip = video_clip.with_audio(audio_clip)
            
            # Add fade effects
            video_clip = video_clip.with_effects([FadeIn(0.5), FadeOut(0.5)])
            
            # Export video
            output_path = self.output_dir / output_filename
            video_clip.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac'
            )
            
            print(f"Video created: {output_path}")
            return str(output_path)
        
        except Exception as e:
            print(f"Error creating video: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            # Clean up
            if 'audio_clip' in locals():
                audio_clip.close()
            if 'video_clip' in locals():
                video_clip.close()
