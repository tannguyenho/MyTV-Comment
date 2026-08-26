# UX User Flows — MyTV Comment

**Phiên bản:** 2.0 · **Ngày:** 19/08/2026  
**Trạng thái:** Đã tách flow theo từng User Story sau vòng review UX C170–C265.

> File này chỉ còn là **index + nguyên tắc dùng chung**. Flow chi tiết nằm trong `USxx_USER_FLOW.md` cạnh User Story tương ứng trong từng Epic.

## Nguyên tắc UX dùng chung

1. **Mở để đọc — đăng nhập để tương tác.** Login quay lại đúng context nhưng không auto-execute action cũ.
2. Comment là **tab riêng** trong trang nội dung. Phim bộ mặc định `Danh sách tập`; phim lẻ mặc định `Đề xuất`; user chủ động mở `Bình luận ({count})`. Đổi tập **không** reload khu vực bình luận vì bình luận thuộc về bộ phim. Deep link comment/thread active thẳng tab Bình luận.
3. **Comment và rating ở cấp phim.** Mỗi bộ phim có duy nhất một khu vực bình luận và một điểm đánh giá, dùng chung cho mọi tập nếu là phim bộ. CMS cấu hình ở cấp phim.
4. Effective Visibility Resolver là source of truth cho render/deep link/fallback.
5. Scope Đóng giữ tab `Bình luận` nhưng bỏ count, hiển thị `Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau` và ẩn list/composer/actions (rating **không** bị ẩn — xem US03 AC11).
6. Phone composer = thanh nhập inline cố định đáy màn hình (nở lên khi bàn phím bật); Web = inline; Smart TV không tạo Comment/Reply/Mention/Chia sẻ, không Sửa/Xóa, không đổi Sort, không chấm sao, không reveal Spoiler và không Timestamp seek — TV chỉ đọc (gồm thread chỉ đọc), Like/Unlike và Báo cáo bình luận.
7. SmartTV hướng dẫn + QR để chuyển sang smartphone khi muốn tham gia bình luận.
8. WCAG 2.1 AA; touch target ≥44×44pt; focus/keyboard/remote navigation phải rõ; state không chỉ dùng màu.
9. CMS moderation chỉ thiết kế **Web/Desktop**.
10. **Ma trận nền tảng đã chốt:** Phone và Web áp dụng US01–US10, US17, US18; **Smart TV chỉ áp dụng US01, US07, US10, US17**; US11–US16, US19, US20 thuộc CMS/quản trị và do backend áp dụng phía sau, không phát sinh chức năng mới trên app người dùng.

## Index 20 User Flow

### EP01 — Trải nghiệm bình luận và đánh giá
- [US01 — Đọc khu vực bình luận](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US01_USER_FLOW.md)
- [US02 — Số lượng và sắp xếp bình luận](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US02_USER_FLOW.md)
- [US03 — Đánh giá phim 5 sao](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US03_USER_FLOW.md)
- [US04 — Đăng bình luận](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US04_USER_FLOW.md)
- [US05 — Sửa và xóa bình luận](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US05_USER_FLOW.md)
- [US06 — Timestamp (chỉ phim lẻ)](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US06_USER_FLOW.md)

### EP02 — Tương tác cộng đồng
- [US07 — Like/Unlike](EP02_TUONG_TAC_CONG_DONG/US07_USER_FLOW.md)
- [US08 — Reply một cấp](EP02_TUONG_TAC_CONG_DONG/US08_USER_FLOW.md)
- [US09 — Mention/Notification](EP02_TUONG_TAC_CONG_DONG/US09_USER_FLOW.md)

### EP03 — An toàn và kiểm duyệt
- [US10 — Report](EP03_AN_TOAN_VA_KIEM_DUYET/US10_USER_FLOW.md)
- [US11 — AI moderation](EP03_AN_TOAN_VA_KIEM_DUYET/US11_USER_FLOW.md)
- [US12 — State/Visibility](EP03_AN_TOAN_VA_KIEM_DUYET/US12_USER_FLOW.md)

### EP04 — CMS quản trị bình luận
- [US13 — CMS Search/Queue](EP04_CMS_QUAN_TRI_BINH_LUAN/US13_USER_FLOW.md)
- [US14 — CMS Moderation](EP04_CMS_QUAN_TRI_BINH_LUAN/US14_USER_FLOW.md)
- [US15 — Pin/Config](EP04_CMS_QUAN_TRI_BINH_LUAN/US15_USER_FLOW.md)
- [US16 — Sanction/Appeal](EP04_CMS_QUAN_TRI_BINH_LUAN/US16_USER_FLOW.md)

### EP05 — Tăng trưởng và phân tích
- [US17 — Badge](EP05_TANG_TRUONG_VA_PHAN_TICH/US17_USER_FLOW.md)
- [US18 — Share](EP05_TANG_TRUONG_VA_PHAN_TICH/US18_USER_FLOW.md)
- [US19 — Analytics](EP05_TANG_TRUONG_VA_PHAN_TICH/US19_USER_FLOW.md)
- [US20 — AI Ops](EP05_TANG_TRUONG_VA_PHAN_TICH/US20_USER_FLOW.md)

## Review result

Các UX decision đã hỏi trong vòng review hiện tại đã được đưa vào flow tương ứng. Điểm blocker cũ **Nickname AI timeout** đã chốt fail-safe: nickname mới không đổi/public khi AI không có decision hợp lệ; giữ old/fallback, cho retry và không tiêu quota.
