#!/usr/bin/env node
/**
 * inspect-docx.js - Doc nguoc mot file .docx ra dang text de kiem tra cau truc.
 *
 *   node inspect-docx.js <file.docx> [--check]
 *
 * In ra: heading (kem style), doan van, bang (dang | o | o |), va header/footer.
 * Voi --check: kiem tra zip + tinh well-formed cua cac phan XML chinh, thoat 1 neu loi.
 *
 * Dung de: (a) doi chieu tai lieu vua sinh voi cau truc chuan trong references/,
 *          (b) phan tich mot file mau .docx khac.
 */

const fs = require('fs');
const zlib = require('zlib');

function zipRead(file) {
  const buf = fs.readFileSync(file);
  let eocd = -1;
  for (let i = buf.length - 22; i >= 0 && i > buf.length - 22 - 65536; i--) {
    if (buf.readUInt32LE(i) === 0x06054b50) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error('Khong phai file zip hop le: ' + file);
  const count = buf.readUInt16LE(eocd + 10);
  let off = buf.readUInt32LE(eocd + 16);
  const out = {};
  for (let i = 0; i < count; i++) {
    const method = buf.readUInt16LE(off + 10);
    const compSize = buf.readUInt32LE(off + 20);
    const nameLen = buf.readUInt16LE(off + 28);
    const extraLen = buf.readUInt16LE(off + 30);
    const commentLen = buf.readUInt16LE(off + 32);
    const localOff = buf.readUInt32LE(off + 42);
    const name = buf.toString('utf8', off + 46, off + 46 + nameLen);
    const start = localOff + 30 + buf.readUInt16LE(localOff + 26) + buf.readUInt16LE(localOff + 28);
    const raw = buf.subarray(start, start + compSize);
    out[name] = method === 8 ? zlib.inflateRawSync(raw) : Buffer.from(raw);
    off += 46 + nameLen + extraLen + commentLen;
  }
  return out;
}

function decode(s) {
  return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, '&');
}

function textOf(frag) {
  let t = '';
  const re = /<w:(t|tab|br)(?:\s[^>]*)?(?:>([\s\S]*?)<\/w:\1>|\/>)/g;
  let m;
  while ((m = re.exec(frag))) {
    if (m[1] === 't') t += decode(m[2] || '');
    else if (m[1] === 'tab') t += '\t';
    else t += ' / ';
  }
  return t;
}

/** Tach cac phan tu cap cao nhat cua body thanh [{kind:'p'|'tbl', xml}] */
function topLevel(body) {
  const items = [];
  let pos = 0;
  while (pos < body.length) {
    const cands = [];
    for (const k of ['p', 'tbl']) {
      for (const open of ['<w:' + k + ' ', '<w:' + k + '>']) {
        const i = body.indexOf(open, pos);
        if (i >= 0) cands.push({ i, k });
      }
    }
    if (!cands.length) break;
    cands.sort((a, b) => a.i - b.i);
    const { i: start, k: kind } = cands[0];
    const endTag = '</w:' + kind + '>';
    let depth = 0, j = start, end = -1;
    while (j < body.length) {
      const nE = body.indexOf(endTag, j);
      if (nE < 0) break;
      const opens = ['<w:' + kind + ' ', '<w:' + kind + '>']
        .map(o => body.indexOf(o, j)).filter(v => v >= 0 && v < nE);
      if (opens.length) { depth++; j = Math.min.apply(null, opens) + 4; continue; }
      depth--;
      if (depth <= 0) { end = nE + endTag.length; break; }
      j = nE + endTag.length;
    }
    if (end < 0) break;
    items.push({ kind, xml: body.slice(start, end) });
    pos = end;
  }
  return items;
}

function dumpBody(xml, label) {
  const bs = xml.indexOf('<w:body>');
  const body = bs >= 0 ? xml.slice(bs + 8, xml.lastIndexOf('</w:body>')) : xml;
  const lines = [];
  if (label) lines.push('===== ' + label + ' =====');
  for (const it of topLevel(body)) {
    if (it.kind === 'p') {
      const st = (it.xml.match(/<w:pStyle w:val="([^"]*)"/) || [])[1] || '';
      const isToc = /TOC \\o/.test(it.xml);
      const t = textOf(it.xml).trim();
      if (isToc) { lines.push('[TOC FIELD]'); continue; }
      if (!t && !st) { lines.push(''); continue; }
      lines.push((st ? '[' + st + '] ' : '') + t);
    } else {
      const rows = [];
      const rre = /<w:tr[ >][\s\S]*?<\/w:tr>/g;
      let rm;
      while ((rm = rre.exec(it.xml))) {
        const cells = [];
        const cre = /<w:tc>[\s\S]*?<\/w:tc>/g;
        let cm;
        while ((cm = cre.exec(rm[0]))) {
          const span = (cm[0].match(/<w:gridSpan w:val="(\d+)"/) || [])[1];
          const vm = /<w:vMerge\/>/.test(cm[0]) ? '^' : '';
          cells.push((span ? '<' + span + 'cols>' : '') + vm + textOf(cm[0]).replace(/\s+/g, ' ').trim());
        }
        rows.push(cells);
      }
      lines.push('[BANG ' + rows.length + ' hang x ' + (rows[0] ? rows[0].length : 0) + ' cot]');
      rows.forEach(r => lines.push('   | ' + r.join(' | ')));
    }
  }
  return lines.join('\n');
}

function wellFormed(name, xml) {
  const re = /<(\/?)([A-Za-z_][\w.:-]*)([^>]*?)(\/?)>/g;
  const st = [];
  let m;
  while ((m = re.exec(xml))) {
    if (m[1] === '/') {
      const top = st.pop();
      if (top !== m[2]) return name + ': the dong </' + m[2] + '> khong khop <' + top + '>';
    } else if (m[4] !== '/') st.push(m[2]);
  }
  return st.length ? name + ': con the chua dong: ' + st.join(', ') : null;
}

function main() {
  const file = process.argv[2];
  const checkOnly = process.argv.includes('--check');
  if (!file) {
    console.error('Dung: node inspect-docx.js <file.docx> [--check]');
    process.exit(1);
  }
  const z = zipRead(file);

  if (checkOnly) {
    const errs = [];
    for (const n of Object.keys(z)) {
      if (!n.endsWith('.xml') && !n.endsWith('.rels')) continue;
      const e = wellFormed(n, z[n].toString('utf8'));
      if (e) errs.push(e);
    }
    if (!z['word/document.xml']) errs.push('thieu word/document.xml');
    if (errs.length) { errs.forEach(e => console.error('LOI  ' + e)); process.exit(1); }
    console.log('OK: zip hop le, tat ca XML well-formed (' + Object.keys(z).length + ' entry).');
    return;
  }

  console.log(dumpBody(z['word/document.xml'].toString('utf8'), null));
  for (const n of Object.keys(z).sort()) {
    if (!/^word\/(header|footer)\d*\.xml$/.test(n)) continue;
    const t = dumpBody(z[n].toString('utf8'), n).trim();
    if (t.replace(/^=+.*=+$/m, '').trim()) console.log('\n' + t);
  }
}

main();
