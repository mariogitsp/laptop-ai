import os
import re
from datetime import datetime


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def save_post_as_markdown(post: dict, base_dir="knowledge/reddit"):
    os.makedirs(base_dir, exist_ok=True)

    slug = slugify(post["title"])
    filename = f"{slug}.md"
    filepath = os.path.join(base_dir, filename)

    markdown = f"""---
source: reddit
url: {post['url']}
scraped_at: {post['scraped_at']}
---

# {post['title']}

{post['body']}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Saved Markdown: {filepath}")
    return filepath


def main() -> None:
    save_post_as_markdown({
        "url": "https://www.reddit.com/r/LenovoLegion/comments/1o7tk8q/my_legion_y540_still_serving_me_after_5_years/",
        "title": "My legion Y540 still serving me after 5 years",
        "body": "Bought this in 2020 during lockdown and have been using it since then, learnt music production on it, blender, unity, programming, video editing. Now I am in my first year college and it's still working smooth as butter, prob because I do take care of it, regularly clearing the SSD, just got it cleaned added new thermal paste and upgraded ram from 8gb to 24gb. Absolutely love this.",
        "scraped_at": "2026-01-26 18:48:19"
    })
    

if __name__ == "__main__":
    main()