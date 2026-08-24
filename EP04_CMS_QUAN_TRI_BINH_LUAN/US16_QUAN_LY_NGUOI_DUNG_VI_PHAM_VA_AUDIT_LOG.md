# US16 — Quản lý người dùng vi phạm và audit log

> Thuộc EP04 — CMS quản trị bình luận
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là Admin/Moderator có quyền moderation**, tôi muốn xem lịch sử vi phạm, áp dụng chế tài và xử lý khiếu nại có audit, để bảo vệ cộng đồng và xử lý tài khoản nhất quán.

### Ưu tiên

**Must**

### Ma trận chế tài mặc định

- **Nhẹ** → Cảnh báo.
- **Trung bình** → Khóa bình luận tạm thời.
- **Nặng** → Admin quyết định Khóa bình luận hoặc Khóa tài khoản tùy bối cảnh; Khóa tài khoản chỉ dùng khi xác định vi phạm chính sách nghiêm trọng.

Cảnh báo phải có notification bắt buộc riêng (in-app bắt buộc + push tùy chọn), **không bị tắt bởi switch cộng đồng** — xem US09 AC9.

### Reason taxonomy cho chế tài

Cảnh báo / Khóa bình luận / Khóa tài khoản dùng cùng taxonomy vi phạm chung của Report/AI/CMS:
- Spoiler
- Spam/quảng cáo
- Xúc phạm/ngôn từ công kích
- Nội dung không phù hợp
- Sai thông tin
- Vi phạm khác

Admin bắt buộc chọn một reason chuẩn khi áp dụng cảnh báo/sanction. Với 5 reason chuẩn đầu, note nội bộ là tùy chọn; nếu chọn **“Vi phạm khác”**, note **bắt buộc**, không chỉ whitespace và tối đa **500 ký tự** ở cả UI/API.

### Hai mức khóa riêng

#### 1. Khóa bình luận

- Chỉ là chế tài cộng đồng, không khóa toàn bộ tài khoản MyTV.
- Chặn **Comment + Reply + Mention + Edit comment/reply mới** kể từ effective time.
- User vẫn được **self-delete content của mình, Like, Report, Rating, Share** nếu các quyền khác hợp lệ.
- Chỉ có khóa tạm thời, **không có khóa bình luận vĩnh viễn**.
- Preset thời hạn: **10 phút, 1 giờ, 1 ngày, 3 ngày, 7 ngày, 1 tháng**, hoặc Admin tự nhập thời hạn.
- Hết hạn tự khôi phục quyền nếu không có sanction khác còn hiệu lực.
- Comment/Reply/Edit đã được gửi hợp lệ **trước effective time** vẫn tiếp tục moderation bình thường; nếu Admin Duyệt trong thời gian Khóa bình luận thì content/version được public bình thường nếu không có gate khác.

#### 2. Khóa tài khoản

- Áp dụng cho vi phạm chính sách nghiêm trọng và khóa toàn bộ tài khoản MyTV theo policy tài khoản.
- **User không thể đăng nhập/không thể vào ứng dụng MyTV** trong thời gian khóa.
- **Mọi Admin/Moderator có quyền moderation đều có thể thực hiện**, không yêu cầu Super Admin hay bước duyệt thứ hai.
- Có thể khóa tạm thời với cùng preset **10 phút, 1 giờ, 1 ngày, 3 ngày, 7 ngày, 1 tháng hoặc custom**, hoặc **khóa vĩnh viễn**.
- Khi account bị khóa, toàn bộ comment/reply đang public của user **tạm non-public** nhưng không bị đổi sang moderation Ẩn/Xóa chỉ vì Account Lock.
- Nếu user là tác giả **root comment**, toàn bộ thread dưới root đó tạm non-public, kể cả reply hợp lệ của user khác; các reply đó **không đổi moderation state và không bị coi là vi phạm**.
- Khi account được mở khóa, comment/reply/thread bị non-public **chỉ vì Account Lock** tự public lại nếu từng item vẫn hợp lệ và không có moderation action/gate khác.
- Với **Permanent Account Lock**, content tiếp tục non-public vô thời hạn; không tự chuyển sang soft-delete/Ẩn/Từ chối. Nếu cần xóa content, Admin phải thực hiện moderation action riêng.
- Rating của account bị loại khỏi **cả điểm trung bình và tổng số lượt đánh giá công khai** trong thời gian khóa; khi mở khóa tự tính lại nếu rating record còn tồn tại theo US03.
- Like do account đã tạo trước khi bị khóa vẫn giữ record nhưng tạm bị loại khỏi **Net Like công khai, Featured Score/ranking và Engagement**; mở khóa tính lại nếu Like/target còn hợp lệ theo US07/US19.
- Pin và huy hiệu **Nổi bật** trên content của account bị khóa chỉ **tạm ẩn**, metadata được giữ; mở khóa có thể tự hiển thị lại nếu source vẫn hợp lệ và Pin chưa hết hạn. Nếu source bị moderation riêng trong thời gian khóa, không tự phục hồi.
- Content/Version đã **Chờ duyệt trước khi Account Lock** vẫn được Admin xử lý. Nếu Duyệt trong thời gian khóa, moderation state được Duyệt/Hiển thị nhưng **không public** cho tới khi mở khóa nếu content vẫn hợp lệ.

### Acceptance Criteria — Lịch sử/chế tài

1. CMS hiển thị lịch sử comment bị xử lý, Report, cảnh báo, sanction và appeal của user.
2. Cảnh báo/sanction bắt buộc chọn **reason từ taxonomy vi phạm chung**; nếu reason = **“Vi phạm khác”** thì note bắt buộc 1–500 ký tự hợp lệ; reason khác note optional.
3. Sanction tạm thời bắt buộc có thời hạn hợp lệ; Khóa tài khoản Permanent không yêu cầu expiry; mọi sanction cần confirmation trước khi áp dụng.
4. UI/API đều enforce đúng phạm vi Khóa bình luận hoặc Khóa tài khoản.
5. Với Khóa bình luận, user vẫn vào app; reason/trạng thái sanction được hiển thị và notification nghiệp vụ bắt buộc hoạt động theo US09.
6. Với Khóa tài khoản, login phải dừng ở **locked-account screen** hiển thị trạng thái khóa, reason và hướng dẫn **gọi Tổng đài MyTV 1800 1166 (miễn phí, hỗ trợ 24/7) để appeal**; có thể gửi push nếu device nhận được nhưng không phụ thuộc Notification Center trong app.
7. Trong thời gian Account Lock, không tạo/gửi **community notification mới** cho Reply/Mention/badge/tương tác; sau unlock không backfill. Chỉ thông tin bắt buộc liên quan sanction/appeal tiếp tục theo US09.
8. Không tự khóa user chỉ vì một/nhiều Report chưa được xác minh.

### Acceptance Criteria — Appeal

1. **Khóa bình luận**: user còn vào app nên có thể gửi appeal trong app.
2. **Khóa tài khoản**: user không thể appeal trong app; user **gọi Tổng đài MyTV 1800 1166 (miễn phí, hỗ trợ 24/7)**, Support/CSKH tiếp nhận và chuyển appeal vào workflow CMS.
3. CMS phải phân biệt/ghi nhận nguồn appeal phù hợp và cho Admin quyết định giữ nguyên hoặc gỡ chế tài; quyết định có audit.
4. SLA xử lý appeal là **48 giờ** kể từ thời điểm appeal được hệ thống ghi nhận/tiếp nhận vào workflow.
5. Quá 48 giờ, sanction vẫn giữ nguyên; appeal được đánh dấu **Quá SLA** và ưu tiên lên đầu queue.
6. Không tự động gỡ sanction chỉ vì appeal quá SLA.

### Acceptance Criteria — Visibility, KPI và badge integration

1. Trong Account Lock, comment/reply/thread tạm non-public do lock bị **tạm loại khỏi public count/KPI/Engagement**; khi mở khóa, contribution public được tính lại nếu source còn hợp lệ.
2. Nếu root author bị Account Lock, contribution public của **toàn thread** tạm bị loại khỏi KPI/Engagement, kể cả reply của user khác, vì thread không public; moderation state của reply khác không đổi.
3. Badge cá nhân dùng semantics riêng tại US17: Account Lock **không hồi tố invalid** contribution hợp lệ của chính locked user hoặc reply hợp lệ của user khác bị ẩn chỉ do locked root.
4. Rolling window Fan badge vẫn chạy bình thường trong Account Lock; không freeze. User không thể phát sinh active day mới sau effective time vì không thể vào app; active day đã ghi trước lock không bị xóa hồi tố.
5. Like user đã nhận trên content của mình vẫn có thể dùng cho Fan badge nếu source chỉ non-public do Account Lock; chỉ loại khi source bị moderation riêng.
6. Like do một liker sau đó bị Account Lock vẫn có semantics badge recipient theo US17, dù tạm bị loại public Net Like/ranking/Engagement.

### Acceptance Criteria — Audit log

1. Audit tối thiểu lưu actor, time, target, action, before, after; `reason` bắt buộc/nullable theo rule action tương ứng ở US14/US16.
2. Audit bao phủ moderation, Report/Flag/Spoiler, pin/config, warning/sanction, appeal, Undo và thay đổi AI policy.
3. Audit log không thể sửa/xóa bởi role vận hành thông thường.
4. Audit log được lưu **2 năm**; retention này độc lập với soft-delete comment 90 ngày.
5. Truy cập/export PII tuân rule US13 và ghi log khi cần.

### Quy tắc nghiệp vụ

- Sanction phải tương xứng mức vi phạm.
- Cảnh báo/Khóa bình luận/Khóa tài khoản dùng cùng taxonomy vi phạm chung để thống nhất Report → Moderation → Sanction.
- “Vi phạm khác” luôn yêu cầu note 1–500 ký tự; các reason chuẩn khác note optional.
- Khóa bình luận không chặn Report để user vẫn có thể báo nội dung vi phạm; cũng không chặn self-delete.
- Sanction chỉ áp dụng từ **effective time**, không hồi tố hủy Comment/Reply/Edit đã gửi hợp lệ trước đó.
- Account Lock là **access + visibility gate**, không tự biến content thành moderation violation.
- Permanent Account Lock giữ gate vô thời hạn; xóa content phải là moderation action riêng.
- Appeal Account Lock đi qua **Tổng đài MyTV 1800 1166 (miễn phí, hỗ trợ 24/7) → Support/CSKH → CMS** vì user không thể vào app; SLA 48h vẫn giữ.
- Public KPI/Engagement và badge eligibility là hai semantic khác nhau; Account Lock có thể loại contribution khỏi public KPI nhưng không tự invalid contribution badge hợp lệ.
- Appeal là cơ chế review sanction; không làm mất audit cũ.
- IDOR ghi cross-scope (Moderator ngoài scope thao tác Cảnh báo/Khóa bình luận/Khóa tài khoản lên user không thuộc scope): xem test case IDOR ghi tại US13 (TC-US13-010), áp dụng tương tự cho các chế tài tại US16.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục Bảo mật — session invalidation khi Account Lock, IDOR theo scope.*

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US16-001 | History | U1 có moderation/Report/sanction | Mở hồ sơ | Hiển thị đúng timeline, không trộn user khác. |
| TC-US16-002 | Light sanction | Vi phạm Nhẹ | Gửi cảnh báo với reason chuẩn | Cảnh báo có reason/actor/time và notification phù hợp. |
| TC-US16-003 | Reason required | Cảnh báo/Khóa bình luận/Khóa tài khoản | Bỏ reason rồi xác nhận | Không cho áp dụng; chọn một reason taxonomy chung mới được tiếp tục. |
| TC-US16-004 | Other note boundary | Chọn “Vi phạm khác” | Thử note rỗng/whitespace, 1, 500, 501 ký tự | Rỗng/whitespace/501 bị chặn; 1–500 hợp lệ. |
| TC-US16-005 | Comment lock permissions | U1 bị Khóa bình luận, có C1 public | Thử Comment/Reply/Mention/Edit/Self-delete/Like/Report/Rating/Share | Comment/Reply/Mention/Edit mới bị chặn; Self-delete/Like/Report/Rating/Share vẫn được phép nếu hợp lệ. |
| TC-US16-006 | Comment lock durations | Chọn từng preset/custom và thử bỏ duration | Áp dụng | Hỗ trợ 10m/1h/1d/3d/7d/1mo/custom; không có Permanent; sanction tạm thiếu duration bị chặn. |
| TC-US16-007 | Comment lock expiry | Sanction sắp hết | Kiểm tra sau expiry | Quyền tự phục hồi nếu không còn sanction khác. |
| TC-US16-008 | Pending before comment lock | U1 gửi C1 hoặc V2 trước effective time, sau đó bị Khóa bình luận | Admin Duyệt trong thời gian khóa | C1/V2 được xử lý và public bình thường nếu không có gate khác; lock không hồi tố. |
| TC-US16-009 | Account lock authorization | Vi phạm nghiêm trọng | Moderator có quyền khóa | Có thể khóa account không cần Super Admin/two-person approval. |
| TC-US16-010 | Account lock duration | Chọn temp preset/custom/permanent | Áp dụng | Temporary bắt buộc duration hợp lệ; Permanent không cần expiry; state account đúng lựa chọn. |
| TC-US16-011 | Access while locked | U1 đang Account Lock | Thử login/vào app | Không vào app; locked-account screen hiển thị status + reason + Tổng đài MyTV **1800 1166**, thông tin **miễn phí, hỗ trợ 24/7** và hướng dẫn appeal. |
| TC-US16-012 | Hide content on account lock | U1 có comment/reply public | Khóa account | Content U1 tạm non-public, không đổi sang moderation Hidden/Deleted. |
| TC-US16-013 | Locked root cascade | U1 sở hữu root C1; U2/U3 có R1/R2 hợp lệ | Khóa U1 | C1 + toàn thread tạm non-public; R1/R2 giữ moderation state và không bị coi là vi phạm. |
| TC-US16-014 | Restore on unlock | Có content/thread non-public chỉ do lock và item có moderation riêng | Mở khóa | Lock-only content/thread public lại nếu hợp lệ; item có moderation action/gate riêng vẫn không public. |
| TC-US16-015 | Permanent lock | U1 có content public; áp Permanent Account Lock | Kiểm tra lâu dài | Content non-public vô thời hạn nhưng không tự soft-delete/Hidden/Rejected; muốn xóa phải moderation riêng. |
| TC-US16-016 | Rating lock/unlock | U1 có rating | Khóa rồi mở account | Khi khóa, rating bị loại khỏi average + total count public; mở khóa tính lại nếu record còn. |
| TC-US16-017 | Like cast lock/unlock | U1 đã Like target hợp lệ | Khóa rồi mở account | Like record còn; khi khóa bị loại public Net Like/ranking/Engagement; mở khóa tính lại nếu hợp lệ. |
| TC-US16-018 | Pin/Featured temporary visibility | Content U1 đang Pin/có Featured badge | Account Lock rồi mở khóa | Trong khóa Pin/Featured tạm ẩn; mở khóa tự trở lại nếu source còn hợp lệ và Pin chưa expiry. |
| TC-US16-019 | Lock plus moderation | Content U1 đang Pin/Featured, U1 bị lock rồi content bị Admin Ẩn/Xóa/Từ chối | Mở khóa | Pin/Featured không tự trở lại vì source có moderation invalidation riêng. |
| TC-US16-020 | Pending content before account lock | C1/V2 đã Pending trước khi U1 bị Account Lock | Admin Duyệt khi lock còn hiệu lực | Moderation xử lý bình thường nhưng target chưa public; mở khóa mới public nếu vẫn hợp lệ. |
| TC-US16-021 | Public KPI lock cascade | U1 root C1 có reply hợp lệ của U2 | Khóa U1 rồi refresh analytics | Toàn thread tạm bị loại public KPI/Engagement; mở khóa tính lại item hợp lệ. |
| TC-US16-022 | Badge contribution during lock | U1 có Fan contribution hợp lệ; U2 có reply dưới root U1 | Khóa U1 và chạy badge job | Account Lock không tự invalid contribution badge hợp lệ; rolling windows tiếp tục theo US17. |
| TC-US16-023 | Active day lock | U1 đã mở comment area trong ngày rồi bị lock | Chạy badge job | Active day đã ghi trước effective time vẫn giữ; sau lock không tạo active day mới. |
| TC-US16-024 | Community notification suppression | U1 đang Account Lock; phát sinh Reply/Mention/badge event | Theo dõi trong lock và sau unlock | Community notification mới bị suppress và không backfill; sanction/appeal status vẫn là mandatory. |
| TC-US16-025 | Comment-lock appeal | U1 bị Khóa bình luận | Gửi appeal trong app, Admin giữ/gỡ | Appeal vào CMS, có state, quyết định, audit. |
| TC-US16-026 | Account-lock appeal | U1 bị Account Lock | Gọi **1800 1166**; Support/CSKH tạo/chuyển appeal vào CMS | Không cần vào app; hotline hiển thị là **1800 1166 (miễn phí, hỗ trợ 24/7)**; CMS nhận appeal đúng user/sanction/source và Admin xử lý. |
| TC-US16-027 | Appeal SLA | Appeal >48h chưa xử lý | Mở queue | Gắn Quá SLA, ưu tiên lên đầu; sanction vẫn hiệu lực. |
| TC-US16-028 | Audit retention | Có audit cũ | Kiểm tra retention | Audit giữ 2 năm độc lập soft-delete 90 ngày. |
| TC-US16-029 | Audit immutability | Role vận hành thường | Thử sửa/xóa audit | Bị chặn. |
| TC-US16-030 | No auto-sanction | C1 chỉ có Report chưa xác minh | Tạo nhiều Report | Không tự cảnh báo/khóa chỉ từ Report count. |
| TC-US16-031 | Session/Account Lock concurrency | U1 đang đăng nhập, mở màn hình comment, đã gõ nội dung chưa gửi | Admin áp Account Lock trong lúc U1 đang gõ: (a) U1 bấm Gửi sau effective time; (b) request gửi TRƯỚC effective time; (c) gọi API bằng access token cũ sau lock | (a) Session vô hiệu ngay tại effective time, U1 bị đẩy về locked-account screen, nội dung chưa gửi không được tạo; (b) request vào moderation nhưng không public tới khi unlock; (c) mọi API dùng access token cũ đều bị từ chối. |
| TC-US16-032 | Boundary SLA appeal 48h | Appeal in-app (Khóa bình luận) và appeal qua Support/CSKH (Account Lock) tại mốc 47h/48h/49h | Mở queue tại từng mốc | 47h chưa gắn Quá SLA; >48h gắn Quá SLA và lên đầu queue; hành vi tại đúng 48h khớp định nghĩa biên; mốc bắt đầu đếm của appeal qua Support (thời điểm tiếp nhận, không phải thời điểm nhập CMS) được ghi nhận rõ ràng. |
| TC-US16-033 | IDOR ghi cross-scope | Xem test case IDOR ghi tại US13 (TC-US13-010); áp dụng tương tự cho Cảnh báo/Khóa bình luận/Khóa tài khoản trên user ngoài scope Moderator | — | Bị từ chối theo scope; không lộ tồn tại; không tạo audit "thành công" (xem chi tiết tại US13). |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Locked-account screen | **Tài khoản của bạn đang bị khóa**<br>Lý do: {reason}. Thời hạn: đến {dd/mm/yyyy hh:mm} (hoặc: Khóa vô thời hạn). **Liên hệ Tổng đài MyTV 1800 1166 (miễn phí, hỗ trợ 24/7) để gửi yêu cầu khiếu nại.** Khi liên hệ, cung cấp mã vụ việc: {CASE-ID}. Chúng tôi phản hồi trong vòng 48 giờ kể từ khi tiếp nhận.<br>`[Gọi 1800 1166]` `[Sao chép mã vụ việc]` |

