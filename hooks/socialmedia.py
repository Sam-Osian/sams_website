from textwrap import dedent
import urllib.parse
import re

x_intent = "https://x.com/intent/tweet"
fb_sharer = "https://www.facebook.com/sharer/sharer.php"
# Blog posts are published at paths like YYYY/MM/DD/slug/
# Match those to add share buttons
include = re.compile(r"\d{4}/\d{2}/\d{2}/.*")

def on_page_markdown(markdown, **kwargs):
    page = kwargs['page']
    config = kwargs['config']
    if not include.match(page.url):
        return markdown

    page_url = config.site_url+page.url
    page_title = urllib.parse.quote(page.title+'\n')

    return markdown + dedent(f"""
    [Share on :simple-x:]({x_intent}?text={page_title}&url={page_url}){{ .md-button }}
    [Share on :simple-facebook:]({fb_sharer}?u={page_url}){{ .md-button }}
    """)
