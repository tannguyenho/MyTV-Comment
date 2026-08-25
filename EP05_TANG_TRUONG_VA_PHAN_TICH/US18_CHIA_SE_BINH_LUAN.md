# US18 — Chia sẻ bình luận

> Thuộc EP05 — Tăng trưởng và phân tích
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là người dùng đã đăng nhập**, tôi muốn chia sẻ ngữ cảnh thảo luận ra ngoài bằng liên kết quay lại MyTV, để giới thiệu nội dung và mời người khác tham gia.

### Ưu tiên

**Could**

### Phạm vi MVP

- Chia sẻ comment/thread bằng **share sheet của thiết bị**.
- **Không chia sẻ frame/clip** trong phiên bản hiện tại; US06 chỉ hỗ trợ timestamp.

### Acceptance Criteria

1. User đã đăng nhập có thể Share một comment đang Hiển thị và đang public tại thời điểm tạo share.
2. Share payload **không chứa nguyên văn text comment**, nickname/phone của tác giả hoặc Spoiler.
3. CTA chính thức: **“Xem nội dung này trên MyTV”**.
4. Preview gồm **poster/thumbnail phim + tên phim + CTA + logo MyTV**; không chứa text comment/PII.
5. Deep link ưu tiên mở đúng phim và đúng comment/thread khi target còn hợp lệ và scope đang khả dụng.
6. Nếu comment có timestamp, deep link **không tự seek player**; người nhận mở đúng comment và chủ động bấm timestamp nếu muốn.
7. Người nhận chưa đăng nhập vẫn được đọc comment public; login chỉ cần khi muốn tương tác.
8. Nếu người nhận chưa cài app, deep link mở **MyTV Web đúng phim/thread** nếu còn hợp lệ; web có thể có CTA cài app.
9. Deep link **không hết hạn theo thời gian**; mỗi lần mở phải kiểm tra lại state/quyền hiện tại.
10. Nếu target bị moderation **Ẩn/Xóa/Từ chối** hoặc không còn hợp lệ, link cũ mở đúng phim và hiển thị **“Bình luận không còn khả dụng”**; không trả 404 và không lộ nội dung cũ. Khi nhiều gate cùng đúng, áp dụng Effective Visibility Resolver tại US12 (mục ưu tiên gate).
11. Nếu target vẫn hợp lệ nhưng scope đang **Đóng bình luận**, link cũ mở đúng phim, không hiển thị thread và hiện **“Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”**. Khi scope mở lại, link cũ hoạt động lại nếu target vẫn hợp lệ. Khi nhiều gate cùng đúng, áp dụng Effective Visibility Resolver tại US12 (mục ưu tiên gate).
12. Nếu target chỉ tạm non-public do **Account Lock của tác giả/root author**, link cũ mở đúng phim, không hiển thị thread và hiện **“Bình luận hiện không khả dụng”**. Khi account được mở khóa, link cũ hoạt động lại nếu target/thread vẫn hợp lệ. Khi nhiều gate cùng đúng, áp dụng Effective Visibility Resolver tại US12 (mục ưu tiên gate).
13. MVP dùng share sheet; không cần tích hợp SDK/API riêng Facebook/Zalo/TikTok.
14. **Share event được tính khi user bấm Share và OS share sheet mở thành công**. Không cần chờ callback xác nhận user đã gửi sang ứng dụng đích.
15. Ghi nhận kênh đích khi nền tảng cung cấp và lượt mở link phục vụ US19; retry/lỗi kỹ thuật phải dedup để không tăng Share KPI sai.
16. Guest không được thực hiện action Share từ MyTV vì Share là interaction; phải đăng nhập trước khi tạo share event.
17. Scope đang Đóng, target không public hoặc user đang Account Lock thì không thể tạo Share event mới từ target đó.

### Quy tắc nghiệp vụ

> *Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục liên quan — an toàn chia sẻ metadata/PII và deep link.*

- Mọi share phải có link quay lại MyTV.
- Preview/text share chỉ dùng metadata an toàn của MyTV/phim.
- Share target Chờ duyệt/Từ chối/Ẩn/Xóa hoặc đang non-public bị chặn tại thời điểm tạo share.
- Việc người nhận đọc public comment không yêu cầu login.
- Deep-link fallback phải phân biệt nguyên nhân: **scope Đóng** → “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”; **Account Lock visibility** → “Bình luận hiện không khả dụng”; **target moderation invalid/deleted** → “Bình luận không còn khả dụng”.
- Closed scope và Account Lock là visibility gate tạm thời nên link cũ có thể hoạt động lại; moderation invalidation tuân state hiện tại của target.
- **Mốc ghi nhận Share = share sheet mở thành công**; đóng/cancel share sheet sau đó không hoàn tác Share event đã ghi.
- Không có watermark/media/DRM sharing rule trong MVP vì frame/clip đã loại khỏi scope.

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US18-001 | Functional | C1 public | User login chọn Share | Share sheet mở với CTA + deep link, không có text comment; ghi nhận 1 Share event khi sheet mở thành công. |
| TC-US18-002 | Preview | C1 có Spoiler/PII trong text | Kiểm tra preview | Chỉ poster/tên phim/CTA/logo; không lộ comment/Spoiler/PII. |
| TC-US18-003 | Deep link | C1 thuộc phim M1/thread T1 | Mở link | Mở đúng M1 và C1/T1 nếu còn hợp lệ. |
| TC-US18-004 | Timestamp | C1 có `18:00` | Mở share link | Mở đúng comment nhưng player không tự seek; user có thể tự bấm timestamp. |
| TC-US18-005 | Guest recipient | Người nhận logout | Mở link | Đọc được C1 public; muốn Like/Reply/etc thì yêu cầu login. |
| TC-US18-006 | Guest sender | Guest đang xem C1 | Chọn Share | Yêu cầu login; share sheet chưa mở và chưa tạo Share event. Sau login phải chủ động bấm Share lại theo US01. |
| TC-US18-007 | No app | Thiết bị chưa cài MyTV | Mở link | Mở MyTV Web đúng context, không mất deep-link target nếu hợp lệ. |
| TC-US18-008 | No expiry | Link cũ lâu ngày, target vẫn valid | Mở | Link vẫn hoạt động sau khi kiểm tra quyền/state hiện tại. |
| TC-US18-009 | Removed target | C1 bị moderation Ẩn/Xóa/Từ chối | Mở link cũ | Mở phim + “Bình luận không còn khả dụng”; không lộ C1. |
| TC-US18-010 | Closed scope | C1 vẫn hợp lệ nhưng scope Đóng | Mở link cũ | Mở đúng phim + “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”; không đổi state C1. |
| TC-US18-011 | Reopen scope | Scope từ Đóng chuyển Mở, C1 vẫn hợp lệ | Mở lại link cũ | Link lại mở đúng C1/thread. |
| TC-US18-012 | Account Lock target | C1/root author bị Account Lock, content chỉ non-public do lock | Mở link cũ | Mở phim + “Bình luận hiện không khả dụng”; không lộ thread và không đổi moderation state. |
| TC-US18-013 | Unlock target | Account được mở khóa; C1/thread vẫn hợp lệ | Mở lại link cũ | Link lại mở đúng C1/thread. |
| TC-US18-014 | Invalid share state | C1 pending/rejected/hidden/deleted, scope Đóng hoặc target non-public | Thử Share UI/API | Bị chặn; share sheet không mở hợp lệ và không tạo Share event. |
| TC-US18-015 | MVP channel | Có nhiều app share cài trên device | Share | Dùng OS share sheet; chưa cần direct integration SDK/API. |
| TC-US18-016 | Share metric | Share sheet mở thành công rồi user đóng/cancel không gửi | Kiểm tra event | Vẫn ghi nhận đúng 1 Share event vì mốc tính là sheet mở thành công. |
| TC-US18-017 | Dedup | Retry/open sheet lặp do lỗi kỹ thuật cùng request | Kiểm tra event | Không tạo duplicate ngoài định nghĩa dedup; KPI Share không tăng sai. |
| TC-US18-018 | Channel + deep link open tracking | Share cùng 1 comment qua nhiều kênh đích khác nhau (OS cung cấp tên kênh cho một số kênh, không cung cấp cho kênh khác); người nhận mở deep link trên thiết bị đã cài app và trên thiết bị chưa cài app; có retry/lỗi kỹ thuật khi mở link | Thực hiện Share qua từng kênh; mở link ở cả hai loại thiết bị; giả lập lỗi/retry khi mở | Kênh đích được ghi nhận đúng khi OS cung cấp; để trống hợp lệ khi OS không cung cấp (không báo lỗi, không suy diễn kênh); lượt mở deep link được ghi nhận tách biệt với Share event (không cộng gộp hai loại event); mở thành công trên thiết bị đã cài và chưa cài app đều được ghi nhận lượt mở; retry/lỗi kỹ thuật khi mở không tạo duplicate lượt mở ngoài định nghĩa dedup. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Fallback — target moderation invalid (Ẩn/Xóa/Từ chối) | **Bình luận không còn khả dụng**<br>Nội dung bạn muốn xem đã bị gỡ hoặc không còn tồn tại.<br>`[Xem phim]` |
| Fallback — scope Đóng bình luận | **Bình luận đang tạm đóng**<br>Phần thảo luận của {tên phim} tạm thời không mở.<br>`[Xem phim]` |
| Fallback — Account Lock của tác giả/root author | **Bình luận hiện không khả dụng**<br>Nội dung này tạm thời không thể hiển thị.<br>`[Xem phim]` |

Ghi chú: 3 chuỗi tiêu đề fallback (**"Bình luận không còn khả dụng"**, **"Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau"**, **"Bình luận hiện không khả dụng"**) giữ nguyên đúng như đã chốt trong AC10–12; phần viết lại theo cấu trúc Tiêu đề/Giải thích/Lối ra ở trên chỉ là đề xuất nâng cao chất lượng hiển thị, không bắt buộc áp dụng.
