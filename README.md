# MYTV COMMENT BACKLOG

## 5 Epic và 20 User Story

> **Cập nhật 06/11/2026 (URD 2.1):** phạm vi giai đoạn này chỉ gồm luồng có thiết kế Figma — Phone/Web: US01, US02, US04, US05, US07, US08, US09, US10, US17; Smart TV: US01, US17. CMS (US11–US16, US19, US20) và Thích/Báo cáo trên TV → giai đoạn sau. Tiêu chí huy hiệu mới: Fan tích cực = 7 ngày có ≥10 bình luận và đã thích ≥20 nội dung khác nhau; Fan kỳ cựu = 30 ngày có ≥30 bình luận và ≥1 bình luận nhận ≥10 like (không còn tính ngày hoạt động). Format thời gian 6 mức (Vừa mới xong / X phút / X giờ / X ngày / X tháng / X năm trước); không phân biệt UI bình luận của mình.
>
> **Rà soát V5 (02/11/2026):** kịch bản đã chốt theo thiết kế Figma Phone/Web/Smart TV. US03, US06, US18 chuyển **Deferred**; nhiều quyết định dưới đây được thay thế — xem [CHANGELOG_RASOAT_V5.md](CHANGELOG_RASOAT_V5.md) (có hiệu lực cao hơn khi mâu thuẫn).

Tài liệu chuyển yêu cầu tính năng Bình luận trên MyTV thành backlog sản phẩm ở cấp PO. Backlog gồm 5 Epic và 20 User Story; frontend/backend/database/infra/test là task triển khai, không phát sinh thêm User Story nếu không tạo giá trị người dùng độc lập.

## 1. Mục tiêu sản phẩm

- Tạo khu vực thảo luận ở **cấp phim** cho cả phim lẻ và phim bộ.
- Mọi người được đọc comment public; đăng nhập mới được tương tác.
- Kết hợp AI + Admin moderation với state/audit rõ ràng.
- Cung cấp CMS để kiểm duyệt, xử lý vi phạm, appeal và theo dõi KPI.
- Tạo cơ chế tăng trưởng qua badge, share/deep link và AI hỗ trợ vận hành.

## 2. Phạm vi hiện tại

- Áp dụng trước cho Phim truyện/VOD có timeline cố định.
- **Comment ở cấp phim.** Mỗi bộ phim — phim lẻ hay phim bộ — có duy nhất một khu vực bình luận dùng chung. (Rating: Deferred theo V5.)
- **Danh tính theo account MyTV**, không theo profile; hồ sơ Trẻ em ẩn hẳn khu vực bình luận (V5).
- **Nội dung là văn bản thuần 1–500 ký tự**, không định dạng (V5).
- Live/đang phát trực tiếp ngoài scope timestamp hiện tại.
- **Không triển khai frame/clip trong MVP**; US06 mốc thời gian **Deferred** (V5).
- Mở rộng sang thể thao/thiếu nhi/giải trí ngoài scope 20 User Story hiện tại.
- Lịch sử thay đổi phạm vi và các quyết định mới nhất: [CHANGELOG_RASOAT_V5.md](CHANGELOG_RASOAT_V5.md) (và [V4](CHANGELOG_RASOAT_V4.md), [V3](CHANGELOG_RASOAT_V3.md)).
- Yêu cầu Accessibility (WCAG 2.1 AA) và Bảo mật (XSS/IDOR/PII) áp dụng xuyên suốt toàn bộ 20 User Story được tổng hợp tại [REQUIREMENTS_A11Y_SECURITY.md](REQUIREMENTS_A11Y_SECURITY.md).

## 3. Danh sách Epic

| Epic | Tên Epic | User Story |
|---|---|---|
| EP01 | Trải nghiệm bình luận và đánh giá | US01–US06 |
| EP02 | Tương tác cộng đồng | US07–US09 |
| EP03 | An toàn và kiểm duyệt | US10–US12 |
| EP04 | CMS quản trị bình luận | US13–US16 |
| EP05 | Tăng trưởng và phân tích | US17–US20 |

## 4. Danh sách 20 User Story

| ID | Tên User Story | Epic | Ưu tiên |
|---|---|---|---|
| US01 | Đọc khu vực bình luận | EP01 | Must |
| US02 | Xem bình luận, số lượng và sắp xếp | EP01 | Must |
| US03 | Đánh giá phim | EP01 | **Deferred** (V5) |
| US04 | Đăng bình luận | EP01 | Must |
| US05 | Sửa và xóa bình luận | EP01 | Must |
| US06 | Bình luận kèm mốc thời gian | EP01 | **Deferred** (V5) |
| US07 | Like và Unlike bình luận | EP02 | Must |
| US08 | Trả lời bình luận một cấp | EP02 | Must |
| US09 | Mention và nhận thông báo | EP02 | Should |
| US10 | Report bình luận vi phạm | EP03 | Must |
| US11 | AI kiểm duyệt theo hai chế độ | EP03 | Must |
| US12 | Quản lý trạng thái và phạm vi hiển thị bình luận | EP03 | Must |
| US13 | Tra cứu bình luận trên CMS | EP04 | Must |
| US14 | Xử lý nội dung trên CMS | EP04 | Must |
| US15 | Quản lý bình luận ghim và cấu hình theo phim | EP04 | Must |
| US16 | Quản lý người dùng vi phạm và audit log | EP04 | Must |
| US17 | Huy hiệu người dùng | EP05 | Could |
| US18 | Chia sẻ bình luận | EP05 | **Deferred** (V5) |
| US19 | Thống kê hoạt động bình luận | EP05 | Must |
| US20 | AI hỗ trợ vận hành cộng đồng | EP05 | Could |

### 4.1. Ma trận nền tảng

| Nền tảng | User Story áp dụng |
|---|---|
| **Phone** (iOS/Android) | US01, US02, US04, US05, US07, US08, US09, US10, US17 |
| **Web** (MyTV Web) | US01, US02, US04, US05, US07, US08, US09, US10, US17 |
| **Smart TV / STB** | US01 (chỉ đọc), US17 (chip). US07/US10 trên TV → giai đoạn sau (06/11/2026) |
| **CMS Web/Desktop (quản trị)** | US11, US12, US13, US14, US15, US16, US19, US20 |

Quy tắc đọc ma trận:

- Phone và Web có phạm vi giống nhau; khác biệt chỉ ở dạng trình bày (composer inline đáy màn hình trên Phone, inline trên Web).
- **Smart TV chỉ đọc và tương tác tối thiểu:** đọc danh sách bình luận gốc, mở trang thread chỉ đọc để xem reply, Thích/Bỏ thích (US07), Báo cáo bình luận với 4 reason, không có "Khác" (US10, V5) và hiển thị huy hiệu (US17). TV không có ô nhập, không Trả lời, không Sửa/Xóa, không Nhắc tên, không Chia sẻ, không đổi cách sắp xếp, không đánh giá phim, không nhảy tới mốc thời gian và không áp dụng cơ chế Làm mờ (nội dung hiển thị nguyên văn).
- Danh sách bình luận trên Smart TV **kế thừa quy tắc render của US02** (count trên tab, tối đa 3 pin trên cùng, thứ tự `Nổi bật`, lazy load 10 root/batch) nhưng không render control sort — xem US01 AC10.
- US11, US12 và US16 nằm ở nhóm CMS vì thao tác thuộc về Admin; phần **hệ quả** của chúng do backend áp dụng và được hiển thị bằng các state đã đặc tả sẵn trên app, không phát sinh chức năng mới cho FE ứng dụng.
- Mục thông báo sẵn có của ứng dụng Smart TV hiển thị **đầy đủ** notification của account (Reply/Mention, moderation/chế tài, kết quả Báo cáo, huy hiệu); bấm notification có target bình luận thì mở đúng phim/tab Bình luận hoặc trang thread chỉ đọc, fallback theo US12. TV cũng mở được link chia sẻ tới comment dù không có action Chia sẻ.
- **Hệ thống không lưu nền tảng nguồn** của bình luận, lượt thích và báo cáo: CMS (US13/US14) và dashboard (US19) không phân biệt bản ghi đến từ Phone, Web hay Smart TV. Đây là quyết định đã chốt, không phải thiếu sót đặc tả.

## 5. Các quyết định nghiệp vụ đã khóa

### 5.1. Quyền truy cập, scope và cấu trúc thảo luận

- Guest đọc được comment public nhưng không tạo Comment, Reply, Like, Mention, Report, Rating, Share hoặc interaction event.
- Khi guest chọn interaction rồi login thành công, hệ thống chỉ đưa user về **đúng phim/thread/comment**; **không tự thực hiện action cũ**, user phải chủ động thao tác lại sau login.
- Rating ở **cấp phim**: một account có tối đa **một rating hiện hành trên mỗi bộ phim**.
- CMS cấu hình ở **cấp phim**: AI threshold/mode kế thừa theo thứ tự **override cấp phim → default hệ thống** (US15).
- Reply chỉ sâu một cấp.
- Reply không hiển thị độc lập nếu root đang non-public.
- Admin **Ẩn root** hoặc Account Lock của root author làm toàn thread tạm non-public nhưng không tự đổi moderation state của reply user khác.
- User **self-delete root** là lifecycle khác: root + **toàn bộ reply cascade soft-delete thật**, không tách reply thành content độc lập.
- Soft-delete comment/reply giữ **90 ngày**.
- Scope Đóng bình luận giữ tab `Bình luận` nhưng bỏ count, ẩn list/composer/actions và chặn Comment/Reply/Like/Mention/Report/Share mới. **Rating không nằm trong phạm vi gate này** — rating thuộc khối thông tin phim nên vẫn hiển thị aggregate và vẫn nhận đánh giá mới (US03 AC1, AC11).
- Deep link vào scope Đóng mở đúng phim nhưng không hiển thị thread và hiện **“Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”**; mở lại scope thì link cũ hoạt động lại nếu target còn hợp lệ.

### 5.2. Sắp xếp, ghim và pagination

- Nổi bật là sort mặc định.
- Hard max **3 comment ghim/scope**; Admin drag-drop vị trí 1–3; pin có expiry tùy chọn.
- Featured Score phần không ghim: `0.5×ln(1+Like) + 0.3×ln(1+Reply) + 0.2×e^(-AgeHours/72)`.
- `Like` dùng cho Featured Score/sort là **Net Like công khai hiện tại**.
- Like do account đang Account Lock tạo vẫn giữ record nhưng tạm **không tính public Net Like/Featured Score/ranking**; unlock tính lại nếu Like/target còn hợp lệ.
- Initial root comments: **10**; lazy load **10/lần**.
- Reply **không hiển thị trong danh sách root**; root có reply chỉ hiện lối vào `{n} phản hồi`. Trong màn Phản hồi: initial **3** reply, nút “Xem thêm {n} phản hồi” tải tối đa **10/lần**, phần còn lại <10 thì tải full.
- Pin trên content của account bị Account Lock chỉ **tạm ẩn và giữ metadata**; unlock tự hiện lại nếu source còn hợp lệ và Pin chưa expiry.
- Moderation Ẩn/Xóa/Từ chối làm mất Pin; **Undo moderation không tự khôi phục Pin**.

### 5.3. Comment/Reply/Nickname

- Comment và Reply: **1–500 ký tự** (V5), văn bản thuần không định dạng, emoji-only hợp lệ, whitespace-only không hợp lệ.
- URL chỉ cho `mytv.com.vn` và subdomain thực của domain này.
- Rate limit chung Comment+Reply: **5 nội dung/1 phút/user**.
- *(Deferred V5 — không có nickname riêng; tên hiển thị = tên tài khoản MyTV, chưa có tên → `0***123`.)* Nickname unique không phân biệt hoa/thường, 3–30 ký tự; cho chữ/số/khoảng trắng/`_`/`-`, không URL/phone/control char.
- Nickname đổi tối đa **1 lần thành công/24 giờ/account** theo US04; submission bị validation/AI chặn không tiêu quota.
- **Nickname dùng global AI moderation policy riêng**, độc lập Mode1/Mode2 và threshold override cấp phim, chỉ còn **2 kết quả**: Nhẹ/An toàn dùng ngay; Trung bình hoặc Nặng đều bị chặn ngay, không tạo hàng chờ duyệt.
- Nickname bị chặn thì giữ nickname hợp lệ cũ; chưa có nickname hợp lệ thì giữ `0` đầu + 3 số cuối, mask toàn bộ số giữa bằng `*`.

### 5.4. Rating *(Deferred theo V5 — giữ để tham khảo khi bật lại)*

- Một rating hiện hành/account/scope; đổi rating không tăng tổng lượt; **user không được xóa rating**, chỉ được đổi mức sao; **không có thao tác DELETE rating trong MVP** (xem US03).
- Average hiển thị **1 chữ số thập phân và luôn làm tròn lên** đến 0.1.
- Khóa bình luận không loại rating.
- Khóa toàn account loại rating khỏi **cả điểm trung bình và tổng số lượt rating công khai**; mở khóa tự tính lại cả hai nếu record còn.

### 5.5. Edit/Delete và timestamp

- User sửa comment/reply bất kỳ lúc nào khi còn quyền sửa. Kết quả một lần sửa **phụ thuộc chế độ kiểm duyệt của phim**: Chế độ 1 + AI Nhẹ thì bản mới public ngay; Chế độ 1 + AI Trung bình hoặc Chế độ 2 thì bản mới vào Chờ duyệt và **bản cũ vẫn public** trong lúc chờ; AI Nặng bị chặn tại submit và bản cũ giữ nguyên.
- **Khóa bình luận chặn Edit mới** nhưng user vẫn được **self-delete** content của mình. Mỗi comment/reply có **Edit rate limit riêng tối đa 5 lần sửa/phút/target**; vượt ngưỡng bị chặn trước khi tạo version/gọi AI.
- Comment/Reply/Edit đã gửi hợp lệ trước effective time của Khóa bình luận vẫn được moderation bình thường; Duyệt trong thời gian khóa vẫn có thể public nếu không có gate khác.
- Bản sửa được duyệt có nhãn **“Đã chỉnh sửa”**; user không xem version history, CMS/Audit xem được.
- User tự xóa không cần reason; **Admin không được Undo để public lại self-delete**.
- User self-delete root → root + toàn bộ reply cascade soft-delete 90 ngày; contribution badge của các reply bị cascade cũng bị loại.
- Undo Xóa tại CMS chỉ áp dụng **CMS/Admin soft-delete**: root + toàn bộ reply bị ẩn do cascade được khôi phục theo state riêng trước cascade, với điều kiện **ROOT còn trong 90 ngày retention**.
- MVP không có frame/clip. **US06 chỉ áp dụng cho phim lẻ**, gắn tối đa **1 timestamp/comment hoặc reply**; **không có chức năng lấy current time từ player** — user tự gõ mốc thời gian trong nội dung, hệ thống nhận chuỗi hợp lệ đầu tiên.
- Bấm timestamp → player seek tới mốc và tiếp tục phát; share deep link không tự seek.

### 5.6. Like/Mention/Notification

- User được Like content của chính mình.
- Like/Unlike dùng optimistic UI; client gom batch tối đa **5 giây** rồi sync BE, flush sớm khi rời màn hình/background; BE là source of truth.
- Nhiều Like/Unlike liên tiếp trên cùng target trong một batch được coalesce về **state cuối cùng**.
- Mention suggestion ưu tiên user trong thread, sau đó user đã tham gia bộ phim.
- *(Switch riêng: Deferred V5 — dùng cài đặt thông báo chung của app.)* In-app retention **90 ngày**. Đích đến khi bấm thông báo theo bảng §3 CHANGELOG V5 (Phone: view Bình luận toàn màn hình).
- Notification moderation/chế tài/appeal/kết quả Report là bắt buộc và không bị switch cộng đồng tắt.
- Khi user đang **Account Lock**, không tạo/gửi community notification mới cho Reply/Mention/badge/tương tác; sau unlock **không backfill**.
- Account Lock không cho user vào MyTV; login dừng ở màn hình khóa hiển thị **status + reason + Tổng đài MyTV 1800 1166 (miễn phí, hỗ trợ 24/7) để appeal**. Có thể push nếu thiết bị nhận được; không phụ thuộc Notification Center trong app.

### 5.7. Report và reason taxonomy

- Taxonomy báo cáo (V5): Có spoiler; Spam/Quảng cáo; Xúc phạm/ngôn từ công kích; Nội dung không phù hợp; Khác (Phone/Web — bỏ "Sai thông tin"); Smart TV chỉ 4 lý do đầu. Taxonomy chế tài CMS giữ thêm "Vi phạm khác".
- Report chọn “Khác” bắt buộc description **1–500 ký tự hợp lệ**, không chấp nhận chỉ khoảng trắng.
- Không được Report content của chính mình.
- Cùng target được Report lại sau **24 giờ**; rate limit **10 Report/1 giờ/user**.
- Report không tự Ẩn/Xóa content dù số lượng lớn.
- Reporter nhận **in-app notification** khi Report được xử lý, không lộ sanction chi tiết, không click mở. Tác giả nhận thông báo kèm lý do; card của tác giả hiện trạng thái bị ẩn/từ chối + lý do, chỉ tác giả thấy (V5).
- CMS dùng một action **“Bỏ qua Report”** cho kết luận không vi phạm; không có “Duyệt giữ nguyên” riêng.
- Với Admin moderation/sanction, nếu reason = **“Vi phạm khác”** thì note **bắt buộc 1–500 ký tự**; với 5 reason chuẩn còn lại note optional.

### 5.8. AI moderation và state transition

- **Blacklist từ khóa** (V5): 1 danh sách toàn hệ thống trong CMS, khớp → chặn ngay, không gọi AI.
- Comment/Reply/Edit: Risk **Nhẹ → giữ nguyên text/Hiển thị ở Mode1; Trung bình → Chờ duyệt; Nặng → chặn**. Pending: chỉ **Hủy đăng**, không Sửa (V5).
- Mode2: Nhẹ/Trung bình đều Chờ Admin; Nặng chặn.
- Nickname không dùng Mode1/Mode2; dùng global policy riêng ở 5.3.
- AI timeout **5 giây**/lỗi/down → Chờ duyệt Admin.
- MVP AI language: Việt + Anh; ngôn ngữ khác/low-confidence → Chờ duyệt.
- Threshold content có default hệ thống và override cấp phim; mọi thay đổi audit.
- Admin có feedback **“AI phân loại sai”** để lưu corrected result.
- Mode2→Mode1: pending có AI safe/Nhẹ tự Hiển thị; Medium tiếp tục pending.
- Mode1→Mode2: content đã Hiển thị vẫn giữ; mode mới chỉ áp dụng dữ liệu mới từ effective time.
- Đóng bình luận giữ queue; Admin vẫn xử lý nhưng item được duyệt không public tới khi mở lại.
- “Sau X giờ” cho Admin chọn mốc. Phim lẻ: giờ phát hành MyTV / giờ phát sóng / mốc Admin nhập. Phim bộ: chỉ giờ phát hành MyTV / mốc Admin nhập.

### 5.9. CMS moderation và Undo

- Queue mặc định: **risk cao trước**, cùng risk thì item chờ lâu hơn trước.
- PII đầy đủ được Admin/Moderator có quyền CMS xem trong scope được cấp.
- Export CSV + XLSX theo filter; mặc định không có full PII, muốn export PII phải tick chủ động.
- Duyệt không cần reason. **Từ chối/Ẩn/Xóa** bắt buộc reason taxonomy chuẩn; “Vi phạm khác” bắt note 1–500, reason khác note optional.
- Bỏ qua Report/Flag/Spoiler không bắt buộc reason.
- Từ chối/Ẩn/Xóa → tác giả thấy reason và nhận thông tin theo kênh phù hợp; Account Lock tuân locked-account/Support flow.
- Bulk moderation chỉ hỗ trợ **Duyệt / Từ chối / Ẩn / Xóa mềm**, hard max **100**, partial success; Report/Flag/Spoiler không bulk trong MVP.
- Bulk Duyệt không cần reason; bulk Từ chối/Ẩn/Xóa dùng reason chung và có thể override từng item; item/batch reason “Vi phạm khác” bắt note hợp lệ.
- Undo ánh xạ state: **Từ chối→Chờ duyệt; Ẩn→Hiển thị; Xóa mềm→state ngay trước Xóa**.
- Điều kiện thời gian Undo theo US14: **Undo Từ chối và Undo Ẩn không giới hạn thời gian**; **Undo Xóa mềm chỉ trong 90 ngày retention kể từ thời điểm xóa** — với Undo Xóa root thì tính theo retention của **ROOT**.
- Mọi Moderator có quyền tương ứng được Undo, không bắt reason nhưng tạo audit event mới.
- Undo Xóa root chỉ áp dụng **CMS/Admin delete**, khôi phục thread theo state từng reply trước cascade; không áp dụng self-delete của user.
- Undo moderation chỉ khôi phục content state; **không tự khôi phục Pin hoặc Featured badge** đã mất do moderation.
- Moderation pending SLA **24 giờ**; quá SLA vẫn pending, đánh dấu Quá SLA và ưu tiên queue, không auto-approve/reject.

### 5.10. Sanction/Appeal/Audit

- Nhẹ → Cảnh báo; Trung bình → Khóa bình luận tạm; Nặng → Admin chọn Khóa bình luận hoặc Khóa tài khoản theo bối cảnh.
- Cảnh báo/Khóa bình luận/Khóa tài khoản dùng **cùng taxonomy vi phạm chung**; reason bắt buộc; “Vi phạm khác” bắt note 1–500.
- Khóa bình luận chặn **Comment+Reply+Mention+Edit mới**; vẫn cho self-delete/Like/Report/Rating/Share. Không có khóa bình luận vĩnh viễn.
- Preset Khóa bình luận: 10 phút, 1 giờ, 1 ngày, 3 ngày, 7 ngày, 1 tháng hoặc custom; sanction tạm bắt buộc duration.
- Khóa tài khoản chỉ cho vi phạm nghiêm trọng; mọi Admin/Moderator có quyền moderation đều được thực hiện.
- Account Lock có temporary cùng preset/custom hoặc Permanent; user **không thể đăng nhập/không thể vào MyTV**.
- Account Lock làm content user tạm non-public nhưng **không đổi moderation state**; nếu user là root author thì toàn thread tạm non-public, replies user khác giữ state.
- Unlock tự public lại lock-only content/thread nếu từng item còn hợp lệ; **Permanent Account Lock giữ non-public vô thời hạn** và không tự soft-delete content.
- Pending Comment/Reply/Edit gửi trước Account Lock vẫn được moderation; nếu Duyệt trong lock thì chưa public tới unlock.
- Khóa bình luận: **appeal qua Tổng đài 1800 1166** (V5 — không có form appeal trong app).
- **Account Lock: appeal qua Tổng đài MyTV 1800 1166 (miễn phí, hỗ trợ 24/7); Support/CSKH chuyển appeal vào CMS**, vì user không vào được app.
- SLA appeal **48 giờ**; quá SLA giữ sanction, đánh dấu Quá SLA và ưu tiên queue.
- Audit log retention **2 năm**, độc lập soft-delete 90 ngày.

### 5.11. Huy hiệu

- **Active day**: user đã đăng nhập mở/đọc khu vực Bình luận **đang khả dụng** ít nhất 1 lần/ngày; tối đa 1 active day/account/ngày. Guest và scope Đóng không tạo active day.
- Fan tích cực: rolling 30d, ≥7 active days + ≥10 comment/reply hợp lệ.
- Fan kỳ cựu: rolling 90d, ≥30 active days + ≥30 comment/reply hợp lệ + ≥30 Like nhận.
- Rolling window tiếp tục chạy trong Account Lock, không freeze; active day đã ghi trước lock giữ nguyên, sau lock không phát sinh active day mới.
- Auto badge evaluation mỗi ngày; không đạt thì grace **7 ngày** trước khi thu hồi Fan badge.
- Tên badge hiển thị trên UI (theo thiết kế Phone đã chốt): **Fan tích cực**, **Fan kỳ cựu**, **Nổi bật** (badge tự động cấp toàn MyTV), **Custom** (badge Admin cấp thủ công/Chuyên gia).
- UI hiển thị tối đa **1 badge**; ưu tiên **Custom (Admin/Chuyên gia cấp) > Nổi bật > Fan kỳ cựu > Fan tích cực**. **Ghim là marker riêng, không chiếm slot badge**; sheet giải thích không hiện số liệu tiêu chí (V5). Thứ tự liệt kê trong sheet giải thích huy hiệu chỉ để giới thiệu, **không** phải thứ tự ưu tiên hiển thị.
- Account Lock **không tự invalid Fan contribution hợp lệ** của locked user hoặc reply user khác bị ẩn chỉ do locked root.
- Like locked user đã nhận vẫn tính Fan badge nếu source chỉ non-public do Account Lock; chỉ loại nếu source bị moderation riêng/lifecycle Delete.
- Like do một past liker sau đó Account Lock **vẫn tính cho Fan kỳ cựu của recipient**, dù Like đó tạm bị loại public Net Like/ranking/Engagement.
- Admin Ẩn/Xóa root không làm mất badge contribution của reply user khác nếu reply không bị moderation state riêng.
- **Self-delete root là ngoại lệ:** toàn reply cascade soft-delete thật nên reply/Like gắn với reply bị loại khỏi badge eligibility.
- Badge **Nổi bật** grant mới: source public có **≥20 public Net Like + ≥5 Reply + Top10% Featured Score toàn MyTV trong 30 ngày** tại thời điểm xét.
- Sau grant, Like<20/Reply<5/tụt Top10% **không tự revoke**; chỉ source moderation invalidation mới revoke.
- Account Lock tác giả chỉ tạm ẩn badge **Nổi bật** và unlock có thể tự hiện lại; **Undo moderation không tự restore badge**, phải re-evaluate/re-grant.
- Badge **Custom** (Admin cấp/Chuyên gia) có expiry tùy chọn; tắt badge type ẩn UI nhưng giữ history/audit.

### 5.12. Share và deep link *(Share: Deferred theo V5; chỉ giữ deep link nội bộ cho thông báo)*

- Share là interaction, người gửi phải login; người nhận logout vẫn đọc được comment public.
- MVP dùng **OS share sheet**, không direct SDK Facebook/Zalo/TikTok.
- Share text không chứa comment; CTA chính thức **“Xem nội dung này trên MyTV”**.
- Preview: poster/thumbnail + tên phim + CTA + logo MyTV; không comment/Spoiler/PII.
- Deep link không hết hạn; chưa cài app → mở MyTV Web đúng context.
- Target moderation Ẩn/Xóa/Từ chối → phim + **“Bình luận không còn khả dụng”**.
- Scope Đóng → phim + **“Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”**; mở scope lại thì link cũ hoạt động lại nếu target valid.
- Target/thread chỉ non-public do Account Lock → phim + **“Bình luận hiện không khả dụng”**; unlock thì link cũ hoạt động lại nếu valid.
- Comment có timestamp: share mở đúng comment nhưng không auto-seek player.
- **Share event được tính khi OS share sheet mở thành công**; không cần xác nhận đã gửi sang app đích, cancel sau đó không hoàn tác event; retry/lỗi kỹ thuật phải dedup.

### 5.13. Analytics và AI Ops

- Engagement Score (V5): `Comment×2 + Reply×2 + Net Like×1` (Rating/Share bổ sung khi bật lại US03/US18).
- `Rating` trong Engagement = **số rating hợp lệ hiện hành** trong scope/thời gian; mỗi account rating hợp lệ = +1 bất kể 1★ hay 5★.
- `Share` trong Engagement = số **share sheet mở thành công** theo US18.
- Public KPI/Engagement Score **KHÔNG bị loại trừ chỉ vì scope Đóng bình luận** — Đóng là gate hiển thị vận hành (chống spoiler/thời điểm nhạy cảm), không phải chế tài nội dung; dữ liệu Like/Reply/Rating/Share/Comment phát sinh trước và trong lúc Đóng vẫn tính đầy đủ. Chỉ đúng 4 nguyên nhân sau mới loại KPI: (1) Ẩn/Từ chối/Xóa do moderation, (2) self-delete cascade, (3) Admin root moderation cascade, (4) Account Lock.
- Account Lock tạm loại content user khỏi public KPI; nếu locked user là root author thì **toàn thread** tạm bị loại public KPI/Engagement; unlock tính lại item còn hợp lệ.
- Like của account đang Account Lock tạm bị loại khỏi public Net Like/ranking/Engagement nhưng record vẫn giữ.
- Admin Hide/Delete root làm toàn thread non-public nên public KPI của thread bị loại; badge eligibility user khác là semantics riêng tại US17.
- User self-delete root soft-delete toàn thread nên bị loại khỏi public KPI và không Admin Undo public lại.
- Unique commenters dựa trên account có ít nhất một Comment/Reply đủ điều kiện public trong filter/time hiện tại.
- Dashboard freshness tối đa **5 phút**; daily reconciliation tự sửa aggregate lệch và ghi log.
- Dashboard hiển thị cả total Like actions và public Net Like; Engagement chỉ dùng public Net Like.
- Export dashboard/report CSV + XLSX.
- KPI MVP giữ cả interaction + confirmed Report rate + hidden/deleted/rejected + AI auto-display rate + queue processing time.
- AI Ops chỉ chạy khi Admin bấm **“AI đề xuất”**; input chỉ từ bộ phim hiện tại.
- Candidate bị loại vì mức nghiêm trọng khi **AI risk = Nặng** hoặc **CMS gắn Flag nghiêm trọng**; nhiều Report chưa xác minh không tự loại candidate chỉ vì Report count.
- AI không tự ghim/đăng; Admin có thể chỉnh câu hỏi → duyệt → đăng, không cần reviewer thứ hai.
- KPI AI: tỷ lệ accept / edit / discard; KPI thấp không tự disable feature.

### 5.14. Effective Visibility Resolver — thứ tự ưu tiên gate hiển thị

Khi một comment/thread rơi vào từ 2 gate ẩn trở lên cùng lúc, hệ thống chọn thông báo theo gate có **mức ưu tiên cao nhất** (số nhỏ hơn = ưu tiên cao hơn = "vĩnh viễn/nghiêm trọng hơn"). Nếu nhiều gate cùng đúng, dùng thông báo của gate có số ưu tiên nhỏ nhất.

| Ưu tiên | Gate | Thông báo fallback |
|---|---|---|
| 1 | Self-delete cascade (user tự xóa root) | *(không hiển thị lại — vĩnh viễn theo lifecycle self-delete)* |
| 2 | Moderation state riêng (Ẩn/Xóa mềm/Từ chối do CMS/Admin) | **"Bình luận không còn khả dụng"** |
| 3 | Admin root moderation cascade | **"Bình luận không còn khả dụng"** |
| 4 | Account Lock (tác giả/root author) | **"Bình luận hiện không khả dụng"** |
| 5 | Scope Đóng bình luận | **"Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau"** |

Chi tiết đầy đủ tại US12.

### 5.15. Glossary thuật ngữ chuẩn hóa

| Thuật ngữ chuẩn | Dùng cho | KHÔNG dùng lẫn với |
|---|---|---|
| **Ghim (Pin)** | Comment được Admin ghim đầu danh sách (US15) | "Nổi bật" |
| **Sắp xếp Nổi bật** (sort mode) | Chế độ sort mặc định dùng Featured Score (US02) | "Ghim" |
| **Huy hiệu Nổi bật** (Featured badge) | Huy hiệu tự động cấp toàn MyTV, hiển thị cạnh nickname (US17) | "Ghim" |

> **Chữ “Nổi bật” mang hai nghĩa và điều này đã được chấp nhận có chủ đích.** Trên UI, `Nổi bật` là tên chế độ sắp xếp (control sort ở đầu danh sách) **và** tên một huy hiệu (chip cạnh nickname). Hai thứ ở hai vị trí khác nhau nên người dùng không nhầm; khi viết tài liệu, test case hoặc trao đổi nội bộ thì phải gọi đủ **“sắp xếp Nổi bật”** hoặc **“huy hiệu Nổi bật”**, không dùng chữ “Nổi bật” trần. Riêng **Ghim (Pin)** vẫn tuyệt đối không được gọi là "Nổi bật".
| **Ẩn** | CHỈ dùng cho moderation state chính thức (US12 bảng state) | Không dùng cho trạng thái tạm do Account Lock/scope Đóng |
| **Non-public tạm thời** | Trạng thái tạm do Account Lock hoặc scope Đóng (không đổi moderation_state) | "Ẩn" |

## 6. Điểm PO còn lại sau vòng refinement

- **Không còn blocker PO đang mở trong 20 User Story sau vòng review và đồng bộ quyết định đến Câu 169.**
- Các khác biệt có chủ đích đã được ghi rõ giữa **public KPI/visibility** và **badge eligibility**, cũng như giữa **Account Lock/Admin Hide visibility cascade** và **self-delete cascade soft-delete**.
- Bốn mục mở từ gói rà soát đã chốt: nickname **1 lần/24h**, Edit **5 lần/phút/target**, Account Lock dùng **1800 1166 — miễn phí, 24/7**, và tên badge **Fan kỳ cựu**.

Các nội dung tiếp theo nên là thiết kế UI, data dictionary, technical implementation hoặc policy vận hành chi tiết dựa trên các business rule đã khóa; chỉ mở lại quyết định PO nếu phát hiện hành vi sản phẩm mới hoặc mâu thuẫn mới trong refinement/implementation.

## 7. Nguyên tắc refinement

Mỗi User Story là một lát cắt giá trị ở cấp PO. Nếu story quá lớn cho một sprint, có thể tách delivery story nhưng phải giữ nguyên business rule/acceptance đã khóa. Không tách web/mobile/API/database thành User Story riêng nếu chỉ là phần kỹ thuật để hoàn thành cùng giá trị.
