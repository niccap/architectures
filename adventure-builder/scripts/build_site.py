#!/usr/bin/env python3
"""Build the offline documentation with Python's standard library only."""
import html
import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT / 'content/pages.json').read_text())


class Outline(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.current = [dict(attrs).get('id'), '']

    def handle_data(self, data):
        if self.current is not None:
            self.current[1] += data

    def handle_endtag(self, tag):
        if tag == 'h2' and self.current is not None:
            if self.current[0]:
                self.items.append(self.current)
            self.current = None


def escape(text):
    return html.escape(text, quote=True)


def relative(target, current):
    return os.path.relpath(target, Path(current).parent).replace(os.sep, '/')


def link(page, current):
    active = ' aria-current="page"' if page['path'] == current else ''
    return f'<a href="{escape(relative(page["path"], current))}"{active}>{escape(page["title"])}</a>'


def build():
    groups = {}
    home = next(p for p in PAGES if p['path'] == 'index.html')
    # Navigation follows the conceptual order, independent of directory depth.
    for name in ['Introduction', 'Views · Modules', 'Views · Runtime', 'Views · Allocation',
                 'Interfaces', 'Mappings & requirements', 'References', 'Templates']:
        groups[name] = [p for p in PAGES if p['group'] == name]
    for page in PAGES:
        current = page['path']
        body = (ROOT / 'content' / current).read_text()
        outline = Outline()
        outline.feed(body)
        toc = ''.join(f'<a href="#{escape(anchor)}">{escape(title)}</a>' for anchor, title in outline.items)
        nav = ''.join(f'<section class="nav-group"><h2>{escape(name)}</h2>'
                      + ''.join(link(p, current) for p in group) + '</section>'
                      for name, group in groups.items())
        download = ''
        if page['group'] == 'Templates':
            name = Path(current).stem
            href = relative(f'assets/downloads/{name}.md', current)
            download = f'<p class="page-tools"><a class="button" href="{escape(href)}" download>Download the Markdown template</a></p>'
        original = ''
        if page.get('source_id'):
            original = f'<span>Source: SEI · page {escape(page["source_id"])}</span>'
        # Search data is embedded in each page: works on file:// without fetching.
        search_data = []
        for item in PAGES:
            source = (ROOT / 'content' / item['path']).read_text()
            text = re.sub('<[^>]+>', ' ', source)
            text = html.unescape(re.sub(r'\s+', ' ', text))
            search_data.append({'title': item['title'], 'group': item['group'],
                                'url': relative(item['path'], current),
                                'description': item['description'], 'text': text})
        payload = json.dumps(search_data, ensure_ascii=False).replace('<', '\\u003c')
        css = relative('assets/css/site.css', current)
        js = relative('assets/js/site.js', current)
        icon = relative('assets/favicon.svg', current)
        home_url = relative('index.html', current)
        document = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(page['title'])} · Adventure Builder</title>
  <meta name="description" content="{escape(page['description'])}">
  <meta name="color-scheme" content="light">
  <link rel="icon" type="image/svg+xml" href="{icon}">
  <link rel="stylesheet" href="{css}">
  <script src="{js}" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="topbar">
  <a class="brand" href="{home_url}"><span class="brand-mark" aria-hidden="true">AB</span><span>Adventure Builder<small>Architecture documentation</small></span></a>
  <span class="edition">Views and Beyond · 2nd edition</span>
  <button class="menu-button" aria-expanded="false" aria-controls="sidebar">Contents</button>
</header>
<div class="layout">
<aside id="sidebar" class="sidebar" aria-label="Documentation contents">
  <nav aria-label="Main navigation"><div class="home-link">{link(home, current)}</div>{nav}</nav>
</aside>
<div class="workspace">
  <div class="search-area">
    <label for="site-search">Search documentation</label>
    <input id="site-search" type="search" placeholder="Services, components, requirements…" autocomplete="off" aria-controls="search-results">
    <div id="search-results" class="search-results" hidden><p class="search-status" role="status"></p><ul></ul></div>
    <noscript>Search requires JavaScript. All pages are accessible from the contents.</noscript>
  </div>
  <div class="reading-layout">
    <main id="main" tabindex="-1">
      <div class="breadcrumb"><a href="{home_url}">Documentation</a><span>/</span><span>{escape(page['group'])}</span></div>
      <div class="page-heading"><p class="eyebrow">{escape(page['group'])}</p><h1>{escape(page['title'])}</h1><p class="description">{escape(page['description'])}</p>{download}</div>
      <article class="document" lang="en">{body}</article>
      <footer class="page-footer"><span>Adventure Builder · Software Architecture Document</span>{original}<a href="#main">Back to top</a></footer>
    </main>
    <aside class="page-outline" aria-label="On this page"><p>On this page</p><nav>{toc}</nav><button class="print-button" type="button">Print this page</button></aside>
  </div>
</div>
</div>
<script id="search-data" type="application/json">{payload}</script>
</body>
</html>
'''
        target = ROOT / current
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(document)
    print(f'Generated {len(PAGES)} static pages.')


if __name__ == '__main__':
    build()
