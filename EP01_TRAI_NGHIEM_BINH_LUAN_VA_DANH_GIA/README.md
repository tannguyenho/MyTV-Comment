# EP01 — TRẢI NGHIỆM BÌNH LUẬN VÀ ĐÁNH GIÁ

## 1. Thông tin Epic

| Thuộc tính | Nội dung |
|---|---|
| Epic ID | EP01 |
| Tên Epic | Trải nghiệm bình luận và đánh giá |
| Mục tiêu | Cho phép người xem khám phá thảo luận, đánh giá nội dung và tự quản lý bình luận của mình một cách rõ ràng, liên tục trên web/mobile |
| Đối tượng | Người xem chưa đăng nhập; người dùng đã đăng nhập |
| Giá trị kinh doanh | Tăng tương tác với phim, hỗ trợ người xem ra quyết định xem và tạo nền tảng cho cộng đồng MyTV |
| Phạm vi | Phim lẻ và phim bộ, bình luận ở cấp phim, trong giai đoạn Phim truyện |

## 2. Kết quả mong đợi

- Người chưa đăng nhập vẫn đọc được các bình luận đang Hiển thị.
- Người dùng hiểu rõ mình đang xem hoặc viết bình luận cho bộ phim nào.
- Người dùng có thể đánh giá, đăng, sửa và xóa nội dung của chính mình.
- Số lượng, điểm đánh giá và trạng thái bình luận được cập nhật nhất quán.
- Nội dung Spoiler và **mốc thời gian trong phim** được hiển thị an toàn, đúng ngữ cảnh.
- MVP không triển khai frame/clip trong bình luận; timestamp là cơ chế ngữ cảnh theo cảnh hiện tại.

## 3. Chỉ số gợi ý

- Tỷ lệ người xem mở/đọc khu vực bình luận.
- Tỷ lệ người xem đăng nhập sau khi chọn thao tác tương tác.
- Tỷ lệ người xem gửi đánh giá hoặc bình luận.
- Tỷ lệ gửi bình luận thành công.
- Tỷ lệ lỗi khi chuyển ngữ cảnh giữa các phim.
- Thời gian cập nhật số lượng bình luận và điểm đánh giá.

---

## Danh sách User Story

| ID | User Story | File |
|---|---|---|
| US01 | Đọc khu vực bình luận | [US01](US01_DOC_KHU_VUC_BINH_LUAN.md) |
| US02 | Xem bình luận, số lượng và sắp xếp | [US02](US02_XEM_BINH_LUAN_SO_LUONG_VA_SAP_XEP.md) |
| US03 | Đánh giá phim | [US03](US03_DANH_GIA_PHIM.md) |
| US04 | Đăng bình luận | [US04](US04_DANG_BINH_LUAN.md) |
| US05 | Sửa và xóa bình luận | [US05](US05_SUA_VA_XOA_BINH_LUAN.md) |
| US06 | Bình luận kèm mốc thời gian | [US06](US06_BINH_LUAN_KEM_MOC_THOI_GIAN.md) |

[← Quay lại backlog tổng](../README.md)

## 4. Điều kiện hoàn thành Epic

- Sáu User Story đạt acceptance criteria theo phạm vi phát hành đã chọn.
- Web/mobile hiển thị nhất quán theo thiết kế được duyệt.
- Dữ liệu giữa các phim không bị trộn lẫn.
- Quyền đọc, đăng, sửa và xóa được kiểm tra ở cả giao diện và API.
- Các sự kiện chính có tracking phục vụ US19.
- Các quyết định PO đã chốt phải được phản ánh đồng nhất ở US, Acceptance Criteria và Test Cases.
