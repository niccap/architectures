(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const button = document.querySelector('.menu-button');
  const sidebar = document.getElementById('sidebar');
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') !== 'true';
    button.setAttribute('aria-expanded', String(open));
    sidebar.classList.toggle('is-open', open);
  });
  document.querySelector('.print-button').addEventListener('click', () => window.print());
  const input = document.getElementById('site-search');
  const results = document.getElementById('search-results');
  const status = results.querySelector('.search-status');
  const list = results.querySelector('ul');
  const pages = JSON.parse(document.getElementById('search-data').textContent);
  const normalize = value => value.toLocaleLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const indexed = pages.map(page => ({...page, haystack: normalize(`${page.title} ${page.description} ${page.text}`)}));
  input.addEventListener('input', () => {
    const query = normalize(input.value.trim());
    list.replaceChildren();
    if (query.length < 2) { results.hidden = true; return; }
    const terms = query.split(/\s+/);
    const matches = indexed.filter(page => terms.every(term => page.haystack.includes(term)))
      .sort((a, b) => Number(normalize(b.title).includes(query)) - Number(normalize(a.title).includes(query)));
    results.hidden = false;
    status.textContent = matches.length ? `${matches.length} ${matches.length === 1 ? 'page' : 'pages'} found` : 'No results. Try a different search term.';
    for (const page of matches) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = page.url;
      const group = document.createElement('small');
      group.textContent = page.group;
      const title = document.createElement('strong');
      title.textContent = page.title;
      const description = document.createElement('p');
      description.textContent = page.description;
      a.append(group, title, description);
      li.append(a);
      list.append(li);
    }
  });
  input.addEventListener('focus', () => { if (input.value.trim().length >= 2) results.hidden = false; });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') { results.hidden = true; input.blur(); }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.search-area')) results.hidden = true;
  });
})();
