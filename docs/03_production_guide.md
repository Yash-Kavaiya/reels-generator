# Production Guide - 1000+ Reels

## 🚀 System Improvements

### 1. **Retry Logic** ✅
- All critical operations have 5 retry attempts
- Exponential backoff (1s, 2s, 4s, 8s, 16s)
- Automatic fallback to gTTS if Sarvam AI fails
- Automatic fallback to MoviePy if Manim fails

### 2. **Logging System** ✅
- Comprehensive logging to files and console
- Logs saved in `logs/` directory
- Timestamped log files
- Debug level for files, Info level for console
- Full error tracebacks captured

### 3. **Batch Processing** ✅
- Sequential processing (safe for API limits)
- Parallel processing (faster, use with caution)
- Progress tracking
- Automatic report generation
- Failed reel tracking

### 4. **Error Handling** ✅
- Try-catch blocks at every level
- Graceful degradation
- Detailed error messages
- Failed reel retry mechanism

### 5. **Scalability** ✅
- Designed for 1000+ reels
- Memory efficient
- Resource cleanup after each reel
- Batch reports with statistics

## 📊 Running Large Batches

### Option 1: Sequential (Recommended for 1000 reels)
```bash
python main.py
# Choose option 5
```

**Pros:**
- Safe for API rate limits
- Predictable resource usage
- Better error recovery
- Recommended for Sarvam AI

**Cons:**
- Slower (but reliable)

**Estimated Time:**
- ~30-60 seconds per reel
- 1000 reels = 8-16 hours

### Option 2: Parallel (Use with caution)
```bash
python main.py
# Choose option 4
```

**Pros:**
- Faster processing
- Better CPU utilization

**Cons:**
- May hit API rate limits
- Higher memory usage
- Risk of quota exhaustion

**Settings:**
- Max workers: 3 (adjustable in code)
- Use for gTTS only

## 📁 Output Structure

```
output/
├── audio/              # Generated audio files
│   ├── quote_1.wav
│   ├── quote_2.wav
│   └── ...
├── videos/             # Final video files
│   ├── reel_quote_1.mp4
│   ├── reel_quote_2.mp4
│   └── ...
├── temp/               # Temporary Manim files
│   └── (auto-cleaned)
└── reports/            # Batch processing reports
    └── batch_report_YYYYMMDD_HHMMSS.json

logs/
└── reels_YYYYMMDD_HHMMSS.log
```

## 📈 Monitoring Progress

### Real-time Monitoring
```bash
# Watch log file
tail -f logs/reels_*.log

# Count completed videos
ls output/videos/*.mp4 | wc -l
```

### Batch Reports
After each batch, check:
```
output/reports/batch_report_*.json
```

Report includes:
- Total requested
- Successful count
- Failed count
- Duration
- Average time per reel
- Success rate
- List of failures

## 🔧 Configuration for Scale

### For 1000 Reels:

1. **Ensure enough quotes:**
```json
// quotes.json should have many quotes
// System will cycle through them
```

2. **Disk space:**
- Audio: ~100KB per file = 100MB for 1000
- Video: ~5-10MB per file = 5-10GB for 1000
- Total: ~10-15GB recommended

3. **API Limits:**
- Sarvam AI: Check your quota
- gTTS: No hard limits but use delays
- Fallback to gTTS if needed

4. **Memory:**
- Each reel: ~500MB peak
- Sequential: Safe for 4GB+ RAM
- Parallel: 8GB+ recommended

## 🛡️ Error Recovery

### If Process Crashes:
1. Check logs: `logs/reels_*.log`
2. Check report: `output/reports/batch_report_*.json`
3. Count completed: `ls output/videos/*.mp4 | wc -l`
4. Resume from where it stopped

### Manual Resume:
```python
# In main.py, modify create_batch call:
# Skip already created quotes
```

### Failed Reels:
- Check `batch_report_*.json` for failures
- Retry specific quote IDs:
```bash
python -c "from main import create_reel; create_reel(QUOTE_ID)"
```

## ⚡ Performance Optimization

### Speed Up Processing:

1. **Use gTTS instead of Sarvam AI:**
```json
// config.json
"use_sarvam": false
```

2. **Use MoviePy instead of Manim:**
```json
// config.json
"use_manim": false
```

3. **Reduce video quality:**
```json
// For Manim: use -ql instead of -qh
// Modify manim_video_creator.py
```

4. **Parallel processing (if safe):**
```bash
python main.py
# Choose option 4
```

## 📊 Expected Performance

### Sequential Processing:
- **With Sarvam AI + Manim:** 45-60s per reel
- **With gTTS + Manim:** 30-45s per reel
- **With gTTS + MoviePy:** 20-30s per reel

### For 1000 Reels:
- **Best case:** 5-6 hours (gTTS + MoviePy)
- **Average:** 8-12 hours (Sarvam + Manim)
- **Worst case:** 16-20 hours (with retries)

## 🔍 Quality Checks

### Random Sampling:
```bash
# Check every 100th video
ls output/videos/reel_quote_*00.mp4
```

### Verify Audio-Video Sync:
```bash
# Play random videos
vlc output/videos/reel_quote_*.mp4
```

### Check Logs for Errors:
```bash
grep "ERROR" logs/reels_*.log
grep "Failed" logs/reels_*.log
```

## 💡 Best Practices

1. **Start Small:**
   - Test with 10 reels first
   - Verify quality
   - Then scale up

2. **Monitor Resources:**
   - Watch disk space
   - Monitor memory usage
   - Check API quotas

3. **Use Sequential for Production:**
   - More reliable
   - Better error handling
   - Respects API limits

4. **Keep Logs:**
   - Don't delete log files
   - Useful for debugging
   - Track success rates

5. **Backup Regularly:**
   - Copy completed videos
   - Save batch reports
   - Keep configuration

## 🚨 Troubleshooting

### Issue: API Rate Limit
**Solution:** 
- Use sequential processing
- Add delays between requests
- Switch to gTTS temporarily

### Issue: Out of Memory
**Solution:**
- Use sequential processing
- Close other applications
- Reduce max_workers

### Issue: Disk Full
**Solution:**
- Clean temp files: `rm -rf output/temp/*`
- Move completed videos
- Increase disk space

### Issue: Many Failures
**Solution:**
- Check logs for patterns
- Verify API keys
- Test single reel first
- Check internet connection

## 📞 Support

For issues:
1. Check logs: `logs/reels_*.log`
2. Check reports: `output/reports/`
3. Review this guide
4. Test with single reel first

---

**System is production-ready for 1000+ reels! 🎉**
