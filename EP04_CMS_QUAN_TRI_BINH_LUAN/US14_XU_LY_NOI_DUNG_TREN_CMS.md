# US14 — Xử lý nội dung trên CMS

> Thuộc EP04 — CMS quản trị bình luận
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là Admin/Moderator kiểm duyệt**, tôi muốn duyệt, từ chối, ẩn, xóa và xử lý Report/Flag/Spoiler, để thực thi chính sách cộng đồng nhất quán và có audit.

### Ưu tiên

**Must**

### Reason taxonomy chuẩn

Các action bắt buộc reason dùng chung taxonomy AI/Report/CMS:
- Spoiler
- Spam/quảng cáo
- Xúc phạm/ngôn từ công kích
- Nội dung không phù hợp
- Sai thông tin
- Vi phạm khác

### Acceptance Criteria — Moderation action

1. Admin có thể Duyệt nội dung Chờ duyệt → Hiển thị, nhưng visibility cuối còn phải tôn trọng gate khác như scope Đóng hoặc Account Lock của tác giả.
2. Admin có thể Từ chối nội dung Chờ duyệt, Ẩn nội dung đang Hiển thị và Xóa mềm comment/reply sau xác nhận.
3. **Duyệt không cần reason**.
4. **Chỉ Từ chối / Ẩn / Xóa bắt buộc reason**: Admin phải chọn một reason chuẩn. Với 5 reason chuẩn đầu, note là tùy chọn; nếu chọn **“Vi phạm khác”**, note **bắt buộc**, không được chỉ khoảng trắng và tối đa **500 ký tự** ở cả UI/API.
5. **Bỏ qua Report / gắn-bỏ Flag / thêm-bỏ Spoiler không bắt buộc reason**.
6. Từ chối/Ẩn/Xóa phải làm tác giả thấy reason trong app và nhận **push + in-app notification** khi user có thể truy cập; Account Lock tuân kênh thông báo riêng tại US09/US16. Notification nghiệp vụ không bị tắt bởi community notification setting.
7. Khi CMS/Admin **Xóa mềm root**, chính root chuyển Xóa mềm 90 ngày và toàn thread không public do cascade; **reply con không tự chuyển sang Xóa mềm** chỉ vì root bị xóa, mà giữ moderation state riêng trước cascade trừ khi có action riêng trên reply. Reply chỉ mang cờ `hidden_by_root_cascade = true`, **không có đồng hồ retention riêng**; retention 90 ngày chỉ áp dụng cho root.
8. **Ẩn root comment** làm toàn bộ thread tạm không public nhưng không tự đổi moderation state của replies; replies hợp lệ của user khác không bị coi là vi phạm chỉ vì root bị Ẩn.
9. CMS kiểm tra state hiện tại trước khi lưu để tránh ghi đè im lặng giữa nhiều Admin.

### Acceptance Criteria — Report/Flag/Spoiler

1. Admin xem reporter, reason, description, time và version target.
2. Chỉ có một action giữ nội dung hợp lệ là **“Bỏ qua Report”**: đóng Report và giữ comment ở trạng thái Hiển thị nếu không có moderation action/gate khác.
3. Không dùng action “Duyệt giữ nguyên” riêng để tránh trùng semantics.
4. Nếu kết luận vi phạm, Admin dùng Ẩn/Xóa hoặc action moderation phù hợp.
5. Nhiều Report không tự đổi state trước quyết định CMS.
6. Lịch sử xử lý từng Report được lưu và reporter nhận in-app notification theo US10.
7. Gắn/bỏ **Flag** và thêm/bỏ **Spoiler** phải cập nhật đúng metadata/state hiển thị tương ứng của item và tạo audit; các action này không tự đồng nghĩa với Từ chối/Ẩn/Xóa nếu Admin chưa chọn moderation action đó.
8. **Phạm vi action Spoiler của Admin là toàn bộ nội dung comment/reply.** Từ US04, Spoiler là thuộc tính của từng đoạn chữ do tác giả tự đánh; Admin **không** chỉnh sửa theo đoạn mà chỉ có một công tắc ở cấp item:
   - **Thêm Spoiler:** toàn bộ phần chữ của comment/reply hiển thị dưới dạng làm mờ, người xem chạm để hiện như bình thường.
   - **Bỏ Spoiler:** trả nội dung về **đúng định dạng gốc của tác giả**, gồm cả những đoạn tác giả đã tự làm mờ — thao tác của Admin không xóa lựa chọn của tác giả mà chỉ chồng lên khi đang bật.
   - Audit ghi rõ đây là spoiler cấp item do Admin đặt, phân biệt với các đoạn làm mờ do tác giả tạo.
   - CMS **không** cung cấp trình soạn thảo cho phép Admin sửa định dạng theo đoạn trong nội dung của người khác.

### Acceptance Criteria — Bulk moderation

1. MVP chỉ hỗ trợ bulk cho đúng 4 action: **Duyệt / Từ chối / Ẩn / Xóa mềm**, tối đa **100 comment/reply/lần**.
2. **Bỏ qua Report / Flag / Spoiler không hỗ trợ bulk** trong MVP và phải xử lý từng item.
3. Hệ thống validate quyền/state từng item trước khi xử lý.
4. Bulk dùng **partial success**: item hợp lệ vẫn thành công; item lỗi báo rõ; không rollback item đã thành công.
5. Bulk **Duyệt không cần reason**. Với bulk **Từ chối/Ẩn/Xóa**, Admin chọn **một reason chung cho batch** và có thể **override reason riêng từng item**.
6. Nếu reason cuối cùng của batch/item là **“Vi phạm khác”**, note tương ứng bắt buộc 1–500 ký tự hợp lệ; item override sang reason khác không bị bắt note “Vi phạm khác”.
7. Không được báo “thành công toàn bộ” nếu có item thất bại.

### Acceptance Criteria — Undo

1. CMS hỗ trợ Undo **Từ chối / Ẩn / Xóa mềm do CMS/Admin**. **Undo Từ chối/Ẩn không giới hạn thời gian; Undo Xóa mềm giới hạn trong 90 ngày kể từ thời điểm xóa.** **Không hỗ trợ Undo để public lại content do user self-delete** theo US05.
2. Undo khôi phục state theo quy tắc đã chốt:
   - Undo **Từ chối** → **Chờ duyệt**.
   - Undo **Ẩn** → **Hiển thị** nếu không có gate khác.
   - Undo **Xóa mềm** → **state ngay trước khi Xóa**.
3. Nếu Undo Xóa mềm một **root comment do CMS/Admin xóa**, với điều kiện **root còn trong 90 ngày retention**, hệ thống khôi phục root và toàn bộ reply đã mất public chỉ do cascade root delete; mỗi reply quay về visibility tương ứng với **state riêng vốn được giữ nguyên** (reply không có đồng hồ retention riêng). Reply có moderation state riêng trước đó không bị tự public lại.
4. Undo Ẩn root làm thread hợp lệ hiện lại theo state riêng của từng reply; không coi reply từng bị visibility cascade là đã bị moderation.
5. Mọi Admin/Moderator có quyền moderation tương ứng đều được Undo, không cần là người thực hiện action ban đầu.
6. **Undo không bắt buộc nhập reason**.
7. **Undo chỉ khôi phục content state**, không tự khôi phục Pin đã mất hoặc huy hiệu Nổi bật đã bị thu hồi do moderation. Pin phải được Admin ghim lại; Featured badge phải được hệ thống đánh giá/cấp lại theo rule hiện hành.
8. Undo tạo audit event mới với actor/time/action/before-after; không xóa/sửa audit cũ.

### Acceptance Criteria — SLA moderation

1. Item Chờ duyệt có SLA **24 giờ** kể từ lúc vào moderation queue.
2. CMS hiển thị thời gian chờ, cảnh báo item sắp/quá SLA.
3. Quá 24 giờ vẫn giữ **Chờ duyệt**, đánh dấu **Quá SLA** và ưu tiên lên đầu trong cùng nhóm risk.
4. Không tự Duyệt/Từ chối chỉ vì quá SLA.
5. Nếu tác giả **hủy đăng** nội dung đang Chờ duyệt (US05 AC15), item **biến mất khỏi moderation queue ngay** và không tính vào SLA. Admin không cần và không thể ra quyết định cho item đã hủy; nếu Admin đang mở item đó thì thao tác Duyệt/Từ chối bị từ chối với thông báo nội dung không còn tồn tại. Thao tác hủy của tác giả **không tạo audit event** nên không xuất hiện trong lịch sử xử lý.

### Quy tắc nghiệp vụ

- Duyệt no reason; Từ chối/Ẩn/Xóa = reason chuẩn bắt buộc; **“Vi phạm khác” = note bắt buộc tối đa 500 ký tự**, các reason khác note optional.
- Flag/Spoiler/Bỏ qua Report không bắt buộc reason và không bulk trong MVP.
- Bulk = Duyệt/Từ chối/Ẩn/Xóa mềm, max 100, partial success.
- Admin Ẩn/Xóa root có thể làm thread non-public do cascade nhưng **không tự đổi moderation state của replies**; đây là cơ sở để giữ badge contribution của reply user khác nếu chính reply vẫn hợp lệ theo US17.
- Undo là action sửa sai độc lập: Từ chối→Chờ duyệt, Ẩn→Hiển thị, Xóa mềm→state trước Xóa; mọi Undo phải audit.
- Undo root delete chỉ đảo phần cascade do **CMS/Admin root delete** gây ra.
- **User self-delete root khác hoàn toàn**: US05 quy định root + toàn bộ replies cùng soft-delete và Admin không Undo public lại.
- Undo moderation không tự phục hồi Pin/Featured badge đã mất do moderation invalidation.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục Bảo mật — XSS/sanitization cho note "Vi phạm khác" và export CSV/XLSX (formula injection), IDOR theo scope.*

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US14-001 | Approve | C1 Chờ duyệt | Duyệt không nhập reason | C1 chuyển Hiển thị về state moderation; public thực tế vẫn tôn trọng scope/account visibility gate; audit before-after. |
| TC-US14-002 | Reason required | Từ chối/Ẩn/Xóa | Bỏ reason rồi xác nhận | Không cho lưu; chọn taxonomy hợp lệ mới xử lý được. |
| TC-US14-003 | Other note | Từ chối/Ẩn/Xóa với reason “Vi phạm khác” | Thử note rỗng/whitespace, 1 ký tự, 500, 501 | Rỗng/whitespace/501 bị chặn; 1–500 ký tự hợp lệ được lưu nhất quán UI/API. |
| TC-US14-004 | Standard reason note | Chọn một trong 5 reason chuẩn đầu | Bỏ note rồi xử lý | Được phép; note là optional. |
| TC-US14-005 | No-reason actions | Bỏ qua Report/Flag/Spoiler | Thực hiện không nhập reason | Action được phép và có audit. |
| TC-US14-006 | Flag/Spoiler effect | C1 đang Hiển thị và **tác giả đã tự làm mờ một đoạn chữ** trong nội dung | Gắn rồi bỏ Flag; Admin thêm Spoiler rồi bỏ Spoiler; đối chiếu hiển thị phía người xem ở từng bước | Metadata/UI state tương ứng thay đổi đúng action; C1 không tự Từ chối/Ẩn/Xóa nếu chưa có moderation action riêng; khi Admin thêm Spoiler thì **toàn bộ** phần chữ bị làm mờ; khi Admin bỏ Spoiler thì nội dung trở lại **đúng định dạng gốc của tác giả**, đoạn tác giả tự làm mờ vẫn còn mờ; audit đầy đủ. |
| TC-US14-007 | Author notification | Admin Từ chối/Ẩn/Xóa C1 | U1 kiểm tra kênh nhận thông tin | U1 thấy reason/notification theo US09/US16; Account Lock không phụ thuộc Notification Center. |
| TC-US14-008 | CMS root delete cascade | C1 có R1/R2 với state riêng | CMS Xóa mềm C1 | C1 soft-delete; toàn thread không public; R1/R2 giữ state riêng và không tự thành soft-delete chỉ do cascade. |
| TC-US14-009 | Hide root cascade | C1 có R1/R2 public | Admin Ẩn C1 | Toàn thread không public; R1/R2 không đổi moderation state. |
| TC-US14-010 | Concurrency | A/B cùng mở C1 | A xử lý trước, B lưu state cũ | B nhận conflict; không ghi đè im lặng. |
| TC-US14-011 | Report semantics | C1 có Report nhưng không vi phạm | Chọn “Bỏ qua Report” | Report đóng; C1 tiếp tục Hiển thị nếu không có gate/action khác; không có “Duyệt giữ nguyên” riêng. |
| TC-US14-012 | Bulk allowed actions | Có item phù hợp cho Duyệt/Từ chối/Ẩn/Xóa và item có Report/Flag/Spoiler | Mở bulk action | Chỉ có 4 action Duyệt/Từ chối/Ẩn/Xóa mềm; Report/Flag/Spoiler không có bulk action. |
| TC-US14-013 | Bulk boundary | 99/100/101 item | Thực hiện bulk | 99/100 được phép; 101 bị chặn/yêu cầu giảm selection. |
| TC-US14-014 | Partial success | 100 item có một số stale/unauthorized | Bulk | Item hợp lệ xử lý thành công; item lỗi báo riêng; không rollback. |
| TC-US14-015 | Bulk reason/Other note | Bulk Duyệt và bulk Từ chối/Ẩn/Xóa; thử reason “Vi phạm khác” | Thực hiện từng loại | Duyệt không bắt reason; Từ chối/Ẩn/Xóa bắt reason; item/batch có reason cuối là “Vi phạm khác” bắt note 1–500. |
| TC-US14-016 | Undo reject | C1 bị Từ chối từ Chờ duyệt | Moderator khác có quyền Undo không nhập reason | C1 quay về Chờ duyệt; audit event mới được tạo. |
| TC-US14-017 | Undo hide | C1 bị Ẩn từ Hiển thị | Undo | C1 về Hiển thị nếu không có gate khác; thread reply hợp lệ hiện lại theo state riêng; audit event mới. |
| TC-US14-018 | Undo soft delete | C1 bị CMS Xóa mềm khi trước đó ở Hiển thị/Ẩn/Chờ duyệt | Undo từng case | C1 quay đúng state ngay trước Xóa, không mặc định về Hiển thị. |
| TC-US14-019 | Undo CMS root cascade | C1 có R1 Hiển thị và R2 Ẩn riêng trước CMS root delete | Xóa root rồi Undo trong retention | C1 trở lại state trước delete; R1 lại public, R2 vẫn Ẩn; replies không cần “restore khỏi soft-delete” vì state riêng không bị đổi bởi cascade. |
| TC-US14-020 | Self-delete no Undo | C1 do chính user self-delete | Admin thử Undo trong 90 ngày | Không cho public lại; root + replies cascade self-delete chỉ phục vụ retention/audit theo US05. |
| TC-US14-021 | Undo side effects | C1 từng Pin + source Featured badge, sau đó Admin Ẩn/Xóa rồi Undo | Kiểm tra sau Undo | Content state được khôi phục nhưng Pin không tự trở lại; Featured badge không tự phục hồi, phải re-evaluate/re-grant. |
| TC-US14-022 | SLA | Item pending 23h/24h/>24h | Mở queue | Hiển thị thời gian/badge; >24h = Quá SLA và ưu tiên trong cùng risk, state vẫn pending. |
| TC-US14-023 | Authorization | Role chỉ đọc | Thử moderation/Undo/bulk | UI/API chặn action không được cấp. |
| TC-US14-024 | State × action âm | 5 item đúng 5 state: pending/visible/rejected/hidden/softdeleted | Gọi Duyệt/Từ chối/Ẩn/Xóa mềm/Bỏ qua Report/Flag/Spoiler qua UI và API cho từng item | Chỉ tổ hợp state × action hợp lệ được thực hiện; tổ hợp còn lại bị chặn cả UI và API, không ghi audit "thành công". |
| TC-US14-025 | Bulk selection trộn state | Selection gồm 5 item ở 5 state khác nhau | Thực hiện bulk action | Item sai state báo lỗi riêng theo item; item hợp lệ vẫn được xử lý; không báo "thành công toàn bộ". |
| TC-US14-026 | Boundary Undo Xóa mềm và Từ chối/Ẩn không giới hạn | C1 bị Xóa mềm tại D-89/D-90/D-91; C2/C3 bị Từ chối/Ẩn từ 8 tháng trước | Undo từng trường hợp | D-89 Undo được; D-90 vẫn trong hạn (đúng biên 90 ngày); D-91 bị chặn; Undo Từ chối/Ẩn ở mốc 8 tháng vẫn thực hiện được vì không giới hạn thời gian. |
| TC-US14-027 | XSS trong note "Vi phạm khác" | Từ chối/Ẩn/Xóa với reason "Vi phạm khác", note chứa payload injection (`<script>`, `=CMD(...)`, v.v.) | Lưu note rồi xem CMS list/detail và export CSV/XLSX | Payload được escape khi hiển thị trên CMS list/detail; export CSV/XLSX vô hiệu hóa formula injection (không thực thi công thức). |
