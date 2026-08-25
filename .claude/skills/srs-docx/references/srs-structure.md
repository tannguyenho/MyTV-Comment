# Cấu trúc chuẩn của tài liệu SRS (BM04_SRS)

Trích xuất từ mẫu gốc `04_BM04_SRS.docx`. Đây là bộ khung bắt buộc — được phép
**bổ sung** mục cho phù hợp dự án, nhưng **không được bỏ** mục nào; mục không áp dụng
thì ghi `N/A`.

SRS là bước sau URD: URD nói **người dùng cần gì**, SRS nói **phần mềm phải làm gì và
làm như thế nào**. Mọi yêu cầu trong SRS phải truy vết ngược được về một mã `URxx`
trong URD.

## Phần đầu (script `build-docx.js` tự sinh từ `meta` / `approvals` / `history`)

1. **Trang bìa**
   - `<Tên dự án>` — canh giữa, đậm, 18pt
   - `ĐẶC TẢ YÊU CẦU PHẦN MỀM` — đậm, 18pt
   - `SRS - Software Requirements Specification` — đậm, 13pt
   - Bảng 3×2: `Mã số` / `Phiên bản` / `Ngày hiệu lực`
   - Bảng ký duyệt 5×5: `Soạn thảo | Xem xét | Thẩm định | Phê chuẩn`
   - Khối `[Hướng dẫn sử dụng mẫu tài liệu]`
2. **LỊCH SỬ THAY ĐỔI** — bảng **7 cột** (khác URD, có thêm *Người xem xét*):
   `STT | Phiên bản | Người thực hiện | Người xem xét | Người phê duyệt | Ngày hiệu lực | Nội dung thay đổi`

   → phải khai `"historyColumns"` đủ 7 cột trong `content.json`.
3. **MỤC LỤC** — trường TOC tự động, cấp 1–5 (`"tocDepth": 5`).

## Thân tài liệu (bạn viết trong mảng `body`)

Heading tự đánh số: H1 = `I.`, H2 = `I.1.`, H3 = `I.1.1.`, H4 = `I.1.1.1.`, H5 = cấp 5.
→ **Không tự gõ số thứ tự vào text của heading.**

SRS lồng sâu tới 5 cấp, chú ý ánh xạ đúng:

```
h1  I.    TỔNG QUAN
h1  II.   NỘI DUNG
h2  II.1.     TỔNG QUAN HỆ THỐNG
h3  II.1.1.       Phát biểu bài toán
h2  II.2.     ĐẶC TẢ YÊU CẦU CHỨC NĂNG HỆ THỐNG
h3  II.2.1.       PHÂN HỆ 1
h4  II.2.1.1.        Module 1: <Quản trị hệ thống>
h5  II.2.1.1.1.        Mô tả tóm tắt / Yêu cầu giao diện / Chức năng 1 / Các tình huống sử dụng
```

### I. TỔNG QUAN  *(h1)*
- **I.1. Mục đích** *(h2)*
- **I.2. Phạm vi** *(h2)*
- **I.3. Tài liệu liên quan** *(h2)* — bảng `STT | Tên tài liệu | Tên file`.
  Bắt buộc liệt kê tài liệu URD tương ứng.
- **I.4. Giải thích từ ngữ và các chữ viết tắt** *(h2)* — bảng `Thuật ngữ | Ý nghĩa`.

### II. NỘI DUNG  *(h1)*

#### II.1. TỔNG QUAN HỆ THỐNG  *(h2)*
- **II.1.1. Phát biểu bài toán** *(h3)* — mô tả bài toán theo yêu cầu khách hàng.
- **II.1.2. Mục tiêu và phạm vi hệ thống** *(h3)* — mục tiêu, nơi triển khai, liệt kê
  các phân hệ chính. Có thể tóm tắt lại hoặc tham chiếu sang URD.
- **II.1.3. Mô hình hệ thống** *(h3)* — hai bảng chuẩn:

  *Mô hình phần mềm:* `STT | Mô hình sản phẩm | Số lớp ứng dụng | Lựa chọn`
  với 4 dòng cố định: Client/Server, Desktop Application, Web Application,
  Mobile Application. Cột *Lựa chọn* đánh dấu `x` cho mô hình áp dụng.

  *Mô hình công nghệ:* `STT | Loại công nghệ | Yêu cầu công nghệ | Bắt buộc`
  với 5 dòng cố định: Giao diện người dùng, Công nghệ xử lý, Công nghệ lưu trữ,
  Công nghệ bảo mật, Công nghệ cập nhật.

  Nếu đã có tài liệu TS (Đề xuất giải pháp) hoặc SAD (Thiết kế kiến trúc) thì
  ghi rõ tham chiếu sang.

#### II.2. ĐẶC TẢ YÊU CẦU CHỨC NĂNG HỆ THỐNG  *(h2)*

Đây là phần lõi, chiếm phần lớn dung lượng tài liệu. Cấu trúc lặp:

- **Phân hệ / Module lớn** *(h3)* — mở đầu bằng danh sách yêu cầu tính năng chung
  của phân hệ (gạch đầu dòng), có thể kèm sơ đồ chức năng.
  - **Module** *(h4)* — ví dụ `Module 1: <Quản trị hệ thống>`
    - **Mô tả tóm tắt** *(h5)* — module giải quyết việc gì, cho ai, ràng buộc chính.
    - **Yêu cầu giao diện** *(h5)* — mô tả màn hình, kèm ảnh mockup nếu có; liệt kê
      các trường dữ liệu (tên trường, kiểu, bắt buộc, quy tắc kiểm tra).
    - **Chức năng N: `<Tìm kiếm / Thêm mới / Sửa / Xoá / In…>`** *(h5)* — mỗi chức năng
      một mục.
    - **Các tình huống sử dụng** *(h5)* — với mỗi chức năng, liệt kê từng tình huống
      (`Tình huống 1: Tìm kiếm dữ liệu hợp lệ`, `Tình huống 2: … không hợp lệ`, …),
      mỗi tình huống kèm một bảng 5 cột:

      `STT | Đối tượng | Hoạt động | Thông tin đầu vào | Thông tin đầu ra`

      Mỗi dòng là một bước tương tác. **Bắt buộc có cả tình huống hợp lệ và tình huống
      ngoại lệ/không hợp lệ** — đây là điểm khác biệt cốt lõi so với URD.

#### II.3. YÊU CẦU PHI CHỨC NĂNG  *(h2)*
12 mục con *(h3)*, **đúng thứ tự này**, mỗi mục một bảng **3 cột** `Mã | Yêu cầu | Đặc tả`
(URD chỉ có 2 cột; cột *Đặc tả* của SRS ghi cách hiện thực / cách đo / cách kiểm chứng):

| # | Tiêu đề mục |
|---|---|
| II.3.1 | Yêu cầu bảo mật, phân quyền người sử dụng |
| II.3.2 | Yêu cầu sao lưu và phục hồi dữ liệu |
| II.3.3 | Yêu cầu về tính khả dụng (Usability) |
| II.3.4 | Yêu cầu về tính ổn định (Reliability) |
| II.3.5 | Yêu cầu về hiệu năng (Performance) |
| II.3.6 | Yêu cầu về tính hỗ trợ (Supportability) |
| II.3.7 | Yêu cầu các ràng buộc thiết kế (Design constraints) |
| II.3.8 | Yêu cầu về giao tiếp (Interfaces) |
| II.3.9 | Các yêu cầu về tài liệu người dùng và hỗ trợ trực tuyến |
| II.3.10 | Các thành phần mua ngoài |
| II.3.11 | Các yêu cầu pháp lý, bản quyền và ghi chú khác |
| II.3.12 | Các tiêu chuẩn áp dụng |

Mục **II.3.8 Giao tiếp** có 6 dòng con:
1. Giao tiếp chung (protocols, ports, logical addresses)
2. Giao tiếp người dùng (User interfaces)
3. Giao tiếp phần cứng (Hardware interfaces)
4. Giao tiếp phần mềm — phần mềm dùng để xây dựng hệ thống
5. Giao tiếp phần mềm — giữa các chức năng bên trong hệ thống
6. Giao tiếp phần mềm — phần mềm bên ngoài & giao tiếp truyền thông

#### II.4. ĐIỀU KIỆN NGHIỆM THU HỆ THỐNG  *(h2)*
Danh sách đánh số các điều kiện. Khác URD (chấp nhận > 90% yêu cầu ưu tiên 1), SRS
yêu cầu đáp ứng **toàn bộ** yêu cầu chức năng ghi nhận trong tài liệu.

### III. PHỤ LỤC  *(h1)*
Bảng ma trận truy vết URD → SRS, danh mục màn hình, từ điển dữ liệu, mockup, mã lỗi…
Nếu không có: ghi `N/A`.

## Nguyên tắc viết nội dung

- Toàn bộ tiếng Việt có dấu.
- Mã yêu cầu SRS đặt dạng `SRS_<PHÂNHỆ>_<số>` (ví dụ `SRS_CMT_01`) và mỗi mã phải có
  cột/ghi chú truy vết về mã `URxx` tương ứng trong URD.
- Đặc tả phải đủ chi tiết để lập trình viên hiện thực và tester viết được test case:
  nêu rõ trường dữ liệu, kiểu, bắt buộc/không, quy tắc kiểm tra, thông báo lỗi.
- Mỗi chức năng phải có ít nhất một tình huống ngoại lệ.
- Mục nào không áp dụng: điền `N/A`, không xoá mục.
