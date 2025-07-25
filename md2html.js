#!/usr/bin/env node

/**
 * md2html.js
 * Node.js script to convert a Markdown file (with special structure) to styled HTML for research docs.
 * Usage: node md2html.js path/to/file.md [output.html]
 */

const fs = require('fs');
const path = require('path');
const process = require('process');
const marked = require('marked');

// --- CONFIG ---
const CSS_FILE = 'dele.css';

// --- HELPERS ---
function escapeHtml(str) {
  return str.replace(/[&<>"']/g, function (tag) {
    const charsToReplace = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    };
    return charsToReplace[tag] || tag;
  });
}

function splitPages(md) {
  // Split by '## Page X' (start of line)
  const pageRegex = /^## Page (\d+)/gm;
  let match, lastIndex = 0, pages = [], pageNum = 1;
  while ((match = pageRegex.exec(md)) !== null) {
    if (match.index > lastIndex) {
      pages.push({
        num: pageNum,
        content: md.slice(lastIndex, match.index).trim()
      });
      pageNum = parseInt(match[1], 10);
      lastIndex = match.index;
    }
  }
  // Push last page
  if (lastIndex < md.length) {
    pages.push({
      num: pageNum,
      content: md.slice(lastIndex).trim()
    });
  }
  // Remove empty first page if exists
  if (pages.length && !pages[0].content) pages.shift();
  return pages;
}

function isDataBlock(text) {
  // Detect if paragraph is a data block:
  // 1. starts with Table/Figure/Data
  // 2. has many numbers
  // 3. has at least 2 key-value pairs (:) or (::)
  // 4. starts with 'Report Highlights'
  const startsWith = /^(Table|Figure|Data)\b/i.test(text);
  const numbers = (text.match(/\d[\d,.]*/g) || []).length;
  const keyValuePairs = (text.match(/:{1,2}/g) || []).length;
  const startsWithHighlights = /^Report Highlights[:：]/i.test(text.trim());
  return startsWith || numbers > 8 || keyValuePairs >= 2 || startsWithHighlights;
}

function splitKeyValueLines(text) {
  // מחלק שורה עם הרבה key-value לשורות עם <br>
  // תומך גם ב-: וגם ב-:: וגם ב-: (עם רווח)
  // דוגמה: "Field1: value1 Field2: value2" => "Field1: value1<br>Field2: value2<br>..."
  // פועל רק אם יש לפחות 2 key-value
  const keyValueRegex = /([^:]+:{1,2}\s*[^:]+)(?=\s+[^:]+:{1,2}|$)/g;
  const matches = text.match(keyValueRegex);
  if (matches && matches.length >= 2) {
    return matches.map(s => s.trim()).join('<br>');
  }
  return text;
}

function highlightNumbers(text) {
  // מדגיש מספרים, תאריכים, כמו 2025, 2024/25, 1,000, 3.5 וכו'
  // כולל טווחים (2024/25), מספרים עם פסיקים, נקודות, אחוזים
  return text.replace(/(\b\d{1,3}(?:[,.]\d{3})*(?:[./]\d+)?%?|\b\d{4}\/\d{2,4}\b)/g, '<span class="num-highlight">$1</span>');
}

function renderPageHtml(page, pageIdx) {
  // Remove the '## Page X' header from the start
  let content = page.content.replace(/^## Page \d+\s*/i, '');
  // Use marked to convert markdown to HTML, but post-process <p> for data-blocks
  let html = marked.parse(content, { mangle: false, headerIds: false });
  // Post-process: add class to <p> if needed, and split key-value lines for data-blocks
  html = html.replace(/<p>([\s\S]*?)<\/p>/g, (match, pText) => {
    if (isDataBlock(pText)) {
      // פיצול שדות
      const keyValuePairs = (pText.match(/:{1,2}/g) || []).length;
      let newText = pText;
      if (keyValuePairs >= 2) {
        newText = splitKeyValueLines(pText);
      }
      // פיצול Highlights מתוך data-block
      const highlightsMatch = newText.match(/([\s\S]*?)(?:<br>)?((?:Report )?Highlights:)([\s\S]*)/i);
      if (highlightsMatch) {
        const before = highlightsMatch[1].trim();
        const label = highlightsMatch[2];
        let rest = highlightsMatch[3].trim();
        rest = highlightNumbers(rest);
        let out = '';
        if (before) {
          out += `<p class="data-block">${before}</p>`;
        }
        out += `<div class="highlight-block"><strong>${label}</strong><br>${rest}</div>`;
        return out;
      }
      return `<p class="data-block">${newText}</p>`;
    }
    return match;
  });
  // Wrap in .document-page
  return `<div class="document-page" data-page="Page ${page.num}">\n${html}\n</div>`;
}

function buildHtmlDoc(bodyHtml, cssContent, title = 'Document') {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(title)}</title>
  <link rel="stylesheet" href="dele.css">
</head>
<body>\n${bodyHtml}\n</body>
</html>`;
}

// --- MAIN ---
(async function main() {
  const [,, mdPath, outPath] = process.argv;
  if (!mdPath) {
    console.error('Usage: node md2html.js path/to/file.md [output.html]');
    process.exit(1);
  }
  const mdRaw = fs.readFileSync(mdPath, 'utf8');
  const cssRaw = fs.readFileSync(CSS_FILE, 'utf8');
  const title = path.basename(mdPath, '.md');

  // Split to pages
  const pages = splitPages(mdRaw);
  const bodyHtml = pages.map(renderPageHtml).join('\n\n');
  const html = buildHtmlDoc(bodyHtml, cssRaw, title);

  const outFile = outPath || mdPath.replace(/\.md$/, '.html');
  fs.writeFileSync(outFile, html, 'utf8');
  console.log(`Converted ${mdPath} → ${outFile}`);
})(); 