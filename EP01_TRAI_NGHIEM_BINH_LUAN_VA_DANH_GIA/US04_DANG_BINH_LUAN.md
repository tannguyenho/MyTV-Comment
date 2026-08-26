# US04 — Đăng bình luận

> Thuộc EP01 — Trải nghiệm bình luận và đánh giá
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là người dùng đã đăng nhập**, tôi muốn đăng bình luận bằng văn bản, emoji và tùy chọn Spoiler, để chia sẻ cảm nhận về bộ phim đang xem.

### Ưu tiên

**Must**

### Acceptance Criteria

1. Comment hỗ trợ văn bản, emoji và Spoiler; **emoji-only là nội dung hợp lệ**. Spoiler là **thuộc tính của từng đoạn chữ trong nội dung**, không phải cờ của cả comment: khi soạn, user bôi chọn đoạn chữ muốn che rồi chọn **Làm mờ** trong menu định dạng của hệ điều hành. Một comment có thể chứa nhiều đoạn được làm mờ hoặc không có đoạn nào.
2. Comment tối thiểu **1 ký tự hợp lệ hoặc 1 emoji**, không tính khoảng trắng; tối đa **1000 ký tự**. UI và API dùng cùng giới hạn.
3. URL chỉ hợp lệ khi hostname là `mytv.com.vn` hoặc subdomain thực sự của `mytv.com.vn`; không chấp nhận domain giả như `mytv.com.vn.evil.com`.
4. Mỗi user tối đa **5 comment/reply trong 1 phút**; quota được tính chung giữa comment và reply.
5. Comment được gắn đúng bộ phim hiện tại và đi qua moderation theo US11.
6. Ở Chế độ 1, nội dung AI mức Nhẹ/An toàn được Hiển thị; Trung bình vào Chờ duyệt; Nặng bị chặn.
7. Ở Chế độ 2, nội dung không bị chặn vẫn vào Chờ duyệt tới khi Admin duyệt.
8. Đoạn chữ được đánh Spoiler hiển thị dưới dạng **dải làm mờ tại đúng vị trí trong nội dung**; người xem **chạm trực tiếp vào đoạn mờ** để hiện chữ. Không dùng overlay phủ cả comment và không có nút reveal riêng. Mở một đoạn không tự mở các đoạn mờ khác trong cùng comment. Cơ chế Làm mờ chỉ áp dụng trên Phone/Web; **Smart TV hiển thị nguyên văn**, không có dải mờ và không có thao tác hiện nội dung (US01 AC13).
9. Menu định dạng khi soạn comment **chỉ gồm Làm mờ, Gạch chân, Đậm và Nghiêng**; **không có mục Link** — luồng comment không cung cấp chức năng chèn hyperlink. Việc dán URL dưới dạng text vẫn chịu validation hostname tại AC3.
10. Nickname phải **unique không phân biệt hoa/thường**, dài **3–30 ký tự**; cho phép chữ, số, khoảng trắng, `_`, `-`; không cho URL, số điện thoại hoặc ký tự điều khiển.
11. User được đổi nickname tối đa **1 lần đổi thành công/24 giờ/account** (submission bị validation/AI chặn không tiêu quota); nickname mới/đổi phải qua **global AI moderation policy độc lập với Chế độ 1/2 của phim**, chỉ có **2 kết quả**: Nhẹ/An toàn → dùng ngay, cập nhật nickname công khai ngay lập tức; Trung bình HOẶC Nặng (gộp) → **bị chặn ngay lập tức tại thời điểm submit**, không tạo bất kỳ trạng thái chờ duyệt nào. Trường hợp AI không cho được quyết định hợp lệ (timeout >5 giây/5xx/dịch vụ không khả dụng, nickname bằng ngôn ngữ ngoài tiếng Việt/tiếng Anh, hoặc AI low-confidence) cũng **không tạo trạng thái chờ duyệt**: nickname không đổi, user được báo lỗi và cho thử lại, và **không tiêu quota** (theo US11).
12. Khi nickname bị chặn tại submit, user thấy lỗi ngay, nickname không đổi và tiếp tục dùng nickname hợp lệ cũ. Nếu chưa từng có nickname hợp lệ, hiển thị số điện thoại đã mask: giữ `0` đầu + 3 số cuối, toàn bộ số giữa thành `*` theo độ dài thực tế, ví dụ `0912345124 → 0******124`.
13. Không hiển thị đầy đủ số điện thoại hoặc PII nhạy cảm trên trải nghiệm người xem.
14. Sau khi gửi thành công, ô nhập được xóa; retry không tạo comment trùng.
15. Người không đăng nhập/không còn quyền bình luận không thể gửi qua UI hoặc API.
16. Không cho upload ảnh/video cá nhân trong luồng comment.

### Quy tắc nghiệp vụ

- Chỉ tài khoản đăng nhập mới được đăng bình luận.
- Giới hạn 1000 ký tự và rate limit 5 nội dung/phút cũng áp dụng Reply tại US08. Giới hạn 1000 ký tự được đếm theo **grapheme cluster** (đơn vị hiển thị/Unicode extended grapheme cluster), không đếm theo code unit/UTF-16, để nhất quán với emoji tổ hợp (ZWJ, skin-tone modifier); UI và API phải dùng cùng thuật toán đếm.
- URL được validate theo hostname, không theo chuỗi chứa tên miền.
- **Nickname là identity toàn tài khoản**, không thuộc scope phim; vì vậy không kế thừa Mode1/Mode2 hay threshold override theo phim. Nickname dùng global AI policy riêng theo US11, chỉ có 2 kết quả: Nhẹ/An toàn dùng ngay; Trung bình hoặc Nặng đều bị chặn ngay tại submit, không tạo hàng chờ duyệt.
- Nickname bị chặn tại submit không public và không tạo bản ghi chờ; nickname công khai giữ nguyên giá trị hợp lệ trước đó.
- Đổi nickname có quota riêng: tối đa **1 lần đổi nickname thành công/24 giờ/account**. Quota được tính khi nickname mới vượt qua validation + global AI policy và được hệ thống chấp nhận lưu; submission bị validation/AI chặn không tiêu quota. Các trường hợp AI timeout/5xx/không khả dụng, nickname ngoài tiếng Việt/tiếng Anh hoặc AI low-confidence cũng bị chặn + cho thử lại (không có trạng thái Chờ duyệt cho nickname) và **không tiêu quota**, theo US11.
- Khi comment bị Từ chối/Ẩn/Xóa bởi Admin, tác giả được xem lý do trong app và nhận notification theo US14/US16.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) — sanitization/XSS cho nội dung comment và nickname, chặn RTL override/zero-width/control char/homoglyph trong nickname.*

---

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US04-001 | Functional | U1 đăng nhập | Gửi text/emoji ở đúng scope | Comment được tạo đúng scope và xử lý moderation. |
| TC-US04-002 | Emoji | U1 đăng nhập | Gửi comment chỉ có 1 emoji | Hợp lệ nếu qua moderation. |
| TC-US04-003 | Minimum | Chuẩn bị rỗng, whitespace, 1 ký tự | Gửi | Rỗng/whitespace bị chặn; 1 ký tự hợp lệ được nhận. |
| TC-US04-004 | Boundary | 999/1000/1001 ký tự | Gửi qua UI/API | 999/1000 hợp lệ; 1001 bị chặn nhất quán. |
| TC-US04-005 | URL | Link `mytv.com.vn`, `www.mytv.com.vn`, `support.mytv.com.vn`, `mytv.com.vn.evil.com`, domain khác | Gửi | Chỉ domain MyTV và subdomain thực được phép. |
| TC-US04-006 | Rate limit | U1 gửi comment/reply liên tiếp | Gửi 5 rồi nội dung thứ 6 trong rolling 1 phút | 5 nội dung đầu có thể được nhận; nội dung thứ 6 bị rate-limit và không tạo record. |
| TC-US04-007 | Spoiler | Comment của U1 có 2 đoạn được Làm mờ và phần chữ thường xen giữa | Gửi; U2 mở comment rồi chạm lần lượt vào từng đoạn mờ | Đúng 2 đoạn bị làm mờ tại vị trí gốc, phần chữ còn lại hiển thị bình thường; chạm đoạn thứ nhất chỉ hiện đoạn đó, đoạn thứ hai vẫn mờ; không có overlay phủ cả comment và không có nút reveal riêng. |
| TC-US04-020 | Format menu | U1 đang soạn comment, bôi chọn một đoạn chữ | Mở menu định dạng của hệ điều hành trên iOS và Android | Menu chỉ có Làm mờ, Gạch chân, Đậm, Nghiêng; **không có mục Link**; không có đường nào tạo hyperlink trong nội dung comment. |
| TC-US04-008 | Moderation | Mode 1 với mức Nhẹ/Trung bình/Nặng | Gửi từng mẫu | Nhẹ Hiển thị, Trung bình Chờ duyệt, Nặng bị chặn. |
| TC-US04-009 | Mode 2 | Nội dung không bị chặn | Gửi | Vào Chờ duyệt; chưa public trước Admin. |
| TC-US04-010 | Nickname uniqueness | Có `MyTVFan` | User khác thử `mytvfan`/`MYTVFAN` | Bị coi là trùng. |
| TC-US04-011 | Nickname format | Nickname 2/3/30/31 ký tự; có URL/phone/control char | Lưu nickname | Chỉ dữ liệu đúng 3–30 và charset/rule hợp lệ được nhận. |
| TC-US04-012 | Nickname global moderation | Các phim lần lượt ở Mode1/Mode2; đổi nickname Nhẹ/Trung bình/Nặng | Thực hiện đổi ở các phim khác nhau | Kết quả nickname giống nhau ở mọi scope: Nhẹ dùng ngay; Trung bình HOẶC Nặng đều **bị chặn ngay tại submit**, không tạo hàng chờ duyệt, nickname cũ được giữ nguyên; Mode1/2 không làm thay đổi decision. |
| TC-US04-013 | Fallback identity | U1 chưa có nickname hợp lệ, phone `0912345124` | Mở comment | Hiển thị `0******124`, không lộ số đầy đủ. |
| TC-US04-014 | Security/idempotency | Logout hoặc retry request | Gửi qua API | Không bypass auth; retry không tạo trùng. |
| TC-US04-015 | Media restriction | Thử upload ảnh/video cá nhân | UI/API | Không có luồng upload; API từ chối. |
| TC-US04-016 | Grapheme boundary | Chuỗi 1000 grapheme cluster có emoji ZWJ đa-codepoint (ví dụ 👨‍👩‍👧‍👦, 🏳️‍🌈) chèn ở nhiều vị trí | Gửi qua UI và API cùng payload | UI và API đếm ra cùng 1000 đơn vị (grapheme cluster); không bị lệch do đếm theo code point/UTF-16; 1001 grapheme bị chặn nhất quán ở cả hai bề mặt. |
| TC-US04-017 | Nickname Unicode abuse | Nickname chứa RTL override (U+202E), zero-width (U+200B/U+200D không thuộc emoji hợp lệ), control char, hoặc ký tự homoglyph giả mạo chữ Latin | Gửi đổi nickname | Bị chặn ngay tại submit theo rule an toàn nickname; xem thêm ../REQUIREMENTS_A11Y_SECURITY.md. |
| TC-US04-018 | XSS payload | Payload `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`, `javascript:alert(1)` gửi làm nội dung comment và làm nickname | Gửi qua UI/API, sau đó hiển thị lại trên mọi bề mặt (danh sách comment, thông báo, CMS) | Payload được escape/sanitize ở mọi nơi hiển thị, không thực thi script; xem thêm ../REQUIREMENTS_A11Y_SECURITY.md. |
| TC-US04-019 | Nickname quota | U1 chưa đổi nickname trong 24h | Đổi nickname hợp lệ thành công, sau đó thử đổi lần 2 trước 24h; thử lại sau đủ 24h; kiểm tra thêm một submission bị validation/AI chặn | Lần đổi thành công đầu được lưu; lần đổi thành công thứ 2 trong 24h bị chặn; sau đủ 24h được đổi lại. Submission bị validation/AI chặn không tiêu quota. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Chưa gửi được bình luận (mất mạng) | **Chưa gửi được bình luận**<br>Kiểm tra kết nối mạng và thử lại. Nội dung bạn đã nhập vẫn được giữ.<br>`[Thử lại]` |
| Bạn đang bình luận hơi nhanh (rate limit) | **Bạn đang bình luận hơi nhanh**<br>Vui lòng chờ một chút rồi gửi lại.<br>`[Đóng]` |
| AI chặn nội dung khi gửi | **Nội dung có thể vi phạm quy định cộng đồng của MyTV** — hiển thị **inline dạng chữ đỏ ngay phía trên ô nhập**, viền ô nhập chuyển đỏ. Không dùng dialog và không có nút hành động; nội dung user đang soạn được giữ nguyên để sửa tiếp. Dùng **đúng một chuỗi trung tính này** cho mọi trường hợp bị AI chặn, không tiết lộ AI phân loại theo lý do gì. |
| Tên này chưa phù hợp (nickname bị chặn) | **Tên này chưa phù hợp**<br>Vui lòng chọn tên khác phù hợp với quy định cộng đồng của MyTV.<br>`[Thử tên khác]` |
| Đoạn chữ bị Làm mờ (spoiler) | Không có nhãn văn bản trên UI — đoạn chữ hiển thị dạng dải mờ, chạm vào để hiện. Accessible name của vùng mờ: **“Hiện nội dung có tiết lộ”** (theo REQUIREMENTS_A11Y_SECURITY mục A.2). |
| Placeholder ô nhập bình luận | **Viết bình luận** — dùng thống nhất ở mọi trạng thái (rỗng, focus, reply) |
| Comment của tác giả đang chờ duyệt | **Bình luận của bạn sẽ sớm được xuất hiện** — dòng trạng thái inline dưới nội dung, chỉ tác giả thấy |
| Gửi bình luận ở Mode 2 | **Không có bước xác nhận trước khi gửi.** Bấm gửi là gửi luôn; sau đó comment xuất hiện inline với dòng trạng thái “Bình luận của bạn sẽ sớm được xuất hiện” chỉ tác giả thấy. |
