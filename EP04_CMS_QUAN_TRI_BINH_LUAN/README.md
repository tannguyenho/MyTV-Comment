# EP04 — CMS QUẢN TRỊ BÌNH LUẬN

## 1. Thông tin Epic

| Thuộc tính | Nội dung |
|---|---|
| Epic ID | EP04 |
| Tên Epic | CMS quản trị bình luận |
| Mục tiêu | Cung cấp cho Admin một không gian làm việc tập trung để tra cứu, kiểm duyệt, cấu hình và xử lý người dùng vi phạm |
| Đối tượng | Admin kiểm duyệt; Admin vận hành; quản lý có quyền xem báo cáo/audit |
| Giá trị kinh doanh | Giảm thời gian xử lý, đảm bảo thực thi chính sách nhất quán và minh bạch hóa hoạt động quản trị |
| Phạm vi | Danh sách/tìm kiếm/lọc, thao tác nội dung, Report/Flag/Spoiler, ghim, cấu hình theo phim, xử lý tài khoản và audit log |

## 2. Kết quả mong đợi

- Admin tìm được đúng bình luận cần xử lý trong thời gian ngắn.
- Admin thấy đủ ngữ cảnh trước khi ra quyết định.
- Các hành động kiểm duyệt và xử lý tài khoản được phân quyền, xác nhận và lưu dấu vết.
- Cấu hình mở/đóng và cơ chế kiểm duyệt được áp dụng chính xác theo phim.
- CMS hỗ trợ vận hành hàng ngày mà không cần can thiệp trực tiếp vào dữ liệu.

## 3. Chỉ số gợi ý

- Thời gian trung bình từ lúc bình luận vào hàng chờ đến khi được xử lý.
- Thời gian trung bình xử lý Report.
- Số bình luận xử lý trên mỗi Admin/ca vận hành.
- Tỷ lệ quyết định bị thay đổi hoặc hoàn tác.
- Tỷ lệ thao tác CMS có audit đầy đủ.
- Số lỗi cấu hình theo phim.

---


## Danh sách User Story

| ID | User Story | File |
|---|---|---|
| US13 | Tra cứu bình luận trên CMS | [US13](US13_TRA_CUU_BINH_LUAN_TREN_CMS.md) |
| US14 | Xử lý nội dung trên CMS | [US14](US14_XU_LY_NOI_DUNG_TREN_CMS.md) |
| US15 | Quản lý bình luận ghim và cấu hình theo phim | [US15](US15_QUAN_LY_BINH_LUAN_GHIM_VA_CAU_HINH_THEO_PHIM.md) |
| US16 | Quản lý người dùng vi phạm và audit log | [US16](US16_QUAN_LY_NGUOI_DUNG_VI_PHAM_VA_AUDIT_LOG.md) |

[← Quay lại backlog tổng](../README.md)

## 4. Điều kiện hoàn thành Epic

- CMS hỗ trợ đầy đủ tra cứu, xử lý, cấu hình và quản lý vi phạm theo quyền.
- Admin luôn thấy đủ ngữ cảnh trước khi ra quyết định.
- Không có thao tác quản trị quan trọng thiếu audit.
- Xung đột thao tác đồng thời được phát hiện hoặc ngăn chặn.
- Dữ liệu cá nhân chỉ hiển thị cho vai trò phù hợp.
- Cấu hình trên CMS được phản ánh đúng trên ứng dụng người dùng.
