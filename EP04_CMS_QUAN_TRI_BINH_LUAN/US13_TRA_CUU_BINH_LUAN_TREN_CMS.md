# US13 — Tra cứu bình luận trên CMS

> Thuộc EP04 — CMS quản trị bình luận
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là Admin/Moderator**, tôi muốn xem, tìm kiếm, lọc và export dữ liệu bình luận, để nhanh chóng xác định nội dung cần xử lý hoặc điều tra.

### Ưu tiên

**Must**

### Acceptance Criteria

1. Admin/Moderator xem được comment/reply trong phạm vi CMS được cấp.
2. Mỗi record có tối thiểu: nội dung, tác giả, phim/series, tập, thời gian, state, Like, Reply, Report, AI risk và thời gian chờ nếu đang moderation.
3. Search theo keyword, nickname/account và định danh user được hỗ trợ.
4. Filter theo phim/tập/thời gian/state/AI label/Report/Spoiler và có thể kết hợp nhiều filter.
5. Moderation queue mặc định sắp **risk cao trước**; trong cùng mức risk, item **cũ hơn/chờ lâu hơn trước**.
6. Item sắp/quá SLA được hiển thị rõ và tham gia ưu tiên queue theo US14.
7. Chi tiết record cho xem thread, version history, AI result, Report/Flag và lịch sử moderation.
8. Mọi Admin/Moderator có quyền truy cập CMS bình luận được xem **PII đầy đủ cần thiết** của user trong phạm vi được cấp; không tách permission PII riêng.
9. CMS hỗ trợ export **CSV + XLSX** theo filter hiện tại.
10. File export **mặc định không kèm PII đầy đủ**. Admin phải chủ động tick lựa chọn “Bao gồm PII” trước khi export nếu cần.
11. Export có PII phải ghi nhận actor/time/filter và cờ include-PII trong audit/log truy cập phù hợp.
12. Pagination/export không lặp/bỏ sót dữ liệu và phản ánh state theo độ trễ vận hành.

### Quy tắc nghiệp vụ

- Quyền truy cập CMS vẫn giới hạn theo phạm vi Admin/Moderator; trong phạm vi đó họ được xem PII đầy đủ theo quyết định PO.
- Export PII cần opt-in rõ ràng để hạn chế việc PII bị đưa ra file ngoài ý muốn.
- Search/filter không làm thay đổi dữ liệu.
- Nickname không tạo hàng chờ CMS vì không còn trạng thái Chờ duyệt cho nickname (xem US04/US11) — CMS chỉ tra cứu comment/reply.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục Bảo mật — IDOR, kiểm soát scope theo phạm vi được cấp.*

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US13-001 | Authorization | Admin có scope P1, Moderator scope P2 | Mở danh sách | Mỗi user chỉ thấy phạm vi được cấp. |
| TC-US13-002 | Default order | Queue có High/Medium/Low và nhiều created time | Mở queue | Risk cao đứng trước; cùng risk thì item cũ hơn trước. |
| TC-US13-003 | Search/filter | Có dữ liệu nhiều phim/state | Search + filter kết hợp | Kết quả thỏa tất cả điều kiện, không lẫn scope. |
| TC-US13-004 | Detail | C1 có thread/version/AI/Report | Mở chi tiết | Hiển thị đủ context trước khi xử lý. |
| TC-US13-005 | PII view | Admin/Moderator có quyền CMS | Mở hồ sơ user trong scope | Có thể xem PII đầy đủ cần thiết theo quyết định PO. |
| TC-US13-006 | Export default | Có filter hiện tại | Export CSV/XLSX không tick PII | File đúng filter và không chứa PII đầy đủ. |
| TC-US13-007 | Export PII opt-in | Tick “Bao gồm PII” | Export CSV/XLSX | File có PII theo quyền; log ghi actor/time/filter/include-PII. |
| TC-US13-008 | Pagination | Kết quả >1 trang | Paginate/lazy load | Không trùng/bỏ sót và thứ tự ổn định. |
| TC-US13-009 | SLA visibility | Có item sắp/quá SLA | Mở queue | Hiển thị badge/thời gian chờ phù hợp để Admin ưu tiên. |
| TC-US13-010 | IDOR ghi (write) | Moderator M2 chỉ có scope P2; biết trước comment ID C1 (thuộc phim P1) và user ID U1 (thuộc phim P1) | M2 gọi TRỰC TIẾP API (không qua UI) để: xem chi tiết C1; Duyệt/Ẩn/Xóa/Undo C1; bulk chứa C1; xem PII của U1; export PII với filter P1; ghim C1 (US15); áp Cảnh báo/Khóa bình luận/Khóa tài khoản lên U1 (US16) | Tất cả bị từ chối theo scope; không lộ sự tồn tại của C1/U1 qua mã lỗi hoặc metadata; không tạo audit event "thành công" cho bất kỳ thao tác nào. |
