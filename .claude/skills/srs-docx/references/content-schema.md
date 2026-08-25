# Schema của file `content.json`

Script `scripts/build-docx.js` nhận đúng một file JSON theo schema dưới đây.

```jsonc
{
  "meta": {
    "projectName":   "Hệ thống Bình luận MyTV",       // in trên bìa
    "title":         "TÀI LIỆU ĐẶC TẢ YÊU CẦU NGƯỜI SỬ DỤNG",
    "subtitle":      "URD - User Requirement Description",
    "docCode":       "BM03_URD",                      // cũng thay vào footer
    "version":       "1.0",                           // cũng thay vào header/footer
    "effectiveDate": "25/08/2026",
    "projectCode":   "MYTV-CMT"                       // thay <MÃ DỰ ÁN> ở header
  },

  "approvals": [                                       // 4 vai trò cố định
    { "role": "Soạn thảo",  "name": "Nguyễn Văn A", "title": "BA",       "date": "20/08/2026" },
    { "role": "Xem xét",    "name": "",             "title": "",         "date": "" },
    { "role": "Thẩm định",  "name": "",             "title": "",         "date": "" },
    { "role": "Phê chuẩn",  "name": "",             "title": "",         "date": "" }
  ],

  "history": [                                         // URD: 6 cột (không có Người xem xét)
    { "no": 1, "version": "1.0", "author": "Nguyễn Văn A",
      "approver": "Trần Thị B", "date": "25/08/2026", "changes": "Khởi tạo tài liệu" }
  ],
  // SRS dùng thêm "reviewer" và phải khai historyColumns 7 cột.

  "showInstructions": true,   // false = bỏ khối [Hướng dẫn sử dụng mẫu tài liệu]
  "tocDepth": 3,              // URD: 3, SRS: 5

  "body": [ /* mảng block, xem bên dưới */ ]
}
```

## Các loại block trong `body`

| `type` | Trường | Ghi chú |
|---|---|---|
| `h1`…`h5` | `text` | Word tự đánh số `I.` / `I.1.` / `I.1.1.` — **đừng gõ số vào text** |
| `p` | `text`, `bold`, `italic`, `align`, `indent`, `size`, `color` | `\n` = ngắt dòng mềm trong cùng đoạn |
| `note` | `text` | Đoạn in nghiêng xám — dùng cho ghi chú hướng dẫn `[...]` |
| `bullet` | `items: []` hoặc `text`, `level` | Gạch đầu dòng |
| `number` | `items: []` hoặc `text`, `level` | Danh sách đánh số |
| `table` | `header`, `rows`, `widths`, `cols`, `caption` | xem dưới |
| `image` | `path`, `widthCm`, `caption` | Đường dẫn tương đối so với file JSON |
| `pagebreak` | — | Ngắt trang |
| `empty` | — | Dòng trống |

Một phần tử là chuỗi thuần được hiểu là `{"type":"p"}`.

### Block `table`

```jsonc
{
  "type": "table",
  "caption": "Bảng 1: Danh sách đối tượng người dùng",   // tuỳ chọn, in nghiêng canh giữa
  "widths": [6, 18, 30, 12, 12, 22],                     // % , tổng nên = 100
  "header": ["STT", "Tên đối tượng", "Mô tả", "Vào", "Ra", "Lợi ích"],
  "rows": [
    ["1", "Người xem", "Khán giả MyTV", "Bình luận", "Danh sách", "Tương tác"]
  ]
}
```

Ô có thể là chuỗi, hoặc object để định dạng / gộp ô:

```jsonc
{ "text": "Tương tác với hệ thống", "colspan": 2, "bold": true, "align": "center" }
{ "text": "STT", "rowspan": 2 }
{ "text": "Ghi chú", "italic": true, "shade": "F2F2F2" }
```

- Hàng `header` mặc định in đậm, canh giữa, nền xám `D9D9D9`, và lặp lại khi bảng
  tràn sang trang mới.
- Trong `text`, `\n` tách thành nhiều đoạn; dòng bắt đầu bằng `- ` thành gạch đầu dòng.
- Khi dùng `rowspan`/`colspan`, các hàng sau **không** khai lại ô đã bị gộp — script tự
  chèn ô `vMerge continue`.

**Header hai tầng** (mẫu URD mục II.2):

```jsonc
"header": [
  { "text": "STT", "rowspan": 2 },
  { "text": "Tên đối tượng", "rowspan": 2 },
  { "text": "Mô tả", "rowspan": 2 },
  { "text": "Tương tác với hệ thống", "colspan": 2 },
  { "text": "Lợi ích mong đợi", "rowspan": 2 }
],
"rows": [
  [ { "text": "Vào", "bold": true, "align": "center", "shade": "D9D9D9" },
    { "text": "Ra",  "bold": true, "align": "center", "shade": "D9D9D9" } ],
  ["1", "Người xem", "...", "...", "...", "..."]
]
```

Hàng thứ hai của header nằm trong `rows` (vì `header` chỉ nhận một hàng), các ô `rowspan`
ở hàng trên đã chiếm chỗ nên hàng này chỉ khai 2 ô `Vào` / `Ra`.

## Cơ chế của script

- Mở file mẫu `.docx`, giữ nguyên `styles.xml`, `numbering.xml`, `header*.xml`,
  `footer*.xml`, `theme`, logo trong `media/`, và `sectPr` (khổ A4, lề, header/footer
  trang đầu khác). Chỉ thay `word/document.xml`.
- Thêm hai định nghĩa list riêng (`numId 900` bullet, `numId 901` số) vào `numbering.xml`
  để không đụng vào numbering sẵn có của mẫu.
- Bật `w:updateFields` trong `settings.xml` để Word hỏi cập nhật mục lục khi mở.
- Thay `<MÃ DỰ ÁN>`, `<x.y>`, `BM03_URD`/`BM04_SRS`, `Phiên bản: 1.0` trong header/footer
  kể cả khi Word đã cắt chuỗi thành nhiều `<w:r>`.
- Ảnh được nhúng thật (thêm vào `media/`, `document.xml.rels`, `[Content_Types].xml`);
  chiều cao tự tính theo tỉ lệ gốc (hỗ trợ PNG, JPEG, GIF).

Không cần cài npm package — chỉ cần `node`.
