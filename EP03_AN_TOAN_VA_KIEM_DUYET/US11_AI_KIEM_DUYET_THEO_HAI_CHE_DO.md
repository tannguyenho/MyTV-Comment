# US11 — AI kiểm duyệt theo hai chế độ

> Thuộc EP03 — An toàn và kiểm duyệt
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là bộ phận vận hành MyTV**, tôi muốn AI kiểm tra nội dung và hỗ trợ hai chế độ kiểm duyệt, để cân bằng tốc độ hiển thị và an toàn theo từng phim.

### Ưu tiên

**Must**

### Phạm vi

- Comment gốc, Reply, phiên bản sửa: áp dụng moderation theo **Mode1/Mode2 của phim**.
- Nickname mới/đổi: áp dụng **global AI moderation policy riêng**, độc lập Mode1/Mode2 và override theo phim; chỉ có 2 kết quả (dùng ngay hoặc chặn ngay), không có trạng thái Chờ duyệt.
- MVP AI language: **Tiếng Việt + Tiếng Anh**. Với **Comment/Reply/Edit**, ngôn ngữ khác hoặc độ tin cậy không đủ → Chờ duyệt Admin. Với **Nickname**, KHÔNG áp dụng Chờ duyệt: ngôn ngữ ngoài Việt/Anh hoặc low-confidence đều bị **chặn và cho thử lại** theo mục "Global policy — Nickname".

### Taxonomy chung

- Spoiler
- Spam/quảng cáo
- Xúc phạm/ngôn từ công kích
- Nội dung không phù hợp
- Sai thông tin
- Vi phạm khác

### Ma trận mức rủi ro

Áp dụng cho **Comment/Reply/Edit** (theo Mode1/Mode2 của scope):
- **Nhẹ** → không che từ, không sửa text.
- **Trung bình** → Chờ duyệt Admin.
- **Nặng** → chặn, không cho gửi/public version mới.

Nickname dùng **chính sách global riêng, KHÔNG theo ma trận 3 mức ở trên** — chỉ 2 kết quả: Nhẹ/An toàn dùng ngay; Trung bình hoặc Nặng (gộp) đều bị chặn ngay tại thời điểm submit, không có trạng thái Chờ duyệt (xem mục "Global policy — Nickname").

> *Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục Security (XSS/Injection) — AI moderation phân loại ngữ nghĩa nội dung, KHÔNG phải hàng rào chống injection; kết quả rủi ro "Nhẹ" không đồng nghĩa nội dung an toàn để render, mọi output vẫn phải qua sanitize/escape ở tầng hiển thị.*

### Acceptance Criteria chung

1. Mọi comment/reply/version sửa và nickname mới/đổi được AI kiểm tra trước khi trở thành dữ liệu public mới.
2. AI lưu taxonomy label, mức Nhẹ/Trung bình/Nặng, reason, model/policy version và thời gian xử lý để CMS tra cứu.
3. Với **Comment/Reply/Edit**, ngưỡng phân loại có default toàn hệ thống do Admin cấu hình trên CMS; mỗi phim có thể override default.
4. Với **Nickname**, hệ thống dùng **global nickname AI policy** với 2 kết quả (Nhẹ/An toàn dùng ngay; Trung bình hoặc Nặng bị chặn ngay, không có trạng thái Chờ duyệt); nickname không kế thừa Mode1/Mode2 hoặc threshold override cấp phim.
5. Mọi thay đổi threshold/policy có audit và chỉ áp dụng từ thời điểm hiệu lực.
6. AI có timeout tối đa **5 giây**. Với **Comment/Reply/Edit**, timeout/5xx/không khả dụng → dữ liệu được nhận ở trạng thái **Chờ duyệt Admin**, không tự công khai. **Ngoại lệ Nickname:** nickname không bao giờ vào Chờ duyệt — timeout/5xx/không khả dụng → nickname bị chặn, giữ nguyên nickname cũ/fallback mask và cho user thử lại (xem mục "Global policy — Nickname").
7. Với **Comment/Reply/Edit**, nội dung ngoài tiếng Việt/Anh hoặc AI không đủ confidence → Chờ duyệt Admin. **Nickname ngoại lệ:** ngôn ngữ ngoài Việt/Anh hoặc low-confidence → chặn ngay + cho thử lại, không tạo Chờ duyệt (xem mục "Global policy — Nickname").
8. CMS có action **“AI phân loại sai”** để Admin ghi kết quả đúng; lưu AI result ban đầu, kết quả sửa, actor/time nhằm đo false positive/false negative.
9. Retry AI/client không tạo comment/version trùng và không tạo nickname decision trùng (nickname không có hàng chờ nên chỉ có đúng một quyết định cho mỗi lần submit).

### Chế độ 1 — AI tiền kiểm, Admin hậu kiểm

Áp dụng **Comment/Reply/Edit** trong scope đang Mode1:
1. Mức Nhẹ/An toàn → Hiển thị ngay, giữ nguyên text.
2. Mức Trung bình → Chờ duyệt, chỉ tác giả thấy.
3. Mức Nặng → chặn không cho gửi/public version mới.
4. Admin vẫn có thể hậu kiểm nội dung đã Hiển thị và xử lý queue.

### Chế độ 2 — Admin duyệt trước

Áp dụng **Comment/Reply/Edit** trong scope đang Mode2:
1. Mức Nặng → chặn.
2. Mức Nhẹ hoặc Trung bình không tự public; đều vào Chờ duyệt Admin.
3. Chỉ Admin Duyệt mới chuyển Hiển thị.

### Global policy — Nickname

Nickname KHÔNG dùng trạng thái Chờ duyệt; chỉ có **2 kết quả**, quyết định ngay tại thời điểm submit:

1. Nickname mức **Nhẹ/An toàn** → dùng ngay, cập nhật nickname công khai ngay lập tức.
2. Nickname mức **Trung bình HOẶC Nặng** (gộp) → **bị chặn ngay tại thời điểm submit**, không tạo bất kỳ hàng chờ nào; user thấy lỗi ngay; nickname không đổi; tiếp tục hiển thị nickname hợp lệ cũ, hoặc fallback mask số điện thoại nếu chưa từng có nickname hợp lệ theo US04.
3. Kết quả này **không thay đổi** theo Mode1/Mode2 của phim nơi user đang thao tác.
4. **Khi AI không cho được quyết định hợp lệ** — timeout quá 5 giây, lỗi 5xx/dịch vụ không khả dụng, nickname bằng ngôn ngữ ngoài tiếng Việt/tiếng Anh, hoặc AI trả về độ tin cậy không đủ (low-confidence) — hệ thống xử lý **giống nhau**: **không đổi nickname**, giữ nguyên nickname hợp lệ cũ (hoặc fallback mask số điện thoại nếu chưa từng có nickname hợp lệ theo US04), báo lỗi **có thể thử lại** cho user, **không tạo hàng chờ duyệt và không tạo queue item**.
5. **Không tiêu quota:** mọi submission nickname bị chặn — do validation, do AI phân loại Trung bình/Nặng, hoặc do AI không cho quyết định hợp lệ theo mục 4 — **không tiêu quota 1 lần đổi nickname thành công/24 giờ/account** (US04). Quota chỉ bị trừ khi nickname mới được chấp nhận và lưu thành công.

### Quy tắc nghiệp vụ

- Chế độ 1 là mặc định cho **content scope**.
- Không còn hành vi tự che `***` cho mức Nhẹ trong policy hiện tại.
- Nickname là identity toàn account nên dùng global policy riêng; không lấy mode của phim làm đầu vào quyết định nickname; nickname KHÔNG có trạng thái Chờ duyệt (chỉ 2 kết quả: dùng ngay hoặc chặn ngay khi submit).
- AI hỗ trợ quyết định; Admin có quyền override theo policy và feedback phải được lưu.
- Fallback khi AI lỗi luôn fail-safe, không fail-open: với **Comment/Reply/Edit** → đưa vào queue Chờ duyệt Admin; với **Nickname** → chặn không đổi nickname và cho user thử lại, KHÔNG tạo queue/hàng chờ.
- Edit (version sửa) áp dụng rate limit riêng: tối đa **5 lần sửa/phút/comment hoặc reply**, tính độc lập theo từng target; request vượt ngưỡng bị chặn trước khi gọi AI/tạo queue item.


## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US11-001 | Coverage | Comment/reply/edit/nickname | Gửi từng loại | Mọi dữ liệu public mới đi AI trước. |
| TC-US11-002 | Mode1/light | Mode1, AI Nhẹ | Gửi Comment/Reply/Edit | Nội dung giữ nguyên text và Hiển thị. |
| TC-US11-003 | Mode1/medium | Mode1, AI Trung bình | Gửi Comment/Reply/Edit | Chờ duyệt; chỉ tác giả thấy. |
| TC-US11-004 | Heavy | Content Mode1/2, AI Nặng | Gửi Comment/Reply/Edit | Bị chặn; không tạo dữ liệu public mới. |
| TC-US11-005 | Mode2 | AI Nhẹ/Trung bình | Gửi Comment/Reply/Edit | Cả hai vào queue; chỉ Admin duyệt mới public. |
| TC-US11-006 | Nickname global policy | Phim M1 Mode1, phim M2 Mode2; cùng mẫu nickname Nhẹ/An toàn và Trung bình/Nặng | Đổi nickname khi đang ở M1 và khi đang ở M2 | Kết quả giống nhau ở mọi scope, không có trạng thái Chờ duyệt: Nhẹ/An toàn dùng ngay; Trung bình hoặc Nặng đều bị chặn ngay tại thời điểm submit, nickname không đổi, tiếp tục hiển thị nickname hợp lệ cũ/mask số điện thoại; Mode1/2 không ảnh hưởng kết quả. |
| TC-US11-007 | Timeout — content | AI >5s/5xx/down | Gửi Comment/Reply/version sửa | Comment/reply/version vào **Chờ duyệt Admin**; không tự public; không fail-open. |
| TC-US11-008 | Language — content | VI/EN/ngôn ngữ khác | Gửi Comment/Reply/version sửa | VI/EN xử lý AI bình thường; ngôn ngữ ngoài phạm vi hoặc low-confidence vào **Chờ duyệt Admin**. |
| TC-US11-009 | Threshold inheritance | Có default hệ thống và override cấp phim | Gửi cùng mẫu Comment/Reply/Edit ở phim có override và phim không có | Phim có override dùng giá trị riêng; phim không có dùng default hệ thống. Nickname không dùng inheritance này. |
| TC-US11-010 | Policy audit | Đổi content threshold/global nickname policy | Tra audit và request trước/sau effective time | Có actor/time/before-after; mỗi decision gắn đúng policy version. |
| TC-US11-011 | Feedback | AI phân loại sai | Admin chọn “AI phân loại sai” và kết quả đúng | Lưu AI result + corrected result + actor/time để đo FP/FN. |
| TC-US11-012 | Idempotency | Client/AI retry | Gửi request lặp cho comment/version và cho đổi nickname | Chỉ một comment/version duy nhất được tạo; với nickname chỉ có **một quyết định (nickname decision) duy nhất**, không tạo hàng chờ và không nhân đôi lần tiêu quota. |
| TC-US11-013 | Edit rate limit | U1 có C1/R1 | Gửi 5 version sửa trên cùng target trong 1 phút rồi gửi lần thứ 6 | 5 lần đầu đi qua pipeline moderation bình thường; lần thứ 6 trên cùng target bị chặn trước khi gọi AI/tạo queue item. C1 và R1 có quota độc lập. |
| TC-US11-014 | Nickname — ngôn ngữ ngoài Việt/Anh | U1 đã có nickname hợp lệ cũ, còn nguyên quota 24h; nickname mới bằng tiếng Hàn (ví dụ `한국사람`) | Gửi đổi nickname | Nickname **bị chặn**, không đổi; U1 tiếp tục hiển thị nickname hợp lệ cũ; hiển thị lỗi cho phép **thử lại**; **không tạo trạng thái Chờ duyệt/queue item**; **không tiêu quota** — U1 đổi ngay sang nickname tiếng Việt hợp lệ vẫn thành công. |
| TC-US11-015 | Nickname — low-confidence | U2 chưa từng có nickname hợp lệ (phone `0912345124`), còn nguyên quota 24h; AI trả kết quả với độ tin cậy dưới ngưỡng | Gửi đổi nickname | Nickname **bị chặn**, không đổi; U2 tiếp tục hiển thị mask `0******124`; hiển thị lỗi cho phép **thử lại**; **không tạo trạng thái Chờ duyệt/queue item**; **không tiêu quota** — lần đổi hợp lệ ngay sau đó vẫn được chấp nhận. |
| TC-US11-016 | Timeout — nickname | AI >5s/5xx/down; U1 đã có nickname hợp lệ cũ và U2 chưa từng có nickname hợp lệ (phone `0912345124`); cả hai còn nguyên quota 24h | Gửi đổi nickname bằng U1 và U2 | Nickname **không đổi**; U1 giữ nickname hợp lệ cũ, U2 giữ mask `0******124`; user thấy lỗi có thể **thử lại**; **không tạo hàng chờ/queue item** nào; **không tiêu quota** 1 lần đổi thành công/24h (đổi lại ngay sau đó vẫn được chấp nhận). |
