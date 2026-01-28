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

    async def generate_summary(self, transcript: str, video_metadata: dict = None, language: str = 'en') -> dict:
        """
        Generate AI summary from transcript

        Args:
            transcript: Full transcript text
            video_metadata: Optional video metadata
            language: Target language for summary (zh/en/ja/ko/es/fr/de)

        Returns:
            Dictionary with summary, key points, and title

        Raises:
            SummarizationError: If summarization fails
        """
        # Language-specific prompts
        language_prompts = {
            'zh': {
                'instruction': '请分析这段视频转录文本并提供：\n1. 精炼的标题（必须使用中文，概括核心内容，适合作为笔记标题和文件名，8-15字，不含标点符号）\n2. 5-7个关键要点（核心论点或主要观点）\n3. 按照视频叙述顺序，将内容组织成2-3个主要部分（适当整合相关内容，避免标题过多）\n   - 每个部分需要 heading（标题）和 content（详细内容数组）\n   - content 是一个数组，包含多个对象，每个对象有 sub_heading 和 details\n   - 只在必要时添加子部分（每个主部分最多2-3个子部分）\n   - 优先整合内容而非细分标题\n\n**格式规范**:\n- 代码、命令、函数名、技术术语等使用 `单行代码` 格式（例如：`print()`、`HTTP`、`React`）\n- 多行代码块使用 ```language 格式（例如：```python, ```javascript）\n- 在必要时提供清晰的示例来帮助理解复杂概念，示例应：\n  * 紧密围绕视频内容展开\n  * 自然融入笔记框架，不单独列出\n  * 基于视频内容或相关领域的典型场景\n  * 只在确实需要澄清概念时添加，避免过度扩展',
                'format_instruction': '请用中文回复，格式为JSON：',
                'system': '你是一位专业的视频内容分析专家。提供清晰、结构化、准确的中文笔记。标题必须精炼、概括核心内容，不要直接使用原视频标题。按照视频的逻辑顺序组织内容，确保层次清晰。注重内容整合，避免标题过多导致碎片化。\n\n重要格式要求：\n1. 正确使用 Markdown 代码格式：单行代码用 `code`，多行代码用 ```language\n2. 在涉及技术概念、复杂逻辑、抽象理念时，提供具体示例帮助理解\n3. 示例必须紧密围绕视频内容，自然融入笔记，不要刻意分离或过度扩展\n4. 保持专业性和准确性，示例要有实际价值'
            },
            'en': {
                'instruction': 'Please analyze this video transcript and provide:\n1. A refined title in English (summarizing core content, suitable for notes title and filename, 3-8 words, no punctuation)\n2. 5-7 key points (core arguments or main ideas)\n3. Organize content into 2-3 main sections following the video narrative order (consolidate related content, avoid excessive headings)\n   - Each section needs heading (title) and content (detailed content array)\n   - content is an array containing objects with sub_heading and details\n   - Only add subsections when necessary (max 2-3 subsections per main section)\n   - Prioritize content consolidation over subdivision\n\n**Format Requirements**:\n- Use `inline code` format for code, commands, function names, technical terms (e.g., `print()`, `HTTP`, `React`)\n- Use ```language format for multi-line code blocks (e.g., ```python, ```javascript)\n- Provide clear examples when necessary to help understand complex concepts. Examples should:\n  * Be closely tied to the video content\n  * Be naturally integrated into the note structure, not listed separately\n  * Be based on video content or typical scenarios from the relevant field\n  * Only be added when truly needed for clarification, avoid over-expansion',
                'format_instruction': 'Format your response as JSON:',
                'system': 'You are an expert at analyzing video content and extracting key information. Provide clear, structured, and accurate notes in English. Create a refined title that captures the essence, not the original video title. Organize content following the video\'s logical flow with clear hierarchy. Focus on consolidating content to avoid fragmentation from too many headings.\n\nImportant format requirements:\n1. Use proper Markdown code formatting: `code` for inline code, ```language for code blocks\n2. Provide concrete examples when dealing with technical concepts, complex logic, or abstract ideas\n3. Examples must be closely related to video content and naturally integrated into notes, not artificially separated or over-expanded\n4. Maintain professionalism and accuracy, examples should have practical value'
            }
        }

        # Get language-specific prompt or default to English
        lang_prompt = language_prompts.get(language, language_prompts['en'])
        # Prepare context
        context = ""
        if video_metadata:
            context = f"""
Video Information:
- Title: {video_metadata.get('title', 'Unknown')}
- Duration: {video_metadata.get('duration_formatted', 'Unknown')}
- Platform: {video_metadata.get('platform', 'Unknown')}

"""

        # Prepare the prompt with structured format
        prompt = f"""{context}Transcript:
{transcript}

{lang_prompt['instruction']}

{lang_prompt['format_instruction']}
{{
    "title": "Brief and clear title",
    "key_points": [
        "Key point 1",
        "Key point 2",
        "Key point 3",
        "Key point 4",
        "Key point 5"
    ],
    "detailed_content": [
        {{
            "heading": "Main Section Title 1",
            "content": [
                {{
                    "sub_heading": "Subsection Title 1.1",
                    "details": "Detailed explanation with proper formatting. Use `inline code` for technical terms and ```language for code blocks."
                }},
                {{
                    "sub_heading": "Subsection Title 1.2",
                    "details": "More detailed content..."
                }}
            ]
        }},
        {{
            "heading": "Main Section Title 2",
            "content": [
                {{
                    "sub_heading": "Subsection Title 2.1",
                    "details": "Content with examples when needed..."
                }}
            ]
        }}
    ]
}}"""

        # Prepare request data
        request_data = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": lang_prompt['system']
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": self.settings.max_tokens
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
                        # Import logging for debug output
                        import logging
                        logger = logging.getLogger(__name__)

                        logger.debug(f"Raw API response (first 300 chars): {content[:300]}")

                        # Clean the response to extract JSON
                        # Handle multiple JSON extraction strategies

                        json_content = None
                        logger.debug(f"Response length: {len(content)}, first 500 chars: {content[:500]}")

                        # Strategy 1: Find balanced JSON object with brace matching (handles markdown code blocks)
                        brace_start = content.find('{')
                        potential_json = None
                        if brace_start >= 0:
                            logger.debug(f"Found opening brace at position {brace_start}")
                            # Find the matching closing brace, accounting for nested structures
                            brace_count = 0
                            in_string = False
                            escape_next = False
                            brace_end = -1

                            for i in range(brace_start, len(content)):
                                char = content[i]

                                # Handle string context to avoid counting braces inside strings
                                if not escape_next:
                                    if char == '"':
                                        in_string = not in_string
                                    elif char == '\\':
                                        escape_next = True
                                        continue
                                    elif not in_string:
                                        if char == '{':
                                            brace_count += 1
                                        elif char == '}':
                                            brace_count -= 1
                                            if brace_count == 0:
                                                brace_end = i + 1
                                                break
                                escape_next = False

                            if brace_end > 0:
                                potential_json = content[brace_start:brace_end]
                                logger.debug(f"Extracted JSON by brace matching ({len(potential_json)} chars)")
                                logger.debug(f"JSON first 200 chars: {potential_json[:200]}")
                                logger.debug(f"JSON last 100 chars: {potential_json[-100:]}")

                                # Try to parse it
                                try:
                                    json.loads(potential_json)
                                    json_content = potential_json
                                    logger.info(f"✓ Valid JSON extracted ({len(json_content)} chars)")
                                except json.JSONDecodeError as err:
                                    logger.warning(f"JSON parse failed: {err.msg} at pos {err.pos}")
                                    logger.debug(f"Context: ...{potential_json[max(0, err.pos-50):min(len(potential_json), err.pos+50)]}...")
                            elif brace_count > 0:
                                # Truncated JSON - try to fix by adding missing braces
                                # Use content from brace_start to the end
                                potential_json = content[brace_start:]
                                logger.warning(f"Could not find matching closing brace (brace_count={brace_count})")
                                logger.debug("Attempting to fix truncated JSON by adding closing braces")
                                potential_json_fixed = potential_json + ('}' * brace_count)
                                try:
                                    json.loads(potential_json_fixed)
                                    json_content = potential_json_fixed
                                    logger.info(f"✓ Fixed truncated JSON by adding {brace_count} closing braces")
                                except json.JSONDecodeError as err:
                                    logger.debug(f"Truncated JSON repair failed: {err.msg}")
                            else:
                                logger.warning(f"No closing brace found from position {brace_start}")

                        if json_content:
                            logger.debug(f"Final JSON to parse (last 100 chars): {json_content[-100:]}")

                            # Try to parse JSON - handle potential encoding issues
                            try:
                                summary_data = json.loads(json_content)
                                logger.debug(f"Raw parsed data - title: {str(summary_data.get('title', 'MISSING'))[:50]}")
                                logger.debug(f"Raw parsed data - key_points: {len(summary_data.get('key_points', []))} items")

                                # Validate and clean the parsed data
                                summary_data = self._validate_and_clean_json(summary_data)
                                logger.info(f"After cleaning - title: {summary_data.get('title', 'MISSING')[:50]}")
                                logger.debug(f"Cleaned data keys: {list(summary_data.keys())}")
                            except json.JSONDecodeError as json_err:
                                logger.error(f"JSON decode failed: {str(json_err)}, attempting text fallback")
                                logger.debug(f"Failed JSON content: {json_content[:500]}")
                                summary_data = self._parse_text_response(content)
                        else:
                            # Fallback if no JSON object found
                            logger.warning(f"No JSON object found in response (first 300 chars): {content[:300]}")
                            summary_data = self._parse_text_response(content)

                        # Validate required fields (allow either summary, sections, or detailed_content)
                        required_fields = ["key_points", "title"]
                        if not all(key in summary_data for key in required_fields):
                            raise SummarizationError("Invalid summary format: missing required fields")

                        # Ensure we have either detailed_content, sections, or summary
                        if not summary_data.get('detailed_content') and not summary_data.get('sections') and not summary_data.get('summary'):
                            raise SummarizationError("Invalid summary format: missing content (detailed_content, sections, or summary)")

                        # Final validation: ensure we have meaningful content
                        if not summary_data.get('key_points'):
                            raise SummarizationError("No valid key points extracted")

                        return summary_data

                    except json.JSONDecodeError:
                        # Fallback to text parsing
                        return self._parse_text_response(content)

        except aiohttp.ClientError as e:
            raise SummarizationError(f"Network error: {str(e)}")
        except Exception as e:
            raise SummarizationError(f"Summarization failed: {str(e)}")

    def _validate_and_clean_json(self, data: dict) -> dict:
        """
        Validate and clean JSON data from AI response

        Sometimes the AI returns malformed JSON where the values themselves
        contain JSON structure markers. This method detects and fixes such issues.

        Args:
            data: Parsed JSON data

        Returns:
            Cleaned and validated data
        """
        import logging
        logger = logging.getLogger(__name__)

        cleaned_data = {}

        # Clean key_points field first (as summary might reference it)
        key_points = data.get('key_points', [])
        cleaned_points = []

        if isinstance(key_points, list):
            for point in key_points:
                if isinstance(point, str):
                    point_stripped = point.strip()

                    # Check if the entire element is a stringified JSON-like structure
                    if (point_stripped.startswith('"key_points"') or
                        point_stripped.startswith('"summary"') or
                        point_stripped.startswith('{')):
                        # This looks like malformed JSON, try to extract array content
                        try:
                            # Try to find and extract array notation  [...]
                            # Use a more specific pattern that looks for quotes strings within brackets
                            array_pattern = r'\[\s*"([^"]+)"(?:\s*,\s*"([^"]+)")*'
                            matches = re.findall(r'"([^"]+)"', point)
                            if matches and len(matches) > 1:
                                # We found multiple quoted strings, likely the actual points
                                for match in matches:
                                    # Skip the "key_points" or "summary" labels
                                    if match in ['key_points', 'summary', 'title']:
                                        continue
                                    if len(match.strip()) > 5:
                                        clean_p = re.sub(r'^\d+[\.、]\s*', '', match.strip())
                                        cleaned_points.append(clean_p)
                                continue
                        except Exception as e:
                            logger.warning(f"Failed to extract points from malformed JSON: {e}")

                        # If extraction failed, skip this malformed point
                        continue

                    # Check if starts with array bracket or other JSON markers
                    if point_stripped.startswith('[') or point_stripped.startswith('{'):
                        continue

                    # Normal point processing
                    clean_point = point_stripped.strip('"').strip("'")
                    clean_point = re.sub(r'^\d+[\.、]\s*', '', clean_point)
                    if clean_point and len(clean_point) > 5:
                        cleaned_points.append(clean_point)

        cleaned_data['key_points'] = cleaned_points[:7]  # Limit to 7 points

        # Clean summary field
        summary = data.get('summary', '')
        if isinstance(summary, str):
            # Check if summary is actually a stringified key_points array
            if summary.strip().startswith('"key_points"') and '[' in summary:
                # Try to extract the first point as summary
                try:
                    array_match = re.search(r'\[(.*)\]', summary, re.DOTALL)
                    if array_match:
                        array_content = '[' + array_match.group(1) + ']'
                        extracted_points = json.loads(array_content)
                        if isinstance(extracted_points, list) and extracted_points:
                            # Use all points to create a summary
                            summary = '本视频主要讨论了以下内容：' + '；'.join([p.strip('"') for p in extracted_points[:3]]) + '。'
                except Exception as e:
                    logger.warning(f"Failed to parse stringified array in summary: {e}")
                    # Use cleaned points if available
                    if cleaned_points:
                        summary = '本视频主要讨论了以下内容：' + '；'.join(cleaned_points[:3]) + '。'
                    else:
                        summary = ''
            # Check if summary contains JSON structure markers
            elif summary.strip().startswith('"summary"') or summary.strip().startswith('{'):
                # Try to extract actual content
                try:
                    inner_json_match = re.search(r'\{.*\}', summary, re.DOTALL)
                    if inner_json_match:
                        inner_data = json.loads(inner_json_match.group(0))
                        summary = inner_data.get('summary', '')
                except:
                    # If parsing fails, try to extract first valid sentence
                    sentences = [s.strip() for s in summary.split('.') if s.strip() and not s.strip().startswith('"')]
                    summary = sentences[0] if sentences else ''

            cleaned_data['summary'] = summary.strip()
        else:
            cleaned_data['summary'] = str(summary).strip()

        # If summary is still empty or malformed, generate from key points
        if not cleaned_data['summary'] or cleaned_data['summary'].startswith('"'):
            if cleaned_points:
                cleaned_data['summary'] = '本视频主要讨论了以下内容：' + '；'.join(cleaned_points[:3]) + '。'
            else:
                cleaned_data['summary'] = '视频内容总结。'

        # Clean title field
        title = data.get('title', 'video_notes')
        if isinstance(title, str):
            # Remove JSON structure markers, quotes, and file extensions
            title = title.strip().strip('"').strip("'")
            title = re.sub(r'\.(md|txt)$', '', title)
            # Remove invalid filename characters
            title = re.sub(r'[<>:"/\\|?*]', '_', title)
            # Ensure title is not too long
            if len(title) > 100:
                title = title[:100]
            cleaned_data['title'] = title.strip() or 'video_notes'
        else:
            cleaned_data['title'] = 'video_notes'

        # If title is empty, generate from first key point
        if not cleaned_data['title'] or cleaned_data['title'] == 'video_notes':
            if cleaned_points:
                # Use first key point as title (limit to 50 chars)
                cleaned_data['title'] = cleaned_points[0][:50].replace('/', '_').replace('\\', '_')
            else:
                cleaned_data['title'] = 'video_notes'

        # Clean detailed_content field (new structured format)
        detailed_content = data.get('detailed_content', [])
        cleaned_detailed_content = []

        if isinstance(detailed_content, list):
            for section in detailed_content:
                if isinstance(section, dict):
                    cleaned_section = {}

                    # Clean section heading
                    heading = section.get('heading', '').strip()
                    if heading:
                        cleaned_section['heading'] = heading

                    # Clean content array
                    content_items = section.get('content', [])
                    cleaned_content_items = []

                    if isinstance(content_items, list):
                        for item in content_items:
                            if isinstance(item, dict):
                                cleaned_item = {}

                                sub_heading = item.get('sub_heading', '').strip()
                                if sub_heading:
                                    cleaned_item['sub_heading'] = sub_heading

                                details = item.get('details', '').strip()
                                if details:
                                    cleaned_item['details'] = details

                                # Only add if has content
                                if cleaned_item:
                                    cleaned_content_items.append(cleaned_item)

                    if cleaned_content_items:
                        cleaned_section['content'] = cleaned_content_items

                    # Only add section if it has content
                    if cleaned_section and cleaned_content_items:
                        cleaned_detailed_content.append(cleaned_section)

        if cleaned_detailed_content:
            cleaned_data['detailed_content'] = cleaned_detailed_content
        else:
            # Fallback: try to clean old sections format
            sections = data.get('sections', [])
            cleaned_sections = []

            if isinstance(sections, list):
                for section in sections:
                    if isinstance(section, dict):
                        cleaned_section = {}

                        section_title = section.get('title', '').strip()
                        if section_title:
                            cleaned_section['title'] = section_title

                        section_content = section.get('content', '').strip()
                        if section_content:
                            cleaned_section['content'] = section_content

                        subsections = section.get('subsections', [])
                        cleaned_subsections = []

                        if isinstance(subsections, list):
                            for subsection in subsections:
                                if isinstance(subsection, dict):
                                    cleaned_subsection = {}

                                    subsection_title = subsection.get('title', '').strip()
                                    if subsection_title:
                                        cleaned_subsection['title'] = subsection_title

                                    subsection_content = subsection.get('content', '').strip()
                                    if subsection_content:
                                        cleaned_subsection['content'] = subsection_content

                                    if cleaned_subsection:
                                        cleaned_subsections.append(cleaned_subsection)

                        if cleaned_subsections:
                            cleaned_section['subsections'] = cleaned_subsections

                        if cleaned_section:
                            cleaned_sections.append(cleaned_section)

            if cleaned_sections:
                cleaned_data['sections'] = cleaned_sections

        return cleaned_data

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

        # Title - use AI-generated refined title
        refined_title = summary_data.get('title', 'Video Notes').replace('_', ' ')
        lines.append(f"# {refined_title}")
        lines.append("")

        # Metadata - video source, duration, author
        if video_metadata:
            lines.append(f"**来源**: {video_metadata.get('url', 'Unknown')}")
            if video_metadata.get('duration_formatted'):
                lines.append(f"**时长**: {video_metadata['duration_formatted']}")
            if video_metadata.get('uploader'):
                lines.append(f"**作者**: {video_metadata['uploader']}")
            lines.append(f"**处理时间**: {self._get_current_timestamp()}")
            lines.append("")

        # Key Points - in blockquote format with ordered list
        if summary_data.get('key_points'):
            lines.append("> **核心要点**")
            for i, point in enumerate(summary_data['key_points'], 1):
                # Clean point and add as ordered list in blockquote
                clean_point = re.sub(r'^\d+[\.、]\s*', '', point.strip())
                lines.append(f"> {i}. {clean_point}")
            lines.append("")

        # Detailed content sections - multi-level headings with numbering
        detailed_content = summary_data.get('detailed_content', [])
        if detailed_content and isinstance(detailed_content, list):
            for section_idx, section in enumerate(detailed_content, 1):
                if not isinstance(section, dict):
                    continue

                # Main section heading (## level 2)
                section_heading = section.get('heading', '').strip()
                if section_heading:
                    lines.append(f"## {section_idx}. {section_heading}")
                    lines.append("")

                # Process content array
                content_items = section.get('content', [])
                if isinstance(content_items, list):
                    for content_item in content_items:
                        if not isinstance(content_item, dict):
                            continue

                        sub_heading = content_item.get('sub_heading', '').strip()
                        details = content_item.get('details', '').strip()

                        if sub_heading:
                            lines.append(f"**{sub_heading}**")
                            lines.append("")

                        if details:
                            lines.append(details)
                            lines.append("")
        else:
            # Fallback: if no detailed_content, check for old format
            sections = summary_data.get('sections', [])
            if sections:
                for section_idx, section in enumerate(sections, 1):
                    section_title = section.get('title', '').strip()
                    section_content = section.get('content', '').strip()

                    if section_title:
                        lines.append(f"## {section_idx}. {section_title}")
                        lines.append("")

                    if section_content:
                        lines.append(section_content)
                        lines.append("")

                    subsections = section.get('subsections', [])
                    for subsection_idx, subsection in enumerate(subsections, 1):
                        subsection_title = subsection.get('title', '').strip()
                        subsection_content = subsection.get('content', '').strip()

                        if subsection_title:
                            lines.append(f"### {section_idx}.{subsection_idx} {subsection_title}")
                            lines.append("")

                        if subsection_content:
                            lines.append(subsection_content)
                            lines.append("")
            elif summary_data.get('summary'):
                # Final fallback: use summary text
                lines.append("## 详细内容")
                summary_text = summary_data['summary']
                # Make sure summary is a string, not a dict or list
                if isinstance(summary_text, (dict, list)):
                    summary_text = str(summary_text)
                lines.append(summary_text)
                lines.append("")

        return '\n'.join(lines)

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in readable format"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
