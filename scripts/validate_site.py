#!/usr/bin/env python3
"""Offline guardrails for the public OAuth disclosure site. Never reads secrets."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re

ROOT = Path(__file__).resolve().parents[1]
HTML = ("index.html", "privacy.html", "terms.html")
LOCAL = set(HTML) | {"style.css"}
EXPECTED_DOMAIN = "drive-oauth.3xmr.com"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = False
        self.titles: list[str] = []
        self.links: list[str] = []
        self.h1 = 0
        self.forms = 0
        self.scripts = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.title = True
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"])
        elif tag == "link" and values.get("href"):
            self.links.append(values["href"])
        elif tag == "h1":
            self.h1 += 1
        elif tag == "form":
            self.forms += 1
        elif tag == "script":
            self.scripts += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title = False

    def handle_data(self, data: str) -> None:
        if self.title:
            self.titles.append(data)


def check() -> None:
    for filename in HTML:
        text = (ROOT / filename).read_text(encoding="utf-8")
        p = PageParser()
        p.feed(text)
        assert p.h1 == 1, f"{filename}: expected exactly one heading"
        assert p.titles and "".join(p.titles).strip(), f"{filename}: missing title"
        assert p.forms == 0 and p.scripts == 0, f"{filename}: no forms/scripts allowed"
        assert 'href="./privacy.html"' in text, f"{filename}: privacy must be linked"
        assert 'href="./terms.html"' in text, f"{filename}: terms must be linked"
        for href in p.links:
            u = urlparse(href)
            if u.scheme in ("https", "mailto"):
                if u.scheme == "https":
                    assert u.netloc, f"{filename}: malformed external URL"
                continue
            assert not u.scheme and not u.netloc, f"{filename}: unexpected URL scheme"
            if u.path in ("", ".", "./", "/"):
                continue
            path = (ROOT / u.path).resolve()
            assert path.is_relative_to(ROOT), f"{filename}: path escaped site root"
            assert path.name in LOCAL and path.is_file(), f"{filename}: missing target {href}"
        assert not re.search(r"GOCSPX-|AIza[0-9A-Za-z_-]{12,}|ya29\.", text), (
            f"{filename}: possible pasted OAuth or API credential"
        )
        print(f"PASS {filename}: title / links / static-only / no obvious credentials")
    cname = (ROOT / "CNAME").read_text().strip()
    assert cname == EXPECTED_DOMAIN
    print(f"PASS CNAME: {cname}")


if __name__ == "__main__":
    check()
