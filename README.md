<div style="text-align: right;">
  <input type="radio" id="lang-en" name="language" checked>
  <label for="lang-en" style="cursor: pointer; color: #0366d6; font-weight: bold;">English</label> | 
  <input type="radio" id="lang-zh" name="language">
  <label for="lang-zh" style="cursor: pointer; color: #666;">中文</label>
</div>

<style>
  input[type="radio"] { display: none; }
  #content-zh { display: none; }
  #lang-en:checked ~ #content-en { display: block; }
  #lang-en:checked ~ #content-zh { display: none; }
  #lang-zh:checked ~ #content-en { display: none; }
  #lang-zh:checked ~ #content-zh { display: block; }
</style>

<div id="content-en">

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

</div>

<div id="content-zh">

# PornSpider 视频爬虫

多网站视频爬虫工具，支持从91porn和Pornhub网站下载视频。

## 🤖 Telegram Bot

如果更喜欢使用Telegram Bot来浏览视频，可以尝试：

👉 https://t.me/xmporn_bot

在Telegram中直接使用，无需安装Python环境，随时随地访问视频内容。

## 功能特点

- ✅ **多网站支持**：支持91porn和Pornhub两个主流视频网站
- ✅ **智能反爬虫**：使用cloudscraper绕过网站反爬虫检测
- ✅ **多种分类**：91porn支持7种分类和搜索功能
- ✅ **自动下载**：自动解析视频列表，获取真实下载地址并下载
- ✅ **多格式支持**：支持MP4和M3U8（HLS流媒体）格式视频下载
- ✅ **断点续传**：已下载的视频会自动跳过，支持断点续传
- ✅ **标签提取**：自动提取视频标签并保存到`tags.txt`文件
- ✅ **下载进度**：实时显示下载进度和文件大小
- ✅ **智能重试**：网络错误时自动重试，提高下载成功率
- ✅ **文件管理**：自动创建分类目录，使用视频标题作为文件名

## 安装依赖

```bash
pip install -r requirements.txt
```

### 依赖包说明

- `requests` - HTTP请求库
- `beautifulsoup4` - HTML解析库
- `lxml` - XML/HTML解析器
- `cloudscraper` - 绕过Cloudflare反爬虫检测
- `m3u8` - M3U8播放列表解析（用于HLS流媒体下载）

## 使用方法

### 1. 启动程序

```bash
python spider.py
```

### 2. 选择网站

程序启动后会提示选择网站：
- 输入 `1` 或直接回车 - 选择91porn
- 输入 `2` - 选择Pornhub

### 3. 选择分类/搜索（91porn）

如果选择91porn，会显示以下分类选项：

```
1. 最新视频
2. 当前最热
3. 本月最热
4. 最近加精
5. 本月收藏
6. 本月讨论
7. 上月最热
8. 搜索
```

- 输入 `1-7` - 选择对应分类
- 输入 `8` - 进入搜索模式，输入搜索关键词

### 4. 输入搜索关键词（Pornhub）

如果选择Pornhub，直接输入搜索关键词即可。

### 5. 开始下载

程序会提示输入起始页码：
- 输入数字（如 `1`） - 从指定页码开始抓取
- 输入 `q` - 退出程序
- 输入 `c` - 重新选择分类/搜索

### 6. 下载过程

- 程序会自动解析当前页面的所有视频
- 显示每个视频的下载进度
- 下载完成后询问是否继续下一页
  - 输入 `y` - 继续下载下一页
  - 输入 `n` 或 `q` - 退出程序
  - 输入 `c` - 重新选择分类/搜索

## 文件结构

```
PornSpider/
├── spider.py                 # 主程序文件
├── requirements.txt          # 依赖包列表
├── README.md                 # 说明文档
├── downloaded_videos.txt     # 已下载视频列表（自动生成）
├── tags.txt                  # 视频标签列表（自动生成）
└── video/                    # 视频存储目录（自动创建）
    ├── 91/                   # 91porn视频目录
    └── pornhub/              # Pornhub视频目录
```

## 输出文件说明

### downloaded_videos.txt

记录已下载的视频标题，用于断点续传功能。程序会自动检查此文件，跳过已下载的视频。

### tags.txt

保存所有下载视频的标签信息，格式如下：

```
================================================================================
视频标签列表
================================================================================

视频标题: [视频标题]
视频链接: [视频链接]
标签: [标签1, 标签2, 标签3, ...]
--------------------------------------------------------------------------------

视频标题: [下一个视频标题]
视频链接: [下一个视频链接]
标签: [标签1, 标签2, 标签3, ...]
--------------------------------------------------------------------------------
```

标签从视频详情页的`class="tagsWrapper"`元素中自动提取。

## 技术特性

### 反爬虫处理

- 使用`cloudscraper`模拟真实浏览器访问
- 自动设置合适的请求头和Cookie
- 添加随机延迟，避免请求过快被限制

### 视频URL解析

- **91porn**：从HTML中解析`<source>`标签获取视频URL
- **Pornhub**：从JavaScript中解析`mediaDefinitions`获取最高质量视频URL
- 支持多种解析方法，提高成功率

### 下载优化

- 使用2MB大块下载，提高下载速度
- 支持断点续传（Range请求）
- 自动检测并处理M3U8格式（HLS流媒体）
- 下载失败时自动重试（最多3次）

### 错误处理

- 网络超时自动重试
- 下载失败自动重试
- 文件完整性检查
- 临时文件自动清理

## 注意事项

⚠️ **重要提示**

1. **合法使用**：请遵守网站使用条款和相关法律法规
2. **个人使用**：下载的视频仅供个人学习研究使用，请勿用于商业用途
3. **合理频率**：请合理控制下载频率，避免对服务器造成过大压力
4. **网络环境**：确保网络连接稳定，下载大文件时可能需要较长时间
5. **存储空间**：确保有足够的磁盘空间存储下载的视频

## 常见问题

### Q: 下载失败怎么办？

A: 程序会自动重试3次。如果仍然失败，可能是：
- 网络连接问题
- 视频URL已失效
- 网站反爬虫策略更新

### Q: 如何继续之前的下载？

A: 程序会自动检查`downloaded_videos.txt`文件，已下载的视频会自动跳过。

### Q: M3U8视频下载需要什么？

A: 需要安装`m3u8`库（已包含在requirements.txt中）。如果系统有ffmpeg，会自动使用ffmpeg合并片段，否则使用简单合并方式。

### Q: 标签提取失败？

A: 标签提取依赖于网页结构，如果网站更新了页面结构，可能需要更新代码。标签提取失败不会影响视频下载。

## 更新日志

- 支持91porn和Pornhub双网站
- 支持M3U8格式视频下载
- 自动提取并保存视频标签
- 优化下载速度和稳定性
- 改进错误处理和重试机制

## 许可证

本项目仅供学习研究使用，请勿用于商业用途。

</div>
