# US10 — Report bình luận vi phạm

> Thuộc EP03 — An toàn và kiểm duyệt
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là người dùng đã đăng nhập**, tôi muốn Report một comment/reply không phù hợp theo lý do cụ thể, để Admin xem xét và bảo vệ môi trường cộng đồng.

### Ưu tiên

**Must**

### Taxonomy chung

Report/AI/CMS dùng chung taxonomy nghiệp vụ:
- Spoiler
- Spam/quảng cáo
- Xúc phạm/ngôn từ công kích
- Nội dung không phù hợp
- Sai thông tin
- Vi phạm khác (UI có thể hiển thị “Khác”)

### Acceptance Criteria

1. User đăng nhập có thể Report comment/reply đang Hiển thị mà mình có quyền xem.
2. User **không được Report comment/reply của chính mình**.
3. Phải chọn một reason taxonomy hợp lệ; khi chọn **Khác/Vi phạm khác**, description là **bắt buộc**, tối đa **500 ký tự**; whitespace-only không hợp lệ. UI và API dùng cùng giới hạn.
4. Report lưu reporter account ID, target ID, version ID, reason, description khi có, thời gian và trạng thái xử lý.
5. Report được chuyển vào CMS; số lượng Report không public trên app.
6. Một hoặc nhiều Report **không tự động Ẩn/Xóa** comment; nội dung tiếp tục Hiển thị cho tới khi CMS/moderation có quyết định khác.
7. Cùng một user chỉ được Report lại cùng target sau **24 giờ kể từ lần Report trước**, miễn target vẫn Hiển thị.
8. Mỗi user tối đa **10 Report trong 1 giờ** trên toàn hệ thống.
9. Sau khi Admin xử lý Report, reporter nhận **in-app notification** xác nhận Report đã được xử lý; không gửi push và không tiết lộ chi tiết chế tài của user bị Report.
10. Guest chọn Report được chuyển sang login; không tạo Report trước xác thực.
11. Danh tính reporter không hiển thị cho cộng đồng.
12. **Smart TV áp dụng US10** với taxonomy rút gọn: TV chỉ hiển thị **5 reason không cần mô tả** (`Có spoiler`, `Spam/Quảng cáo bình luận`, `Xúc phạm/ngôn từ công kích`, `Nội dung không phù hợp`, `Sai thông tin`). Reason **Khác/Vi phạm khác** bị **ẩn trên TV** vì bắt buộc nhập mô tả 1–500 ký tự, và TV không nhập văn bản. Toàn bộ luồng thao tác bằng remote.
13. Trên Smart TV, entry Báo cáo nằm trong **menu action rút gọn của comment/reply chỉ gồm `Báo cáo`** (TV không có Sửa/Xóa/Chia sẻ). Các quy tắc còn lại giữ nguyên như Phone/Web: không Report nội dung của chính mình, cooldown 24 giờ cùng target, rate limit 10 Report/giờ và guest phải đăng nhập trước khi tạo Report.
14. Thông báo kết quả xử lý Report cho reporter trên Smart TV vào **mục thông báo sẵn có của ứng dụng Smart TV**; nội dung thông báo giống Phone/Web và không tiết lộ chế tài của user bị Report. Bấm vào thông báo mở đúng phim/comment liên quan nếu target còn khả dụng, ngược lại dùng fallback theo Effective Visibility Resolver (US12).

### Quy tắc nghiệp vụ

- Report là tín hiệu, không phải kết luận vi phạm.
- “Bỏ qua Report” tại US14 là action đóng Report khi Admin xác định nội dung không vi phạm; không có action “Duyệt giữ nguyên” riêng.
- Description của “Khác/Vi phạm khác”: bắt buộc, **1–500 ký tự hợp lệ** sau khi loại trường hợp chỉ có khoảng trắng.
- Rate limit 10 Report/giờ và cooldown 24h/cùng target áp dụng đồng thời.
- Taxonomy rút gọn trên Smart TV **không** đổi taxonomy nghiệp vụ chung: Report từ TV vào CMS cùng một luồng và cùng cấu trúc dữ liệu, chỉ khác là bản ghi từ TV không bao giờ có reason `Vi phạm khác`.
- Ma trận nền tảng: US10 áp dụng Phone, Web và Smart TV. Rate limit và cooldown tính theo **account**, không theo thiết bị: Report trên TV và trên Phone dùng chung quota.

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Nhãn 6 lựa chọn trên form | `Có spoiler` · `Spam/Quảng cáo bình luận` · `Xúc phạm/ngôn từ công kích` · `Nội dung không phù hợp` · `Sai thông tin` · `Khác` |
| Nhãn lựa chọn trên Smart TV | Chỉ 5 lựa chọn, **ẩn `Khác`**: `Có spoiler` · `Spam/Quảng cáo bình luận` · `Xúc phạm/ngôn từ công kích` · `Nội dung không phù hợp` · `Sai thông tin`. Không có ô mô tả trên TV. |
| Ô mô tả khi chọn Khác | Placeholder **“Nhập phản ánh của bạn về bình luận này”**, kèm bộ đếm `{n}/500`; nút `Báo cáo` disabled tới khi có nội dung hợp lệ |
| Report đã gửi thành công | **Báo cáo thành công, bình luận sẽ được xem xét** — dạng toast tự tắt, không có nút hành động. |
| Report cooldown 24h (Report lại cùng target quá sớm) | **Bạn đã báo cáo bình luận này**<br>Có thể báo cáo lại sau {n} giờ nếu nội dung vẫn còn.<br>`[Đóng]` |
| Report rate limit 10/giờ | **Bạn đã gửi 10 báo cáo trong 1 giờ qua**<br>Vui lòng thử lại sau {mm:ss}.<br>`[Đóng]` |
| Notification kết quả report (không tiết lộ chi tiết chế tài) | **Kết quả báo cáo của bạn**<br>MyTV đã xem xét báo cáo của bạn trong {tên phim}. Cảm ơn bạn đã giúp giữ cộng đồng an toàn.<br>`[Xem chi tiết]` |

---

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US10-001 | Functional | U1 login; C1/R1 public | Report C1/R1 | Form mở và Report hợp lệ vào CMS. |
| TC-US10-002 | Taxonomy | Mở form | Kiểm tra reason | Có đủ 6 nhóm taxonomy chung. |
| TC-US10-003 | Other validation | Chọn Khác | Gửi description rỗng/whitespace/1/500/501 ký tự | Rỗng/whitespace/501 bị chặn; 1 và 500 ký tự hợp lệ được nhận nhất quán UI/API. |
| TC-US10-004 | Self-report | U1 là tác giả C1 | Thử Report | UI/API chặn, không tạo Report. |
| TC-US10-005 | Data integrity | U1 Report C1 V1 | Kiểm tra CMS | Có reporter/target/version/reason/time đầy đủ. |
| TC-US10-006 | Visibility | C1 nhận nhiều Report | Refresh public app | C1 không tự đổi state chỉ vì Report count. |
| TC-US10-007 | Cooldown | U1 vừa Report C1 | Report lại trước/sau 24h | Trước 24h bị chặn; từ 24h trở đi được phép nếu C1 vẫn public. |
| TC-US10-008 | Rate limit | U1 gửi Report nhiều target | Gửi 10 rồi Report thứ 11 trong 1 giờ | Report thứ 11 bị chặn; không làm sai dữ liệu. |
| TC-US10-009 | Reporter notification | Admin xử lý Report | Mở notification của reporter | Có in-app notification kết quả xử lý, không có push/chi tiết sanction. |
| TC-US10-010 | Privacy/auth | Guest hoặc U2 xem C1 đã bị U1 Report | Kiểm tra UI/API public | Guest phải login để Report; không lộ danh tính/số Report. |
| TC-US10-011 | SmartTV taxonomy | Smart TV; U1 đã đăng nhập; C1 của user khác | Mở menu action của C1 rồi mở form Báo cáo bằng remote | Menu action trên TV **chỉ có** `Báo cáo`; form hiện **đúng 5 reason** và **không có** `Khác`; không có ô mô tả; submit 1 reason thành công vào CMS. |
| TC-US10-012 | SmartTV limit | U1 vừa Report C1 trên Phone; U1 mở C1 trên Smart TV | Report lại C1 trên TV trong vòng 24h; sau đó gửi tổng cộng 11 Report trong 1 giờ từ cả hai thiết bị | Cooldown 24h và rate limit 10/giờ tính theo account nên TV bị chặn đúng như Phone; microcopy cooldown/rate-limit hiển thị được trên TV. |
| TC-US10-013 | SmartTV notification | U1 Report C1 từ Smart TV; Admin xử lý Report | Mở mục thông báo của ứng dụng Smart TV | Reporter nhận được thông báo kết quả xử lý trong mục thông báo sẵn có của TV; không tiết lộ chế tài của user bị Report. |
