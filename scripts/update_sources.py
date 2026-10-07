#!/usr/bin/env python3
"""Refresh public, commit-pinned HallResearch.ai source snapshots (stdlib only)."""
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'content' / 'upstream'
REQUIRED = ['.github', 'ai_governance_policy_resources',
            'ai_assessment_implementation_resources', 'ai_research_guides',
            'basic-ml-security', 'basic-xai-example',
            'basic-model-testing-red-teaming-user-testing-example',
            'basic-explainable-ml-bias-management-example', 'basic-ml-eval-example',
            'ai-rmf-rag-prototype', 'example-system-card', 'bib-lib']
OPTIONAL = ['basic-chatbot-guidance', 'tabred']

def get(url):
    request = urllib.request.Request(url, headers={
        'User-Agent': 'HallResearch-Library-Snapshot',
        'Accept': 'application/vnd.github+json' if 'api.github.com' in url else '*/*'})
    with urllib.request.urlopen(request, timeout=40) as response:
        return response.read()

def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def fetch_repo(repo, destination):
    name, branch = repo['name'], repo['default_branch']
    commit = json.loads(get(f'https://api.github.com/repos/hallresearch-ai/{name}/commits/{branch}'))
    sha = commit['sha']
    tree = json.loads(get(f'https://api.github.com/repos/hallresearch-ai/{name}/git/trees/{sha}?recursive=1'))
    if tree.get('truncated'):
        raise RuntimeError(f'Incomplete tree for {name}')
    folder = destination / name
    folder.mkdir(parents=True, exist_ok=True)
    info = {k: repo.get(k) for k in ('name', 'html_url', 'description', 'default_branch',
            'archived', 'license', 'homepage', 'pushed_at')}
    info.update(commit=sha, commit_date=commit['commit']['committer']['date'])
    save_json(folder / 'repository.json', info)
    save_json(folder / 'tree.json', tree)
    files, notebook_data, bibliography_data = [], [], []
    for item in tree['tree']:
        if item['type'] != 'blob':
            continue
        path = item['path']
        basename = Path(path).name.upper()
        is_text = path.lower().endswith('.md') or basename.startswith(('LICENSE', 'COPYING')) or basename.endswith('_LICENSE')
        is_notebook = path.endswith('.ipynb') and name != 'tabred'
        is_bib = path.endswith('.bib')
        if not (is_text or is_notebook or is_bib):
            continue
        url = f'https://raw.githubusercontent.com/hallresearch-ai/{name}/{sha}/' + urllib.parse.quote(path, safe='/')
        raw = get(url)
        if is_text:
            target = folder / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
            files.append({'path': path, 'source_url': url, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
        elif is_notebook:
            notebook = json.loads(raw)
            cells = notebook.get('cells', [])
            notebook_data.append({'path': path, 'sha256': hashlib.sha256(raw).hexdigest(),
                'bytes': len(raw), 'cells': len(cells), 'markdown': [''.join(c.get('source', [])) for c in cells if c.get('cell_type') == 'markdown'],
                'code': [''.join(c.get('source', [])) for c in cells if c.get('cell_type') == 'code']})
        elif is_bib:
            import re
            entries = re.findall(r'(?m)^\s*@([a-zA-Z]+)\s*\{([^,]+),', raw.decode('utf-8', errors='replace'))
            bibliography_data.append({'path': path, 'sha256': hashlib.sha256(raw).hexdigest(),
                'bytes': len(raw), 'entries': len(entries), 'sample_keys': [e[1] for e in entries[:8]]})
    if notebook_data:
        save_json(folder / 'notebook-inspection.json', notebook_data)
    if bibliography_data:
        save_json(folder / 'bibliography-inspection.json', bibliography_data)
    print(f'{name}: {sha[:12]}, {len(tree["tree"])} paths, {len(files)} text files, {len(notebook_data)} notebooks inspected', flush=True)
    return {'repo': name, 'commit': sha, 'commit_date': info['commit_date'],
            'default_branch': branch, 'archived': repo['archived'], 'files': files}

def main():
    org_url = 'https://api.github.com/orgs/hallresearch-ai/repos?per_page=100&type=public'
    repos = json.loads(get(org_url))
    if len(repos) == 100:
        raise RuntimeError('Organization pagination required; refuse an incomplete inventory')
    staging = Path(tempfile.mkdtemp(prefix='upstream-refresh-', dir=ROOT / 'content'))
    save_json(staging / 'organization-repositories.json', [{k: r.get(k) for k in ('name', 'html_url', 'description', 'archived', 'default_branch')} for r in repos])
    by_name = {r['name']: r for r in repos}
    missing = set(REQUIRED) - by_name.keys()
    if missing:
        raise RuntimeError(f'Required repositories missing: {missing}')
    names = REQUIRED + [n for n in OPTIONAL if n in by_name]
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            snapshots = list(pool.map(lambda repo: fetch_repo(repo, staging), [by_name[n] for n in names]))
    except Exception:
        shutil.rmtree(staging)
        raise
    manifest = {'checked_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'authority': 'https://github.com/hallresearch-ai', 'repositories': snapshots,
                'unclassified_repositories': sorted(by_name.keys() - set(names))}
    manifest_path = ROOT / 'content' / 'source-manifest.json'
    temporary_manifest = manifest_path.with_suffix('.json.tmp')
    save_json(temporary_manifest, manifest)
    backup = ROOT / 'content/upstream-previous'
    if backup.exists(): shutil.rmtree(backup)
    if DEST.exists(): os.replace(DEST, backup)
    os.replace(staging, DEST)
    os.replace(temporary_manifest, manifest_path)
    if backup.exists(): shutil.rmtree(backup)
    print('All authoritative source snapshots refreshed.', flush=True)

if __name__ == '__main__':
    main()
