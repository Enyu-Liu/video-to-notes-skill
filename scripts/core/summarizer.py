"""AI summarization module using OpenRouter API"""

import asyncio
import aiohttp
from typing import List, Optional
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import get_settings
from core.exceptions import SummarizationError


class Summarizer:
    """Handles AI summarization using OpenRouter API"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize summarizer with API configuration

        Args:
            api_key: OpenRouter API key. If None, uses value from settings
            model: AI model to use. If None, uses value from settings
        """
        self.settings = get_settings()
        self.api_key = api_key or self.settings.openrouter_api_key
        self.model = model or self.settings.ai_model
        self.base_url = "https://openrouter.ai/api/v1"

        if not self.api_key:
            raise SummarizationError("OpenRouter API key is required")

    async def generate_summary(self, transcript: str, video_metadata: dict = None) -> dict:
        """
        Generate AI summary from transcript

        Args:
            transcript: Full transcript text
            video_metadata: Optional video metadata

        Returns:
            Dictionary with summary, key points, and title

        Raises:
            SummarizationError: If summarization fails
        """
        # Prepare context
        context = ""
        if video_metadata:
            context = f"""
Video Information:
- Title: {video_metadata.get('title', 'Unknown')}
- Duration: {video_metadata.get('duration_formatted', 'Unknown')}
- Platform: {video_metadata.get('platform', 'Unknown')}

"""

        # Prepare the prompt
        prompt = f"""{context}Transcript:
{transcript}

Please analyze this video transcript and provide:
1. A concise but comprehensive summary (200-300 words)
2. 5-7 key bullet points highlighting the main takeaways
3. A suitable filename for the notes (without extension, max 50 characters)

Format your response as JSON:
{{
    "summary": "...",
    "key_points": ["...", "...", "..."],
    "title": "..."
}}"""

        # Prepare request data
        request_data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert at analyzing video content and extracting key information. Provide clear, concise, and accurate summaries."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/anthropics/claude-code",
                    "X-Title": "Video Note Skill"
                }

                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=request_data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise SummarizationError(f"API request failed: {response.status} - {error_text}")

                    result = await response.json()

                    # Extract content from response
                    if "choices" not in result or not result["choices"]:
                        raise SummarizationError("Invalid API response format")

                    content = result["choices"][0]["message"]["content"]

                    # Try to parse JSON response
                    try:
                        # Clean the response to extract JSON
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            json_content = json_match.group(0)
                            summary_data = json.loads(json_content)
                        else:
                            # Fallback if JSON parsing fails
                            summary_data = self._parse_text_response(content)

                        # Validate required fields
                        if not all(key in summary_data for key in ["summary", "key_points", "title"]):
                            raise SummarizationError("Invalid summary format")

                        return summary_data

                    except json.JSONDecodeError:
                        # Fallback to text parsing
                        return self._parse_text_response(content)

        except aiohttp.ClientError as e:
            raise SummarizationError(f"Network error: {str(e)}")
        except Exception as e:
            raise SummarizationError(f"Summarization failed: {str(e)}")

    def _parse_text_response(self, content: str) -> dict:
        """
        Fallback method to parse response if JSON parsing fails

        Args:
            content: Raw response content

        Returns:
            Parsed summary data
        """
        # Initialize default values
        summary = ""
        key_points = []
        title = "video_notes"

        lines = content.strip().split('\n')
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try to identify sections
            if "summary" in line.lower():
                current_section = "summary"
                continue
            elif "key points" in line.lower() or "bullet points" in line.lower():
                current_section = "key_points"
                continue
            elif "title" in line.lower() or "filename" in line.lower():
                current_section = "title"
                continue

            # Extract content based on current section
            if current_section == "summary":
                if not summary:
                    summary = line
                else:
                    summary += " " + line
            elif current_section == "key_points":
                # Remove bullet markers and clean
                clean_point = re.sub(r'^[-*•]\s*', '', line).strip()
                if clean_point:
                    key_points.append(clean_point)
            elif current_section == "title":
                if not title or title == "video_notes":
                    title = re.sub(r'^(title|filename):\s*', '', line, flags=re.IGNORECASE).strip()

        # Ensure we have at least some key points
        if not key_points and summary:
            # Split summary into sentences and create key points
            sentences = [s.strip() for s in summary.split('.') if s.strip()]
            key_points = sentences[:3]  # Take first 3 sentences as key points

        return {
            "summary": summary,
            "key_points": key_points[:5],  # Limit to 5 points
            "title": title or "video_notes"
        }

    def format_markdown_note(self, summary_data: dict, video_metadata: dict = None) -> str:
        """
        Format summary data into markdown note

        Args:
            summary_data: Summary data from generate_summary
            video_metadata: Optional video metadata

        Returns:
            Formatted markdown string
        """
        lines = []

        # Title
        if video_metadata and video_metadata.get('title'):
            lines.append(f"# {video_metadata['title']}")
        else:
            lines.append(f"# {summary_data.get('title', 'Video Notes').replace('_', ' ')}")

        lines.append("")

        # Key Points
        if summary_data.get('key_points'):
            lines.append("## 核心要点")
            for point in summary_data['key_points']:
                # Convert Chinese numbering to bullet points if needed
                clean_point = re.sub(r'^\d+[\.、]\s*', '', point.strip())
                lines.append(f"- {clean_point}")
            lines.append("")

        # Summary
        if summary_data.get('summary'):
            lines.append("## 详细总结")
            lines.append(summary_data['summary'])
            lines.append("")

        # Metadata
        lines.append("---")
        if video_metadata:
            lines.append(f"**来源**: {video_metadata.get('url', 'Unknown')}")
            if video_metadata.get('duration_formatted'):
                lines.append(f"**时长**: {video_metadata['duration_formatted']}")
            if video_metadata.get('uploader'):
                lines.append(f"**作者**: {video_metadata['uploader']}")
        lines.append(f"**处理时间**: {self._get_current_timestamp()}")

        return '\n'.join(lines)

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in readable format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
