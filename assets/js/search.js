const stems = new Map(Object.entries({policies:'policy', universities:'university', incidents:'incident', failures:'failure', agents:'agent', systems:'system', frameworks:'framework', explainable:'explainability', xai:'explainability'}));
export function normalize(value) {
  return String(value).normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, ' ').trim().split(/\s+/)
    .map((word) => stems.get(word) || word).join(' ');
}
export function searchIndex(index, query, area = '', includeArchived = true) {
  const q = normalize(query);
  if (!q) return [];
  const terms = [...new Set(q.split(' '))];
  const matches = [];
  for (const entry of index) {
    const locations = (entry.locations || [entry]).filter((location) =>
      (!area || location.area === area) && (includeArchived || !location.archived));
    if (!locations.length) continue;
    const title = normalize(entry.title);
    const summary = normalize(entry.summary || '');
    const context = normalize(locations.map((location) => [location.section, location.subsection].filter(Boolean).join(' ')).join(' '));
    const haystack = title + ' ' + summary + ' ' + context;
    const words = new Set(haystack.split(' '));
    if (!terms.every((term) => words.has(term))) continue;
    let score = title.includes(q) ? 60 : 0;
    score += terms.reduce((n, term) => n + (title.split(' ').includes(term) ? 12 : 0) + (summary.split(' ').includes(term) ? 4 : 0), 0);
    if (entry.kind === 'page') score += 2;
    matches.push({...entry, ...locations[0], score});
  }
  matches.sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));
  const seen = new Set();
  return matches.filter((entry) => {
    const key = entry.resource_url?.replace(/\/$/, '') || entry.url;
    if (seen.has(key)) return false;
    seen.add(key); return true;
  });
}
async function initializeSearch() {
  const input = document.querySelector('#q');
  if (!input) return;
  const form = document.querySelector('#search-form');
  const area = document.querySelector('#area');
  const archived = document.querySelector('#include-archived');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#results');
  const more = document.querySelector('#more-results');
  const retry = document.querySelector('#retry-search');
  let index = null, matches = [], limit = 30, timer;
  const parameters = new URLSearchParams(location.search);
  input.value = parameters.get('q') || '';
  if ([...area.options].some((option) => option.value === parameters.get('area'))) area.value = parameters.get('area');
  archived.checked = parameters.get('include_archived') !== '0';
  function link(label, href) {
    const anchor = document.createElement('a'); anchor.textContent = label;
    const url = new URL(href, location.href);
    if (!['https:', 'http:'].includes(url.protocol)) throw new Error('Invalid result URL');
    anchor.href = url.href; return anchor;
  }
  function render() {
    results.replaceChildren();
    const shown = matches.slice(0, limit);
    status.textContent = matches.length ? `${matches.length.toLocaleString()} result${matches.length === 1 ? "" : "s"}. Showing ${shown.length.toLocaleString()}.` : 'No results. Try fewer terms or another Library area.';
    for (const entry of shown) {
      const article = document.createElement('article'); article.className = 'result';
      const h = document.createElement('h2'); h.append(link(entry.title, entry.url)); article.append(h);
      const context = document.createElement('p'); context.className = 'result-context';
      context.textContent = [entry.section, entry.subsection !== entry.section ? entry.subsection : '', entry.archived ? 'Archived' : ''].filter(Boolean).join(' · '); article.append(context);
      if (entry.summary) { const snippet = document.createElement('p'); snippet.textContent = entry.summary; article.append(snippet); }
      if (entry.resource_url) {
        const p = document.createElement('p'); const original = link('Open resource', entry.resource_url);
        original.setAttribute('aria-label', `Open ${entry.title} at its original source`); p.append(original); article.append(p);
      }
      results.append(article);
    }
    more.hidden = matches.length <= limit;
  }
  function run(updateHistory = true) {
    if (!index) return;
    const q = input.value.trim();
    if (updateHistory) {
      const params = new URLSearchParams();
      if (q) params.set('q', q);
      if (area.value) params.set('area', area.value);
      if (!archived.checked) params.set('include_archived', '0');
      history.replaceState(null, '', location.pathname + (params.size ? '?' + params : ''));
    }
    limit = 30; more.hidden = true;
    if (!q) { results.replaceChildren(); status.textContent = 'Enter search terms to find resources, guide summaries, and project documentation.'; return; }
    matches = searchIndex(index, q, area.value, archived.checked); render();
  }
  async function load() {
    index = null; retry.hidden = true; more.hidden = true;
    status.textContent = 'Loading search…'; results.replaceChildren();
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try {
      const response = await fetch(new URL('../data/search-index.json', import.meta.url), {signal:controller.signal});
      if (!response.ok) throw new Error('Could not fetch search index');
      const data = await response.json();
      if (!Array.isArray(data) || !data.length) throw new Error('Invalid search index');
      index = data; run(false);
    } catch {
      status.textContent = 'Search could not load. Retry, or browse the Library using the navigation above.';
      retry.hidden = false;
    } finally { clearTimeout(timeout); }
  }
  form.addEventListener('submit', (event) => { event.preventDefault(); clearTimeout(timer); run(); });
  input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(run, 140); });
  area.addEventListener('change', () => run()); archived.addEventListener('change', () => run());
  more.addEventListener('click', () => { limit += 30; render(); });
  retry.addEventListener('click', load);
  await load();
}
if (typeof document !== 'undefined') initializeSearch();
