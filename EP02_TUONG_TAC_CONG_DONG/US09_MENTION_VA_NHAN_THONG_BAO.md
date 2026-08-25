# US09 — Mention và nhận thông báo

> Thuộc EP02 — Tương tác cộng đồng
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là người dùng đã đăng nhập**, tôi muốn mention tài khoản phù hợp và nhận thông báo khi có người reply/mention mình, để tiếp tục cuộc trò chuyện liên quan.

### Ưu tiên

**Should**

### Acceptance Criteria

1. User nhập `@` để chọn tài khoản hợp lệ; mention được lưu theo account ID, không chỉ chuỗi nickname.
2. Danh sách gợi ý ưu tiên **user đã tham gia thread hiện tại**, sau đó mở rộng sang user đã tham gia **bộ phim hiện tại**; không mặc định tìm toàn bộ user MyTV.
3. Gợi ý mention không làm lộ full phone/PII; dùng nickname hoặc identity hiển thị hợp lệ.
4. Khi reply/mention đã đủ điều kiện Hiển thị, người nhận nhận **push + in-app notification** nếu công tắc Thông báo cộng đồng đang bật và hệ điều hành cho phép push.
5. Nếu cùng sự kiện vừa Reply vừa Mention cùng một user, chỉ tạo một notification phù hợp.
6. Không gửi notification cho hành động của chính user.
7. Nội dung Chờ duyệt không tạo notification cho người khác trước khi được Hiển thị.
8. User có **một công tắc chung trong Cài đặt** để bật/tắt toàn bộ thông báo tương tác cộng đồng; không có switch riêng Reply/Mention.
9. Công tắc cộng đồng chỉ ảnh hưởng Reply, Mention, huy hiệu và thông báo tương tác tương tự. Các thông báo bắt buộc về **Cảnh báo, Từ chối/Ẩn/Xóa, khóa bình luận/khóa tài khoản, appeal và kết quả Report** không bị tắt bởi setting này.
10. In-app notification cộng đồng được lưu **90 ngày**.
11. Bấm notification mở đúng phim/thread/comment khi target và scope còn khả dụng. Nếu target không còn hợp lệ thì không lộ dữ liệu và dùng fallback phù hợp. Cụ thể theo loại notification:
    - **Cộng đồng (mention, reply, huy hiệu):** deep-link **thẳng tới comment/thread**, không đi qua màn trung gian.
    - **Chế tài và thông báo hệ thống không có comment target:** mở màn **Chi tiết thông báo** (C14) chứa lý do và lối ra tương ứng (khiếu nại, tổng đài).
12. Nếu deep link notification trỏ tới comment/thread thuộc scope đang **Đóng bình luận**, hệ thống mở đúng phim nhưng không hiển thị thread và hiện **“Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”**; khi scope mở lại, link cũ hoạt động lại nếu target vẫn hợp lệ. Nếu target rơi vào nhiều gate ẩn cùng lúc (ví dụ vừa Đóng scope vừa Ẩn/Account Lock), thông báo hiển thị theo **Effective Visibility Resolver** (thứ tự ưu tiên gate) định nghĩa tại US12 — US09 không tự định nghĩa lại thứ tự này.
13. Payload push không lộ Spoiler hoặc PII nhạy cảm trên màn hình khóa.
14. Khi user đang **Account Lock**, hệ thống **không tạo/gửi community notification mới** cho Reply/Mention/badge/tương tác cộng đồng; sau khi mở khóa **không backfill** các community notification đã bỏ qua trong thời gian khóa.
15. Với **Account Lock**, user không vào được MyTV; lần đăng nhập phải vào màn hình tài khoản bị khóa hiển thị **trạng thái khóa + reason + Tổng đài MyTV 1800 1166 (miễn phí, hỗ trợ 24/7) để appeal**. Có thể gửi push nếu thiết bị nhận được; không phụ thuộc vào việc user đọc in-app Notification Center.
16. Trong thời gian Account Lock, chỉ notification bắt buộc liên quan **sanction/Account Lock/appeal status** tiếp tục được xử lý theo US16; community notification bị suppress.

### Quy tắc nghiệp vụ

- Một switch chung cho notification cộng đồng.
- Notification moderation/chế tài là thông báo nghiệp vụ bắt buộc và độc lập với switch cộng đồng.
- Account Lock là ngoại lệ truy cập: **màn hình locked-account + Tổng đài MyTV 1800 1166 (miễn phí, hỗ trợ 24/7)** là kênh chính; in-app Notification Center không được coi là kênh bắt buộc vì user không thể vào app.
- Community notification bị suppress trong Account Lock và không gửi bù sau unlock.
- Đóng bình luận là visibility gate của scope, không đổi moderation state của target deep link.
- Retention in-app: 90 ngày.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục B.4 (PII trong push notification) và B.5 (PII trong gợi ý mention).*

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US09-001 | Suggestion | Thread có U2/U3, phim có U4 | Nhập `@` | Ưu tiên U2/U3 trước, sau đó U4; không mở search toàn hệ thống mặc định. |
| TC-US09-002 | Identity | U2 đổi nickname | Mở mention cũ | Quan hệ vẫn trỏ đúng account ID. |
| TC-US09-003 | Notification | U1 reply/mention U2, switch bật | Publish nội dung | U2 nhận push + in-app nếu push OS cho phép. |
| TC-US09-004 | Preference | U2 tắt switch cộng đồng | Tạo Reply/Mention | Không tạo notification tương tác mới cho U2. |
| TC-US09-005 | Mandatory bypass | U2 tắt switch cộng đồng | Comment U2 bị Từ chối/Ẩn/Xóa hoặc account bị sanction | Notification nghiệp vụ bắt buộc vẫn được xử lý theo US14/US16. |
| TC-US09-006 | Dedup | Một reply vừa mention U2 | Publish | Không gửi hai notification trùng. |
| TC-US09-007 | Self | U1 reply/mention chính mình | Publish | Không gửi self-notification. |
| TC-US09-008 | Moderation | Nội dung Chờ duyệt | Theo dõi notification | Không gửi cho người khác trước khi nội dung public. |
| TC-US09-009 | Retention | Có notification >/<90 ngày | Mở notification center | Chỉ dữ liệu còn trong retention theo policy được giữ. |
| TC-US09-010 | Removed target | Target bị Ẩn/Xóa hoặc mất quyền | Bấm notification cũ | Không lộ nội dung; hiển thị fallback hợp lệ. |
| TC-US09-011 | Closed-scope deep link | C1 hợp lệ nhưng scope đang Đóng | Bấm notification cũ tới C1 | Mở đúng phim + “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”; không hiển thị C1 và không đổi state C1. |
| TC-US09-012 | Account Lock community suppression | U2 đang Account Lock; phát sinh Reply/Mention/badge event cho U2 | Theo dõi push/in-app trong lock và sau unlock | Không tạo/gửi community notification mới; sau unlock không gửi bù các event đã suppress. |
| TC-US09-013 | Locked-account notice | U2 bị Account Lock | U2 thử đăng nhập; kiểm tra push nếu thiết bị cho phép | Không vào app; thấy lock status + reason + **1800 1166 (miễn phí, hỗ trợ 24/7)** và hướng dẫn appeal; push có thể được gửi nhưng không phụ thuộc Notification Center. |
| TC-US09-014 | Appeal mandatory channel | U2 đang Account Lock và Support/CMS cập nhật appeal | Theo dõi thông tin user nhận được | Sanction/appeal status vẫn thuộc nhóm bắt buộc; không bị community switch tắt. |
| TC-US09-015 | Push payload PII/Spoiler | Comment C1 có gắn Spoiler; U1 chưa có nickname hợp lệ (hiển thị dạng phone `0912345124`) mention/reply U2 | Publish, bắt payload push thực tế trên iOS và Android ở trạng thái màn hình khóa và notification shade | Payload push không chứa nguyên văn nội dung Spoiler của C1; không chứa full SĐT `0912345124` của U1 (chỉ dùng nickname/mask dạng `0******124` nếu cần hiển thị định danh); nội dung hiển thị trên màn hình khóa và notification shade tuân cùng rule che PII/Spoiler. |
| TC-US09-016 | Mention suggestion PII | 3 user: U2 có nickname hợp lệ; U3 vừa bị chặn nickname mới theo chính sách Trung bình/Nặng (Quyết định 2 — không có Chờ duyệt, hiển thị theo fallback mask); U4 chưa từng có nickname hợp lệ (hiển thị `0******124`) | Gõ `@` trong thread có cả 3 user; kiểm tra UI dropdown và response API gợi ý mention; thử gõ ký tự để dò user ngoài phạm vi thread/phim | UI và response API chỉ trả nickname hợp lệ (U2) hoặc identity mask dạng `0******124` (U3, U4); không trả về full phone/email của bất kỳ user nào; không thể dùng ô mention để enumerate account ngoài phạm vi thread/phim hiện tại. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Không tìm thấy kết quả mention phù hợp | **Không tìm thấy người dùng phù hợp.**<br>Bạn có thể nhắc đến người đã tham gia thảo luận này. |
