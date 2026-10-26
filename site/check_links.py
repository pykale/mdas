"""Check generated HTML links, anchors and local assets without network requests."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

HTML = Path(__file__).resolve().parent / "_build/html"


class Page(HTMLParser):
    def __init__(self, path: Path):
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append(attrs[name])


def main() -> int:
    pages = {path.resolve(): Page(path) for path in HTML.rglob("*.html")
             if not any(part.startswith("_") for part in path.relative_to(HTML).parts)}
    if not pages:
        raise SystemExit("No generated HTML found; run python site/build.py first.")
    errors = []
    count = 0
    for path, page in pages.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            count += 1
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{path.relative_to(HTML)}: missing {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(HTML)}: missing anchor {link}")
    for error in errors:
        print(error)
    print(f"Checked {len(pages)} HTML pages and {count} local links/assets; {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
