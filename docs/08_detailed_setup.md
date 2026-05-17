# Setup Guide - YouTube Reels Automation

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for TTS)

## Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Gujarati Font (Optional but Recommended)
For better text rendering, download a Gujarati font:

**Option A: Noto Sans Gujarati (Recommended)**
1. Visit: https://fonts.google.com/noto/specimen/Noto+Sans+Gujarati
2. Download the font
3. Extract and copy `NotoSansGujarati-Regular.ttf` to `assets/fonts/`

**Option B: Use System Font**
- The script will work with default fonts if no Gujarati font is provided
- Text may not render perfectly

### 3. Create Required Directories
```bash
mkdir -p assets/fonts
mkdir -p assets/backgrounds
mkdir -p output/audio
mkdir -p output/videos
```

### 4. Add More Quotes
Edit `quotes.json` to add your own Gujarati quotes:
```json
{
  "id": 6,
  "text": "તમારો ગુજરાતી ક્વોટ અહીં",
  "author": "લેખક નામ",
  "category": "motivation",
  "used": false
}
```

## Usage

### Basic Usage
Run the main script:
```bash
python main.py
```

Then choose from the menu:
1. Create single reel (random quote)
2. Create single reel (specific quote ID)
3. Create batch of reels
4. Exit

### Quick Single Reel
```python
from main import create_reel
create_reel()  # Creates one reel with random quote
```

### Batch Creation
```python
from main import create_batch
create_batch(10)  # Creates 10 reels
```

## Configuration

Edit `config.json` to customize:

### Video Settings
- `width`, `height`: Video dimensions (default: 1080x1920 for vertical)
- `fps`: Frames per second (default: 30)
- `background_color`: Hex color code
- `text_color`: Hex color code
- `font_size`: Text size in pixels

### Audio Settings
- `language`: Language code (gu for Gujarati)
- `tld`: Top-level domain for accent (co.in for Indian accent)
- `slow`: Set to true for slower speech

## Troubleshooting

### Issue: "No module named 'moviepy'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Font not rendering properly
**Solution:** Download and install Gujarati font (see step 2)

### Issue: Audio generation fails
**Solution:** Check internet connection (gTTS requires internet)

### Issue: Video creation is slow
**Solution:** This is normal. Video rendering takes time. For faster processing:
- Reduce video resolution in config.json
- Reduce fps to 24
- Use a more powerful computer

### Issue: "ImageMagick not found"
**Solution:** MoviePy may need ImageMagick for some features
```bash
# Windows: Download from https://imagemagick.org/
# Mac: brew install imagemagick
# Linux: sudo apt-get install imagemagick
```

## Automation Options

### 1. Windows Task Scheduler
Create a batch file `run_automation.bat`:
```batch
@echo off
cd /d "C:\path\to\your\project"
python -c "from main import create_reel; create_reel()"
```

Schedule it in Task Scheduler to run daily.

### 2. Linux/Mac Cron Job
```bash
# Edit crontab
crontab -e

# Add line to run daily at 9 AM
0 9 * * * cd /path/to/project && python3 -c "from main import create_reel; create_reel()"
```

### 3. Python Script for Scheduling
```python
import schedule
import time
from main import create_reel

def job():
    create_reel()

# Run every day at 9:00 AM
schedule.every().day.at("09:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## YouTube Upload (Optional)

To automatically upload to YouTube, you'll need:
1. YouTube Data API credentials
2. OAuth 2.0 authentication
3. Additional code for upload functionality

See `modules/uploader.py` (to be implemented) for upload features.

## Tips for Better Results

1. **Quote Quality**: Use meaningful, short quotes (2-3 lines max)
2. **Font Size**: Adjust based on text length
3. **Background**: Add gradient or images for visual appeal
4. **Music**: Add background music for engagement
5. **Consistency**: Post regularly for better reach
6. **Hashtags**: Use relevant hashtags when uploading

## Next Steps

1. Test with sample quotes
2. Add your own quote collection
3. Customize video style
4. Set up automation schedule
5. Consider YouTube upload integration

## Support

For issues or questions:
- Check the troubleshooting section
- Review MoviePy documentation: https://zulko.github.io/moviepy/
- Review gTTS documentation: https://gtts.readthedocs.io/
