# Video-to-Notes Troubleshooting Guide

Detailed solutions for common issues when using the video-to-notes skill.

## Table of Contents

1. [Environment Setup Issues](#environment-setup-issues)
2. [API Key Problems](#api-key-problems)
3. [Video Download Errors](#video-download-errors)
4. [Audio Extraction Failures](#audio-extraction-failures)
5. [Transcription Issues](#transcription-issues)
6. [Summarization Errors](#summarization-errors)
7. [Performance Problems](#performance-problems)

## Environment Setup Issues

### FFmpeg not found

**Error**: `FFmpeg failed` or `ffmpeg: command not found`

**Solution**:
1. Install FFmpeg:
   ```bash
   # Windows (using Chocolatey)
   choco install ffmpeg

   # macOS
   brew install ffmpeg

   # Linux (Ubuntu/Debian)
   sudo apt-get install ffmpeg
   ```

2. Verify installation:
   ```bash
   ffmpeg -version
   ```

3. If installed but not found, add to PATH or use absolute path

### yt-dlp not found

**Error**: Video download fails with module/command not found

**Solution**:
```bash
# Install yt-dlp
pip install yt-dlp

# Verify
yt-dlp --version
```

### Python dependencies missing

**Error**: Import errors when running script

**Solution**:
```bash
cd scripts
pip install -r requirements.txt
```

## API Key Problems

### Missing OPENAI_API_KEY

**Error**: `OpenAI API key is required for Whisper API`

**Solution**:
1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env` file in scripts directory:
   ```env
   OPENAI_API_KEY=sk-...
   ```
3. Verify `.env` is in the correct location (same directory as process_video.py)

### Missing OPENROUTER_API_KEY

**Error**: `OpenRouter API key is required`

**Solution**:
1. Get API key from https://openrouter.ai/
2. Add to `.env` file:
   ```env
   OPENROUTER_API_KEY=sk-...
   ```

### Invalid API keys

**Error**: API request returns 401 Unauthorized

**Solution**:
1. Check API keys are correct (no extra spaces, complete key)
2. Verify keys haven't expired
3. Test keys manually:
   ```bash
   # Test OpenAI key
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_KEY"

   # Test OpenRouter key
   curl https://openrouter.ai/api/v1/models \
     -H "Authorization: Bearer YOUR_KEY"
   ```

## Video Download Errors

### "Video too long"

**Error**: `Video too long: XXXXs > 7200s`

**Solution**:
- Video exceeds maximum length (default 2 hours)
- Options:
  1. Use shorter video
  2. Increase limit in `.env`: `MAX_VIDEO_LENGTH=14400`
  3. Process video in segments manually

### Private or restricted video

**Error**: Download fails with "This video is private" or region error

**Solution**:
- Video is not publicly accessible
- Check if video requires login or is region-blocked
- Use a different video or request access from uploader

### Network timeout

**Error**: Download fails with timeout error

**Solution**:
1. Check internet connection
2. Try again (script has retry logic)
3. For slow connections, split into download and processing:
   ```bash
   # Download first with yt-dlp directly
   yt-dlp URL -o video.mp4

   # Then process with script
   python process_video.py --url URL
   ```

## Audio Extraction Failures

### FFmpeg timeout

**Error**: `FFmpeg process timed out after 30 seconds`

**Solution**:
- Video file is very large
- Check available disk space
- Try with smaller video first to verify setup

### Output file not created

**Error**: `Audio extraction failed - output file not created`

**Solution**:
1. Check temp directory permissions
2. Verify enough disk space
3. Check video file is valid (can be played)

### Windows popup window issue

**Symptom**: Black console windows appearing during processing

**Solution**:
- This is expected on Windows
- Script uses CREATE_NO_WINDOW flag to minimize this
- Windows themselves are harmless

## Transcription Issues

### Audio file too large

**Error**: `Audio file too large: XX.XMB > 25MB limit`

**Solution**:
- Video is too long (>20-30 minutes typically)
- Whisper API has 25MB file limit
- Options:
  1. Use shorter video
  2. Compress audio manually:
     ```bash
     ffmpeg -i audio.mp3 -b:a 32k -ac 1 -ar 16000 audio_compressed.mp3
     ```
  3. Consider using local Whisper instead (slower but no size limit)

### Transcription quality issues

**Symptom**: Transcription has many errors

**Solution**:
1. Specify language explicitly:
   ```bash
   python process_video.py --url URL --language zh
   ```
2. Check audio quality (background noise, clarity)
3. For technical content, results may vary

### API rate limiting

**Error**: Whisper API returns 429 error

**Solution**:
- Hit OpenAI rate limits
- Wait a few minutes and retry
- Check OpenAI dashboard for usage limits

## Summarization Errors

### Summary quality issues

**Symptom**: Summary is generic or misses key points

**Solution**:
1. Try different AI model:
   ```bash
   python process_video.py --url URL --ai-model "google/gemini-2.5-flash"
   ```
2. Check transcript quality first
3. For very long videos, AI may struggle with full context

### OpenRouter API errors

**Error**: API request failed with 4XX/5XX error

**Solution**:
1. Check API key is valid
2. Verify model name is correct
3. Check OpenRouter status page
4. Try alternative model

### JSON parsing errors

**Error**: `Invalid summary format` or JSON parsing failure

**Solution**:
- AI didn't return properly formatted JSON
- Script has fallback text parsing
- Usually retrying works
- If persistent, check model compatibility

## Performance Problems

### Slow processing

**Symptom**: Processing takes much longer than expected

**Solution**:
1. Check network speed (affects download and API calls)
2. Whisper API typically fastest part (~10-15 seconds)
3. For repeated slowness:
   - Test network: `ping api.openai.com`
   - Check API status pages
   - Try during off-peak hours

### Memory issues

**Error**: Out of memory or system slowdown

**Solution**:
- Very large video files can cause memory pressure
- Close other applications
- For persistent issues, use smaller videos

### Disk space issues

**Error**: No space left on device

**Solution**:
1. Clean temp directory:
   ```bash
   cd scripts/temp
   rm -rf *
   ```
2. Check available space: `df -h` (Linux/Mac) or `dir` (Windows)
3. Set custom temp directory with more space:
   ```env
   TEMP_DIRECTORY=/path/with/more/space
   ```

## Debug Mode

Enable verbose logging to diagnose issues:

```bash
python process_video.py --url URL --verbose
```

This outputs:
- Detailed progress logs
- FFmpeg command details
- API request/response info
- Timing information

## Getting Additional Help

If issues persist after troubleshooting:

1. Check logs in stderr output
2. Note exact error message and exit code
3. Verify all prerequisites are met
4. Test with a known working video (short, public YouTube video)
5. Check system resources (disk, memory, network)

## Common Environment-Specific Issues

### Windows

- Path issues with spaces: Use quotes around paths
- Encoding issues: Set `PYTHONIOENCODING=utf-8`
- Permission issues: Run as administrator if needed

### macOS

- FFmpeg installation: Use Homebrew
- Python version: Ensure using Python 3.10+
- Permissions: May need `chmod +x` on scripts

### Linux

- Package manager differences: Use appropriate package manager
- Python/pip: May need `python3` instead of `python`
- FFmpeg: Install via apt/yum/pacman depending on distro
