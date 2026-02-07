#!/usr/bin/env python3

import warnings
import os

os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning:urllib3'

warnings.filterwarnings('ignore', message='.*urllib3.*OpenSSL.*')
warnings.filterwarnings('ignore', message='.*urllib3 v2 only supports OpenSSL.*')
warnings.filterwarnings('ignore', message='.*NotOpenSSLWarning.*')
warnings.filterwarnings('ignore', message='.*LibreSSL.*')
warnings.filterwarnings('ignore', category=UserWarning, module='urllib3')

import os
import re
import time
import requests
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, quote
import html
import urllib3
import tempfile
import shutil

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)
except (AttributeError, NameError):
    pass

class VideoSpider:
    def __init__(self):
        self.site_type = None
        self.base_url = None
        self.list_url_template = None
        self.mv_flag = None
        self.search_keyword = None
        self.session = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'darwin',
                'desktop': True
            }
        )
        self.session.proxies = {
            'http': None,
            'https': None,
        }
        self.session.headers.update({
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.video_dir = None
        self.downloaded_list_file = "downloaded_videos.txt"
        self.chunk_size = 1024 * 1024 * 2
    
    def select_site(self):
        print("\n" + "=" * 60)
        print("Please select a website:")
        print("=" * 60)
        print("1. 91porn")
        print("2. Pornhub")
        print("=" * 60)
        
        while True:
            try:
                choice = input("Enter option (1-2): ").strip()
                
                if choice == "1":
                    self.site_type = "91porn"
                    self.base_url = "https://91porn.com"
                    self.list_url_template = "https://91porn.com/v.php?next=watch&page={}"
                    self.mv_flag = "Latest Videos"
                    self.video_dir = os.path.join("video", "91")
                    self._ensure_video_dir()
                    self.session.headers.update({
                        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                    })
                    print(f"\nSelected website: 91porn")
                    self._init_session()
                    return
                elif choice == "2":
                    self.site_type = "pornhub"
                    self.base_url = "https://www.pornhub.com"
                    self.list_url_template = None
                    self.mv_flag = None
                    self.video_dir = os.path.join("video", "pornhub")
                    self._ensure_video_dir()
                    self.session.headers.update({
                        'Accept-Language': 'en-US,en;q=0.9',
                    })
                    print(f"\nSelected website: Pornhub")
                    self._init_session()
                    return
                else:
                    print("Invalid option, please enter a number between 1-2")
                    continue
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user")
                raise
            except Exception as exc:
                print(f"Input error: {str(exc)}, please try again")
    
    def select_category(self):
        if self.site_type == "pornhub":
            while True:
                try:
                    search_input = input("\nEnter search keyword: ").strip()
                    if not search_input:
                        print("Search keyword cannot be empty, please try again")
                        continue
                    self.search_keyword = search_input
                    self.mv_flag = f"Search: {search_input}"
                    print(f"\nSearch keyword set: {search_input}")
                    return
                except KeyboardInterrupt:
                    print("\n\nProgram interrupted by user")
                    raise
                except Exception as e:
                    print(f"Input error: {str(e)}, please try again")
            return
        
        print("\n" + "=" * 60)
        print("Please select a category:")
        print("=" * 60)
        print("1. Latest Videos")
        print("2. Currently Hot")
        print("3. This Month Hot")
        print("4. Recently Featured")
        print("5. This Month Favorites")
        print("6. This Month Discussions")
        print("7. Last Month Hot")
        print("8. Search")
        print("=" * 60)
        
        while True:
            try:
                choice = input("Enter option (1-8): ").strip()
                
                if choice == "1":
                    url = 'https://91porn.com/v.php?next=watch&page={}'
                    self.mv_flag = "Latest Videos"
                    self.search_keyword = None
                elif choice == "2":
                    url = 'https://91porn.com/v.php?category=hot&viewtype=basic&page={}'
                    self.mv_flag = "Currently Hot"
                    self.search_keyword = None
                elif choice == "3":
                    url = 'https://91porn.com/v.php?category=top&viewtype=basic&page={}'
                    self.mv_flag = "This Month Hot"
                    self.search_keyword = None
                elif choice == "4":
                    url = 'https://91porn.com/v.php?category=rf&viewtype=basic&page={}'
                    self.mv_flag = "Recently Featured"
                    self.search_keyword = None
                elif choice == "5":
                    url = 'https://91porn.com/v.php?category=tf&viewtype=basic&page={}'
                    self.mv_flag = "This Month Favorites"
                    self.search_keyword = None
                elif choice == "6":
                    url = 'https://91porn.com/v.php?category=md&viewtype=basic&page={}'
                    self.mv_flag = "This Month Discussions"
                    self.search_keyword = None
                elif choice == "7":
                    url = 'https://91porn.com/v.php?category=top&m=-1&viewtype=basic&page={}'
                    self.mv_flag = "Last Month Hot"
                    self.search_keyword = None
                elif choice == "8":
                    search_input = input("Enter search keyword: ").strip()
                    if not search_input:
                        print("Search keyword cannot be empty, please try again")
                        continue
                    encoded_keyword = quote(search_input)
                    url = f'https://91porn.com/search_result.php?search_type=search_videos&search_id={encoded_keyword}&page={{}}'
                    self.mv_flag = f"Search: {search_input}"
                    self.search_keyword = search_input
                else:
                    print("Invalid option, please enter a number between 1-8")
                    continue
                
                self.list_url_template = url
                print(f"\nSelected category: {self.mv_flag}")
                return
                
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user")
                raise
            except Exception as exc:
                print(f"Input error: {str(exc)}, please try again")
    
    def _init_session(self):
        try:
            print("Initializing session...")
            response = self.session.get(self.base_url, timeout=30, allow_redirects=True)
            if response.status_code == 200:
                print("Session initialized successfully")
            else:
                print(f"Session initialization warning, status code: {response.status_code}")
            time.sleep(1)
        except Exception as exc:
            print(f"Session initialization error: {str(exc)}")
    
    def _ensure_video_dir(self):
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)
            print(f"Created video directory: {self.video_dir}")
    
    def _load_downloaded_list(self):
        downloaded_titles = set()
        if os.path.exists(self.downloaded_list_file):
            try:
                with open(self.downloaded_list_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        title = line.strip()
                        if title:
                            downloaded_titles.add(title)
            except Exception as exc:
                print(f"Failed to read downloaded list file: {str(exc)}")
        return downloaded_titles
    
    def _add_to_downloaded_list(self, title):
        try:
            with open(self.downloaded_list_file, 'a', encoding='utf-8') as f:
                f.write(f"{title}\n")
        except Exception as exc:
            print(f"Failed to append to downloaded list file: {str(exc)}")
    
    def _get_video_tags(self, video_page_url):
        try:
            time.sleep(1)
            html_content = self.get_page(video_page_url, referer=self.base_url)
            if not html_content:
                return []
            
            soup = BeautifulSoup(html_content, 'lxml')
            tags = []
            
            tags_wrapper = soup.find('div', class_='tagsWrapper')
            if not tags_wrapper:
                tags_wrapper = soup.find('div', class_=re.compile(r'tagsWrapper|tags-wrapper|tags'))
            
            if tags_wrapper:
                tag_links = tags_wrapper.find_all('a', href=True)
                for tag_link in tag_links:
                    tag_text = tag_link.get_text(strip=True)
                    if tag_text:
                        tags.append(tag_text)
                
                if not tags:
                    tag_elements = tags_wrapper.find_all(['span', 'li', 'div'], class_=re.compile(r'tag|label'))
                    for element in tag_elements:
                        tag_text = element.get_text(strip=True)
                        if tag_text and tag_text not in tags:
                            tags.append(tag_text)
            
            if not tags:
                tag_containers = soup.find_all(['div', 'section'], class_=re.compile(r'tag|category', re.I))
                for container in tag_containers:
                    tag_links = container.find_all('a', href=True)
                    for tag_link in tag_links:
                        tag_text = tag_link.get_text(strip=True)
                        if tag_text and tag_text not in tags:
                            tags.append(tag_text)
            
            return tags
        except Exception as exc:
            print(f"  Failed to get tags: {str(exc)}")
            return []
    
    @staticmethod
    def _save_tags_to_file(title, tags, video_page_url):
        if not tags:
            return
        
        try:
            tag_file = "tags.txt"
            file_exists = os.path.exists(tag_file)
            
            with open(tag_file, 'a', encoding='utf-8') as f:
                if not file_exists:
                    f.write("=" * 80 + "\n")
                    f.write("Video Tags List\n")
                    f.write("=" * 80 + "\n\n")
                
                f.write(f"Video Title: {title}\n")
                f.write(f"Video URL: {video_page_url}\n")
                f.write(f"Tags: {', '.join(tags)}\n")
                f.write("-" * 80 + "\n\n")
        except (IOError, OSError) as exc:
            print(f"  Failed to save tags: {str(exc)}")
    
    @staticmethod
    def _sanitize_filename(filename):
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.strip()
        if len(filename) > 200:
            filename = filename[:200]
        return filename
    
    def _check_video_exists(self, title, _output_dir):
        safe_title = self._sanitize_filename(title)
        downloaded_titles = self._load_downloaded_list()
        
        if safe_title in downloaded_titles:
            return True, safe_title
        
        for downloaded_title in downloaded_titles:
            if (downloaded_title == safe_title or 
                downloaded_title.startswith(safe_title[:50]) or 
                safe_title.startswith(downloaded_title[:50])):
                return True, downloaded_title
        
        return False, None
    
    def get_page(self, url, retry=3, referer=None):
        headers = {}
        if referer:
            headers['Referer'] = referer
        else:
            headers['Referer'] = self.base_url
        
        for i in range(retry):
            try:
                if i > 0:
                    time.sleep(2 * i)
                
                response = self.session.get(
                    url, 
                    timeout=(10, 30),
                    allow_redirects=True,
                    headers=headers
                )
                response.encoding = 'utf-8'
                
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 403:
                    print(f"\n  Request denied (403), possible anti-scraping detection (attempt {i+1}/{retry})")
                    if i < retry - 1:
                        time.sleep(3)
                else:
                    print(f"\n  Request failed, status code: {response.status_code} (attempt {i+1}/{retry})")
            except requests.exceptions.Timeout:
                print(f"\n  Request timeout (attempt {i+1}/{retry})")
                if i < retry - 1:
                    time.sleep(2)
            except Exception as exc:
                print(f"\n  Request error (attempt {i+1}/{retry}): {str(exc)}")
                if i < retry - 1:
                    time.sleep(2)
        return None
    
    def parse_list_page(self, page_num):
        if self.site_type == "pornhub":
            return self._parse_pornhub_list(page_num)
        else:
            return self._parse_91porn_list(page_num)
    
    def _parse_pornhub_list(self, page_num):
        if not self.search_keyword:
            return []
        
        encoded_keyword = quote(self.search_keyword)
        url = f"{self.base_url}/video/search?search={encoded_keyword}&page={page_num}"
        print(f"\n[{self.mv_flag}] Page {page_num}")
        time.sleep(1)
        html_content = self.get_page(url, referer=self.base_url)
        if not html_content:
            print(f"Failed to get page {page_num} content")
            return []
        
        soup = BeautifulSoup(html_content, 'lxml')
        videos = []
        
        video_list = soup.find('ul', class_=re.compile(r'phuiUListStandard|searchVideo'))
        if video_list:
            video_items = video_list.find_all('li', class_=re.compile(r'pcVideoListItem'))
        else:
            video_items = soup.find_all('li', class_=re.compile(r'pcVideoListItem|videoblock'))
        
        if not video_items:
            video_items = soup.find_all('div', class_=re.compile(r'phimage|videoPreview|wrap'))
        
        if not video_items:
            all_links = soup.find_all('a', href=re.compile(r'/view_video\.php|/video/'))
            for a_tag in all_links:
                try:
                    video_url = a_tag.get('href')
                    if not video_url:
                        continue
                    
                    if not video_url.startswith('http'):
                        video_url = urljoin(self.base_url, video_url)
                    
                    title = a_tag.get('title', '').strip()
                    if not title:
                        title = a_tag.get_text(strip=True)
                    
                    if title and video_url:
                        if not any(v['url'] == video_url for v in videos):
                            videos.append({
                                'title': title,
                                'url': video_url
                            })
                except (AttributeError, KeyError, ValueError):
                    continue
        
        for item in video_items:
            try:
                a_tag = item.find('a', href=re.compile(r'/view_video\.php|/video/'))
                if not a_tag:
                    continue
                
                video_url = a_tag.get('href')
                if not video_url:
                    continue
                
                if not video_url.startswith('http'):
                    video_url = urljoin(self.base_url, video_url)
                
                title = None
                title_span = item.find('span', class_=re.compile(r'title|videoTitle'))
                if title_span:
                    title = title_span.get_text(strip=True)
                
                if not title:
                    title = a_tag.get('title', '').strip()
                
                if not title:
                    title = a_tag.get_text(strip=True)
                
                if title and video_url:
                    if not any(v['url'] == video_url for v in videos):
                        videos.append({
                            'title': title,
                            'url': video_url
                        })
            except (AttributeError, KeyError, ValueError):
                continue
        
        return videos
    
    def _parse_91porn_list(self, page_num):
        url = self.list_url_template.format(page_num)
        print(f"\n[{self.mv_flag}] Page {page_num}")
        time.sleep(1)
        html_content = self.get_page(url, referer=self.base_url)
        if not html_content:
            print(f"Failed to get page {page_num} content")
            return []
        
        soup = BeautifulSoup(html_content, 'lxml')
        videos = []
        
        video_divs = soup.find_all('div', class_='well well-sm videos-text-align')
        
        if not video_divs:
            all_links = soup.find_all('a', href=re.compile(r'view_video\.php'))
            for a_tag in all_links:
                try:
                    video_url = a_tag.get('href')
                    if not video_url:
                        continue
                    
                    if not video_url.startswith('http'):
                        video_url = urljoin(self.base_url, video_url)
                    
                    title_span = a_tag.find('span', class_='video-title title-truncate m-t-5')
                    if title_span:
                        video_title = title_span.get_text(strip=True)
                    else:
                        title_span = a_tag.find('span', class_=re.compile(r'title'))
                        if title_span:
                            video_title = title_span.get_text(strip=True)
                        else:
                            video_title = a_tag.get_text(strip=True)
                    
                    if not video_title:
                        parent = a_tag.parent
                        if parent:
                            title_span = parent.find('span', class_=re.compile(r'title'))
                            if title_span:
                                video_title = title_span.get_text(strip=True)
                    
                    if video_title and video_url:
                        if not any(v['url'] == video_url for v in videos):
                            videos.append({
                                'title': video_title,
                                'url': video_url
                            })
                except (AttributeError, KeyError, ValueError):
                    continue
        
        for div in video_divs:
            try:
                a_tag = div.find('a', href=True)
                if not a_tag:
                    continue
                
                video_url = a_tag.get('href')
                if not video_url:
                    continue
                
                if not video_url.startswith('http'):
                    video_url = urljoin(self.base_url, video_url)
                
                title_span = a_tag.find('span', class_='video-title title-truncate m-t-5')
                if title_span:
                    title = title_span.get_text(strip=True)
                else:
                    title = a_tag.get_text(strip=True)
                
                if title and video_url:
                    if not any(v['url'] == video_url for v in videos):
                        videos.append({
                            'title': title,
                            'url': video_url
                        })
            except (AttributeError, KeyError, ValueError):
                continue
        
        return videos
    
    def get_video_download_url(self, video_page_url):
        if self.site_type == "pornhub":
            return self._get_pornhub_video_url(video_page_url)
        else:
            return self._get_91porn_video_url(video_page_url)
    
    def _get_pornhub_video_url(self, video_page_url):
        time.sleep(2)
        html_content = self.get_page(video_page_url, referer=self.base_url)
        if not html_content:
            return None
        
        def is_valid_video_url(url):
            if not url:
                return False
            url_lower = url.lower()
            if any(keyword in url_lower for keyword in ['thumb', 'thumbnail', 'small', 'medium', 'large', '.jpg', '.jpeg', '.png', '.gif', '.webp', 'image']):
                return False
            if 'get_media' in url_lower:
                return False
            if '.mp4' in url_lower or '.m3u8' in url_lower or '.ts' in url_lower or 'phncdn.com' in url_lower or 'cdn' in url_lower:
                if 'original' in url_lower or '/videos/' in url_lower or '.m3u8' in url_lower:
                    if re.search(r'/videos/\d{4}/\d{2}/\d+', url_lower) or '.m3u8' in url_lower or '.ts' in url_lower:
                        return True
            return False
        
        def clean_url(url_str):
            if not url_str:
                return None
            url_str = str(url_str).replace('\\/', '/').replace('\\u002F', '/')
            url_str = html.unescape(url_str)
            url_str = url_str.replace('cn.pornhub.com', 'www.pornhub.com')
            if not url_str.startswith('http'):
                url_str = 'https://' + str(url_str).lstrip('/')
            return url_str
        
        def extract_video_urls_from_media_definitions(page_html):
            regex_patterns = [
                r'var\s+mediaDefinitions\s*=\s*(\[[^\]]*\])',
                r'"mediaDefinitions"\s*:\s*(\[[^\]]*\])',
                r'mediaDefinitions\s*=\s*(\[[^\]]*\])',
            ]
            
            for regex_pattern in regex_patterns:
                found_matches = re.findall(regex_pattern, page_html, re.DOTALL)
                for matched_content in found_matches:
                    quality_url_pattern = r'\{"quality"\s*:\s*"(\d+)"[^}]*"videoUrl"\s*:\s*"([^"]+)"'
                    quality_url_pairs = re.findall(quality_url_pattern, matched_content)
                    if quality_url_pairs:
                        best_url = None
                        max_quality = 0
                        for quality_val, vid_url in quality_url_pairs:
                            try:
                                q = int(quality_val)
                                cleaned_url = clean_url(vid_url)
                                if cleaned_url and is_valid_video_url(cleaned_url) and q > max_quality:
                                    max_quality = q
                                    best_url = cleaned_url
                            except (ValueError, TypeError):
                                pass
                        if best_url:
                            return best_url
            return None
        
        video_url = extract_video_urls_from_media_definitions(html_content)
        if video_url:
            return video_url
        flashvars_patterns = [
            r'var\s+flashvars\s*=\s*({.*?});',
            r'flashvars\s*=\s*({.*?});',
            r'"flashvars"\s*:\s*({.*?})',
        ]
        for flashvars_pattern in flashvars_patterns:
            flashvars_match = re.search(flashvars_pattern, html_content, re.DOTALL)
            if flashvars_match:
                flashvars_str = flashvars_match.group(1)
                video_url_pattern = r'"videoUrl"\s*:\s*"([^"]+)"'
                url_list = re.findall(video_url_pattern, flashvars_str)
                if url_list:
                    for video_url_item in reversed(url_list):
                        normalized_url = clean_url(video_url_item)
                        if normalized_url and is_valid_video_url(normalized_url):
                            return normalized_url
        
        m3u8_patterns = [
            r'https?://[^"\'\s<>]+\.m3u8[^"\'\s<>]*',
            r'\"([^\"]*\.m3u8[^\"]*)\"',
            r'\'([^\']*\.m3u8[^\']*)\'',
            r'([^\s\"\'<>]+master[^\s\"\'<>]*\.m3u8[^\s\"\'<>]*)',
            r'([^\s\"\'<>]+playlist[^\s\"\'<>]*\.m3u8[^\s\"\'<>]*)',
        ]
        for m3u8_pattern in m3u8_patterns:
            m3u8_matches = re.findall(m3u8_pattern, html_content, re.IGNORECASE)
            if m3u8_matches:
                master_urls = [m3u8_url for m3u8_url in m3u8_matches if 'master' in m3u8_url.lower() or 'playlist' in m3u8_url.lower()]
                if master_urls:
                    normalized_url = clean_url(master_urls[0])
                    if normalized_url:
                        return normalized_url
                normalized_url = clean_url(m3u8_matches[0])
                if normalized_url:
                    return normalized_url
        
        cdn_patterns = [
            r'https?://[^"\']*phncdn\.com[^"\']*original[^"\']*\.mp4[^"\']*',
            r'https?://[^"\']*phncdn\.com[^"\']*videos/[^"\']*\.mp4[^"\']*',
            r'https?://[^"\']*phncdn\.com[^"\']*\.mp4[^"\']*',
        ]
        for cdn_pattern in cdn_patterns:
            cdn_matches = re.findall(cdn_pattern, html_content, re.IGNORECASE)
            if cdn_matches:
                video_urls = []
                for cdn_url in cdn_matches:
                    normalized_url = clean_url(cdn_url)
                    if normalized_url and is_valid_video_url(normalized_url):
                        video_urls.append(normalized_url)
                
                if video_urls:
                    original_urls = [vid_url for vid_url in video_urls if 'original' in vid_url.lower()]
                    if original_urls:
                        return max(original_urls, key=len)
                    else:
                        return max(video_urls, key=len)
        
        video_url_pattern = r'"videoUrl"\s*:\s*"([^"]+)"'
        url_matches = re.findall(video_url_pattern, html_content)
        if url_matches:
            valid_urls = []
            for video_url_item in url_matches:
                normalized_url = clean_url(video_url_item)
                if normalized_url and is_valid_video_url(normalized_url):
                    valid_urls.append(normalized_url)
            
            if valid_urls:
                original_urls = [vid_url for vid_url in valid_urls if 'original' in vid_url.lower()]
                if original_urls:
                    return original_urls[-1]
                else:
                    return valid_urls[-1]
        
        soup = BeautifulSoup(html_content, 'lxml')
        video_tag = soup.find('video', id='player')
        if not video_tag:
            video_tag = soup.find('video')
        
        if video_tag:
            source_tags = video_tag.find_all('source', src=True)
            if source_tags:
                best_source = None
                max_resolution = 0
                
                for source in source_tags:
                    quality_str = source.get('data-res', '') or source.get('quality', '')
                    src_url = source.get('src', '')
                    if src_url:
                        normalized_url = clean_url(src_url)
                        if normalized_url and is_valid_video_url(normalized_url):
                            if quality_str:
                                quality_match = re.search(r'(\d+)', quality_str)
                                if quality_match:
                                    resolution = int(quality_match.group(1))
                                    if resolution > max_resolution:
                                        max_resolution = resolution
                                        best_source = normalized_url
                            else:
                                if not best_source:
                                    best_source = normalized_url
                
                if best_source:
                    return best_source
        
        js_var_patterns = [
            r'var\s+media_\d+\s*=\s*({[^}]*"videoUrl"[^}]*})',
            r'player_quality_\d+\s*=\s*({[^}]*"videoUrl"[^}]*})',
            r'var\s+player_quality\s*=\s*({[^}]*"videoUrl"[^}]*})',
        ]
        for js_pattern in js_var_patterns:
            js_matches = re.findall(js_pattern, html_content, re.DOTALL)
            for match_content in js_matches:
                url_list = re.findall(r'"videoUrl"\s*:\s*"([^"]+)"', match_content)
                for vid_url_item in url_list:
                    norm_url = clean_url(vid_url_item)
                    if norm_url and is_valid_video_url(norm_url):
                        return norm_url
        
        all_video_patterns = [
            r'https?://[^"\'\s<>]+\.m3u8[^"\'\s<>]*',
            r'https?://[^"\'\s<>]+\.mp4[^"\'\s<>]*',
            r'https?://[^"\'\s<>]+\.ts[^"\'\s<>]*',
        ]
        for video_pattern in all_video_patterns:
            found_urls = re.findall(video_pattern, html_content, re.IGNORECASE)
            if found_urls:
                valid_urls = []
                for vid_url_item in found_urls:
                    norm_url = clean_url(vid_url_item)
                    if norm_url and is_valid_video_url(norm_url):
                        valid_urls.append(norm_url)
                
                if valid_urls:
                    original_urls = [vid_url for vid_url in valid_urls if 'original' in vid_url.lower() or 'master' in vid_url.lower()]
                    if original_urls:
                        return max(original_urls, key=len)
                    else:
                        return max(valid_urls, key=len)
        
        return None
    
    def _get_91porn_video_url(self, video_page_url):
        time.sleep(1)
        print(f"  [Parsing] Parsing video page...", end='', flush=True)
        html_content = self.get_page(video_page_url, referer=self.base_url)
        if not html_content:
            print(f"\r  [Failed] Unable to get video page content")
            return None
        print(f"\r  [Parsing] Parsing video page... Done")
        
        soup = BeautifulSoup(html_content, 'lxml')
        
        video_tag = soup.find('video', id='player_one_html5_api')
        if not video_tag:
            video_tag = soup.find('video', class_='vjs-tech')
        if not video_tag:
            video_tag = soup.find('video')
        
        if video_tag:
            source_tags = video_tag.find_all('source', src=True)
            if source_tags:
                source_tag = source_tags[-1]
                vid_url = source_tag.get('src')
                if vid_url:
                    vid_url = html.unescape(vid_url)
                    return vid_url
        
        html_without_comments = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        source_pattern = r'<source\s+[^>]*src=["\']([^"\']+\.mp4[^"\']*)["\'][^>]*>'
        source_matches = re.findall(source_pattern, html_without_comments, re.IGNORECASE)
        if source_matches:
            vid_url = html.unescape(source_matches[-1])
            return vid_url
        
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string:
                strencode_pattern = r'strencode2\(["\']([^"\']+)["\']\)'
                match = re.search(strencode_pattern, script.string)
                if match:
                    encoded_url = match.group(1)
                    try:
                        decoded_url = unquote(encoded_url)
                        src_pattern = r"src=['\"]([^'\"]+\.mp4[^'\"]*)['\"]"
                        url_match = re.search(src_pattern, decoded_url, re.IGNORECASE)
                        if url_match:
                            vid_url = html.unescape(url_match.group(1))
                            return vid_url
                    except (ValueError, AttributeError, IndexError):
                        pass
                
                js_patterns = [
                    r'src=["\']([^"\']*la\.btc620\.com[^"\']*\.mp4[^"\']*)["\']',
                    r'src=["\']([^"\']*ccm\.91p52\.com[^"\']*\.mp4[^"\']*)["\']',
                    r'["\']([^"\']+\.mp4\?[^"\']*)["\']'
                ]
                for js_pattern in js_patterns:
                    js_match = re.search(js_pattern, script.string, re.IGNORECASE)
                    if js_match:
                        vid_url = html.unescape(js_match.group(1))
                        return vid_url
        
        source_tags = soup.find_all('source', src=True)
        for source_tag in reversed(source_tags):
            vid_url = source_tag.get('src')
            if vid_url and '.mp4' in vid_url:
                vid_url = html.unescape(vid_url)
                return vid_url
        
        return None
    
    def download_video(self, video_url, title, output_dir, retry=3, video_page_url=None):
        exists, existing_file = self._check_video_exists(title, output_dir)
        if exists:
            print(f"  [Skip] {os.path.basename(existing_file)}")
            return True
        
        safe_title = self._sanitize_filename(title)
        filepath = os.path.join(output_dir, f"{safe_title}.mp4")
        
        print(f"  [Download] Starting download: {safe_title}")
        if self.site_type == "pornhub":
            referer = 'https://www.pornhub.com/'
            accept_lang = 'en-US,en;q=0.9'
        else:
            referer = 'https://91porn.com/'
            accept_lang = 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        
        headers = {
            'Referer': video_page_url if video_page_url else referer,
            'Origin': referer.replace('/view_video.php', '').rstrip('/'),
            'Accept': '*/*',
            'Accept-Language': accept_lang,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'video',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'Range': 'bytes=0-'
        }
        if video_url and '.m3u8' in video_url.lower():
            return self._download_m3u8_video(video_url, safe_title, filepath, headers, video_page_url, title)
        
        for attempt in range(retry):
            try:
                print(f"  [Connecting] Connecting to video server...", end='', flush=True)
                response = self.session.get(
                    video_url, 
                    headers=headers, 
                    stream=True, 
                    timeout=(10, 120),
                    proxies={'http': None, 'https': None}
                )
                print(f"\r  [Connecting] Connected, status: {response.status_code}")
                
                if response.status_code == 200 or response.status_code == 206:
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    
                    print(f"  [Info] Content-Length: {total_size} bytes ({total_size//1024//1024}MB)" if total_size > 0 else "  [Info] Content-Length: unknown")
                    
                    content_type = response.headers.get('content-type', '').lower()
                    if content_type and 'video' not in content_type and 'application' not in content_type:
                        print(f"  Warning: Response content type is not video: {content_type}")
                        if 'image' in content_type:
                            print(f"  Error: Got image URL instead of video file")
                            response.close()
                            if attempt < retry - 1 and video_page_url:
                                print(f"  Trying to re-fetch video URL...")
                                if self.site_type == "pornhub":
                                    new_url = self._get_pornhub_video_url(video_page_url)
                                    if new_url and new_url != video_url:
                                        print(f"  Re-fetched new video URL")
                                        video_url = new_url
                                        time.sleep(2)
                                        continue
                                elif self.site_type == "91porn":
                                    new_url = self._get_91porn_video_url(video_page_url)
                                    if new_url and new_url != video_url:
                                        print(f"  Re-fetched new video URL")
                                        video_url = new_url
                                        time.sleep(2)
                                        continue
                            if attempt < retry - 1:
                                time.sleep(2)
                                continue
                            return False
                    
                    temp_file = None
                    try:
                        temp_fd, temp_file = tempfile.mkstemp(suffix='.mp4', dir=output_dir)
                        temp_f = os.fdopen(temp_fd, 'wb')
                        
                        try:
                            last_print_time = time.time()
                            last_data_time = time.time()
                            chunk_timeout = 30
                            
                            buffer_list = []
                            buffer_size = 0
                            max_buffer_size = 10 * 1024 * 1024
                            
                            if total_size > 0:
                                print(f"\r  [Download] 0.0% (0MB/{total_size//1024//1024}MB)", end='', flush=True)
                            else:
                                print(f"\r  [Download] Starting...", end='', flush=True)
                            
                            chunk_count = 0
                            iter_start_time = time.time()
                            
                            try:
                                first_chunk_time = None
                                for chunk in response.iter_content(chunk_size=self.chunk_size):
                                    if chunk_count == 0 and time.time() - iter_start_time > 5:
                                        wait_time = time.time() - iter_start_time
                                        print(f"\r  [Download] Waiting for data... ({wait_time:.0f}s)", end='', flush=True)
                                    
                                    if chunk:
                                        if first_chunk_time is None:
                                            first_chunk_time = time.time()
                                            wait_time = first_chunk_time - iter_start_time
                                            if wait_time > 1:
                                                print(f"\r  [Download] Data stream started ({wait_time:.1f}s)                    ", flush=True)
                                        
                                        buffer_list.append(chunk)
                                        buffer_size += len(chunk)
                                        downloaded += len(chunk)
                                        last_data_time = time.time()
                                        chunk_count += 1
                                        
                                        current_time = time.time()
                                        
                                        if total_size > 0:
                                            if current_time - last_print_time >= 0.2 or downloaded == total_size or chunk_count % 5 == 0:
                                                percent = (downloaded / total_size) * 100
                                                print(f"\r  [Download] {percent:.1f}% ({downloaded//1024//1024}MB/{total_size//1024//1024}MB)", end='', flush=True)
                                                last_print_time = current_time
                                        else:
                                            if current_time - last_print_time >= 0.2 or chunk_count % 5 == 0:
                                                print(f"\r  [Download] Downloaded: {downloaded//1024//1024}MB", end='', flush=True)
                                                last_print_time = current_time
                                        
                                        buffer_full = buffer_size >= max_buffer_size
                                        has_total_size = total_size > 0
                                        download_complete = has_total_size and downloaded >= total_size
                                        if buffer_full or download_complete:
                                            temp_f.write(b''.join(buffer_list))
                                            temp_f.flush()
                                            buffer_list = []
                                            buffer_size = 0
                                            
                                            if download_complete:
                                                print(f"\r  [Download] 100.0% ({downloaded//1024//1024}MB/{total_size//1024//1024}MB)", end='', flush=True)
                                        
                                        if time.time() - last_data_time > chunk_timeout:
                                            raise requests.exceptions.Timeout(f"Download timeout: no new data received within {chunk_timeout} seconds")
                                    else:
                                        if time.time() - last_data_time > chunk_timeout:
                                            raise requests.exceptions.Timeout(f"Download timeout: no new data received within {chunk_timeout} seconds")
                            except requests.exceptions.ChunkedEncodingError as e:
                                print(f"\n  [Error] Chunked encoding error: {str(e)}")
                                raise
                            except requests.exceptions.Timeout as e:
                                print(f"\n  [Error] Download timeout: {str(e)}")
                                raise
                            except Exception as e:
                                print(f"\n  [Error] Error during download: {type(e).__name__}: {str(e)}")
                                raise
                            
                            if buffer_list:
                                temp_f.write(b''.join(buffer_list))
                            
                            temp_f.flush()
                            os.fsync(temp_f.fileno())
                            temp_f.close()
                            
                            shutil.move(temp_file, filepath)
                            temp_file = None
                            
                            self._add_to_downloaded_list(safe_title)
                            
                            if video_page_url:
                                tags = self._get_video_tags(video_page_url)
                                if tags:
                                    VideoSpider._save_tags_to_file(title, tags, video_page_url)
                            
                            file_size = os.path.getsize(filepath)
                            file_size_mb = file_size / (1024 * 1024)
                            print(f"\n  [Complete] {safe_title}.mp4 ({file_size_mb:.2f}MB)")
                            return True
                            
                        except Exception as exc:
                            if temp_f:
                                temp_f.close()
                            raise exc
                            
                    except Exception as exc:
                        if temp_file and os.path.exists(temp_file):
                            try:
                                os.remove(temp_file)
                            except (OSError, IOError):
                                pass
                        raise exc
                else:
                    if attempt < retry - 1:
                        time.sleep(2)
                        continue
                    print(f"  [Failed] {safe_title} - Status code: {response.status_code}")
                    return False
                    
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as exc:
                error_msg = str(exc)
                if attempt < retry - 1:
                    wait_time = (attempt + 1) * 2
                    print(f"  [Retry] Network error, retrying in {wait_time} seconds... ({error_msg})")
                    time.sleep(wait_time)
                    continue
                print(f"  [Failed] {safe_title} - Network error: {error_msg}")
            except Exception as exc:
                error_msg = str(exc)
                if attempt < retry - 1:
                    wait_time = (attempt + 1) * 2
                    time.sleep(wait_time)
                    continue
                print(f"  [Failed] {safe_title} - {error_msg}")
                
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except (OSError, IOError):
                        pass
                
                return False
        
        return False
    
    def _download_m3u8_video(self, m3u8_url, safe_title, filepath, headers, video_page_url, title=None):
        try:
            import m3u8
        except ImportError:
            print(f"  [Error] m3u8 library required: pip install m3u8")
            return False
        
        try:
            import subprocess
        except ImportError:
            subprocess = None
        
        try:
            m3u8_headers = headers.copy()
            if 'Range' in m3u8_headers:
                del m3u8_headers['Range']
            
            response = self.session.get(m3u8_url, headers=m3u8_headers, timeout=30)
            if response.status_code not in [200, 206]:
                print(f"  [Failed] Unable to download m3u8 playlist, status code: {response.status_code}")
                return False
            
            playlist = m3u8.loads(response.text, uri=m3u8_url)
            
            sub_playlist_url = None
            if playlist.is_variant:
                best_playlist = max(playlist.playlists, key=lambda p: p.stream_info.bandwidth if p.stream_info else 0)
                sub_playlist_url = best_playlist.uri
                if not sub_playlist_url.startswith('http'):
                    sub_playlist_url = urljoin(m3u8_url, sub_playlist_url)
                
                sub_response = self.session.get(sub_playlist_url, headers=m3u8_headers, timeout=30)
                if sub_response.status_code in [200, 206]:
                    sub_playlist = m3u8.loads(sub_response.text, uri=sub_playlist_url)
                    video_segments = sub_playlist.segments
                else:
                    print(f"  [Failed] Unable to download sub-playlist, status code: {sub_response.status_code}")
                    return False
            else:
                video_segments = playlist.segments
            
            if not video_segments:
                print(f"  [Failed] No video segments found in playlist")
                return False
            
            temp_dir = tempfile.mkdtemp(dir=os.path.dirname(filepath))
            ts_files = []
            total_segments = len(video_segments)
            last_progress_time = time.time()
            
            try:
                for idx, segment in enumerate(video_segments, 1):
                    segment_url = segment.uri
                    if not segment_url.startswith('http'):
                        base_url = sub_playlist_url if playlist.is_variant else m3u8_url
                        segment_url = urljoin(base_url, segment_url)
                    
                    ts_file = os.path.join(temp_dir, f"segment_{idx:05d}.ts")
                    
                    seg_response = self.session.get(segment_url, headers=headers, timeout=30, stream=True)
                    if seg_response.status_code in [200, 206]:
                        with open(ts_file, 'wb') as f:
                            for chunk in seg_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        ts_files.append(ts_file)
                        
                        current_time = time.time()
                        if current_time - last_progress_time >= 1.0 or idx == total_segments:
                            percent = (idx / total_segments) * 100
                            print(f"\r  [Download] {percent:.1f}% ({idx}/{total_segments} segments)", end='', flush=True)
                            last_progress_time = current_time
                    else:
                        print(f"\n  [Warning] Segment {idx} download failed, status code: {seg_response.status_code}")
                
                print()
                
                if not ts_files:
                    print(f"  [Failed] No segments downloaded successfully")
                    return False
                
                print(f"  [Merge] Merging {len(ts_files)} segments...", end='', flush=True)
                
                if subprocess is not None:
                    try:
                        file_list_path = os.path.join(temp_dir, 'file_list.txt')
                        with open(file_list_path, 'w', encoding='utf-8') as f:
                            for ts_file in ts_files:
                                f.write(f"file '{os.path.abspath(ts_file)}'\n")
                        
                        ffmpeg_cmd = [
                            'ffmpeg',
                            '-f', 'concat',
                            '-safe', '0',
                            '-i', file_list_path,
                            '-c', 'copy',
                            '-y',
                            filepath
                        ]
                        
                        result = subprocess.run(
                            ffmpeg_cmd,
                            capture_output=True,
                            text=True,
                            timeout=300,
                            check=False
                        )
                        
                        if result.returncode == 0 and os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                            self._add_to_downloaded_list(safe_title)
                            
                            if video_page_url:
                                tags = self._get_video_tags(video_page_url)
                                if tags:
                                    VideoSpider._save_tags_to_file(title if title else safe_title, tags, video_page_url)
                            
                            file_size = os.path.getsize(filepath)
                            file_size_mb = file_size / (1024 * 1024)
                            print(f"\n  [Complete] {safe_title}.mp4 ({file_size_mb:.2f}MB)")
                            
                            try:
                                if os.path.exists(temp_dir):
                                    shutil.rmtree(temp_dir)
                            except (OSError, IOError):
                                pass
                            
                            return True
                    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
                        pass
                    except (OSError, IOError):
                        pass
                
                with open(filepath, 'wb') as outfile:
                    for ts_file in ts_files:
                        with open(ts_file, 'rb') as infile:
                            shutil.copyfileobj(infile, outfile)  # type: ignore[arg-type]
                
                if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                    self._add_to_downloaded_list(safe_title)
                    
                    if video_page_url:
                        tags = self._get_video_tags(video_page_url)
                        if tags:
                            VideoSpider._save_tags_to_file(title if title else safe_title, tags, video_page_url)
                    
                    file_size = os.path.getsize(filepath)
                    file_size_mb = file_size / (1024 * 1024)
                    print(f"\n  [Complete] {safe_title}.mp4 ({file_size_mb:.2f}MB)")
                    
                    try:
                        if os.path.exists(temp_dir):
                            shutil.rmtree(temp_dir)
                    except (OSError, IOError):
                        pass
                    
                    return True
                else:
                    print(f"\n  [Failed] Merged file is invalid")
                    return False
                
            finally:
                try:
                    if os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                except (OSError, IOError):
                    pass
                    
        except (requests.exceptions.RequestException, IOError, OSError) as exc:
            print(f"\n  [Failed] m3u8 download exception: {str(exc)[:200]}")
            return False
    
    def crawl_page(self, page_num):
        videos = self.parse_list_page(page_num)
        
        if not videos:
            print(f"Page {page_num} has no videos")
            return False
        
        if self.site_type == "pornhub":
            if self.search_keyword:
                encoded_keyword = quote(self.search_keyword)
                page_url = f"{self.base_url}/video/search?search={encoded_keyword}&page={page_num}"
            else:
                page_url = "N/A"
        else:
            page_url = self.list_url_template.format(page_num) if self.list_url_template else "N/A"
        
        print(f"\nFound {len(videos)} videos, starting download...")
        print(f"URL: {page_url}")
        
        success_count = 0
        fail_count = 0
        
        for idx, video_info in enumerate(videos, 1):
            print(f"\n[{idx}/{len(videos)}] {video_info['title']}")
            
            video_page_url = video_info['url']
            
            if self.site_type == "pornhub":
                print(f"  [Getting URL] Fetching video download URL...")
                video_url = self.get_video_download_url(video_page_url)
                if video_url:
                    if self.download_video(video_url, video_info['title'], self.video_dir, video_page_url=video_page_url):
                        success_count += 1
                    else:
                        fail_count += 1
                else:
                    print(f"  [Failed] Unable to get video download URL")
                    fail_count += 1
                continue
            
            print(f"  [Getting URL] Fetching video download URL...")
            video_url = self.get_video_download_url(video_page_url)

            if not video_url:
                print(f"  [Failed] Unable to get video download URL")
                fail_count += 1
                continue
            
            if self.download_video(video_url, video_info['title'], self.video_dir, video_page_url=video_page_url):
                success_count += 1
            else:
                fail_count += 1
            
            if self.site_type == "pornhub":
                time.sleep(3)
            else:
                time.sleep(0.5)
        
        print(f"\nPage {page_num} completed: {success_count} successful, {fail_count} failed")
        return True
    
    def run(self):
        print("=" * 60)
        print("Multi-Site Video Spider")
        print("=" * 60)
        
        self.select_site()
        
        self.select_category()
        
        current_page = 1
        
        while True:
            try:
                if current_page == 1:
                    page_input = input(f"\n[{self.mv_flag}] Enter starting page number (enter 'q' to quit, 'c' to reselect category): ").strip()
                    
                    if page_input.lower() == 'q':
                        print("Exiting program")
                        break
                    
                    if page_input.lower() == 'c':
                        self.select_category()
                        current_page = 1
                        continue
                    
                    try:
                        current_page = int(page_input)
                        if current_page < 1:
                            print("Page number must be greater than 0")
                            continue
                    except ValueError:
                        print("Please enter a valid number")
                        continue
                
                has_videos = self.crawl_page(current_page)
                
                if not has_videos:
                    print("\n" + "=" * 60)
                    print("No data on current page, may have reached the last page")
                    print("=" * 60)
                    choice = input("Do you want to select another category to continue? (y/n): ").strip().lower()
                    if choice == 'y':
                        self.select_category()
                        current_page = 1
                        continue
                    else:
                        print("Exiting program")
                        break
                
                print("\n" + "-" * 60)
                next_choice = input(f"Continue to page {current_page + 1}? (y/n/q/c): ").strip().lower()
                
                if next_choice == 'y':
                    current_page += 1
                    continue
                elif next_choice == 'n' or next_choice == 'q':
                    print("Exiting program")
                    break
                elif next_choice == 'c':
                    self.select_category()
                    current_page = 1
                    continue
                else:
                    print("Invalid input, exiting program")
                    break
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user")
                break
            except Exception as exc:
                print(f"Error occurred: {str(exc)}")
                continue

if __name__ == "__main__":
    spider = VideoSpider()
    spider.run()
