#!/usr/bin/env node
/**
 * build-docx.js - Sinh file .docx theo mẫu BM03_URD / BM04_SRS.
 *
 * Cách chạy:
 *   node build-docx.js <content.json> <template.docx> <output.docx>
 *
 * Nguyên tắc: KHÔNG dựng docx từ số 0. Script mở file mẫu (.docx là một file zip),
 * giữ nguyên toàn bộ styles.xml / numbering.xml / header*.xml / footer*.xml / theme /
 * logo trong media, và CHỈ thay word/document.xml bằng nội dung sinh mới.
 * Nhờ vậy font Times New Roman, cách đánh số heading I / I.1 / I.1.1, header có logo
 * VNPT và footer "Mã số tài liệu ... Trang x/y" được bảo toàn 100%.
 *
 * Không phụ thuộc npm package nào (tự đọc/ghi zip bằng zlib).
 */

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

/* ==================================================================== */
/* 1. ZIP: doc va ghi                                                    */
/* ==================================================================== */

const CRC_TABLE = (() => {
  const t = new Int32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c;
  }
  return t;
})();

function crc32(buf) {
  let c = -1;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ -1) >>> 0;
}

/** Doc toan bo entry cua mot file zip -> [{name, data}] theo thu tu central directory. */
function zipRead(file) {
  const buf = fs.readFileSync(file);
  let eocd = -1;
  for (let i = buf.length - 22; i >= 0 && i > buf.length - 22 - 65536; i--) {
    if (buf.readUInt32LE(i) === 0x06054b50) { eocd = i; break; }
  }
  if (eocd < 0) throw new Error('Khong phai file zip hop le: ' + file);
  const count = buf.readUInt16LE(eocd + 10);
  let off = buf.readUInt32LE(eocd + 16);
  const entries = [];
  for (let i = 0; i < count; i++) {
    if (buf.readUInt32LE(off) !== 0x02014b50) throw new Error('Central directory hong');
    const method = buf.readUInt16LE(off + 10);
    const compSize = buf.readUInt32LE(off + 20);
    const nameLen = buf.readUInt16LE(off + 28);
    const extraLen = buf.readUInt16LE(off + 30);
    const commentLen = buf.readUInt16LE(off + 32);
    const localOff = buf.readUInt32LE(off + 42);
    const name = buf.toString('utf8', off + 46, off + 46 + nameLen);
    const lNameLen = buf.readUInt16LE(localOff + 26);
    const lExtraLen = buf.readUInt16LE(localOff + 28);
    const start = localOff + 30 + lNameLen + lExtraLen;
    const raw = buf.subarray(start, start + compSize);
    entries.push({ name, data: method === 8 ? zlib.inflateRawSync(raw) : Buffer.from(raw) });
    off += 46 + nameLen + extraLen + commentLen;
  }
  return entries;
}

/** Ghi danh sach entry thanh file zip (deflate). */
function zipWrite(entries, outFile) {
  const chunks = [];
  const central = [];
  let offset = 0;
  for (const e of entries) {
    const nameBuf = Buffer.from(e.name, 'utf8');
    const deflated = zlib.deflateRawSync(e.data, { level: 9 });
    const useStore = deflated.length >= e.data.length;
    const payload = useStore ? e.data : deflated;
    const method = useStore ? 0 : 8;
    const crc = crc32(e.data);

    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6);          // UTF-8 filename
    local.writeUInt16LE(method, 8);
    local.writeUInt16LE(0, 10);              // time
    local.writeUInt16LE(0x21, 12);           // date co dinh -> build tai lap duoc
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(payload.length, 18);
    local.writeUInt32LE(e.data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26);
    local.writeUInt16LE(0, 28);
    chunks.push(local, nameBuf, payload);

    const cd = Buffer.alloc(46);
    cd.writeUInt32LE(0x02014b50, 0);
    cd.writeUInt16LE(20, 4);
    cd.writeUInt16LE(20, 6);
    cd.writeUInt16LE(0x0800, 8);
    cd.writeUInt16LE(method, 10);
    cd.writeUInt16LE(0, 12);
    cd.writeUInt16LE(0x21, 14);
    cd.writeUInt32LE(crc, 16);
    cd.writeUInt32LE(payload.length, 20);
    cd.writeUInt32LE(e.data.length, 24);
    cd.writeUInt16LE(nameBuf.length, 28);
    cd.writeUInt32LE(offset, 42);
    central.push(cd, nameBuf);

    offset += local.length + nameBuf.length + payload.length;
  }
  const cdBuf = Buffer.concat(central);
  const eocd = Buffer.alloc(22);
  eocd.writeUInt32LE(0x06054b50, 0);
  eocd.writeUInt16LE(entries.length, 8);
  eocd.writeUInt16LE(entries.length, 10);
  eocd.writeUInt32LE(cdBuf.length, 12);
  eocd.writeUInt32LE(offset, 16);
  fs.writeFileSync(outFile, Buffer.concat([...chunks, cdBuf, eocd]));
}

/* ==================================================================== */
/* 2. Tien ich XML                                                       */
/* ==================================================================== */

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');
}

/**
 * Thay chuoi text trong XML ke ca khi Word da cat no thanh nhieu <w:r>.
 * Giu nguyen moi the (field PAGE/NUMPAGES, tab, rPr...): chi sua phan chu.
 */
function replaceTextAcrossRuns(xml, find, repl) {
  const re = /<w:t(?:\s[^>]*)?>([\s\S]*?)<\/w:t>/g;
  const chars = [];
  let m;
  while ((m = re.exec(xml))) {
    const inner = m[1];
    const base = m.index + m[0].length - inner.length - '</w:t>'.length;
    let i = 0;
    while (i < inner.length) {
      if (inner[i] === '&') {
        const j = inner.indexOf(';', i);
        if (j > 0 && j - i <= 8) {
          const ent = inner.slice(i, j + 1);
          const dec = { '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&apos;': "'" }[ent];
          chars.push({ ch: dec !== undefined ? dec : ent, s: base + i, e: base + j + 1 });
          i = j + 1;
          continue;
        }
      }
      chars.push({ ch: inner[i], s: base + i, e: base + i + 1 });
      i++;
    }
  }
  // Word tron lan NFC/NFD trong cung mot header -> so khop tren dang NFD.
  // Moi ky tu nguon co the no ra nhieu ky tu NFD, nen giu ban do vi tri.
  const plainParts = [];
  const owner = [];                       // vi tri NFD -> chi so trong `chars`
  chars.forEach((c, i) => {
    const d = c.ch.normalize('NFD');
    plainParts.push(d);
    for (let k = 0; k < d.length; k++) owner.push(i);
  });
  const plain = plainParts.join('');
  const at = plain.indexOf(find.normalize('NFD'));
  if (at < 0) return xml;
  const end = at + find.normalize('NFD').length - 1;
  const hit = chars.slice(owner[at], owner[end] + 1);
  const groups = [];
  for (const c of hit) {
    const last = groups[groups.length - 1];
    if (last && last.e === c.s) last.e = c.e;
    else groups.push({ s: c.s, e: c.e });
  }
  let out = xml;
  for (let i = groups.length - 1; i >= 0; i--) {
    const g = groups[i];
    out = out.slice(0, g.s) + (i === 0 ? esc(repl) : '') + out.slice(g.e);
  }
  return out;
}

/* ==================================================================== */
/* 3. Sinh cac khoi OOXML                                                */
/* ==================================================================== */

const NUM_BULLET = 900;   // numId tu them vao numbering.xml
const NUM_DECIMAL = 901;

const ALIGN = { left: 'left', center: 'center', right: 'right', justify: 'both', both: 'both' };

function rPr(o) {
  o = o || {};
  // thu tu con cua w:rPr phai dung theo schema CT_RPr: b, i, color, sz, szCs, u
  let s = '';
  if (o.bold) s += '<w:b/>';
  if (o.italic) s += '<w:i/>';
  if (o.color) s += '<w:color w:val="' + esc(String(o.color).replace('#', '')) + '"/>';
  if (o.size) s += '<w:sz w:val="' + o.size * 2 + '"/><w:szCs w:val="' + o.size * 2 + '"/>';
  if (o.underline) s += '<w:u w:val="single"/>';
  return s ? '<w:rPr>' + s + '</w:rPr>' : '';
}

function run(text, o) {
  const parts = String(text == null ? '' : text).split('\n');
  return parts.map((t, i) =>
    (i ? '<w:r><w:br/></w:r>' : '') +
    '<w:r>' + rPr(o) + '<w:t xml:space="preserve">' + esc(t) + '</w:t></w:r>'
  ).join('');
}

function para(text, o) {
  o = o || {};
  let p = '';
  if (o.style) p += '<w:pStyle w:val="' + o.style + '"/>';
  if (o.numId != null) p += '<w:numPr><w:ilvl w:val="' + (o.level || 0) + '"/><w:numId w:val="' + o.numId + '"/></w:numPr>';
  p += '<w:spacing w:before="' + (o.before != null ? o.before : 60) + '" w:after="' + (o.after != null ? o.after : 60) + '"/>';
  if (o.indent) p += '<w:ind w:left="' + Math.round(o.indent * 567) + '"/>';
  if (o.align) p += '<w:jc w:val="' + (ALIGN[o.align] || o.align) + '"/>';
  return '<w:p><w:pPr>' + p + rPr(o) + '</w:pPr>' +
    (text === '' || text == null ? '' : run(text, o)) + '</w:p>';
}

function heading(level, text) {
  return '<w:p><w:pPr><w:pStyle w:val="Heading' + level + '"/></w:pPr>' + run(text, {}) + '</w:p>';
}

function pageBreak() {
  return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>';
}

/** Truong muc luc tu dong; Word cap nhat so trang khi mo file. */
function tocField(maxLevel) {
  return '<w:p>' +
    '<w:r><w:fldChar w:fldCharType="begin"/></w:r>' +
    '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-' + maxLevel + '" \\h \\z \\u </w:instrText></w:r>' +
    '<w:r><w:fldChar w:fldCharType="separate"/></w:r>' +
    '<w:r><w:t>Nhan Ctrl+A roi F9 trong Word de cap nhat muc luc.</w:t></w:r>' +
    '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>';
}

function cellW(widths, ci, span, nCols) {
  if (widths && widths.length === nCols) {
    let s = 0;
    for (let i = ci; i < ci + span && i < nCols; i++) s += widths[i];
    return Math.round(s * 50);            // % -> pct (5000 = 100%)
  }
  return Math.round(5000 / nCols * span);
}

function vMergeContinueCell(widths, ci, nCols) {
  return '<w:tc><w:tcPr><w:tcW w:w="' + cellW(widths, ci, 1, nCols) + '" w:type="pct"/>' +
    '<w:vMerge/></w:tcPr>' + para('', {}) + '</w:tc>';
}

/**
 * Bang. O co the la chuoi hoac {text, bold, italic, align, colspan, rowspan, shade}.
 * rowspan hien thuc bang vMerge (restart / continue).
 * Trong text: "\n" tach doan; dong bat dau bang "- " thanh gach dau dong.
 */
function table(spec) {
  const widths = spec.widths;
  const allRows = [];
  if (spec.header) allRows.push({ cells: spec.header, isHeader: true });
  (spec.rows || []).forEach(r => allRows.push({ cells: r, isHeader: false }));
  if (!allRows.length) return '';

  const nCols = spec.cols || Math.max.apply(null, allRows.map(r =>
    r.cells.reduce((a, c) => a + ((c && c.colspan) || 1), 0)));

  const occupied = allRows.map(() => new Array(nCols).fill(false));

  const grid = widths && widths.length === nCols
    ? widths.map(w => '<w:gridCol w:w="' + Math.round(w / 100 * 9060) + '"/>').join('')
    : new Array(nCols).fill('<w:gridCol w:w="' + Math.round(9060 / nCols) + '"/>').join('');

  let xml = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>' +
    '<w:tblW w:w="5000" w:type="pct"/><w:tblLayout w:type="fixed"/>' +
    '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>' +
    '</w:tblPr><w:tblGrid>' + grid + '</w:tblGrid>';

  for (let ri = 0; ri < allRows.length; ri++) {
    const row = allRows[ri];
    let tr = '<w:tr>';
    if (row.isHeader) tr += '<w:trPr><w:tblHeader/></w:trPr>';
    let ci = 0;
    for (const raw of row.cells) {
      while (ci < nCols && occupied[ri][ci]) { tr += vMergeContinueCell(widths, ci, nCols); ci++; }
      if (ci >= nCols) break;
      const c = (raw && typeof raw === 'object') ? raw : { text: raw };
      const span = c.colspan || 1;
      const rspan = c.rowspan || 1;
      for (let k = 1; k < rspan; k++)
        for (let j = 0; j < span; j++)
          if (occupied[ri + k]) occupied[ri + k][ci + j] = true;

      let tcPr = '<w:tcW w:w="' + cellW(widths, ci, span, nCols) + '" w:type="pct"/>';
      if (span > 1) tcPr += '<w:gridSpan w:val="' + span + '"/>';
      if (rspan > 1) tcPr += '<w:vMerge w:val="restart"/>';
      const shade = c.shade || (row.isHeader ? 'D9D9D9' : null);
      if (shade) tcPr += '<w:shd w:val="clear" w:color="auto" w:fill="' + shade + '"/>';
      tcPr += '<w:vAlign w:val="center"/>';

      const opts = {
        bold: c.bold != null ? c.bold : row.isHeader,
        italic: !!c.italic,
        align: c.align || (row.isHeader ? 'center' : null),
        before: 20, after: 20,
      };
      const lines = String(c.text == null ? '' : c.text).split('\n');
      let body = '';
      for (const line of lines) {
        const isBullet = /^\s*[-*]\s/.test(line);
        const t = line.replace(/^\s*[-*]\s?/, '');
        const po = isBullet
          ? Object.assign({}, opts, { numId: NUM_BULLET, indent: 0.5, align: null })
          : opts;
        body += para(t, po);
      }
      tr += '<w:tc><w:tcPr>' + tcPr + '</w:tcPr>' + (body || para('', opts)) + '</w:tc>';
      ci += span;
    }
    while (ci < nCols) {
      tr += occupied[ri][ci]
        ? vMergeContinueCell(widths, ci, nCols)
        : '<w:tc><w:tcPr><w:tcW w:w="' + cellW(widths, ci, 1, nCols) + '" w:type="pct"/></w:tcPr>' + para('', {}) + '</w:tc>';
      ci++;
    }
    xml += tr + '</w:tr>';
  }
  return xml + '</w:tbl>' + para('', { before: 0, after: 60 });
}

/* --- anh ------------------------------------------------------------ */

function imageSize(buf) {
  if (buf.length > 24 && buf.readUInt32BE(0) === 0x89504e47)
    return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };            // PNG
  if (buf[0] === 0x47 && buf[1] === 0x49 && buf[2] === 0x46)
    return { w: buf.readUInt16LE(6), h: buf.readUInt16LE(8) };              // GIF
  if (buf[0] === 0xff && buf[1] === 0xd8) {                                 // JPEG
    let i = 2;
    while (i < buf.length - 9) {
      if (buf[i] !== 0xff) { i++; continue; }
      const mk = buf[i + 1];
      if (mk >= 0xc0 && mk <= 0xcf && mk !== 0xc4 && mk !== 0xc8 && mk !== 0xcc)
        return { h: buf.readUInt16BE(i + 5), w: buf.readUInt16BE(i + 7) };
      i += 2 + buf.readUInt16BE(i + 2);
    }
  }
  return { w: 800, h: 600 };
}

function imagePara(rid, name, cx, cy) {
  return '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr><w:r><w:drawing>' +
    '<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="' + cx + '" cy="' + cy + '"/>' +
    '<wp:effectExtent l="0" t="0" r="0" b="0"/>' +
    '<wp:docPr id="' + rid + '" name="' + esc(name) + '"/><wp:cNvGraphicFramePr/>' +
    '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData ' +
    'uri="http://schemas.openxmlformats.org/drawingml/2006/picture">' +
    '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">' +
    '<pic:nvPicPr><pic:cNvPr id="' + rid + '" name="' + esc(name) + '"/><pic:cNvPicPr/></pic:nvPicPr>' +
    '<pic:blipFill><a:blip r:embed="rId' + rid + '"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>' +
    '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="' + cx + '" cy="' + cy + '"/></a:xfrm>' +
    '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>' +
    '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>';
}

/* ==================================================================== */
/* 4. Trang bia + lich su + muc luc                                      */
/* ==================================================================== */

function coverPage(c) {
  const m = c.meta || {};
  let x = '';
  x += para('', { before: 0, after: 0 });
  x += para('', { before: 0, after: 0 });
  x += para(m.projectName || '<Ten du an>', { align: 'center', bold: true, size: 18, before: 120, after: 120 });
  x += para('', { before: 0, after: 0 });
  x += para(m.title || '', { align: 'center', bold: true, size: 18, before: 120, after: 120 });
  x += para(m.subtitle || '', { align: 'center', bold: true, size: 13, before: 120, after: 240 });
  x += para('', { before: 0, after: 0 });

  x += table({
    cols: 2, widths: [35, 65],
    rows: [
      [{ text: 'Mã số:', bold: true }, m.docCode || ''],
      [{ text: 'Phiên bản:', bold: true }, m.version || ''],
      [{ text: 'Ngày hiệu lực:', bold: true }, m.effectiveDate || ''],
    ],
  });

  x += para('', { before: 0, after: 0 });
  const roles = c.approvalRoles || ['Soạn thảo', 'Xem xét', 'Thẩm định', 'Phê chuẩn'];
  const ap = {};
  (c.approvals || []).forEach(a => { ap[a.role] = a; });
  x += table({
    cols: 5, widths: [16, 26, 22, 18, 18],
    header: ['', 'Họ và tên', 'Chức danh', 'Ngày, tháng', 'Ký tên'],
    rows: roles.map(r => [
      { text: r, bold: true },
      (ap[r] && ap[r].name) || '', (ap[r] && ap[r].title) || '',
      (ap[r] && ap[r].date) || '', '',
    ]),
  });

  if (c.showInstructions !== false) {
    x += para('', { before: 0, after: 0 });
    x += para('[', { before: 0, after: 0 });
    x += para('Hướng dẫn sử dụng mẫu tài liệu', { bold: true, italic: true });
    const ins = c.instructions || [
      'Các nội dung đặt trong các cặp dấu [], <> là thông tin hướng dẫn của mẫu tài liệu. Những nội dung này phải được xóa và thay thế bằng các thông tin tương ứng của dự án.',
      'Tài liệu thực tế có thể bổ sung thêm các mục mới so với mẫu tài liệu để phù hợp với đặc thù của dự án cụ thể.',
    ];
    ins.forEach(t => { x += para(t, { italic: true, numId: NUM_BULLET, indent: 0.75 }); });
    x += para(']', { before: 0, after: 0 });
  }
  return x;
}

function historyPage(c) {
  const cols = c.historyColumns ||
    ['STT', 'Phiên bản', 'Người thực hiện', 'Người phê duyệt', 'Ngày hiệu lực', 'Nội dung thay đổi'];
  const n = cols.length;
  const has7 = n === 7;
  const rows = (c.history || []).map((h, i) => {
    if (Array.isArray(h)) return h;
    const base = [h.no != null ? h.no : i + 1, h.version || '', h.author || ''];
    if (has7) base.push(h.reviewer || '');
    base.push(h.approver || '', h.date || '', h.changes || '');
    return base.slice(0, n);
  });
  while (rows.length < 3) rows.push(new Array(n).fill(''));

  const widths = has7 ? [6, 10, 16, 16, 16, 13, 23] : [7, 11, 18, 18, 15, 31];
  return pageBreak() +
    para('LỊCH SỬ THAY ĐỔI', { align: 'center', bold: true, size: 14, before: 120, after: 120 }) +
    para('', { before: 0, after: 0 }) +
    table({ cols: n, widths: widths, header: cols, rows: rows });
}

function tocPage(c) {
  return pageBreak() +
    para('MỤC LỤC', { align: 'center', bold: true, size: 14, before: 120, after: 240 }) +
    tocField(c.tocDepth || 4) +
    pageBreak();
}

/* ==================================================================== */
/* 5. Dung than tai lieu                                                 */
/* ==================================================================== */

function buildBody(items, ctx) {
  let xml = '';
  for (const raw of items || []) {
    const it = typeof raw === 'string' ? { type: 'p', text: raw } : raw;
    const t = (it.type || 'p').toLowerCase();
    switch (t) {
      case 'h1': case 'h2': case 'h3': case 'h4': case 'h5':
        xml += heading(t[1], it.text); break;
      case 'heading':
        xml += heading(it.level || 1, it.text); break;
      case 'p': case 'text':
        xml += para(it.text, it); break;
      case 'note': case 'guide':
        xml += para(it.text, Object.assign({}, it, { italic: true, color: '808080' })); break;
      case 'bullet': case 'ul':
        (Array.isArray(it.items) ? it.items : [it.text]).forEach(v => {
          xml += para(v, { numId: NUM_BULLET, level: it.level || 0, indent: 0.75, italic: !!it.italic });
        });
        break;
      case 'number': case 'ol':
        (Array.isArray(it.items) ? it.items : [it.text]).forEach(v => {
          xml += para(v, { numId: NUM_DECIMAL, level: it.level || 0, indent: 0.75, italic: !!it.italic });
        });
        break;
      case 'table':
        if (it.caption) xml += para(it.caption, { italic: true, align: 'center' });
        xml += table(it); break;
      case 'image': case 'img': {
        const p = path.resolve(ctx.baseDir, it.path);
        if (!fs.existsSync(p)) {
          xml += para('[Thiếu ảnh: ' + it.path + ']', { italic: true, color: 'C00000' });
          break;
        }
        const data = fs.readFileSync(p);
        const ext = path.extname(p).slice(1).toLowerCase();
        const rid = ctx.nextRid++;
        const name = 'media/img' + rid + '.' + ext;
        ctx.media.push({ name: 'word/' + name, data: data, ext: ext });
        ctx.rels.push('<Relationship Id="rId' + rid + '" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="' + name + '"/>');
        const dim = imageSize(data);
        const cx = Math.round((it.widthCm || 15.5) * 360000);
        const cy = Math.round(cx * dim.h / dim.w);
        xml += imagePara(rid, path.basename(p), cx, cy);
        if (it.caption) xml += para(it.caption, { italic: true, align: 'center', size: 11 });
        break;
      }
      case 'pagebreak': case 'break':
        xml += pageBreak(); break;
      case 'empty': case 'spacer':
        xml += para('', { before: 0, after: 0 }); break;
      default:
        xml += para(it.text || '', it);
    }
  }
  return xml;
}

/* ==================================================================== */
/* 6. Chay                                                               */
/* ==================================================================== */

function extraNumbering() {
  const BULLET_CHARS = ['', 'o', ''];
  const lv = (i, fmt, text, ind) =>
    '<w:lvl w:ilvl="' + i + '"><w:start w:val="1"/><w:numFmt w:val="' + fmt + '"/>' +
    '<w:lvlText w:val="' + text + '"/><w:lvlJc w:val="left"/>' +
    '<w:pPr><w:ind w:left="' + ind + '" w:hanging="360"/></w:pPr>' +
    (fmt === 'bullet'
      ? '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr>'
      : '') +
    '</w:lvl>';

  let a1 = '<w:abstractNum w:abstractNumId="900"><w:multiLevelType w:val="hybridMultilevel"/>';
  for (let i = 0; i < 9; i++) a1 += lv(i, 'bullet', BULLET_CHARS[i % 3], 720 + i * 360);
  a1 += '</w:abstractNum>';

  const fmts = ['decimal', 'lowerLetter', 'lowerRoman'];
  let a2 = '<w:abstractNum w:abstractNumId="901"><w:multiLevelType w:val="hybridMultilevel"/>';
  for (let i = 0; i < 9; i++) a2 += lv(i, fmts[i % 3], '%' + (i + 1) + '.', 720 + i * 360);
  a2 += '</w:abstractNum>';

  return {
    abs: a1 + a2,
    nums: '<w:num w:numId="' + NUM_BULLET + '"><w:abstractNumId w:val="900"/></w:num>' +
      '<w:num w:numId="' + NUM_DECIMAL + '"><w:abstractNumId w:val="901"/></w:num>',
  };
}

function main() {
  const jsonPath = process.argv[2];
  const tplPath = process.argv[3];
  const outPath = process.argv[4];
  if (!jsonPath || !tplPath || !outPath) {
    console.error('Dung: node build-docx.js <content.json> <template.docx> <output.docx>');
    process.exit(1);
  }
  const content = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  const entries = zipRead(tplPath);
  const get = n => entries.find(e => e.name === n);

  const docEntry = get('word/document.xml');
  if (!docEntry) throw new Error('Template khong co word/document.xml');
  const origDoc = docEntry.data.toString('utf8');

  // giu nguyen khai bao namespace va sectPr (kho giay, le, header/footer) cua mau
  const openTag = origDoc.match(/<w:document[^>]*>/)[0];
  const decl = origDoc.slice(0, origDoc.indexOf('<w:document'));
  const si = origDoc.lastIndexOf('<w:sectPr');
  const sectPr = si > 0 ? origDoc.slice(si, origDoc.indexOf('</w:sectPr>', si) + 11) : '';

  const relsEntry = get('word/_rels/document.xml.rels');
  const usedIds = (relsEntry.data.toString('utf8').match(/Id="rId(\d+)"/g) || [])
    .map(s => parseInt(s.match(/\d+/)[0], 10));
  const ctx = {
    baseDir: path.dirname(path.resolve(jsonPath)),
    nextRid: Math.max.apply(null, [100].concat(usedIds)) + 1,
    media: [], rels: [],
  };

  const body = coverPage(content) + historyPage(content) + tocPage(content) +
    buildBody(content.body, ctx) + sectPr;
  docEntry.data = Buffer.from(decl + openTag + '<w:body>' + body + '</w:body></w:document>', 'utf8');

  // numbering: them dinh nghia bullet / so cua rieng script
  const numEntry = get('word/numbering.xml');
  if (numEntry) {
    let n = numEntry.data.toString('utf8');
    if (n.indexOf('w:abstractNumId="900"') < 0) {
      const ex = extraNumbering();
      const firstNum = n.indexOf('<w:num ');
      if (firstNum > 0) {
        n = n.slice(0, firstNum) + ex.abs +
          n.slice(firstNum).replace('</w:numbering>', ex.nums + '</w:numbering>');
      } else {
        n = n.replace('</w:numbering>', ex.abs + ex.nums + '</w:numbering>');
      }
      numEntry.data = Buffer.from(n, 'utf8');
    }
  }

  // settings: bat cap nhat field khi mo -> muc luc tu sinh so trang
  const setEntry = get('word/settings.xml');
  if (setEntry) {
    let s = setEntry.data.toString('utf8');
    if (s.indexOf('w:updateFields') < 0) {
      // theo schema CT_Settings, updateFields dung truoc compat / rsids / mathPr
      const anchor = ['<w:compat', '<w:rsids', '<w:mathPr', '</w:settings>']
        .find(a => s.indexOf(a) >= 0);
      s = s.replace(anchor, '<w:updateFields w:val="true"/>' + anchor);
      setEntry.data = Buffer.from(s, 'utf8');
    }
  }

  // header/footer: thay ma du an, ma tai lieu, phien ban
  const m = content.meta || {};
  const subs = [];
  if (m.projectCode) subs.push(['<MÃ DỰ ÁN>', m.projectCode]);
  if (m.version) {
    subs.push(['<x.y>', m.version]);
    subs.push(['Phiên bản: 1.0', 'Phiên bản: ' + m.version]);
  }
  if (m.docCode) {
    subs.push(['BM03_URD', m.docCode]);
    subs.push(['BM04_SRS', m.docCode]);
  }
  for (const e of entries) {
    if (!/^word\/(header|footer)\d*\.xml$/.test(e.name)) continue;
    let s = e.data.toString('utf8');
    for (const pair of subs) s = replaceTextAcrossRuns(s, pair[0], pair[1]);
    e.data = Buffer.from(s, 'utf8');
  }

  // anh chen them
  if (ctx.media.length) {
    let rels = relsEntry.data.toString('utf8');
    rels = rels.replace('</Relationships>', ctx.rels.join('') + '</Relationships>');
    relsEntry.data = Buffer.from(rels, 'utf8');

    const ctEntry = get('[Content_Types].xml');
    let ct = ctEntry.data.toString('utf8');
    const mime = {
      png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg',
      gif: 'image/gif', bmp: 'image/bmp', emf: 'image/x-emf',
    };
    for (const md of ctx.media) {
      if (ct.indexOf('Extension="' + md.ext + '"') < 0) {
        ct = ct.replace('</Types>', '<Default Extension="' + md.ext + '" ContentType="' +
          (mime[md.ext] || 'application/octet-stream') + '"/></Types>');
      }
      entries.push({ name: md.name, data: md.data });
    }
    ctEntry.data = Buffer.from(ct, 'utf8');
  }

  fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
  zipWrite(entries, outPath);
  console.log('Đã tạo: ' + path.resolve(outPath));
  console.log('Mở bằng Word rồi nhấn Ctrl+A, F9 để cập nhật số trang mục lục.');
}

main();
