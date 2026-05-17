from manim import *
from pathlib import Path
import subprocess
import os
import random
from moviepy import AudioFileClip

class ManimVideoCreator:
    def __init__(self, config):
        self.config = config
        self.width = config['video']['width']
        self.height = config['video']['height']
        self.fps = config['video']['fps']
        self.output_dir = Path(config['output']['video_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path("output/temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.last_gradient_index = -1
        self.last_color_scheme_index = -1
    
    def get_random_gradient(self):
        """Get a random gradient different from last one"""
        gradients = self.config['animation'].get('background_gradients', [
            ["#1a1a2e", "#16213e", "#0f3460"]
        ])
        
        available = [i for i in range(len(gradients)) if i != self.last_gradient_index]
        if not available:
            available = list(range(len(gradients)))
        
        index = random.choice(available)
        self.last_gradient_index = index
        return gradients[index]
    
    def get_random_color_scheme(self):
        """Get a random color scheme different from last one"""
        schemes = self.config['video'].get('color_schemes', [
            {"background": "#1a1a2e", "text": "#ffffff", "accent": "#FFD700"}
        ])
        
        available = [i for i in range(len(schemes)) if i != self.last_color_scheme_index]
        if not available:
            available = list(range(len(schemes)))
        
        index = random.choice(available)
        self.last_color_scheme_index = index
        return schemes[index]
    
    def create_video(self, quote, audio_path, output_filename):
        """Create video using Manim with audio sync"""
        try:
            print("Creating video with Manim animations...")
            
            # Get audio duration
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            audio_clip.close()
            
            # Ensure minimum 10 seconds
            video_duration = max(audio_duration, 10.0)
            print(f"Audio: {audio_duration:.2f}s, Video: {video_duration:.2f}s")
            
            # Get random colors
            gradient = self.get_random_gradient()
            color_scheme = self.get_random_color_scheme()
            
            print(f"Colors: BG={gradient[0]}, Text={color_scheme['text']}, Accent={color_scheme['accent']}")
            
            # Get font
            font_path = self.config['fonts'].get('gujarati', 'C:\\Windows\\Fonts\\shruti.ttf')
            
            # Create temporary Python file for Manim scene
            scene_file = self.temp_dir / f"scene_{quote['id']}.py"
            
            # Escape quotes in text
            quote_text = quote['text'].replace('"', '\\"').replace("'", "\\'")
            author_text = quote['author'].replace('"', '\\"').replace("'", "\\'")
            
            # Write scene file
            scene_code = f'''
from manim import *

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 30

class QuoteScene(Scene):
    def construct(self):
        # Gradient background
        bg_top = Rectangle(
            width=9, height=5.33,
            fill_color="{gradient[0]}", fill_opacity=1, stroke_width=0
        ).move_to(UP * 5.33)
        
        bg_mid = Rectangle(
            width=9, height=5.33,
            fill_color="{gradient[1]}", fill_opacity=1, stroke_width=0
        )
        
        bg_bottom = Rectangle(
            width=9, height=5.33,
            fill_color="{gradient[2]}", fill_opacity=1, stroke_width=0
        ).move_to(DOWN * 5.33)
        
        self.add(bg_top, bg_mid, bg_bottom)
        
        # Decorative elements
        top_line = Line(LEFT * 3, RIGHT * 3, color="{color_scheme['accent']}", stroke_width=4).move_to(UP * 5.5)
        bottom_line = Line(LEFT * 3, RIGHT * 3, color="{color_scheme['accent']}", stroke_width=4).move_to(DOWN * 5.5)
        
        # Decorative circles
        circle1 = Circle(radius=0.15, color="{color_scheme['accent']}", fill_opacity=1).move_to(LEFT * 3.5 + UP * 5.5)
        circle2 = Circle(radius=0.15, color="{color_scheme['accent']}", fill_opacity=1).move_to(RIGHT * 3.5 + UP * 5.5)
        circle3 = Circle(radius=0.15, color="{color_scheme['accent']}", fill_opacity=1).move_to(LEFT * 3.5 + DOWN * 5.5)
        circle4 = Circle(radius=0.15, color="{color_scheme['accent']}", fill_opacity=1).move_to(RIGHT * 3.5 + DOWN * 5.5)
        
        # Quote text using MarkupText for proper Gujarati rendering
        quote = MarkupText(
            f'<span font_family="Shruti" size="52000" foreground="{color_scheme['text']}" weight="bold">{quote_text}</span>',
            line_spacing=1.8
        ).scale(0.65)
        
        if quote.width > 7.5:
            quote.scale(7.5 / quote.width)
        
        # Author using MarkupText
        author = MarkupText(
            f'<span font_family="Shruti" size="36000" foreground="{color_scheme['accent']}" style="italic">- {author_text}</span>'
        ).scale(0.65)
        
        quote.move_to(ORIGIN)
        author.next_to(quote, DOWN, buff=1.0)
        
        # Animations
        self.play(
            Create(top_line), Create(bottom_line),
            FadeIn(circle1), FadeIn(circle2), FadeIn(circle3), FadeIn(circle4),
            run_time=1.0
        )
        
        self.play(Write(quote), run_time=2.5)
        self.play(FadeIn(author, shift=UP * 0.3), run_time=0.8)
        
        # Gentle pulse
        self.play(quote.animate.scale(1.08), run_time=0.6)
        self.play(quote.animate.scale(1/1.08), run_time=0.6)
        
        # Hold based on audio duration
        hold_time = max({video_duration} - 6.5, 2.0)
        self.wait(hold_time)
        
        # Fade out
        self.play(
            FadeOut(quote), FadeOut(author),
            FadeOut(top_line), FadeOut(bottom_line),
            FadeOut(circle1), FadeOut(circle2), FadeOut(circle3), FadeOut(circle4),
            run_time=1.2
        )
'''
            
            with open(scene_file, 'w', encoding='utf-8') as f:
                f.write(scene_code)
            
            # Render with Manim
            cmd = [
                'manim',
                '-qh',  # High quality
                '--format=mp4',
                '--disable_caching',
                f'--media_dir={self.temp_dir}',
                str(scene_file),
                'QuoteScene'
            ]
            
            print(f"Rendering with Manim...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Manim error: {result.stderr}")
                return None
            
            # Find generated video
            manim_output = list(self.temp_dir.glob("**/QuoteScene.mp4"))
            if not manim_output:
                print("Manim video not found")
                return None
            
            video_without_audio = manim_output[0]
            print(f"Manim video created: {video_without_audio}")
            
            # Add audio using ffmpeg
            final_output = self.output_dir / output_filename
            
            # If audio is shorter than video, extend with silence
            if audio_duration < video_duration:
                # Create extended audio with silence
                extended_audio = self.temp_dir / f"extended_audio_{quote['id']}.wav"
                cmd = [
                    'ffmpeg', '-y',
                    '-i', str(audio_path),
                    '-af', f'apad=pad_dur={video_duration - audio_duration}',
                    str(extended_audio)
                ]
                subprocess.run(cmd, capture_output=True)
                audio_to_use = extended_audio
            else:
                audio_to_use = audio_path
            
            # Combine video and audio
            cmd = [
                'ffmpeg', '-y',
                '-i', str(video_without_audio),
                '-i', str(audio_to_use),
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-shortest',
                '-pix_fmt', 'yuv420p',
                str(final_output)
            ]
            
            print("Adding audio to video...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"FFmpeg error: {result.stderr}")
                return None
            
            print(f"✓ Video created: {final_output}")
            
            # Cleanup
            try:
                scene_file.unlink()
                if video_without_audio.exists():
                    video_without_audio.unlink()
            except:
                pass
            
            return str(final_output)
            
        except Exception as e:
            print(f"Error creating video: {e}")
            import traceback
            traceback.print_exc()
            return None
