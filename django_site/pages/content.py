from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
import html
from math import ceil
from pathlib import Path
import re
from typing import Any

import markdown
import yaml


DOCS_DIR = Path(__file__).resolve().parents[2] / "docs"
POSTS_DIR = DOCS_DIR / "posts"
CV_PATH = DOCS_DIR / "cv.md"
AUTHORS_PATH = DOCS_DIR / ".authors.yml"
SITE_CONFIG_PATH = Path(__file__).resolve().parent / "site_config.yaml"
POSTS_CONFIG_PATH = Path(__file__).resolve().parent / "featured_post.yaml"
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
    post_id: int | None
    slug: str
    title: str
    date: date | None
    draft: bool
    authors: list[str]
    tags: list[str]
    toc_entries: list["PostTocEntry"]
    reading_time_minutes: int
    summary_html: str
    main_body_html: str
    body_html: str
    cover_image_url: str | None

    @property
    def url(self) -> str:
        return f"/{self.slug}/"


@dataclass
class CVEntry:
    period: str
    role: str
    organisation: str
    context: str
    highlights: list[str]


@dataclass
class CVContent:
    title: str
    headline_title: str
    headline_description: str
    experience_title: str
    education_title: str
    skills_title: str
    intro_html: str
    entries: list[CVEntry]
    education_entries: list[CVEntry] = field(default_factory=list)
    key_skills: list[str] = field(default_factory=list)


@dataclass
class PostTocEntry:
    title: str
    anchor: str


@dataclass
class AuthorProfile:
    key: str
    name: str
    description: str
    avatar_url: str | None
    url: str | None


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


def _normalize_asset_url(raw_url: str) -> str:
    url = raw_url.strip()
    if not url:
        return url
    if url.startswith(("http://", "https://", "mailto:")):
        return url
    if url.startswith("../assets/"):
        return f"/static/assets/{url.removeprefix('../assets/')}"
    if url.startswith("assets/"):
        return f"/static/{url}"
    if url.startswith("/assets/"):
        return f"/static{url}"
    if url == "favicon.png":
        return "/static/favicon.png"
    return url


def _normalize_markdown_paths(content: str) -> str:
    content = re.sub(
        r"\]\(\s*([^\)]+)\)",
        lambda match: f"]({_normalize_asset_url(match.group(1))})",
        content,
    )
    content = re.sub(r"\]\(\s*index\.md\)", "](/)", content)
    content = re.sub(r"\]\(\s*about\.md\)", "](/about/)", content)
    content = re.sub(r"\]\(\s*publications\.md\)", "](/publications/)", content)
    content = re.sub(r"\]\(\s*posts/([a-zA-Z0-9\-]+)\.md\)", r"](/\1/)", content)
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


def _parse_post_id(value: Any) -> int | None:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def _is_truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _as_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _extract_toc_entries(body_html: str) -> list[PostTocEntry]:
    entries: list[PostTocEntry] = []
    matches = re.findall(
        r"<h2\s+[^>]*id=[\"']([^\"']+)[\"'][^>]*>(.*?)</h2>",
        body_html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for anchor, title_html in matches:
        title = _html_to_text(title_html)
        if not title:
            continue
        entries.append(PostTocEntry(title=title, anchor=anchor))
    return entries


def _extract_cover_image(metadata: dict[str, Any], body: str) -> str | None:
    image = metadata.get("image")
    if isinstance(image, str) and image.strip():
        return _normalize_asset_url(image)

    meta_items = metadata.get("meta")
    if isinstance(meta_items, list):
        for item in meta_items:
            if isinstance(item, dict) and item.get("property") == "og:image":
                content = item.get("content")
                if isinstance(content, str) and content.strip():
                    return _normalize_asset_url(content)

    image_match = re.search(r"!\[[^\]]*\]\(([^\)]+)\)", body)
    if image_match:
        return _normalize_asset_url(image_match.group(1))

    return None


def _strip_cover_image_from_body(body: str, cover_image_url: str | None) -> str:
    if not cover_image_url:
        return body

    image_pattern = re.compile(
        r"(?m)^\s*!\[[^\]]*\]\(([^\)]+)\)(?:\{[^\}]*\})?\s*$"
    )

    for match in image_pattern.finditer(body):
        raw_url = match.group(1)
        if _normalize_asset_url(raw_url) != cover_image_url:
            continue
        start, end = match.span()
        stripped = f"{body[:start].rstrip()}\n\n{body[end:].lstrip()}"
        return stripped

    return body


def _html_to_text(content: str) -> str:
    content = re.sub(r"<[^>]+>", " ", content)
    content = html.unescape(content)
    return re.sub(r"\s+", " ", content).strip()


def _estimate_reading_time_minutes(*chunks: str) -> int:
    words = 0
    for chunk in chunks:
        plain = _html_to_text(chunk)
        if plain:
            words += len(plain.split())
    if words <= 0:
        return 1
    return max(1, ceil(words / 225))


def load_page(page_key: str) -> PageContent:
    source_path = PAGE_MAP[page_key]
    raw = source_path.read_text(encoding="utf-8")
    metadata, body = _split_front_matter(raw)

    title = str(metadata.get("title") or _title_from_markdown_body(body))
    rendered = _render_markdown(body)
    return PageContent(title=title, html=rendered)


def load_page_excerpt(page_key: str, max_chars: int = 320) -> str:
    page = load_page(page_key)
    plain_text = _html_to_text(page.html)
    if len(plain_text) <= max_chars:
        return plain_text
    clipped = plain_text[: max_chars + 1]
    cutoff = clipped.rfind(" ")
    if cutoff <= 0:
        cutoff = max_chars
    return f"{clipped[:cutoff].rstrip()}..."


def _load_post(source_path: Path) -> PostContent:
    raw = source_path.read_text(encoding="utf-8")
    metadata, body = _split_front_matter(raw)

    slug = str(metadata.get("slug") or source_path.stem)
    title = str(metadata.get("title") or _title_from_markdown_body(body))
    published_date = _parse_date(metadata.get("date"))
    draft = _is_truthy(metadata.get("draft", False))
    authors = _as_string_list(metadata.get("authors"))
    tags = _as_string_list(metadata.get("tags"))
    if not tags:
        tags = _as_string_list(metadata.get("categories"))
    cover_image_url = _extract_cover_image(metadata, body)

    has_read_more = READ_MORE_MARKER in body
    summary_source, remainder = body.split(READ_MORE_MARKER, maxsplit=1) if has_read_more else (body, body)
    summary_source = _strip_cover_image_from_body(summary_source, cover_image_url)
    main_body_source = _strip_cover_image_from_body(remainder, cover_image_url)

    summary_html = _render_markdown(summary_source)
    main_body_html = _render_markdown(main_body_source)
    body_source = _strip_cover_image_from_body(body.replace(READ_MORE_MARKER, ""), cover_image_url)
    body_html = _render_markdown(body_source)

    return PostContent(
        post_id=_parse_post_id(metadata.get("id")),
        slug=slug,
        title=title,
        date=published_date,
        draft=draft,
        authors=authors,
        tags=tags,
        toc_entries=_extract_toc_entries(main_body_html),
        reading_time_minutes=_estimate_reading_time_minutes(summary_html, main_body_html),
        summary_html=summary_html,
        main_body_html=main_body_html,
        body_html=body_html,
        cover_image_url=cover_image_url,
    )


def load_authors_index() -> dict[str, AuthorProfile]:
    if not AUTHORS_PATH.exists():
        return {}

    raw = AUTHORS_PATH.read_text(encoding="utf-8")
    parsed = yaml.safe_load(raw) or {}
    if not isinstance(parsed, dict):
        return {}

    authors_map = parsed.get("authors")
    if not isinstance(authors_map, dict):
        return {}

    index: dict[str, AuthorProfile] = {}
    for key, value in authors_map.items():
        if not isinstance(value, dict):
            continue
        author_key = str(key).strip()
        if not author_key:
            continue
        name = str(value.get("name", "")).strip() or author_key
        description = str(value.get("description", "")).strip()
        raw_avatar = str(value.get("avatar", "")).strip()
        avatar_url = _normalize_asset_url(raw_avatar) if raw_avatar else None
        raw_url = str(value.get("url", "")).strip()
        url = raw_url or None
        index[author_key] = AuthorProfile(
            key=author_key,
            name=name,
            description=description,
            avatar_url=avatar_url,
            url=url,
        )
    return index


def _parse_cv_entry(entry: Any) -> CVEntry | None:
    if not isinstance(entry, dict):
        return None

    period = str(entry.get("period", "")).strip()
    role = str(entry.get("role", "")).strip()
    organisation = str(entry.get("organisation", "")).strip()
    context = str(entry.get("context", "")).strip()
    highlights_raw = entry.get("highlights", [])
    highlights: list[str] = []
    if isinstance(highlights_raw, list):
        highlights = [str(item).strip() for item in highlights_raw if str(item).strip()]

    if not (period and role):
        return None

    return CVEntry(
        period=period,
        role=role,
        organisation=organisation,
        context=context,
        highlights=highlights,
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


def load_site_config() -> dict[str, Any]:
    if not SITE_CONFIG_PATH.exists():
        return {}

    raw = SITE_CONFIG_PATH.read_text(encoding="utf-8")
    parsed = yaml.safe_load(raw) or {}
    if isinstance(parsed, dict):
        return parsed
    return {}


def load_posts_config() -> dict[str, Any]:
    if not POSTS_CONFIG_PATH.exists():
        return {}

    raw = POSTS_CONFIG_PATH.read_text(encoding="utf-8")
    parsed = yaml.safe_load(raw) or {}
    if isinstance(parsed, dict):
        return parsed
    return {}


def load_cv() -> CVContent:
    if not CV_PATH.exists():
        return CVContent(
            title="Curriculum Vitae",
            headline_title="Curriculum Vitae",
            headline_description="",
            experience_title="Experience",
            education_title="Education",
            skills_title="Skills",
            intro_html="",
            entries=[],
            education_entries=[],
            key_skills=[],
        )

    raw = CV_PATH.read_text(encoding="utf-8")
    metadata, body = _split_front_matter(raw)

    title = str(metadata.get("title") or "Curriculum Vitae").strip()
    headline_title = str(metadata.get("headline_title") or title).strip()
    headline_description = str(metadata.get("headline_description") or "").strip()
    experience_title = str(metadata.get("experience_title") or "Experience").strip()
    education_title = str(metadata.get("education_title") or "Education").strip()
    skills_title = str(metadata.get("skills_title") or "Skills").strip()

    experience_entries_raw = metadata.get("experience_entries")
    if not isinstance(experience_entries_raw, list):
        experience_entries_raw = metadata.get("entries", [])
    entries: list[CVEntry] = []
    if isinstance(experience_entries_raw, list):
        for entry in experience_entries_raw:
            parsed = _parse_cv_entry(entry)
            if parsed is not None:
                entries.append(parsed)

    education_entries_raw = metadata.get("education_entries", [])
    education_entries: list[CVEntry] = []
    if isinstance(education_entries_raw, list):
        for entry in education_entries_raw:
            parsed = _parse_cv_entry(entry)
            if parsed is not None:
                education_entries.append(parsed)

    key_skills_raw = metadata.get("key_skills", [])
    key_skills: list[str] = []
    if isinstance(key_skills_raw, list):
        key_skills = [str(skill).strip() for skill in key_skills_raw if str(skill).strip()]

    intro_html = _render_markdown(body.strip()) if body.strip() else ""

    return CVContent(
        title=title,
        headline_title=headline_title,
        headline_description=headline_description,
        experience_title=experience_title,
        education_title=education_title,
        skills_title=skills_title,
        intro_html=intro_html,
        entries=entries,
        education_entries=education_entries,
        key_skills=key_skills,
    )
