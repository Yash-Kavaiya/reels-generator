# 📁 Project File Structure

## Overview

This document describes the complete file structure of the YouTube Reels Automation system.

## Root Directory

```
reels-generator/
├── .git/                       # Git repository
├── .gitignore                  # Git ignore rules
├── README.md                   # Main documentation
├── requirements.txt            # Python dependencies
├── main.py                     # Main application entry point
├── config.json                 # Configuration (not in git)
├── config.template.json        # Configuration template
├── quotes.json                 # Quote database
│
├── modules/                    # Core application modules
├── scripts/                    # Utility scripts
├── tests/                      # Test files
├── docs/                       # Documentation
├── assets/                     # Static assets
├── output/                     # Generated content
└── logs/                       # Log files
```

## Detailed Structure

### 📦 `/modules/` - Core Application Modules

```
modules/
├── __init__.py                 # Package initializer
├── quote_manager.py            # Quote selection and tracking
├── sarvam_tts.py              # Sarvam AI TTS integration
├── tts_generator.py           # TTS with fallback logic
├── manim_video_creator.py     # Manim animation creator
├── video_creator.py           # MoviePy video creator (fallback)
├── batch_processor.py         # Batch processing engine
├── retry_handler.py           # Retry logic with backoff
└── logger.py                  # Logging configuration
```

**Purpose:** Core business logic and functionality

### 🔧 `/scripts/` - Utility Scripts

```
scripts/
├── run.bat                    # Windows launcher
├── run.sh                     # Linux/Mac launcher
├── scheduler.py               # Automation scheduler
└── download_font.py           # Font downloader utility
```

**Purpose:** Helper scripts for setup and automation

### 🧪 `/tests/` - Test Files

```
tests/
├── test_production.py         # Production readiness tests
└── test_setup.py              # Setup verification tests
```

**Purpose:** Quality assurance and validation

### 📚 `/docs/` - Documentation

```
docs/
├── 00_file_structure.md       # This file
├── 01_project_plan.md         # Original project plan
├── 02_setup_guide.md          # Quick setup guide
├── 03_production_guide.md     # Production usage guide
├── 04_system_status.md        # System features status
├── 05_upgrade_summary.md      # Upgrade notes
├── 06_production_ready.md     # Production readiness summary
├── 07_git_push_summary.md     # Git push documentation
└── 08_detailed_setup.md       # Detailed setup instructions
```

**Purpose:** Comprehensive project documentation

### 🎨 `/assets/` - Static Assets

```
assets/
└── fonts/
    ├── .gitkeep               # Keep directory in git
    └── *.ttf                  # Gujarati fonts (not in git)
```

**Purpose:** Fonts and other static resources

### 📤 `/output/` - Generated Content

```
output/
├── audio/
│   ├── .gitkeep              # Keep directory in git
│   └── *.mp3, *.wav          # Generated audio (not in git)
├── videos/
│   ├── .gitkeep              # Keep directory in git
│   └── *.mp4                 # Final videos (not in git)
├── temp/
│   ├── .gitkeep              # Keep directory in git
│   └── *                     # Temporary files (not in git)
└── reports/
    ├── .gitkeep              # Keep directory in git
    └── *.json                # Batch reports (not in git)
```

**Purpose:** All generated content and reports

### 📝 `/logs/` - Log Files

```
logs/
└── reels_*.log               # Timestamped log files (not in git)
```

**Purpose:** Application logs and debugging

## File Naming Conventions

### Python Modules
- **Format:** `lowercase_with_underscores.py`
- **Examples:** `quote_manager.py`, `batch_processor.py`

### Documentation
- **Format:** `##_descriptive_name.md`
- **Examples:** `01_project_plan.md`, `02_setup_guide.md`
- **Numbering:** Sequential for reading order

### Scripts
- **Format:** `descriptive_name.ext`
- **Examples:** `run.bat`, `scheduler.py`

### Configuration
- **Format:** `name.json` or `name.template.json`
- **Examples:** `config.json`, `config.template.json`

### Generated Files
- **Audio:** `quote_{id}.wav` or `quote_{id}_sarvam.wav`
- **Video:** `reel_quote_{id}.mp4`
- **Reports:** `batch_report_{timestamp}.json`
- **Logs:** `reels_{timestamp}.log`

## Important Files

### Configuration Files

| File | Purpose | In Git? |
|------|---------|---------|
| `config.json` | Actual configuration with API keys | ❌ No |
| `config.template.json` | Configuration template | ✅ Yes |
| `quotes.json` | Quote database | ✅ Yes |
| `requirements.txt` | Python dependencies | ✅ Yes |

### Entry Points

| File | Purpose | Usage |
|------|---------|-------|
| `main.py` | Main application | `python main.py` |
| `scripts/scheduler.py` | Automation | `python scripts/scheduler.py` |
| `tests/test_production.py` | Testing | `python tests/test_production.py` |

### Documentation Priority

1. **README.md** - Start here
2. **docs/02_setup_guide.md** - Setup instructions
3. **docs/03_production_guide.md** - Production usage
4. **docs/04_system_status.md** - Feature overview

## Git Tracking

### Tracked (In Repository)
- ✅ Source code (`.py` files)
- ✅ Documentation (`.md` files)
- ✅ Configuration templates
- ✅ Sample data (`quotes.json`)
- ✅ Requirements (`requirements.txt`)
- ✅ Scripts and utilities
- ✅ Directory structure (`.gitkeep` files)

### Not Tracked (Ignored)
- ❌ Configuration with secrets (`config.json`)
- ❌ Generated content (`output/`)
- ❌ Log files (`logs/`)
- ❌ Python cache (`__pycache__/`)
- ❌ Virtual environment (`venv/`)
- ❌ Large assets (fonts)

## Directory Purposes

| Directory | Purpose | Size | Tracked |
|-----------|---------|------|---------|
| `/modules/` | Core logic | Small | ✅ Yes |
| `/scripts/` | Utilities | Small | ✅ Yes |
| `/tests/` | Testing | Small | ✅ Yes |
| `/docs/` | Documentation | Medium | ✅ Yes |
| `/assets/` | Static files | Medium | Partial |
| `/output/` | Generated | Large | ❌ No |
| `/logs/` | Logs | Medium | ❌ No |

## Quick Navigation

### For Developers
- **Start:** `README.md`
- **Setup:** `docs/02_setup_guide.md`
- **Code:** `modules/` directory
- **Tests:** `tests/` directory

### For Users
- **Start:** `README.md`
- **Setup:** `docs/02_setup_guide.md`
- **Usage:** `main.py`
- **Automation:** `scripts/scheduler.py`

### For Production
- **Guide:** `docs/03_production_guide.md`
- **Status:** `docs/06_production_ready.md`
- **Tests:** `tests/test_production.py`

## File Count Summary

- **Python Files:** 10 (8 modules + 2 entry points)
- **Documentation:** 9 markdown files
- **Scripts:** 4 utility scripts
- **Tests:** 2 test files
- **Config:** 2 configuration files
- **Total Tracked:** ~27 files

## Maintenance

### Adding New Features
1. Create module in `/modules/`
2. Add tests in `/tests/`
3. Document in `/docs/`
4. Update `README.md`

### Adding Documentation
1. Create numbered file in `/docs/`
2. Follow naming: `##_descriptive_name.md`
3. Update this file structure doc
4. Link from `README.md`

### Adding Scripts
1. Create in `/scripts/`
2. Make executable (Linux/Mac)
3. Document usage
4. Update `README.md`

---

**Last Updated:** 2026-05-17
**Version:** 1.0.0
