#!/usr/bin/env python3
"""Check all generated links, fragments, assets and offline dependencies."""
import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.refs = []
        self.errors = []
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.h1 += 1
        for attr in ['href', 'src']:
            if attrs.get(attr):
                self.refs.append((tag, attr, attrs[attr]))
        if tag == 'img' and not attrs.get('alt'):
            self.errors.append('Image without alternative text')
        if tag in ['iframe', 'form'] or any(k.startswith('on') for k in attrs):
            self.errors.append(f'Unexpected runtime markup: {tag}')


def validate():
    pages = json.loads((ROOT / 'content/pages.json').read_text())
    documents = {}
    errors = []
    for page in pages:
        path = ROOT / page['path']
        if not path.is_file():
            errors.append(f'Missing page: {page["path"]}')
            continue
        doc = Document()
        doc.feed(path.read_text())
        documents[path.resolve()] = doc
        errors += [f'{page["path"]}: {error}' for error in doc.errors]
        if doc.h1 != 1:
            errors.append(f'{page["path"]}: expected one H1, found {doc.h1}')
        for anchor, count in Counter(doc.ids).items():
            if count > 1:
                errors.append(f'{page["path"]}: duplicate ID {anchor}')
    links = 0
    for path, doc in documents.items():
        for tag, attr, ref in doc.refs:
            links += 1
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                if attr == 'src' or tag == 'link':
                    errors.append(f'{path.relative_to(ROOT)}: external runtime dependency {ref}')
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append(f'{path.relative_to(ROOT)}: missing target {ref}')
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                errors.append(f'{path.relative_to(ROOT)}: missing fragment {ref}')
    legacy = ['files', 'wget.sh']
    for name in legacy:
        if (ROOT / name).exists():
            errors.append(f'Original download still present: {name}')
    # Source fragments should contain no Confluence chrome or Pet Store content.
    for page in pages:
        fragment = (ROOT / 'content' / page['path']).read_text()
        for forbidden in ['Pet Store', 'Petstore', 'PetStore', 'viewpage.action', 'livesearch', 'atlassian-token']:
            if forbidden in fragment:
                errors.append(f'{page["path"]}: legacy content {forbidden}')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK: {len(documents)} pages; {links} links/resources; no broken local links, duplicate IDs or external runtime dependencies.')
    return 0


if __name__ == '__main__':
    sys.exit(validate())
