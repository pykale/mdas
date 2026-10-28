"""Check generated HTML links, anchors and local assets without network requests."""

import argparse
from html.parser import HTMLParser
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit, urljoin

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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://pykale.github.io/mdas/",
                        help="Published directory URL used to check project-prefix resolution")
    base = urlsplit(parser.parse_args().base_url)
    prefix = base.path.rstrip("/") + "/"
    base_url = base._replace(path=prefix, query="", fragment="").geturl()
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
            published_page = urljoin(base_url, path.relative_to(HTML).as_posix())
            resolved = urlsplit(urljoin(published_page, link))
            if not resolved.path.startswith(prefix):
                errors.append(f"{path.relative_to(HTML)}: link escapes project prefix: {link}")
                continue
            target = (HTML / unquote(resolved.path[len(prefix):])).resolve()
            if not target.is_relative_to(HTML):
                errors.append(f"{path.relative_to(HTML)}: link escapes output directory: {link}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{path.relative_to(HTML)}: missing {link}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f"{path.relative_to(HTML)}: missing anchor {link}")
    # CSS font/image URLs are not represented by HTML href/src attributes.
    for css in HTML.rglob("*.css"):
        for link in re.findall(r"url\(\s*['\"]?([^)'\"\s]+)", css.read_text(encoding="utf-8")):
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            count += 1
            resolved = urlsplit(urljoin(urljoin(base_url, css.relative_to(HTML).as_posix()), link))
            if not resolved.path.startswith(prefix):
                errors.append(f"{css.relative_to(HTML)}: CSS URL escapes project prefix: {link}")
            elif not (HTML / unquote(resolved.path[len(prefix):])).is_file():
                errors.append(f"{css.relative_to(HTML)}: missing CSS asset {link}")
    for required in (".nojekyll", "search.html", "searchindex.js", "_static/searchtools.js",
                     "_static/mdas-logo.png", "_static/mdas.css",
                     "_static/mdas-interactive.js", "_static/mdas-interactive.css"):
        if not (HTML / required).is_file():
            errors.append(f"Missing expected site artifact: {required}")
    print(f"Checked deployment prefix: {base_url}")
    for error in errors:
        print(error)
    print(f"Checked {len(pages)} HTML pages and {count} local links/assets; {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
