import fs from 'node:fs';
import { marked } from 'marked';

// GFM preserves tables, nested lists, inline code, fenced code and task lists.
// DOM processing, source-relative URLs and heading IDs are handled by build.py.
const sources = JSON.parse(fs.readFileSync(0, 'utf8'));
const rendered = {};
for (const [key, markdown] of Object.entries(sources)) {
  rendered[key] = marked.parse(markdown, { gfm: true, breaks: false });
}
process.stdout.write(JSON.stringify(rendered));
