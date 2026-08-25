---
name: srs-docx
description: Tạo tài liệu SRS (Đặc tả yêu cầu phần mềm) dạng file .docx theo đúng mẫu BM04_SRS của VNPT/Tổng công ty Truyền thông — giữ nguyên trang bìa, bảng ký duyệt, lịch sử thay đổi 7 cột, mục lục tự động 5 cấp, header có logo và footer "Mã số tài liệu / Trang x/y". Dùng khi người dùng yêu cầu viết, sinh, xuất hoặc cập nhật tài liệu SRS / "đặc tả yêu cầu phần mềm" / BM04, hoặc muốn chuyển một tài liệu URD thành SRS.
---

# Tạo tài liệu SRS (BM04_SRS) dạng .docx

## Quy trình

### Bước 1 — Đọc cấu trúc chuẩn

Đọc `references/srs-structure.md` để nắm bộ khung 3 chương (trong đó chương II lồng
tới 5 cấp heading) và nội dung từng mục. **Không được bỏ mục nào**; mục không áp dụng
thì điền `N/A`.

Đọc `references/content-schema.md` để nắm schema của file JSON đầu vào (các loại
block, cách khai bảng, gộp ô, chèn ảnh).

### Bước 2 — Thu thập thông tin dự án

SRS là bước sau URD. **Nếu dự án đã có tài liệu URD, hãy đọc nó trước** — SRS phải
truy vết ngược được về các mã `URxx` trong URD.

Xác định:

- Tên dự án, mã dự án, mã tài liệu, phiên bản, ngày hiệu lực
- Người soạn thảo / xem xét / thẩm định / phê chuẩn
- Phát biểu bài toán, mục tiêu, mô hình phần mềm và mô hình công nghệ
- Danh sách phân hệ → module → chức năng
- Với mỗi chức năng: các trường dữ liệu, quy tắc kiểm tra, tình huống hợp lệ và
  tình huống ngoại lệ
- Ràng buộc phi chức năng cùng **cách kiểm chứng** (cột *Đặc tả*)

Nếu người dùng chưa cung cấp, lấy từ tài liệu sẵn có trong repo (URD, README,
ARCHITECTURE, BACKLOG, user story…), rồi hỏi bổ sung **một lần** những gì thực sự
không suy ra được. Không bịa số liệu — thiếu ngưỡng thì ghi `<Cần PO xác nhận>`.

### Bước 3 — Viết file `content.json`

Tạo file JSON theo schema, đặt cạnh nơi sẽ xuất tài liệu (đường dẫn ảnh trong JSON
được hiểu là tương đối so với chính file JSON).

Tham khảo `examples/srs-example.json` — bản mẫu đã đủ 3 chương, đủ 12 mục phi chức
năng và có ma trận truy vết ở phụ lục.

Quy tắc khi viết:

- **Không tự gõ số thứ tự vào heading.** Word tự đánh `I.` … `I.1.1.1.1.`
- **Bắt buộc** khai `historyColumns` đủ 7 cột và `"tocDepth": 5`
  (SRS khác URD ở hai điểm này):

  ```json
  "historyColumns": ["STT", "Phiên bản", "Người thực hiện", "Người xem xét",
                     "Người phê duyệt", "Ngày hiệu lực", "Nội dung thay đổi"],
  "tocDepth": 5
  ```

- Ánh xạ heading đúng độ sâu: `h2` = phần lớn (Tổng quan hệ thống / Đặc tả chức năng /
  Phi chức năng / Điều kiện nghiệm thu), `h3` = phân hệ, `h4` = module,
  `h5` = Mô tả tóm tắt / Yêu cầu giao diện / Chức năng N / Các tình huống sử dụng.
- Bảng phi chức năng của SRS có **3 cột** `Mã | Yêu cầu | Đặc tả` (URD chỉ 2 cột).
  Cột *Đặc tả* ghi cách hiện thực, cách đo hoặc cách kiểm chứng — không được để trống.
- Mỗi chức năng phải có **ít nhất một tình huống ngoại lệ**, ngoài tình huống hợp lệ.
  Bảng tình huống: `STT | Đối tượng | Hoạt động | Thông tin đầu vào | Thông tin đầu ra`.
- Mã yêu cầu đặt dạng `SRS_<PHÂNHỆ>_<số>` và ghi rõ truy vết về mã `URxx`.
- Đặc tả phải đủ để lập trình viên hiện thực và tester viết test case: nêu tên trường,
  kiểu, bắt buộc/không, quy tắc kiểm tra, thông báo lỗi.
- Chỗ cần mockup/sơ đồ mà chưa có ảnh: dùng block `note` đánh dấu `[Chèn ảnh …]`.
- Phát hành bản chính thức: đặt `"showInstructions": false`.

### Bước 4 — Sinh file .docx

```bash
node .claude/skills/srs-docx/scripts/build-docx.js \
     <content.json> \
     .claude/skills/srs-docx/assets/BM04_SRS_template.docx \
     <output.docx>
```

Chỉ cần `node`, không phải cài npm package nào.

### Bước 5 — Kiểm tra

```bash
node .claude/skills/srs-docx/scripts/inspect-docx.js <output.docx> --check   # zip + XML hợp lệ
node .claude/skills/srs-docx/scripts/inspect-docx.js <output.docx>           # in lại cấu trúc
```

Đối chiếu danh sách heading in ra với `references/srs-structure.md`, xác nhận:
đủ 12 mục phi chức năng, mỗi module có đủ 4 mục `h5`, mỗi chức năng có tình huống
ngoại lệ, và phụ lục có ma trận truy vết.

Báo cho người dùng: mở file bằng Word rồi nhấn **Ctrl+A → F9** để cập nhật số trang
trong mục lục.

## Những gì script tự lo, đừng viết tay

Trang bìa, bảng `Mã số / Phiên bản / Ngày hiệu lực`, bảng ký duyệt 4 vai trò,
trang **LỊCH SỬ THAY ĐỔI**, trang **MỤC LỤC** đều sinh từ `meta` / `approvals` /
`history` / `historyColumns`. **Không** thêm các phần này vào `body` — `body` bắt đầu
thẳng từ chương `TỔNG QUAN`.

Header (logo VNPT, mã dự án, phiên bản) và footer (mã tài liệu, dấu `NỘI BỘ`,
`Trang x/y`) lấy nguyên từ file mẫu, chỉ thay giá trị theo `meta`.

## Cập nhật một tài liệu đã sinh

Sửa `content.json` rồi chạy lại lệnh build — file .docx được ghi đè hoàn toàn.
Giữ `content.json` cạnh tài liệu và commit kèm, vì đó mới là nguồn để chỉnh sửa lần sau.
Nhớ thêm một dòng vào `history` mỗi lần tăng phiên bản.
