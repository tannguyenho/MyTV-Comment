# US06 — Bình luận kèm mốc thời gian (chỉ phim lẻ)

> Thuộc EP01 — Trải nghiệm bình luận và đánh giá
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là người dùng đang xem phim lẻ VOD**, tôi muốn gắn một mốc thời gian vào comment/reply, để người khác biết chính xác đoạn nội dung tôi đang thảo luận và có thể nhảy tới đoạn đó.

### Giá trị

- Giữ ngữ cảnh thảo luận gắn với nội dung mà không cần xử lý media.
- Giảm phụ thuộc DRM/bản quyền/renderer so với frame/clip.
- Tạo trải nghiệm thảo luận theo khoảnh khắc đơn giản cho MVP.

### Ưu tiên

**Could**

### Phạm vi MVP

- **Chỉ áp dụng cho phim lẻ.** Phim bộ không có chức năng mốc thời gian: khu vực bình luận ở cấp phim nên một mốc không xác định được thuộc tập nào.
- **Không triển khai tạo/chia sẻ frame hoặc clip trong phiên bản hiện tại.**
- Chỉ hỗ trợ gắn timestamp vào comment/reply của nội dung VOD/timeline cố định.
- Live/đang phát trực tiếp **ngoài scope hiện tại**.

### Acceptance Criteria

1. **Không có chức năng “Gắn thời gian hiện tại”.** Hệ thống không cung cấp nút hay thao tác nào lấy mốc đang phát từ player để chèn vào ô nhập.
2. User **tự nhập mốc thời gian** trong nội dung comment/reply theo định dạng `mm:ss` hoặc `hh:mm:ss` khi cần; hệ thống nhận diện chuỗi hợp lệ và hiển thị thành mốc bấm được.
3. Mỗi comment/reply được gắn tối đa **1 timestamp**. Nếu nội dung chứa nhiều chuỗi thời gian hợp lệ, chỉ chuỗi **đầu tiên** được nhận làm timestamp, phần còn lại giữ nguyên là text thường.
4. **Chức năng chỉ bật với phim lẻ.** Trên phim bộ, UI không hiển thị mốc bấm được và API không nhận timestamp; chuỗi thời gian trong nội dung giữ nguyên là text thường.
5. Timestamp phải thuộc phạm vi thời lượng của đúng phim đang bình luận; giá trị âm hoặc vượt duration bị chặn với thông báo **“Mốc thời gian không hợp lệ”**.
6. Comment/reply lưu content ID và timestamp cần thiết để tái tạo ngữ cảnh; không lưu/tạo frame/clip.
7. Timestamp hiển thị dạng có thể bấm, ví dụ `18:00`.
8. Khi user bấm timestamp, player **seek trực tiếp tới đúng mốc và tiếp tục phát từ đó**.
9. Timestamp không làm thay đổi rule Spoiler/moderation của phần text.
10. Nếu nội dung/timestamp không còn khả dụng, text comment vẫn hiển thị và timestamp được disable/hiển thị trạng thái không khả dụng; không làm hỏng thread.
11. Không cho upload ảnh/video cá nhân trong luồng này.

### Quy tắc nghiệp vụ

- Một comment/reply tối đa một timestamp, lấy theo chuỗi thời gian hợp lệ đầu tiên trong nội dung.
- **Không lấy mốc thời gian từ trạng thái player**; timestamp hoàn toàn do user gõ, nên không phụ thuộc việc user đang phát hay đang tạm dừng.
- Không cho timestamp trỏ sang phim khác.
- Không hỗ trợ frame/clip/watermark/DRM media trong scope hiện tại; các nhu cầu đó chuyển Future/Phase sau.
- Deep link chia sẻ comment có timestamp không tự seek player; người nhận mở đúng comment rồi chủ động bấm timestamp theo US18.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) — timestamp phải là `<button>` thật, accessible name "Xem từ phút {m} giây {s}".*

---

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US06-001 | Functional | U1 đang xem phim lẻ M1 | Rà toàn bộ UI ô nhập bình luận/reply tìm nút hoặc thao tác lấy mốc đang phát; sau đó tự gõ `18:00` vào nội dung và gửi | **Không tồn tại** chức năng “Gắn thời gian hiện tại” trên UI lẫn API; comment do user gõ tay lưu timestamp 18:00 đúng M1 và hiển thị thành mốc bấm được. |
| TC-US06-001a | Scope phim bộ | U1 đang xem một tập của phim bộ S1 | Gõ nội dung có chuỗi `18:00` và gửi qua UI; sau đó gửi thẳng API kèm trường timestamp | UI hiển thị `18:00` là text thường, không phải mốc bấm được; API từ chối hoặc bỏ qua trường timestamp; nội dung text vẫn được đăng bình thường. |
| TC-US06-002 | Manual input | Nội dung duration 45:00 | Gõ nội dung có `17:55`; sau đó gõ nội dung có hai chuỗi `17:55` và `20:10` | Trường hợp 1 lưu timestamp 17:55. Trường hợp 2 chỉ nhận `17:55` (chuỗi hợp lệ đầu tiên) làm timestamp, `20:10` giữ nguyên là text thường. |
| TC-US06-003 | Boundary | Nội dung duration 45:00 | Gửi 00:00, 45:00, 45:01, số âm | Giá trị trong phạm vi được nhận; vượt/âm bị chặn theo boundary player thực tế. |
| TC-US06-004 | Max one | Comment đã có timestamp | Thử gắn timestamp thứ hai | Không cho lưu hơn 1 timestamp/comment hoặc reply. |
| TC-US06-005 | Scope | Đang comment phim lẻ M1 | Sửa request trỏ timestamp sang phim M2 | API từ chối mismatch. |
| TC-US06-006 | Playback | Comment có `18:00` | Bấm timestamp | Player seek 18:00 và tiếp tục phát. |
| TC-US06-007 | Fallback | Source/timestamp không còn khả dụng | Mở comment | Text/thread vẫn hiển thị; timestamp không gây crash và có trạng thái thay thế. |
| TC-US06-008 | No media | Kiểm tra UI/API | Tìm chức năng frame/clip/upload | Không có chức năng tạo/share frame/clip hoặc upload media cá nhân trong MVP. |
| TC-US06-009 | Live scope | Nội dung Live | Kiểm tra timestamp comment | Không cung cấp tính năng timestamp theo US06 trong scope hiện tại. |
| TC-US06-010 | Spoiler + timestamp cùng lúc | Comment vừa bật Spoiler vừa có timestamp hợp lệ | Gửi và mở bằng U2 | Timestamp không làm thay đổi rule Spoiler/moderation của phần text; text vẫn bị che theo Spoiler cho tới khi U2 chủ động mở, timestamp vẫn hiển thị/hoạt động độc lập với trạng thái che. |
| TC-US06-011 | Timestamp format sai | Chuỗi "abc", "99:99", "12:60" nhập làm timestamp | Gửi qua UI/API | Toàn bộ giá trị định dạng sai bị chặn kèm thông báo “Mốc thời gian không hợp lệ”, không được lưu thành timestamp hợp lệ. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Mốc thời gian sai định dạng hoặc ngoài thời lượng | **Mốc thời gian không hợp lệ** — dùng chung cho giá trị âm, sai định dạng và vượt thời lượng phim. |
| Mốc thời gian không còn khả dụng | **Mốc thời gian không còn khả dụng**<br>Nội dung tại mốc này hiện không thể phát.<br>(timestamp hiển thị dạng disable, không bấm được) |
| Bấm timestamp khi chưa có player đang chạy (đã có quyền xem) | Hệ thống khởi tạo player và phát trực tiếp từ mốc `mm:ss` được gắn. |
| Bấm timestamp khi chưa có quyền xem phim | **Xem phim để nhảy tới mốc {mm:ss}**<br>Bạn cần xem phim này để phát từ mốc được nhắc đến.<br>`[Xem ngay]` |
