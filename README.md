# PornSpider Video Spider

Multi-site video spider tool that supports downloading videos from 91porn and Pornhub websites.

## 🤖 Telegram Bot

If you prefer using a Telegram Bot to browse videos, try:

👉 https://t.me/xmporn_bot

Use it directly in Telegram without installing Python environment, access video content anytime, anywhere.

## Features

- ✅ **Multi-site Support**: Supports two mainstream video sites: 91porn and Pornhub
- ✅ **Anti-scraping**: Uses cloudscraper to bypass website anti-scraping detection
- ✅ **Multiple Categories**: 91porn supports 7 categories and search functionality
- ✅ **Auto Download**: Automatically parses video lists, gets real download URLs and downloads
- ✅ **Multi-format Support**: Supports MP4 and M3U8 (HLS streaming) video downloads
- ✅ **Resume Download**: Automatically skips already downloaded videos, supports resume download
- ✅ **Tag Extraction**: Automatically extracts video tags and saves to `tags.txt` file
- ✅ **Download Progress**: Real-time display of download progress and file size
- ✅ **Smart Retry**: Automatically retries on network errors, improves download success rate
- ✅ **File Management**: Automatically creates category directories, uses video titles as filenames

## Installation

```bash
pip install -r requirements.txt
```

### Dependencies

- `requests` - HTTP request library
- `beautifulsoup4` - HTML parsing library
- `lxml` - XML/HTML parser
- `cloudscraper` - Bypass Cloudflare anti-scraping detection
- `m3u8` - M3U8 playlist parser (for HLS streaming downloads)

## Usage

### 1. Start the Program

```bash
python spider.py
```

### 2. Select Website

After starting, the program will prompt you to select a website:
- Enter `1` or press Enter - Select 91porn
- Enter `2` - Select Pornhub

### 3. Select Category/Search (91porn)

If you select 91porn, the following category options will be displayed:

```
1. Latest Videos
2. Currently Hot
3. This Month Hot
4. Recently Featured
5. This Month Favorites
6. This Month Discussions
7. Last Month Hot
8. Search
```

- Enter `1-7` - Select corresponding category
- Enter `8` - Enter search mode, input search keyword

### 4. Enter Search Keyword (Pornhub)

If you select Pornhub, simply enter the search keyword.

### 5. Start Download

The program will prompt you to enter the starting page number:
- Enter a number (e.g., `1`) - Start crawling from specified page
- Enter `q` - Exit program
- Enter `c` - Reselect category/search

### 6. Download Process

- Program automatically parses all videos on current page
- Displays download progress for each video
- After download completes, asks whether to continue to next page
  - Enter `y` - Continue to next page
  - Enter `n` or `q` - Exit program
  - Enter `c` - Reselect category/search

## File Structure

```
PornSpider/
├── spider.py                 # Main program file
├── requirements.txt          # Dependency list
├── README.md                 # Documentation
├── downloaded_videos.txt     # Downloaded video list (auto-generated)
├── tags.txt                  # Video tags list (auto-generated)
└── video/                    # Video storage directory (auto-created)
    ├── 91/                   # 91porn video directory
    └── pornhub/              # Pornhub video directory
```

## Output Files

### downloaded_videos.txt

Records downloaded video titles for resume download functionality. The program automatically checks this file and skips already downloaded videos.

### tags.txt

Saves tag information for all downloaded videos, format as follows:

```
================================================================================
Video Tags List
================================================================================

Video Title: [Video Title]
Video URL: [Video URL]
Tags: [Tag1, Tag2, Tag3, ...]
--------------------------------------------------------------------------------

Video Title: [Next Video Title]
Video URL: [Next Video URL]
Tags: [Tag1, Tag2, Tag3, ...]
--------------------------------------------------------------------------------
```

Tags are automatically extracted from the `class="tagsWrapper"` element on the video detail page.

## Technical Features

### Anti-scraping Handling

- Uses `cloudscraper` to simulate real browser access
- Automatically sets appropriate request headers and Cookies
- Adds random delays to avoid being limited by too frequent requests

### Video URL Parsing

- **91porn**: Parses `<source>` tags from HTML to get video URL
- **Pornhub**: Parses `mediaDefinitions` from JavaScript to get highest quality video URL
- Supports multiple parsing methods to improve success rate

### Download Optimization

- Uses 2MB large chunks for faster download speed
- Supports resume download (Range requests)
- Automatically detects and handles M3U8 format (HLS streaming)
- Automatically retries on download failure (up to 3 times)

### Error Handling

- Automatic retry on network timeout
- Automatic retry on download failure
- File integrity check
- Automatic temporary file cleanup

## Important Notes

⚠️ **Important**

1. **Legal Use**: Please comply with website terms of service and relevant laws and regulations
2. **Personal Use**: Downloaded videos are for personal learning and research only, do not use for commercial purposes
3. **Reasonable Frequency**: Please reasonably control download frequency to avoid putting too much pressure on servers
4. **Network Environment**: Ensure stable network connection, downloading large files may take a long time
5. **Storage Space**: Ensure sufficient disk space to store downloaded videos

## FAQ

### Q: What if download fails?

A: The program will automatically retry 3 times. If it still fails, it may be due to:
- Network connection issues
- Video URL has expired
- Website anti-scraping policy updates

### Q: How to continue previous downloads?

A: The program automatically checks the `downloaded_videos.txt` file, already downloaded videos will be automatically skipped.

### Q: What is needed for M3U8 video download?

A: Need to install `m3u8` library (already included in requirements.txt). If the system has ffmpeg, it will automatically use ffmpeg to merge segments, otherwise use simple merge method.

### Q: Tag extraction failed?

A: Tag extraction depends on webpage structure. If the website updates the page structure, the code may need to be updated. Tag extraction failure will not affect video download.

## Changelog

- Support for 91porn and Pornhub dual sites
- Support for M3U8 format video downloads
- Automatic extraction and saving of video tags
- Optimized download speed and stability
- Improved error handling and retry mechanism

## License

This project is for learning and research purposes only, do not use for commercial purposes.
