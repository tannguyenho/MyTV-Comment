# US12 — Quản lý trạng thái và phạm vi hiển thị bình luận

> Thuộc EP03 — An toàn và kiểm duyệt
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là Admin vận hành**, tôi muốn hệ thống áp dụng trạng thái và phạm vi hiển thị theo cấu hình từng phim, để kiểm soát chính xác ai được xem nội dung ở từng giai đoạn moderation.

### Ưu tiên

**Must**

### Trạng thái nghiệp vụ

| Trạng thái | Tác giả | Cộng đồng | Ý nghĩa |
|---|---:|---:|---|
| Chờ duyệt | Có | Không | Chờ Admin quyết định |
| Hiển thị | Có | Có (*) | Public |
| Từ chối | Có + lý do | Không | Không được duyệt |
| Ẩn | Có + lý do | Không | Admin ẩn khỏi cộng đồng |
| Xóa mềm | Không trong public UI | Không | Giữ dữ liệu theo retention |

(*) **Hiển thị = đủ điều kiện public NẾU KHÔNG có gate hiển thị cao hơn đang active.** `moderation_state = Hiển thị` là điều kiện cần nhưng không phải điều kiện đủ để cộng đồng thực sự xem được nội dung — nếu có Account Lock của tác giả/root author hoặc scope Đóng bình luận đang active, comment vẫn ở `moderation_state = Hiển thị` (không đổi state) nhưng **không public tạm thời** với cộng đồng. Xem đầy đủ thứ tự ưu tiên tại mục "Effective Visibility Resolver" ngay dưới đây.

### Effective Visibility Resolver — thứ tự ưu tiên khi nhiều gate cùng đúng

Một comment/thread có thể rơi vào từ 2 "gate ẩn" trở lên cùng lúc (ví dụ vừa bị Account Lock của tác giả vừa nằm trong scope đang Đóng). Khi đó hệ thống **CHỈ hiển thị một thông báo duy nhất**, chọn theo gate có **mức ưu tiên cao nhất** (số nhỏ hơn = ưu tiên cao hơn = "vĩnh viễn/nghiêm trọng hơn"). Đây là định nghĩa gốc — US01, US02, US08, US09, US18, US19 chỉ dẫn chiếu về mục này, không lặp lại toàn bộ luật.

| Ưu tiên | Gate | Thông báo fallback |
|---|---|---|
| 1 | Self-delete cascade (user tự xóa root) | *(không hiển thị lại — vĩnh viễn theo lifecycle self-delete)* |
| 2 | Moderation state riêng (Ẩn/Xóa mềm/Từ chối do CMS/Admin) | **"Bình luận không còn khả dụng"** |
| 3 | Admin root moderation cascade | **"Bình luận không còn khả dụng"** |
| 4 | Account Lock (tác giả/root author) | **"Bình luận hiện không khả dụng"** |
| 5 | Scope Đóng bình luận | **"Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau"** |

Quy tắc chọn thông báo:
- Nếu nhiều gate cùng đúng cho cùng một comment/thread, hệ thống dùng thông báo của gate có **số ưu tiên nhỏ nhất** trong bảng trên (gate 2/3 thắng gate 4, gate 4 thắng gate 5).
- Gate 2 và 3 dùng chung chuỗi hiển thị "Bình luận không còn khả dụng" theo quy ước cũ — KHÔNG đổi chuỗi này, chỉ làm rõ rằng cả hai đều ưu tiên hơn gate 4 và 5.
- Gate chỉ ảnh hưởng đến **thông báo hiển thị/khả năng public**, KHÔNG ảnh hưởng `moderation_state` lưu trữ của comment — mỗi gate quản lý một cờ/trường dữ liệu độc lập (moderation_state, cascade flag, account lock flag, scope status); việc "thắng" trong bảng ưu tiên chỉ quyết định UI/thông báo nào được người dùng nhìn thấy tại một thời điểm, không xóa hay ghi đè trạng thái của các gate khác.
- Việc mở lại một gate có ưu tiên thấp hơn (ví dụ mở lại scope Đóng) không tự động làm nội dung public nếu vẫn còn gate có ưu tiên cao hơn đang active (ví dụ vẫn còn Account Lock hoặc vẫn Ẩn/Từ chối).

### Acceptance Criteria

1. Chờ duyệt chỉ hiển thị với tác giả; không xuất hiện ở public API/count/notification cho người khác.
2. Bản sửa Chờ duyệt không ghi đè version public cũ; nếu bị Từ chối/chặn, version cũ vẫn Hiển thị.
3. Mỗi phim có ba trạng thái vận hành: Chế độ 1, Chế độ 2, Đóng bình luận.
4. Khi Đóng, tab `Bình luận` **vẫn hiển thị nhưng bỏ count**; danh sách comment/reply, ô nhập và các action tương tác bị ẩn, thay bằng **“Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”**. UI/API chặn **Comment, Reply, Like, Mention, Report và Share mới**. **Rating không nằm trong phạm vi gate này**: rating thuộc khối thông tin phim nên vẫn hiển thị aggregate và vẫn nhận đánh giá mới khi scope đang Đóng (US03 AC11).
5. Đóng bình luận không xóa dữ liệu lịch sử và không đổi moderation state của comment/reply chỉ vì scope bị Đóng.
6. Khi mở lại, dữ liệu đủ điều kiện được hiển thị lại; nội dung đã Từ chối/Ẩn/Xóa vẫn không public.
7. Khi chuyển **Chế độ 2 → Chế độ 1**, comment đang Chờ duyệt mà **đã có AI result an toàn/Nhẹ trước đó** tự chuyển Hiển thị; các case Trung bình/không đủ điều kiện tiếp tục Chờ duyệt.
8. Khi chuyển **Chế độ 1 → Chế độ 2**, nội dung đã Hiển thị trước effective time vẫn giữ Hiển thị; Chế độ 2 áp dụng cho nội dung mới/version mới từ effective time.
9. Khi chuyển sang **Đóng** trong lúc còn queue, queue được giữ và Admin vẫn xử lý trên CMS; item được Duyệt trong lúc Đóng không public cho tới khi mở lại.
10. Deep link cũ từ Share/Notification tới target trong scope đang Đóng vẫn mở đúng phim nhưng **không hiển thị comment/thread**; thông báo fallback chọn theo **Effective Visibility Resolver** — nếu target CHỈ bị gate scope Đóng thì hiển thị **“Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”**, nếu target còn bị moderation riêng/Admin root cascade/Account Lock thì hiển thị thông báo của gate có ưu tiên cao hơn. Khi mở lại scope, link cũ hoạt động lại nếu target vẫn hợp lệ và không còn gate ưu tiên cao hơn đang active.
11. Rule “sau X giờ” cho phép **Admin chọn loại mốc khi cấu hình**. **Phim lẻ** có ba loại mốc: giờ phát hành MyTV, giờ phát sóng thực tế, hoặc mốc Admin nhập thủ công. **Phim bộ** chỉ có hai loại: giờ phát hành MyTV hoặc mốc Admin nhập thủ công — mốc “giờ phát sóng thực tế” không áp dụng vì cấu hình ở cấp phim trong khi mỗi tập có giờ phát sóng riêng.
12. Thay đổi mode/schedule chỉ áp dụng từ effective time và có timezone nhất quán.
13. Khi comment bị **Từ chối / Ẩn / Xóa**, tác giả thấy lý do cụ thể trong app và nhận notification nghiệp vụ bắt buộc.
14. Mọi transition/configuration được lưu audit.
15. Trong thời gian scope Đóng, việc user chỉ truy cập trang phim **không tạo active day badge** vì khu vực Bình luận không thể được mở/đọc theo định nghĩa US17.

### Quy tắc nghiệp vụ

- Mode1: Nhẹ Hiển thị, Trung bình queue, Nặng chặn theo US11.
- Mode2: Nhẹ/Trung bình queue, Nặng chặn.
- Đóng là lớp visibility/interaction gate; không hủy moderation data và không đồng nghĩa moderation Ẩn/Xóa.
- Deep link trong scope Đóng dùng fallback theo **Effective Visibility Resolver**: nếu target CHỈ bị gate scope Đóng thì hiển thị “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”; nếu target còn có moderation riêng (Ẩn/Xóa mềm/Từ chối), Admin root cascade hoặc Account Lock thì dùng thông báo của gate có ưu tiên cao hơn theo bảng ưu tiên ở mục “Effective Visibility Resolver”.
- Notification reason cho Từ chối/Ẩn/Xóa không bị tắt bởi switch thông báo cộng đồng US09.
- Active day chỉ được ghi khi comment area thực sự khả dụng để user đăng nhập mở/đọc.
- Concurrency tại effective time: mọi request submit Comment/Reply/Rating/Share xử lý theo mode/scope **có hiệu lực tại thời điểm hệ thống nhận request**, không theo thời điểm AI trả kết quả — kể cả khi AI xử lý bất đồng bộ và trả kết quả sau khi effective time đã đổi, quyết định mode/scope áp dụng vẫn chốt tại thời điểm nhận request ban đầu.
- Chỉ các cặp (state hiện tại → action) hợp lệ mới được thực hiện: Duyệt và Từ chối chỉ áp dụng từ Chờ duyệt; Ẩn chỉ áp dụng từ Hiển thị. Mọi tổ hợp khác bị chặn ở cả UI lẫn API, không ghi audit "thành công" và không đổi state.

> *Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục IDOR/Session — API phải kiểm tra quyền xem theo từng gate hiển thị (Chờ duyệt/Ẩn/Xóa mềm/Account Lock/scope Đóng) ở tầng server, không chỉ ẩn ở UI; mục WCAG 2.1 AA — thông báo fallback ("Bình luận không còn khả dụng", "Bình luận hiện không khả dụng", "Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau") phải được screen reader đọc rõ khi thay thế nội dung comment/thread.*

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US12-001 | Visibility | C1 Chờ duyệt | U1/U2 mở UI/API | U1 thấy status; U2 không thấy UI/API/count/notification. |
| TC-US12-002 | Versioning | C1 public, V2 pending | U2 mở trước/sau duyệt V2 | Trước duyệt thấy C1; sau duyệt thấy V2. |
| TC-US12-003 | Mode2→1 safe | Pending có AI Nhẹ/an toàn | Chuyển Mode2 → Mode1 | Item tự Hiển thị từ effective time, không cần Admin duyệt lại. |
| TC-US12-004 | Mode2→1 medium | Pending có AI Trung bình | Chuyển Mode2 → Mode1 | Item tiếp tục Chờ duyệt. |
| TC-US12-005 | Mode1→2 | Có C1 đã public | Chuyển Mode1 → Mode2 | C1 vẫn public; nội dung mới sau effective time vào queue. |
| TC-US12-006 | Close UI/API | Phim đang Đóng bình luận | Mở UI và gọi Comment/Reply/Like/Mention/Report/Rating/Share APIs | Toàn bộ comment area/rating ẩn; mọi interaction mới trong scope bị chặn. |
| TC-US12-007 | Close with queue | Có pending item | Đóng rồi Admin duyệt item | Queue vẫn xử lý; item đã duyệt không public trong lúc Đóng. |
| TC-US12-008 | Reopen | Đang Đóng có data cũ/item đã duyệt | Mở lại | Data đủ điều kiện public lại; state xử lý riêng vẫn được tôn trọng. |
| TC-US12-009 | Closed deep link | Scope Đóng; TH1: C1 hợp lệ, chỉ bị gate scope Đóng. TH2: C1 vừa trong scope Đóng vừa bị Ẩn/Từ chối riêng. TH3: C1 trong scope Đóng và tác giả đang Account Lock | Mở deep link Share/Notification tới C1 ở từng TH | Cả 3 TH đều mở đúng phim, không hiển thị C1 và không đổi state C1. Thông báo theo Effective Visibility Resolver: TH1 “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”; TH2 “Bình luận không còn khả dụng” (gate 2 thắng gate 5); TH3 “Bình luận hiện không khả dụng” (gate 4 thắng gate 5). |
| TC-US12-010 | Reopen deep link | Scope mở lại, C1 vẫn hợp lệ | Mở lại deep link cũ | Link lại mở đúng C1/thread, không cần tạo link mới. |
| TC-US12-011 | X-hours | Cấu hình lần lượt 3 loại mốc | Kiểm tra trước/đúng/sau mốc | Transition đúng loại mốc Admin chọn và timezone. |
| TC-US12-012 | Reason notification | Admin Từ chối/Ẩn/Xóa C1 | U1 mở app/notification | U1 thấy lý do cụ thể và nhận notification bắt buộc. |
| TC-US12-013 | Active day closed | U1 đăng nhập; scope đang Đóng | U1 mở trang phim nhiều lần | Không phát sinh active day vì comment area không khả dụng. |
| TC-US12-014 | Audit | Đổi mode/schedule/state | Tra audit | Có actor/time/before-after/effective config. |
| TC-US12-015 | State × Action matrix | 5 state (Chờ duyệt/Hiển thị/Từ chối/Ẩn/Xóa mềm) × 8 action (Duyệt/Từ chối/Ẩn/Xóa mềm/Undo/Bỏ qua Report/Flag/Spoiler) | Với mỗi state, thử lần lượt cả 8 action qua UI và API | Chỉ tổ hợp hợp lệ được thực hiện: Duyệt chỉ từ Chờ duyệt; Từ chối chỉ từ Chờ duyệt; Ẩn chỉ từ Hiển thị. Mọi tổ hợp không hợp lệ khác bị chặn ở cả UI và API, không ghi audit "thành công", không đổi state. |
| TC-US12-016 | Concurrency tại effective time | Scope sắp chuyển Đóng, hoặc Mode1 sắp chuyển Mode2 tại effective time T | User gửi Comment/Reply/Rating/Share ngay trước T và ngay sau T | Request nhận trước T được xử lý theo mode/scope cũ; request nhận sau T được xử lý theo mode/scope mới; quyết định bám theo **thời điểm hệ thống nhận request**, không phụ thuộc thời điểm AI trả kết quả (kể cả khi AI trả kết quả chậm, sau T). |
