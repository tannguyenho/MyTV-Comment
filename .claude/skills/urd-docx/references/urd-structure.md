# Cấu trúc chuẩn của tài liệu URD (BM03_URD)

Trích xuất từ mẫu gốc `03_BM03_URD.docx`. Đây là bộ khung bắt buộc — được phép
**bổ sung** mục cho phù hợp dự án, nhưng **không được bỏ** mục nào; mục không áp dụng
thì ghi `N/A`.

## Phần đầu (script `build-docx.js` tự sinh từ `meta` / `approvals` / `history`)

1. **Trang bìa**
   - `<Tên dự án>` — canh giữa, đậm, 18pt
   - `TÀI LIỆU ĐẶC TẢ YÊU CẦU NGƯỜI SỬ DỤNG` — đậm, 18pt
   - `URD - User Requirement Description` — đậm, 13pt
   - Bảng 3×2: `Mã số` / `Phiên bản` / `Ngày hiệu lực`
   - Bảng ký duyệt 5×5: cột `Họ và tên | Chức danh | Ngày, tháng | Ký tên`;
     hàng `Soạn thảo | Xem xét | Thẩm định | Phê chuẩn`
   - Khối `[Hướng dẫn sử dụng mẫu tài liệu]` — xoá khi phát hành bản chính thức
     (`"showInstructions": false`)
2. **LỊCH SỬ THAY ĐỔI** — bảng 6 cột:
   `STT | Phiên bản | Người thực hiện | Người phê duyệt | Ngày hiệu lực | Nội dung thay đổi`
   (URD dùng 6 cột, khác SRS dùng 7 cột)
3. **MỤC LỤC** — trường TOC tự động, cấp 1–3

## Thân tài liệu (bạn viết trong mảng `body`)

Heading tự đánh số theo style của mẫu: H1 = `I.`, H2 = `I.1.`, H3 = `I.1.1.`
→ **Không tự gõ số thứ tự vào text của heading.**

### I. TỔNG QUAN  *(h1)*
- **I.1. Mục đích** *(h2)* — mục đích viết tài liệu, giải quyết vấn đề gì.
- **I.2. Phạm vi** *(h2)* — phạm vi ảnh hưởng tới phòng ban/đơn vị nào.
- **I.3. Tài liệu liên quan** *(h2)* — bảng `STT | Tên tài liệu | Tên file`.
- **I.4. Giải thích từ ngữ và các chữ viết tắt** *(h2)* — bảng `Thuật ngữ | Ý nghĩa`.

### II. TỔNG QUAN HỆ THỐNG  *(h1)*
- **II.1. Mục tiêu hệ thống** *(h2)* — bảng
  `STT | Mã mục tiêu | Tên mục tiêu | Đối tượng liên quan | Mức độ ưu tiên`.
- **II.2. Đối tượng người dùng của hệ thống** *(h2)* — sơ đồ ngữ cảnh (ảnh) + bảng
  `STT | Tên đối tượng | Mô tả | Tương tác với hệ thống (Vào / Ra) | Lợi ích mong đợi`.
  Cột "Tương tác với hệ thống" là **header 2 tầng**: dùng `colspan: 2` ở hàng 1 và
  `rowspan: 2` cho các cột còn lại (xem `examples/urd-example.json`).

### III. QUY TRÌNH NGHIỆP VỤ  *(h1)*
- **III.1. Quy trình nghiệp vụ tổng thể** *(h2)* — lưu đồ workflow (ảnh) nêu rõ đầu vào,
  đầu ra, các bước; kèm bảng
  `Mã bước thực hiện | Tên bước | Người thực hiện | Diễn giải bước thực hiện`.

  Quy ước mã bước (bắt buộc giữ nguyên trong tài liệu):
  - `<Viết tắt quy trình>.xx.<Tên bước>`, với `xx` từ 01–99.
  - Quy trình con mang cả mã quy trình mẹ: `<Viết tắt quy trình>.xx.yy.<Tên bước con>`.
- **III.2. Quy trình nghiệp vụ chi tiết** *(h2)* — mỗi quy trình một *(h3)*, mỗi mục gồm
  lưu đồ chi tiết + bảng mô tả bước + (nếu cần) bảng yêu cầu chung
  `STT | Mã yêu cầu | Tên yêu cầu | Mô tả yêu cầu | Mức độ ưu tiên | Đối tượng có liên quan`.

### IV. YÊU CẦU CHỨC NĂNG  *(h1)*
Mở đầu bằng sơ đồ cây chức năng tổng thể (tree view hoặc business use-case model).
Mỗi module/phân hệ là một *(h2)*, gồm sơ đồ chức năng + bảng 7 cột:

`STT | Mã yêu cầu | Tên yêu cầu | Mô tả | Mức độ ưu tiên | Mức độ quan trọng | Đối tượng liên quan`

Cột **Mô tả** bắt buộc đủ 5 khối, mỗi khối một dòng (`\n` trong JSON):

```
Phát biểu yêu cầu: ...
Thông tin đầu vào: ...
Thông tin đầu ra: ...
Chức năng xử lý: ...
Các ngoại lệ: ...
```

Mã yêu cầu đánh theo dạng `UR01`, `UR02`, … và phải duy nhất trong toàn tài liệu
(mục VI tham chiếu ngược lại các mã này).

### V. CÁC YÊU CẦU PHI CHỨC NĂNG  *(h1)*
12 mục con *(h2)*, **theo đúng thứ tự này**, mỗi mục là một bảng 2 cột `Mã | Yêu cầu`:

| # | Tiêu đề mục |
|---|---|
| V.1 | Yêu cầu bảo mật, phân quyền người sử dụng |
| V.2 | Yêu cầu sao lưu và phục hồi dữ liệu |
| V.3 | Yêu cầu về tính khả dụng (Usability) |
| V.4 | Yêu cầu về tính ổn định (Reliability) |
| V.5 | Yêu cầu về hiệu năng (Performance) |
| V.6 | Yêu cầu về tính hỗ trợ (Supportability) |
| V.7 | Yêu cầu các ràng buộc thiết kế (Design constraints) |
| V.8 | Yêu cầu về giao tiếp (Interfaces) |
| V.9 | Các yêu cầu về tài liệu người dùng và hỗ trợ trực tuyến |
| V.10 | Các thành phần mua ngoài |
| V.11 | Các yêu cầu pháp lý, bản quyền và ghi chú khác |
| V.12 | Các tiêu chuẩn áp dụng |

Mục **V.8 Giao tiếp** có 6 dòng con, mỗi dòng một loại giao tiếp:
1. Giao tiếp chung (protocols, ports, logical addresses)
2. Giao tiếp người dùng (User interfaces) — font, độ phân giải, định dạng ngày `dd/mm/yyyy`, định dạng số
3. Giao tiếp phần cứng (Hardware interfaces) — cấu hình máy chủ / máy trạm
4. Giao tiếp phần mềm — phần mềm dùng để xây dựng hệ thống
5. Giao tiếp phần mềm — giao tiếp giữa các module bên trong hệ thống
6. Giao tiếp phần mềm — phần mềm bên ngoài & giao tiếp truyền thông (Communication interfaces)

Gợi ý đánh mã: `UR_NF_01`, `UR_NF_02`, … hoặc theo nhóm `SEC_01`, `PERF_01`.

### VI. TIÊU CHUẨN NGHIỆM THU (*)  *(h1)*
Mô tả quy trình và điều kiện nghiệm thu, dạng danh sách đánh số. Phải nêu ngưỡng
định lượng (ví dụ: đáp ứng > 90% yêu cầu ưu tiên 1 ở mục IV), việc hiệu chỉnh sau
triển khai thử nghiệm, đào tạo người dùng, và bàn giao tài liệu + mã nguồn.

## Nguyên tắc viết nội dung

- Toàn bộ tiếng Việt có dấu.
- Giữ nguyên cách dùng ngoặc của mẫu: `<...>` là chỗ điền, `[...]` là ghi chú hướng dẫn.
  Khi phát hành bản thật thì thay hết bằng nội dung dự án.
- Mỗi yêu cầu phải **kiểm chứng được** (có tiêu chí đo, có ngưỡng), không viết chung chung.
- Mục nào không áp dụng: điền `N/A`, không xoá mục.
- Mức độ ưu tiên / quan trọng dùng thang `Cao | Trung bình | Thấp` (hoặc `1 | 2 | 3`) và
  dùng nhất quán trong cả tài liệu.
