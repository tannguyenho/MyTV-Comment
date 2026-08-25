# US17 — Huy hiệu người dùng

> Thuộc EP05 — Tăng trưởng và phân tích
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là người dùng tích cực**, tôi muốn được ghi nhận bằng huy hiệu phù hợp, để có động lực tiếp tục đóng góp nội dung chất lượng.

### Ưu tiên

**Could**

### Các loại và tiêu chí đã chốt

#### Fan tích cực
- Xét rolling **30 ngày gần nhất**.
- Hoạt động ít nhất **7 ngày**.
- Có ít nhất **10 comment/reply hợp lệ**.
- Không yêu cầu Like nhận được.

#### Fan kỳ cựu
- Xét rolling **90 ngày gần nhất**.
- Hoạt động ít nhất **30 ngày**.
- Có ít nhất **30 comment/reply hợp lệ**.
- Nhận ít nhất **30 Like** trong 90 ngày theo semantics badge tại US này.


#### Nổi bật
- Badge tự động cấp toàn MyTV cho tác giả có bình luận nổi bật.
- Điều kiện grant và revoke theo README mục 5.11 (≥20 public Net Like + ≥5 Reply + Top10% Featured Score toàn MyTV trong 30 ngày).
- Tên hiển thị trên UI là **Nổi bật**; trong tài liệu và test case gọi đủ là **huy hiệu Nổi bật** để không lẫn với **sắp xếp Nổi bật** (xem glossary README 5.15).

#### Custom (Admin cấp / Chuyên gia)
- Admin cấp thủ công cho user phù hợp; tên hiển thị trên UI là **Custom**.
- Có thể đặt ngày hết hạn hoặc không; nếu không đặt thì giữ tới khi Admin thu hồi/tắt loại badge.

### Acceptance Criteria

1. Hệ thống đánh giá badge tự động **mỗi ngày 1 lần**.
2. Một **ngày hoạt động** được tính khi user **đã đăng nhập mở/đọc khu vực Bình luận đang khả dụng ít nhất 1 lần trong ngày**; mở nhiều lần cùng ngày vẫn chỉ tính 1 active day. Guest không tích lũy active day.
3. Nếu scope đang **Đóng bình luận**, việc chỉ mở trang phim không tạo active day vì user không thể mở/đọc comment area.
4. Nếu user bị **Account Lock** sau khi đã có active day trong ngày, active day đã ghi **không bị xóa hồi tố**. Từ effective time của lock không phát sinh active day mới vì user không thể vào MyTV.
5. Rolling window 30/90 ngày vẫn chạy bình thường trong Account Lock, **không freeze**. Nếu Fan badge không còn đạt điều kiện thì vẫn áp dụng grace bình thường.
6. Nếu user không còn đạt điều kiện Fan tích cực/Fan kỳ cựu, áp dụng **grace period 7 ngày**; hết 7 ngày vẫn không đạt mới tự thu hồi.
7. Mỗi user chỉ hiển thị tối đa **1 badge** cạnh tên.
8. Thứ tự ưu tiên hiển thị: **Custom (Admin/Chuyên gia cấp) > Nổi bật > Fan kỳ cựu > Fan tích cực**. Thứ tự này đồng bộ với README mục 5.11. Sheet giải thích huy hiệu trong thiết kế liệt kê theo trình tự khác, đó chỉ là thứ tự giới thiệu nội dung và **không** dùng làm thứ tự ưu tiên hiển thị badge cạnh nickname.
9. Khi user được cấp hoặc bị thu hồi badge, gửi **push + in-app notification** nếu notification cộng đồng đang bật theo US09; nếu user đang Account Lock thì community notification bị suppress và không backfill sau unlock.
10. Khi Admin tắt một loại badge, badge đó **ẩn khỏi UI ngay** nhưng lịch sử sở hữu/cấp/thu hồi vẫn được giữ cho audit; bật lại không tạo duplicate.
11. Comment/reply bị **moderation riêng** Ẩn/Xóa/Từ chối/spam không được dùng để tích lũy điều kiện badge tự động.
12. **Account Lock không tự làm mất Fan contribution hợp lệ của chính locked user**: comment/reply và Like đã nhận vẫn được tính cho Fan badge nếu source chỉ tạm non-public do Account Lock; chỉ loại khi source bị moderation riêng hoặc bị lifecycle Delete hợp lệ khác.
13. Nếu root author bị Account Lock hoặc Admin Ẩn/Xóa root làm thread non-public nhưng reply của user khác **không bị đổi moderation state**, contribution badge hợp lệ của user reply **vẫn được giữ**; không phạt user khác vì hành vi/state của root author.
14. Ngoại lệ self-delete: nếu root author **tự xóa root**, root + toàn bộ reply cascade soft-delete theo US05; các reply bị cascade này và Like gắn với chúng **không còn là contribution badge hợp lệ**.
15. Like do một account tạo rồi account đó bị **Account Lock** vẫn **được tính cho Fan kỳ cựu của recipient**. Đây là semantics badge cố ý khác public Net Like/ranking/Engagement để badge recipient không dao động theo lock/unlock của past liker.
16. Like mà locked user **đã nhận** trên content của mình vẫn được tính cho Fan kỳ cựu nếu source chỉ non-public do Account Lock; nếu source bị moderation Ẩn/Xóa/Từ chối thì loại.
17. Report chưa xác minh không tự làm mất badge.
18. Mọi thay đổi cấu hình/cấp thủ công/thu hồi có audit.

### Quy tắc nghiệp vụ

- “Ngày hoạt động” là **read/open activity có account** của khu vực Bình luận đang khả dụng, không yêu cầu Comment/Reply/Like/Rating/Report/Share.
- Một account tối đa **1 active day/ngày** dù mở khu vực Bình luận nhiều lần hoặc ở nhiều phim.
- Guest chỉ đọc không tạo active day; scope Đóng cũng không tạo active day.
- Điều kiện active day và điều kiện số lượng comment/reply của Fan badge là **hai điều kiện độc lập**; việc chỉ đọc có thể tăng active day nhưng không tăng count comment/reply.
- Account Lock là visibility/access gate, **không retroactively invalidate** historical badge contribution hợp lệ; rolling window vẫn tự trượt theo thời gian.
- Public KPI/Net Like và badge eligibility là hai data semantics khác nhau: Like từ locked liker bị loại public aggregate nhưng vẫn giữ cho Fan kỳ cựu recipient.
- Với user khác reply dưới root non-public do Account Lock/Admin moderation root, contribution badge giữ nếu chính reply không bị invalid. **Self-delete root là khác biệt:** reply bị cascade soft-delete thật nên bị loại.
- Grace period 7 ngày áp dụng badge hành vi Fan tích cực/Fan kỳ cựu.
- Featured grant dùng public metrics tại thời điểm xét; sau grant, metric/ranking drop không tự revoke.
- Unlock Account Lock có thể tự hiện lại Featured badge chỉ tạm ẩn; Undo moderation không tự restore badge đã revoke.
- Khi user có nhiều badge hiệu lực, UI luôn chọn **badge có cấp ưu tiên cao nhất** theo thứ tự đã chốt.

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US17-001 | Active day | U1 đăng nhập; comment area Mở | Mở/đọc khu vực Bình luận ít nhất 1 lần trong ngày | Ngày đó được tính đúng 1 active day cho U1. |
| TC-US17-002 | Active dedup | U1 đăng nhập | Mở khu vực Bình luận nhiều lần, nhiều phim trong cùng ngày | Vẫn chỉ tính 1 active day trong ngày. |
| TC-US17-003 | Guest active | Phiên guest | Mở/đọc khu vực Bình luận nhiều lần | Không tạo active day badge vì không có account. |
| TC-US17-004 | Closed scope active | U1 login; scope Đóng bình luận | Mở trang phim | Không tạo active day vì comment area không khả dụng. |
| TC-US17-005 | Fan active | 30d: U1 có 7 active days + 10 comment/reply hợp lệ | Chạy daily job | Cấp Fan tích cực. |
| TC-US17-006 | Fan active boundary | 6 active days hoặc 9 comment/reply | Chạy job | Không cấp. |
| TC-US17-007 | Loyal | 90d: 30 active days, 30 comment/reply, 30 Like nhận theo badge semantics | Chạy job | Cấp Fan kỳ cựu. |
| TC-US17-008 | Loyal boundary | Thiếu một trong ba ngưỡng | Chạy job | Không cấp. |
| TC-US17-009 | Daily/grace | User vừa không còn đạt badge Fan | Chạy daily job trong grace và sau grace | Badge giữ trong 7-day grace; hết grace vẫn không đạt thì thu hồi. |
| TC-US17-010 | Account Lock rolling | U1 đang có Fan badge rồi bị Account Lock | Chạy job qua nhiều ngày | Window vẫn trượt; không có active day mới sau lock; grace vẫn áp dụng nếu tụt ngưỡng. |
| TC-US17-011 | Active day before lock | U1 đã mở comment area trong ngày, sau đó bị Account Lock | Chạy job | Active day đã ghi vẫn giữ, không xóa hồi tố. |
| TC-US17-012 | Locked user content contribution | U1 có comment/reply/Like nhận hợp lệ, sau đó Account Lock | Chạy Fan job | Contribution vẫn dùng cho badge nếu source chỉ non-public do lock; không đồng nhất với public KPI exclusion. |
| TC-US17-013 | Reply under locked root | U2 có R1 hợp lệ dưới root U1; U1 bị Account Lock | Chạy badge job U2 | R1 và Like U2 nhận vẫn giữ eligibility; U2 không bị phạt vì U1 bị khóa. |
| TC-US17-014 | Reply under admin-hidden/deleted root | U2 có R1 hợp lệ; Admin Ẩn/Xóa root U1 nhưng R1 không bị moderation riêng | Chạy badge job U2 | Contribution badge hợp lệ của U2 vẫn giữ dù thread không public. |
| TC-US17-015 | Self-delete root cascade | U2 có R1 dưới root U1; U1 self-delete root | Chạy job sau cascade | R1 đã soft-delete theo US05 nên R1 và Like gắn với R1 bị loại khỏi eligibility. |
| TC-US17-016 | Locked liker exception | U1 đã Like content U2 rồi U1 bị Account Lock | Chạy Fan kỳ cựu job U2 | Like vẫn tính cho U2 dù public Net Like tạm loại Like U1. |
| TC-US17-018 | Featured locked-liker threshold | Comment có 20 Like record nhưng 1 Like từ account đang Lock nên public Net Like=19 | Chạy grant job | Không đạt ngưỡng ≥20 tại lần cấp mới. |
| TC-US17-019 | Featured stability metrics | Badge đã cấp, Like<20/Reply<5 hoặc tụt Top10% nhưng source vẫn public/hợp lệ | Chạy job | Không thu hồi chỉ do metric/ranking tụt. |
| TC-US17-020 | Featured moderation invalid | Source bị Ẩn/Xóa/Từ chối riêng | Chạy job | Badge bị thu hồi. |
| TC-US17-021 | Featured Account Lock | Source hợp lệ nhưng tác giả bị Account Lock rồi mở khóa | Kiểm tra badge | Badge tạm ẩn trong lock, không revoke; mở khóa tự hiện lại nếu source vẫn hợp lệ. |
| TC-US17-022 | Featured Undo moderation | Badge đã revoke vì source bị Admin Ẩn/Xóa; sau đó Undo | Chạy/không chạy evaluation | Undo content không tự restore badge; chỉ re-evaluation/re-grant theo rule hiện hành mới có thể cấp lại. |
| TC-US17-023 | Priority display | U1 có đồng thời cả 4 badge: Custom (Admin/Chuyên gia cấp), Nổi bật, Fan kỳ cựu, Fan tích cực | Mở comment; sau đó lần lượt thu hồi từng badge theo thứ tự ưu tiên và mở lại | Luôn chỉ hiển thị **1 badge** cạnh nickname theo thứ tự **Custom > Nổi bật > Fan kỳ cựu > Fan tích cực**: đủ 4 badge thì hiện Custom; thu hồi Custom thì hiện Nổi bật; thu hồi tiếp thì hiện Fan kỳ cựu; cuối cùng là Fan tích cực. |
| TC-US17-024 | Admin badge expiry | Cấp badge với/không expiry | Kiểm tra trước/sau expiry | Có expiry thì hết hiệu lực đúng mốc; không expiry thì giữ tới thu hồi. |
| TC-US17-025 | Toggle type | Tắt loại badge đang có owner | Refresh UI | Badge ẩn ngay; history còn; bật lại không duplicate. |
| TC-US17-026 | Notification | Grant/revoke badge khi account bình thường và khi Account Lock | Kiểm tra push/in-app | Bình thường gửi theo setting US09; Account Lock suppress community notification và không backfill sau unlock. |
| TC-US17-027 | Top 10% boundary calculation | Dataset 1000 comment public đăng trong 30 ngày, gộp toàn bộ phim trên hệ thống, Featured Score (biến thể không freshness) đã biết trước cho từng comment; comment hạng 99, 100, 101 (quanh biên Top 10%) đều đạt ≥20 Net Like công khai + ≥5 Reply công khai; nhiễu thêm: 1 comment đang được Ghim, 1 comment non-public do Account Lock tác giả, 1 comment đã Ẩn, đều nằm trong 1000 comment gốc | Chạy job cấp huy hiệu Nổi bật, đối chiếu dân số dùng để tính Top 10% và danh sách comment được cấp; chạy lại job nhiều lần với cùng dữ liệu | Dân số dùng để tính Top 10% chỉ gồm comment đủ điều kiện public (loại trừ comment Ẩn và comment non-public do Account Lock; comment Ghim không bị loại chỉ vì đang ghim); comment hạng 99 và hạng 100 (đúng biên 10%) được cấp badge; comment hạng 101 không được cấp; chạy lại job nhiều lần với cùng dữ liệu cho kết quả xếp hạng đồng hạng ổn định, lặp lại giống nhau giữa các lần chạy. |
| TC-US17-028 | Grace period 7 ngày boundary | U1 đang có Fan tích cực/Fan kỳ cựu, tụt dưới ngưỡng từ ngày D0 | Chạy job daily tại D+6, D+7, D+8; tình huống phụ: U1 đạt lại ngưỡng ở D+5 rồi tụt lại ở D+6 | D+6 badge còn giữ (trong grace); D+7 (đúng biên 7 ngày) và D+8 xử lý theo định nghĩa "hết 7 ngày vẫn không đạt mới tự thu hồi" đã chốt; tình huống phụ: khi U1 đạt lại ngưỡng ở D+5, bộ đếm grace được reset (hủy đếm dở), nên khi tụt lại ở D+6 grace 7 ngày mới được tính lại từ D+6, không cộng dồn với lần tụt trước. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Bottom sheet giải thích badge (chạm vào chip badge trên card) | **Huy hiệu thành viên**<br>Là huy hiệu dành cho những thành viên có những đóng góp tích cực trong hoạt động cộng đồng.<br>**Fan kỳ cựu** — Là huy hiệu dành cho những thành viên tích cực hoạt động trong thời gian dài. · **Fan tích cực** — Là huy hiệu dành cho những thành viên đã tích cực tham gia các hoạt động. · **Nổi bật** — Là huy hiệu dành riêng cho những thành viên nổi trội và những đóng góp nổi bật trong cộng đồng. · *và những huy hiệu độc quyền khác…*<br>`[Đóng]`<br><br>Đây là **thứ tự giới thiệu nội dung**, không phải thứ tự ưu tiên hiển thị badge cạnh nickname (xem AC8). |
| Notification khi được cấp badge mới | **Bạn nhận huy hiệu {tên badge}**<br>Cảm ơn bạn đã đồng hành cùng cộng đồng MyTV.<br>`[Xem huy hiệu]` |
