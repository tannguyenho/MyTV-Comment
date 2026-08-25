---
name: urd-docx
description: Tạo tài liệu URD (Đặc tả yêu cầu người sử dụng) dạng file .docx theo đúng mẫu BM03_URD của VNPT/Tổng công ty Truyền thông — giữ nguyên trang bìa, bảng ký duyệt, lịch sử thay đổi, mục lục tự động, header có logo và footer "Mã số tài liệu / Trang x/y". Dùng khi người dùng yêu cầu viết, sinh, xuất hoặc cập nhật tài liệu URD / "đặc tả yêu cầu người sử dụng" / BM03 cho một dự án hoặc tính năng.
---

# Tạo tài liệu URD (BM03_URD) dạng .docx

## Quy trình

### Bước 1 — Đọc cấu trúc chuẩn

Đọc `references/urd-structure.md` để nắm bộ khung 6 chương bắt buộc và nội dung
từng mục. **Không được bỏ mục nào**; mục không áp dụng thì điền `N/A`.

Đọc `references/content-schema.md` để nắm schema của file JSON đầu vào (các loại
block, cách khai bảng, gộp ô, chèn ảnh).

### Bước 2 — Thu thập thông tin dự án

Trước khi viết, xác định các thông tin sau. Nếu người dùng chưa cung cấp, hãy lấy
từ tài liệu sẵn có trong repo (README, ARCHITECTURE, BACKLOG, user story…), rồi
hỏi bổ sung **một lần** những gì thực sự không suy ra được:

- Tên dự án, mã dự án, mã tài liệu, phiên bản, ngày hiệu lực
- Người soạn thảo / xem xét / thẩm định / phê chuẩn
- Mục tiêu hệ thống, các nhóm người dùng
- Các quy trình nghiệp vụ chính
- Danh sách module/phân hệ và yêu cầu chức năng
- Ràng buộc phi chức năng đã biết (hiệu năng, bảo mật, hạ tầng…)

Không bịa số liệu. Nếu thiếu ngưỡng định lượng, viết `<Cần PO xác nhận>` để người
dùng điền, đừng tự đặt con số nghe hợp lý.

### Bước 3 — Viết file `content.json`

Tạo file JSON theo schema, đặt cạnh nơi sẽ xuất tài liệu (đường dẫn ảnh trong JSON
được hiểu là tương đối so với chính file JSON).

Tham khảo `examples/urd-example.json` — đây là bản mẫu đã đủ 6 chương và đủ 12 mục
phi chức năng, dùng làm điểm khởi đầu rồi thay nội dung.

Quy tắc khi viết:

- **Không tự gõ số thứ tự vào heading.** Word tự đánh `I.`, `I.1.`, `I.1.1.` theo
  style của mẫu. Viết `{"type":"h1","text":"TỔNG QUAN"}`, không viết `"I. TỔNG QUAN"`.
- Toàn bộ nội dung bằng tiếng Việt có dấu.
- Cột **Mô tả** của bảng yêu cầu chức năng phải đủ 5 khối, ngăn bằng `\n`:
  `Phát biểu yêu cầu:` / `Thông tin đầu vào:` / `Thông tin đầu ra:` /
  `Chức năng xử lý:` / `Các ngoại lệ:`.
- Mã yêu cầu (`UR01`, `UR02`, …) phải duy nhất và được tham chiếu lại ở chương
  Tiêu chuẩn nghiệm thu.
- Mỗi yêu cầu phải kiểm chứng được: có tiêu chí đo và ngưỡng cụ thể.
- Chỗ nào cần vẽ lưu đồ/sơ đồ mà chưa có ảnh: dùng block `note` để đánh dấu
  `[Chèn lưu đồ …]`, không bỏ trống im lặng.
- Khi phát hành bản chính thức, đặt `"showInstructions": false` để bỏ khối hướng dẫn
  dùng mẫu ở trang bìa.

### Bước 4 — Sinh file .docx

```bash
node .claude/skills/urd-docx/scripts/build-docx.js \
     <content.json> \
     .claude/skills/urd-docx/assets/BM03_URD_template.docx \
     <output.docx>
```

Chỉ cần `node`, không phải cài npm package nào.

### Bước 5 — Kiểm tra

Sau khi sinh, luôn kiểm lại trước khi báo cáo xong:

```bash
node .claude/skills/urd-docx/scripts/inspect-docx.js <output.docx> --check   # zip + XML hợp lệ
node .claude/skills/urd-docx/scripts/inspect-docx.js <output.docx>           # in lại cấu trúc
```

`inspect-docx.js` in ra toàn bộ heading, đoạn văn và bảng của file đã sinh. Đối chiếu
danh sách heading với `references/urd-structure.md` để xác nhận đủ 6 chương và đủ
12 mục phi chức năng, không thiếu mục nào.

Cùng script này cũng dùng để **phân tích ngược một file .docx mẫu khác** khi cần.

Báo cho người dùng: mở file bằng Word rồi nhấn **Ctrl+A → F9** để cập nhật số trang
trong mục lục (Word cũng tự hỏi khi mở, vì script đã bật `updateFields`).

## Những gì script tự lo, đừng viết tay

Trang bìa, bảng `Mã số / Phiên bản / Ngày hiệu lực`, bảng ký duyệt 4 vai trò,
trang **LỊCH SỬ THAY ĐỔI**, trang **MỤC LỤC** (trường TOC tự động) đều được sinh từ
`meta` / `approvals` / `history`. **Không** thêm các phần này vào mảng `body` —
`body` bắt đầu thẳng từ chương `TỔNG QUAN`.

Header (logo VNPT, mã dự án, phiên bản) và footer (mã tài liệu, `Trang x/y`) lấy
nguyên từ file mẫu, chỉ thay giá trị theo `meta`.

## Cập nhật một tài liệu đã sinh

Sửa lại `content.json` rồi chạy lại lệnh build — file .docx được ghi đè hoàn toàn.
Giữ `content.json` cạnh tài liệu và commit kèm, vì đó mới là nguồn để chỉnh sửa lần sau.
Nhớ thêm một dòng vào `history` mỗi lần tăng phiên bản.
