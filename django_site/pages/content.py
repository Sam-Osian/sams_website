from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re
from typing import Any

import markdown
import yaml


DOCS_DIR = Path(__file__).resolve().parents[2] / "docs"
POSTS_DIR = DOCS_DIR / "posts"
PAGE_MAP = {
    "home": DOCS_DIR / "index.md",
    "about": DOCS_DIR / "about.md",
    "publications": DOCS_DIR / "publications.md",
}
READ_MORE_MARKER = "<!-- more -->"
MARKDOWN_EXTENSIONS = [
    "admonition",
    "abbr",
    "attr_list",
    "footnotes",
    "toc",
    "pymdownx.superfences",
    "pymdownx.snippets",
    "pymdownx.tabbed",
    "pymdownx.emoji",
    "pymdownx.blocks.caption",
]


@dataclass
class PageContent:
    title: str
    html: str


@dataclass
class PostContent:
    slug: str
    title: str
    date: date | None
    draft: bool
    summary_html: str
    body_html: str

    @property
    def url(self) -> str:
        return f"/{self.slug}/"


def _split_front_matter(raw: str) -> tuple[dict[str, Any], str]:
    if not raw.startswith("---"):
        return {}, raw

    lines = raw.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, raw

    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            front_matter = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1 :])
            parsed = yaml.safe_load(front_matter) or {}
            if not isinstance(parsed, dict):
                parsed = {}
            return parsed, body

    return {}, raw


def _normalize_markdown_paths(content: str) -> str:
    content = re.sub(r"\]\(\s*(?:\.\./)?assets/", "](/static/assets/", content)
    content = re.sub(r"\]\(\s*/assets/", "](/static/assets/", content)
    content = re.sub(r"\]\(\s*favicon\.png", "](/static/favicon.png", content)
    content = re.sub(r"\]\(\s*index\.md\)", "](/)", content)
    content = re.sub(r"\]\(\s*about\.md\)", "](/about/)", content)
    content = re.sub(r"\]\(\s*publications\.md\)", "](/publications/)", content)
    content = re.sub(
        r"\]\(\s*posts/([a-zA-Z0-9\-]+)\.md\)", r"](/\1/)", content
    )
    return content


def _render_markdown(content: str) -> str:
    cleaned = _normalize_markdown_paths(content)
    return markdown.markdown(
        cleaned,
        extensions=MARKDOWN_EXTENSIONS,
        output_format="html5",
    )


def _title_from_markdown_body(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.removeprefix("# ").strip()
    return "Untitled"


def _parse_date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def _is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def load_page(page_key: str) -> PageContent:
    source_path = PAGE_MAP[page_key]
    raw = source_path.read_text(encoding="utf-8")
    metadata, body = _split_front_matter(raw)

    title = str(metadata.get("title") or _title_from_markdown_body(body))
    html = _render_markdown(body)
    return PageContent(title=title, html=html)


def _load_post(source_path: Path) -> PostContent:
    raw = source_path.read_text(encoding="utf-8")
    metadata, body = _split_front_matter(raw)

    slug = str(metadata.get("slug") or source_path.stem)
    title = str(metadata.get("title") or _title_from_markdown_body(body))
    published_date = _parse_date(metadata.get("date"))
    draft = _is_truthy(metadata.get("draft", False))

    summary_source = body.split(READ_MORE_MARKER, maxsplit=1)[0]
    body_source = body.replace(READ_MORE_MARKER, "")

    return PostContent(
        slug=slug,
        title=title,
        date=published_date,
        draft=draft,
        summary_html=_render_markdown(summary_source),
        body_html=_render_markdown(body_source),
    )


def load_posts(include_drafts: bool = False) -> list[PostContent]:
    posts = [_load_post(path) for path in sorted(POSTS_DIR.glob("*.md"))]

    if not include_drafts:
        posts = [post for post in posts if not post.draft]

    posts.sort(
        key=lambda post: (post.date or date.min, post.title.lower()),
        reverse=True,
    )
    return posts


def get_post(slug: str, include_drafts: bool = False) -> PostContent | None:
    for post in load_posts(include_drafts=include_drafts):
        if post.slug == slug:
            return post
    return None
