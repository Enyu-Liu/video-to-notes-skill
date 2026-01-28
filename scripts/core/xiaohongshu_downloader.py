"""Xiaohongshu video downloader module"""

import json
import re
import logging
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Try to use curl_cffi for better browser impersonation
try:
    from curl_cffi import requests as curl_requests
    HAS_CURL_CFFI = True
except ImportError:
    import requests as curl_requests
    HAS_CURL_CFFI = False

import requests  # Still need regular requests for video download


class XiaohongshuDownloader:
    """Download videos from Xiaohongshu (小红书)"""

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    def __init__(self, temp_dir: Path):
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        # Use curl_cffi session if available for browser impersonation
        if HAS_CURL_CFFI:
            self.session = curl_requests.Session(impersonate="chrome")
        else:
            self.session = requests.Session()
            self.session.headers.update(self.HEADERS)

    @staticmethod
    def is_xiaohongshu_url(url: str) -> bool:
        """Check if URL is a Xiaohongshu URL"""
        parsed = urlparse(url)
        return 'xiaohongshu.com' in parsed.netloc or 'xhslink.com' in parsed.netloc

    @staticmethod
    def extract_note_id(url: str) -> Optional[str]:
        """Extract note ID from URL"""
        # Pattern: /explore/xxx or /discovery/item/xxx
        patterns = [
            r'/explore/([a-f0-9]+)',
            r'/discovery/item/([a-f0-9]+)',
            r'/item/([a-f0-9]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def _parse_initial_state(self, html: str) -> Optional[dict]:
        """Parse __INITIAL_STATE__ from HTML"""
        # Find the initial state script
        pattern = r'window\.__INITIAL_STATE__\s*=\s*(\{.+?\})\s*</script>'
        match = re.search(pattern, html, re.DOTALL)
        if not match:
            # Try alternative pattern
            pattern = r'window\.__INITIAL_STATE__\s*=\s*(.+?);?\s*(?:</script>|window\.)'
            match = re.search(pattern, html, re.DOTALL)

        if not match:
            logger.error("Could not find __INITIAL_STATE__ in page")
            return None

        try:
            # Fix JS object to JSON (undefined -> null)
            js_obj = match.group(1)
            js_obj = re.sub(r'\bundefined\b', 'null', js_obj)
            return json.loads(js_obj)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse __INITIAL_STATE__: {e}")
            return None

    def _extract_video_info(self, state: dict, note_id: str) -> Optional[dict]:
        """Extract video info from initial state"""
        try:
            # Navigate to note data
            note_detail_map = state.get('note', {}).get('noteDetailMap', {})
            note_data = note_detail_map.get(note_id, {}).get('note', {})

            if not note_data:
                # Try alternative path
                note_data = state.get('noteData', {}).get('data', {}).get('noteData', {})

            if not note_data:
                logger.error("Could not find note data in state")
                return None

            video_data = note_data.get('video', {})
            if not video_data:
                logger.error("This note does not contain a video")
                return None

            # Get video streams
            media = video_data.get('media', {})
            streams = media.get('stream', {})

            video_urls = []

            # Collect all video URLs
            for quality, stream_list in streams.items():
                if isinstance(stream_list, list):
                    for stream in stream_list:
                        master_url = stream.get('masterUrl')
                        if master_url:
                            video_urls.append({
                                'url': master_url,
                                'quality': quality,
                                'width': stream.get('width', 0),
                                'height': stream.get('height', 0),
                            })
                        # Also check backup URLs
                        backup_urls = stream.get('backupUrls', [])
                        for backup_url in backup_urls:
                            if backup_url:
                                video_urls.append({
                                    'url': backup_url,
                                    'quality': quality,
                                    'width': stream.get('width', 0),
                                    'height': stream.get('height', 0),
                                })

            # Try to get original video
            origin_key = video_data.get('originVideoKey')
            if origin_key:
                origin_url = f"https://sns-video-bd.xhscdn.com/{origin_key}"
                video_urls.insert(0, {
                    'url': origin_url,
                    'quality': 'origin',
                    'width': 0,
                    'height': 0,
                })

            if not video_urls:
                logger.error("No video URLs found")
                return None

            # Get metadata
            title = note_data.get('title', '') or note_data.get('desc', '')[:50] or f'xiaohongshu_{note_id}'
            user = note_data.get('user', {})

            return {
                'title': self._sanitize_filename(title),
                'uploader': user.get('nickname', 'Unknown'),
                'user_id': user.get('userId', ''),
                'duration': video_data.get('duration', 0) // 1000,  # ms to seconds
                'description': note_data.get('desc', ''),
                'video_urls': video_urls,
                'note_id': note_id,
            }

        except Exception as e:
            logger.error(f"Error extracting video info: {e}")
            return None

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe file system usage"""
        # Remove invalid characters
        invalid_chars = r'[<>:"/\\|?*\n\r\t]'
        filename = re.sub(invalid_chars, '_', filename)
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        return filename.strip() or 'xiaohongshu_video'

    def _download_video(self, video_urls: list, output_path: Path) -> bool:
        """Try to download video from URL list"""
        for video_info in video_urls:
            url = video_info['url']
            try:
                logger.info(f"Trying to download from: {url[:80]}...")

                # Use streaming download
                response = self.session.get(url, stream=True, timeout=60)

                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if 'video' in content_type or url.endswith('.mp4') or 'xhscdn.com' in url:
                        with open(output_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)

                        # Verify file size
                        if output_path.stat().st_size > 1000:
                            logger.info(f"Download successful: {output_path.name}")
                            return True
                        else:
                            logger.warning("Downloaded file too small, trying next URL")
                            output_path.unlink(missing_ok=True)
                    else:
                        logger.warning(f"Unexpected content type: {content_type}")
                else:
                    logger.warning(f"HTTP {response.status_code} for URL")

            except Exception as e:
                logger.warning(f"Failed to download from URL: {e}")
                continue

        return False

    def download(self, url: str) -> Tuple[Optional[str], Optional[dict]]:
        """
        Download video from Xiaohongshu URL

        Returns:
            Tuple of (video_path, metadata) or (None, None) on failure
        """
        note_id = self.extract_note_id(url)
        if not note_id:
            logger.error(f"Could not extract note ID from URL: {url}")
            return None, None

        logger.info(f"Downloading Xiaohongshu video: {note_id}")

        # Clean URL (remove extra parameters)
        clean_url = f"https://www.xiaohongshu.com/explore/{note_id}"

        try:
            # Fetch page
            response = self.session.get(clean_url, timeout=30)
            html = response.text

            # Check for regional restriction (redirected to 404)
            if '404' in str(response.url) or 'error_code=300031' in str(response.url):
                logger.error("Xiaohongshu regional restriction detected")
                logger.error("小红书检测到您的网络位于中国大陆以外，拒绝访问。")
                logger.error("解决方案:")
                logger.error("  1. 手动下载视频到本地，然后使用 --local-video 参数")
                logger.error("  2. 使用中国大陆的网络/VPN")
                logger.error("  3. 使用第三方工具如 dlbunny.com 下载后使用本地视频")
                raise RegionalRestrictionError(
                    "Xiaohongshu regional restriction: This content is not accessible from outside mainland China. "
                    "Please download the video manually and use --local-video option."
                )

            response.raise_for_status()

            # Parse initial state
            state = self._parse_initial_state(html)
            if not state:
                return None, None

            # Extract video info
            video_info = self._extract_video_info(state, note_id)
            if not video_info:
                return None, None

            # Download video
            output_path = self.temp_dir / f"{video_info['title']}.mp4"

            if not self._download_video(video_info['video_urls'], output_path):
                logger.error("All download attempts failed")
                return None, None

            # Prepare metadata
            metadata = {
                'title': video_info['title'],
                'uploader': video_info['uploader'],
                'duration': video_info['duration'],
                'description': video_info['description'],
                'upload_date': '',
                'url': url,
                'id': note_id,
                'platform': 'xiaohongshu',
            }

            return str(output_path), metadata

        except RegionalRestrictionError:
            raise
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None, None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None, None


class RegionalRestrictionError(Exception):
    """Raised when Xiaohongshu blocks access due to regional restrictions"""
    pass
