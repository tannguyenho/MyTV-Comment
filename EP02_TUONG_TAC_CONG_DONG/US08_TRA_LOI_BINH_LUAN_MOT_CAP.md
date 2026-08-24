# US08 — Trả lời bình luận một cấp

> Thuộc EP02 — Tương tác cộng đồng
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là người dùng đã đăng nhập**, tôi muốn trả lời trực tiếp một bình luận, để tham gia cuộc trò chuyện mà vẫn giữ cấu trúc hội thoại dễ theo dõi.

### Ưu tiên

**Must**

### Acceptance Criteria

1. User có thể Reply một comment gốc đang Hiển thị và cho phép tương tác.
2. Reply luôn được lưu ở **một cấp** dưới root comment; khi trả lời một reply, dữ liệu mới vẫn thuộc root và UI có thể mention người được trả lời để giữ ngữ cảnh.
3. Reply hỗ trợ text, emoji, Spoiler và timestamp theo cùng rule content của comment.
4. Reply tối thiểu **1 ký tự hợp lệ hoặc 1 emoji**, tối đa **1000 ký tự**; emoji-only hợp lệ.
5. URL trong reply chỉ hợp lệ với `mytv.com.vn` hoặc subdomain hợp lệ; áp dụng cùng hostname validation US04.
6. Comment + reply dùng chung rate limit **5 nội dung/1 phút/user**.
7. Reply đi qua cùng moderation theo US11.
8. Reply công khai làm tăng tổng số bình luận; reply Chờ duyệt/Từ chối/Ẩn/Xóa không làm tăng số công khai.
9. Danh sách root **không hiển thị reply nào**; root có reply chỉ hiện lối vào `{n} phản hồi` (US02 AC11). Khi mở màn **Phản hồi**, hệ thống tải **3 reply đầu**, phần còn lại tải bằng nút `Xem thêm {n} phản hồi` theo AC10.
10. Xóa một reply riêng lẻ làm reply biến mất hoàn toàn khỏi UI, **không để placeholder**.
11. Root không còn public thì thread không được hiển thị độc lập khỏi root. **Admin Ẩn root** làm toàn thread tạm không public nhưng không đổi moderation state của reply (reply chỉ mang cờ `hidden_by_root_cascade`, không có đồng hồ retention riêng); Undo Ẩn root làm các reply hợp lệ hiện lại theo state riêng, với điều kiện **root còn trong 90 ngày retention**.
12. Nếu tác giả root bị **Account Lock**, root và toàn bộ thread tạm không public; reply của user khác **không bị đổi moderation state/không bị coi là vi phạm**. Khi root author được mở khóa, thread hiện lại nếu từng item vẫn hợp lệ.
13. Nếu user **self-delete root**, root + toàn bộ reply bị cascade soft-delete theo US05; reply chỉ mang cờ ẩn theo cascade, không có retention riêng — toàn bộ retention 90 ngày tính theo root. Nếu CMS/Admin Xóa mềm root, thread không public và root + toàn bộ reply bị ẩn do cascade có thể được Undo cùng lúc theo rule US14, với điều kiện **root còn trong 90 ngày retention**.
14. Guest chọn Reply được chuyển sang login; không tạo dữ liệu trước xác thực.

### Quy tắc nghiệp vụ

- Reply depth = 1.
- Reply không tham gia danh sách root comment khi sort.
- Pagination reply **chỉ tồn tại trong màn Phản hồi**: initial 3, sau đó batch tối đa 10 cho tới hết. Danh sách root không preload và không hiển thị reply.
- Tất cả validation text/emoji/URL/rate limit đồng bộ với US04.
- **Visibility cascade** do Admin Hide hoặc Account Lock của root author không tự thay đổi state moderation của reply; reply chỉ mang cờ `hidden_by_root_cascade = true/false`, **không có đồng hồ retention 90 ngày riêng cho reply**.
- **Delete cascade** là lifecycle riêng: self-delete root soft-delete toàn thread; CMS/Admin soft-delete root tuân US14. Root + toàn bộ reply bị ẩn do cascade được khôi phục cùng lúc khi Undo, với điều kiện **ROOT còn trong 90 ngày retention** (không phải reply còn retention).
- Reply không được hiển thị như content độc lập khi root đang non-public.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục A.2 — "Xem thêm phản hồi" phải giữ focus tại nút sau khi tải xong và announce số lượng vừa tải qua `aria-live`.*

---

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US08-001 | Functional | U1 login; C1 public | Reply C1 | Reply đúng root/scope và đi moderation. |
| TC-US08-002 | Depth | C1 có R1 | Reply R1 | Reply mới vẫn là cấp 1 dưới C1, không tạo cây sâu. |
| TC-US08-003 | Boundary | 999/1000/1001 ký tự | Gửi reply | 999/1000 hợp lệ; 1001 bị chặn. |
| TC-US08-004 | Emoji/minimum | Emoji-only, whitespace, 1 ký tự | Gửi | Emoji-only/1 ký tự hợp lệ; whitespace bị chặn. |
| TC-US08-005 | URL | MyTV domain/subdomain và domain giả | Gửi | Chỉ hostname MyTV hợp lệ được nhận. |
| TC-US08-006 | Rate limit | U1 đã tạo tổng 5 comment/reply trong phút | Gửi thêm reply | Bị rate-limit, không tạo record thứ 6. |
| TC-US08-007 | Initial display | C1 có >3 reply public | Mở danh sách root, sau đó mở màn Phản hồi của C1 | Trong danh sách root **không có reply nào** hiển thị, chỉ có lối vào `{n} phản hồi`; mở màn Phản hồi thì hiển thị đúng 3 reply đầu kèm nút `Xem thêm {n} phản hồi`. |
| TC-US08-008 | Load more | C1 còn 24 reply sau initial | Bấm “Xem thêm {n} phản hồi” nhiều lần | Nút hiển thị đúng số lượng còn lại (ví dụ “Xem thêm 24 phản hồi”); lần lượt tải tối đa 10/10/phần còn lại; không trùng/bỏ sót; số hiển thị trên nút cập nhật đúng sau mỗi lần tải. |
| TC-US08-009 | Delete reply | R1 bị user/Admin xóa | Refresh thread | R1 biến mất hoàn toàn, không placeholder; reply khác giữ nguyên. |
| TC-US08-010 | Admin hide root | C1 public có R1/R2 hợp lệ | Admin Ẩn C1 rồi Undo Ẩn | Khi Ẩn: toàn thread không public, R1/R2 giữ state; Undo: các item hợp lệ hiện lại, item có moderation riêng vẫn theo state riêng. |
| TC-US08-011 | Root author Account Lock | U1 sở hữu C1; U2/U3 sở hữu R1/R2 | Account Lock U1 rồi mở khóa | Khi khóa: cả thread không public nhưng R1/R2 không đổi state; mở khóa: thread hiện lại nếu từng item còn hợp lệ. |
| TC-US08-012 | Self-delete root | U1 sở hữu C1 có reply của user khác | U1 self-delete C1 | C1 và toàn bộ reply cascade soft-delete theo US05; không tách reply thành nội dung độc lập. |
| TC-US08-013 | Authentication | Guest | Chọn Reply | Yêu cầu login; không tạo reply trước auth. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Nút tải thêm reply (thay đổi từ bản cũ "Xem thêm phản hồi" trần trụi sang có số lượng) | `[Xem thêm {n} phản hồi]` |
