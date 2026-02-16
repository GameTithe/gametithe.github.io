import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from markdownify import markdownify as md
from tqdm import tqdm

BLOG_URL = "https://tithingbygame.tistory.com"
START_ID = 31
END_ID = 400  # first test range
DELAY_SEC = 0.6

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"
IMG_ROOT = ROOT / "assets" / "images" / "posts"
FAILED_LOG = ROOT / "failed_posts.txt"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/132.0.0.0 Safari/537.36"
    )
}


def pick_one(soup, selectors):
    for selector in selectors:
        el = soup.select_one(selector)
        if el:
            return el
    return None


def clean_text(text):
    return re.sub(r"\s+", " ", (text or "").strip())


def slugify(text, fallback):
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s if s else fallback


def parse_date(text, default_year=2023):
    if not text:
        return f"{default_year:04d}-01-01"
    try:
        return date_parser.parse(text, fuzzy=True).strftime("%Y-%m-%d")
    except Exception:
        m = re.search(r"(\d{4})[.\-/\s]+(\d{1,2})[.\-/\s]+(\d{1,2})", text)
        if m:
            year, month, day = m.groups()
            return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
        return f"{default_year:04d}-01-01"


def esc_yaml(text):
    if text is None:
        return ""
    return str(text).replace('"', '\\"')


def ensure_dirs():
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    IMG_ROOT.mkdir(parents=True, exist_ok=True)


def get_post_html(post_id):
    url = f"{BLOG_URL}/{post_id}"
    response = requests.get(url, headers=HEADERS, timeout=20)
    return response, url


def extract_post(soup, post_id):
    title_el = pick_one(
        soup,
        [
            ".article-header .title-article",
            "h1.tit_blogview",
            "h1",
            "meta[property='og:title']",
        ],
    )
    if title_el and title_el.name == "meta":
        title = clean_text(title_el.get("content", ""))
    else:
        title = clean_text(title_el.get_text() if title_el else f"tistory-post-{post_id}")

    date_el = pick_one(
        soup,
        [
            ".article-header .date",
            ".info_post .txt_date",
            "meta[property='article:published_time']",
            "time",
        ],
    )
    if date_el and date_el.name == "meta":
        raw_date = date_el.get("content", "")
    else:
        raw_date = clean_text(date_el.get_text() if date_el else "")
    date_str = parse_date(raw_date)

    category_el = pick_one(
        soup,
        [
            ".article-header .category a",
            ".info_post .link_cate",
            ".category a",
        ],
    )
    category = clean_text(category_el.get_text()) if category_el else "Tistory"

    tag_els = soup.select(".article-tag a, .tag_trial a, a[rel='tag']")
    tags = []
    for tag in tag_els:
        txt = clean_text(tag.get_text())
        if txt and txt not in tags:
            tags.append(txt)

    content_el = pick_one(
        soup,
        [
            ".article-view .contents_style",
            ".tt_article_useless_p_margin",
            ".entry-content",
            ".article_view",
            "#article-view",
        ],
    )
    if not content_el:
        return None

    for bad in content_el.select("script, style, iframe[src*='ads'], .revenue_unit_wrap"):
        bad.decompose()

    return {
        "title": title,
        "date": date_str,
        "category": category,
        "tags": tags,
        "content_el": content_el,
    }


def download_images_and_replace(content_el, post_key):
    post_img_dir = IMG_ROOT / post_key
    post_img_dir.mkdir(parents=True, exist_ok=True)

    replace_map = {}
    idx = 1
    for img in content_el.select("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            continue
        if src.startswith("//"):
            src = "https:" + src
        if src.startswith("/"):
            src = urljoin(BLOG_URL, src)

        try:
            response = requests.get(src, headers=HEADERS, timeout=20)
            if response.status_code != 200:
                continue

            ext = os.path.splitext(urlparse(src).path)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"]:
                ext = ".png"
            filename = f"img-{idx}{ext}"
            save_path = post_img_dir / filename
            with open(save_path, "wb") as f:
                f.write(response.content)

            replace_map[src] = f"/assets/images/posts/{post_key}/{filename}"
            idx += 1
        except Exception:
            continue

    html_str = str(content_el)
    for old, new in replace_map.items():
        html_str = html_str.replace(old, new)
    return html_str


def make_front_matter(title, date_str, category, tags):
    lines = [
        "---",
        f'title: "{esc_yaml(title)}"',
        f"date: {date_str}",
        "toc: true",
        "categories:",
        f'  - "{esc_yaml(category)}"',
        "tags:",
    ]
    if tags:
        for tag in tags:
            lines.append(f'  - "{esc_yaml(tag)}"')
    else:
        lines.append('  - "tistory"')
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def run():
    ensure_dirs()
    failed = []

    for post_id in tqdm(range(START_ID, END_ID + 1), desc="Migrating"):
        try:
            response, url = get_post_html(post_id)
            if response.status_code == 404:
                continue
            if response.status_code != 200:
                failed.append(f"{post_id}\tHTTP {response.status_code}\t{url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            post = extract_post(soup, post_id)
            if not post:
                failed.append(f"{post_id}\tNO_CONTENT\t{url}")
                continue

            fallback = f"tistory-post-{post_id}"
            slug = slugify(post["title"], fallback)
            html_with_local_img = download_images_and_replace(post["content_el"], slug)
            body_md = md(html_with_local_img, heading_style="ATX")
            front_matter = make_front_matter(
                post["title"], post["date"], post["category"], post["tags"]
            )

            filename = f"{post['date']}-{slug}.md"
            out_path = POSTS_DIR / filename
            if out_path.exists():
                filename = f"{post['date']}-{slug}-{post_id}.md"
                out_path = POSTS_DIR / filename

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(front_matter + body_md)

            time.sleep(DELAY_SEC)
        except Exception as e:
            failed.append(f"{post_id}\tEXCEPTION\t{e}")

    with open(FAILED_LOG, "w", encoding="utf-8") as f:
        for line in failed:
            f.write(line + "\n")

    print(f"Done. failed={len(failed)}")
    print(f"Check: {FAILED_LOG}")


if __name__ == "__main__":
    run()
