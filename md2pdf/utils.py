import re
import hashlib
import os
import sys
from pathlib import Path


def preprocess_strip_wrapping_fence(text: str) -> str:
    """检测并剥离包裹整个文档的外层代码 fence。"""
    lines = text.split('\n')
    if not lines:
        return text
    first_line = lines[0].strip()
    fence_match = re.match(r'^(`{3,4})(.*)$', first_line)
    if not fence_match:
        return text
    fence_char = fence_match.group(1)
    last_line = lines[-1].strip()
    closing_match = re.match(r'^`{3,4}$', last_line)
    if closing_match and closing_match.group() == fence_char:
        return '\n'.join(lines[1:-1])
    elif len(lines) > 1:
        has_md = any(
            l.strip().startswith(s)
            for s in ['#', '|', '- ', '* ', '1.', '>']
            for l in lines[1:20]
        )
        if has_md:
            return '\n'.join(lines[1:])
    return text


def preprocess_mrkdwn(text: str) -> str:
    """预处理 Slack mrkdwn 特有语法为标准 Markdown。"""
    text = re.sub(r'<@([A-Z0-9]+)>', r'<span class="mrkdwn-mention">@\1</span>', text)
    text = re.sub(r'<#([A-Z0-9]+)>', r'<span class="mrkdwn-mention">#\1</span>', text)
    text = re.sub(r'<([^|>]+)\|([^>]+)>', r'[\2](\1)', text)
    return text


def slugify(text: str) -> str:
    """将文本转换为 URL 友好的锚点 id。"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\u4e00-\u9fff]+', '-', text)
    return text.strip('-') or 'section'


def escape_html(text: str) -> str:
    """HTML 转义。"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def today() -> str:
    """返回今天的日期字符串。"""
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d')
