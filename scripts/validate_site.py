#!/usr/bin/env python3
"""Dependency-free structural checks for the static portfolio."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.references: list[str] = []
        self.html_lang: str | None = None
        self.blank_links: list[dict[str, str]] = []
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if tag == "html":
            self.html_lang = values.get("lang")
        if element_id := values.get("id"):
            self.ids.add(element_id)
        for attribute in ("href", "src"):
            if reference := values.get(attribute):
                self.references.append(reference)
        if tag == "a" and values.get("target") == "_blank":
            self.blank_links.append(values)
        if tag == "meta":
            key = values.get("property") or values.get("name")
            if key:
                self.meta[key] = values.get("content", "")


def parse_html(path: Path) -> Document:
    document = Document()
    document.feed(path.read_text())
    if document.html_lang != "en":
        raise AssertionError(f"{path.name} must declare html lang=en")
    return document


def check_references(document: Document) -> None:
    for reference in document.references:
        if reference.startswith(("https://", "mailto:", "tel:")):
            continue
        if reference.startswith("http://"):
            raise AssertionError(f"insecure external reference: {reference}")
        path_part, _, fragment = reference.partition("#")
        if fragment and fragment not in document.ids:
            raise AssertionError(f"missing fragment target: #{fragment}")
        if path_part and not (ROOT / path_part.lstrip("/")).exists():
            raise AssertionError(f"missing local reference: {path_part}")
    for link in document.blank_links:
        rel = set(link.get("rel", "").split())
        if not {"noreferrer", "noopener"} & rel:
            raise AssertionError(f"target=_blank link lacks rel protection: {link.get('href')}")


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


def main() -> None:
    index = parse_html(ROOT / "index.html")
    not_found = parse_html(ROOT / "404.html")
    check_references(index)
    check_references(not_found)

    expected_meta = {
        "og:image": "https://itstofi.github.io/assets/social-preview.png",
        "og:image:width": "1200",
        "og:image:height": "630",
        "twitter:card": "summary_large_image",
    }
    for key, expected in expected_meta.items():
        if index.meta.get(key) != expected:
            raise AssertionError(f"unexpected {key}: {index.meta.get(key)!r}")

    if png_dimensions(ROOT / "assets/social-preview.png") != (1200, 630):
        raise AssertionError("social preview must be 1200x630")

    ET.parse(ROOT / "sitemap.xml")
    ET.parse(ROOT / "assets/favicon.svg")
    if "https://itstofi.github.io/sitemap.xml" not in (ROOT / "robots.txt").read_text():
        raise AssertionError("robots.txt must reference the production sitemap")

    print("Static-site structure, references, metadata, and XML are valid.")


if __name__ == "__main__":
    main()
