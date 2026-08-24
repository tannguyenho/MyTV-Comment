# US01 — Đọc khu vực bình luận

> Thuộc EP01 — Trải nghiệm bình luận và đánh giá
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)


### User Story

**Là người xem**, tôi muốn đọc bình luận về nội dung đang xem mà không cần đăng nhập, để tham khảo ý kiến cộng đồng trước hoặc trong khi xem phim.

### Giá trị

- Giảm rào cản tiếp cận cộng đồng.
- Tăng khả năng người dùng chú ý đến phim và các thảo luận nổi bật.
- Tạo điểm chuyển đổi tự nhiên từ người xem chưa đăng nhập sang người dùng tương tác.

### Ưu tiên

**Must**

### Điều kiện tiên quyết

- Phim được Admin bật tính năng bình luận.
- Hệ thống có ít nhất trạng thái bình luận được phép hiển thị công khai.

### Acceptance Criteria

1. Khi phim đang mở bình luận, người xem chưa đăng nhập truy cập trang chi tiết/xem phim thì nhìn thấy khu vực Bình luận.
2. Người chưa đăng nhập đọc được toàn bộ bình luận và reply đang ở trạng thái công khai.
3. Khu vực Bình luận hiển thị rõ ràng trên cả web và mobile theo thiết kế đã duyệt.
4. Nội dung bị ẩn, bị xóa hoặc đang chờ duyệt không được hiển thị cho người xem khác.
5. Người chưa đăng nhập chỉ được đọc; khi chọn Đăng bình luận, Reply, Like/Unlike, Mention, Report, Rating, Chia sẻ hoặc bất kỳ thao tác tương tác nào khác, hệ thống yêu cầu đăng nhập trước khi tạo dữ liệu tương tác.
6. Sau khi đăng nhập thành công, hệ thống đưa người dùng trở lại **đúng phim/tập/thread/comment** liên quan nhưng **không tự thực hiện action đã chọn trước login**; user phải chủ động thao tác lại sau khi đã xác thực. Khi quay lại, hệ thống **set focus + highlight nhẹ vào comment/thread target và không hiển thị toast thông báo**.
7. Khi phim bị đóng bình luận, tab `Bình luận` **vẫn hiển thị nhưng bỏ số count**; toàn bộ danh sách comment/reply, ô nhập và các action tương tác bị ẩn, thay bằng thông báo **“Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”**. Rating không bị ảnh hưởng vì nằm ở khối thông tin phim/tập (US03 AC11). Quy tắc chi tiết được quản lý tại US12 và US15.
8. Nếu người dùng mở deep link cũ tới comment/thread trong scope đang **Đóng bình luận**, hệ thống vẫn mở đúng phim/tập nhưng **không hiển thị comment/thread**, hiển thị thông báo **“Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”**; đây là visibility gate của scope, không đổi target sang trạng thái Ẩn/Xóa. Khi Admin mở lại, deep link cũ hoạt động lại nếu target vẫn hợp lệ. Khi nhiều gate cùng đúng, áp dụng Effective Visibility Resolver tại US12 (mục ưu tiên gate).

### Quy tắc nghiệp vụ

- Áp dụng nguyên tắc “Mở để đọc — Đăng nhập để tương tác”.
- Phiên khách không được tạo bình luận, Like, Reply, Mention, Report, Rating, Chia sẻ hoặc bất kỳ bản ghi tương tác cộng đồng nào; việc chỉ đọc không được tính thành một tương tác bình luận.
- Luồng login chỉ giữ **context điều hướng**; không giữ pending action để tự động tạo interaction sau xác thực.
- Chỉ hiển thị dữ liệu mà người xem có quyền xem.
- Việc không đăng nhập không làm thay đổi thứ tự hoặc nội dung bình luận công khai.
- Đóng bình luận là gate theo scope; không đồng nghĩa target deep link bị moderation Ẩn/Xóa.

### Phụ thuộc

- Dịch vụ nội dung/phim.
- Hệ thống đăng nhập MyTV.
- US12 — Quản lý trạng thái và phạm vi hiển thị bình luận.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) — set focus vào comment target sau login (không chỉ scroll), điều hướng bàn phím.*

### Ngoài phạm vi

- Cá nhân hóa thứ tự bình luận theo từng người xem.
- Bình luận trên nội dung ngoài Phim truyện trong giai đoạn hiện tại.

---

## Phân tích kiểm thử

### Mục tiêu

Xác nhận người xem chưa đăng nhập đọc được đúng nội dung công khai, không làm lộ dữ liệu theo trạng thái/quyền, và được đưa qua luồng đăng nhập khi thực hiện tương tác.

### Rủi ro chính

- Lộ bình luận Chờ duyệt, Ẩn hoặc Xóa mềm qua UI, API hoặc cache.
- Phiên khách tạo được dữ liệu tương tác hoặc bị tính nhầm thành tương tác bình luận.
- Mất ngữ cảnh phim/tập/thread sau khi đăng nhập.
- Hệ thống tự thực hiện interaction cũ sau login dù user chưa thao tác lại.
- Khu vực bình luận vẫn xuất hiện khi phim đã Đóng bình luận.
- Deep link cũ làm lộ comment/thread khi scope đang Đóng hoặc làm sai state moderation của target.

### Dữ liệu kiểm thử

Một phim đang Mở bình luận có bình luận gốc, reply, Chờ duyệt, Ẩn và Xóa mềm; một phim Đóng bình luận; tài khoản khách và tài khoản đã đăng nhập.

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US01-001 | Functional | Phim đang Mở bình luận | Mở trang chi tiết phim bằng phiên khách | Khu vực Bình luận hiển thị đúng vị trí và có thể mở danh sách. |
| TC-US01-002 | Authorization | Có bình luận công khai, Chờ duyệt, Ẩn và Xóa mềm | Mở danh sách bằng phiên khách; kiểm tra UI và response API công khai | Chỉ bình luận/reply công khai xuất hiện; các trạng thái còn lại không được trả về hoặc hiển thị. |
| TC-US01-003 | Compatibility | Có cùng dữ liệu trên web và mobile | Mở cùng phim trên web và mobile | Khu vực, nội dung và quyền đọc nhất quán; không làm lộ dữ liệu ở một nền tảng. |
| TC-US01-004 | Authentication | Phiên khách; có bình luận công khai | Chọn lần lượt Đăng bình luận, Like, Reply, Mention, Report, Rating và Chia sẻ | Mỗi thao tác yêu cầu đăng nhập; không tạo record/event tương tác cộng đồng trước khi xác thực. |
| TC-US01-005 | Navigation/post-login | Khách đang ở E1/thread T1/comment C1 và chọn Like/Reply | Đăng nhập thành công từ màn hình yêu cầu login | Quay lại đúng E1/T1/C1; Like/Reply **chưa được thực hiện**; user phải bấm lại action sau login; **không có toast** nào xuất hiện sau khi quay lại. |
| TC-US01-006 | State/Deep link | Phim ở trạng thái Đóng bình luận; có deep link cũ tới C1 | Mở trang chi tiết, gọi API đọc và mở deep link C1 | Tab `Bình luận` còn nhưng không có count; list/composer/actions bị ẩn; rating ở khối thông tin phim vẫn hiển thị và vẫn chấm được; deep link mở đúng phim/tập nhưng không hiển thị C1/thread và hiện “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”; C1 không bị đổi sang Ẩn/Xóa. |
| TC-US01-007 | Security | Có ID bình luận Chờ duyệt/Ẩn | Gọi trực tiếp API bằng phiên khách với ID nội dung không công khai | API từ chối hoặc trả dữ liệu rỗng theo chuẩn bảo mật; không suy ra nội dung qua mã lỗi/metadata. |
| TC-US01-008 | Reopen deep link | Scope từng Đóng, C1 vẫn hợp lệ | Mở lại scope rồi mở lại deep link cũ | Deep link lại mở đúng C1/thread; không cần phát hành link mới. |
| TC-US01-009 | Accessibility | Khách chọn Like/Reply tại comment C1, được điều hướng qua login | Đăng nhập thành công và quay lại | Hệ thống set focus (không chỉ scroll) vào đúng C1/thread; điều hướng bàn phím tới được C1 ngay sau khi quay lại. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
> Bảy dòng “Guest chặn …” dưới đây dùng **chung một luồng đăng nhập**, chỉ khác phần nội dung hiển thị. File thiết kế cố ý chỉ demo một luồng đại diện; các biến thể còn lại áp dụng tương tự, không cần frame riêng.

| Guest chặn Like | **Đăng nhập để thích bình luận**<br>Đăng nhập để bày tỏ cảm xúc với bình luận này.<br>`[Đăng nhập]` |
| Guest chặn Rating | **Đăng nhập để đánh giá**<br>Đăng nhập để chấm điểm nội dung này.<br>`[Đăng nhập]` |
| Guest chặn Comment | **Đăng nhập để bình luận**<br>Đăng nhập để chia sẻ cảm nhận của bạn.<br>`[Đăng nhập]` |
| Guest chặn Reply | **Đăng nhập để trả lời**<br>Đăng nhập để tham gia thảo luận này.<br>`[Đăng nhập]` |
| Guest chặn Mention | **Đăng nhập để nhắc tên người khác**<br>Đăng nhập để gắn thẻ người dùng trong bình luận.<br>`[Đăng nhập]` |
| Guest chặn Report | **Đăng nhập để báo cáo**<br>Đăng nhập để gửi báo cáo vi phạm.<br>`[Đăng nhập]` |
| Guest chặn Share | **Đăng nhập để chia sẻ**<br>Đăng nhập để chia sẻ bình luận này.<br>`[Đăng nhập]` |
| Sau khi quay lại từ login | **Không hiển thị toast.** Hệ thống chỉ set focus vào đúng comment/thread target và highlight nhẹ; không thông báo và không tự chạy lại action. |
| Chưa có bình luận nào | **Hãy là người dùng đầu tiên bình luận** — một dòng duy nhất kèm minh họa, dùng chung cho cả khách và người đã đăng nhập. **Không có CTA riêng trong empty state**: nút `Đăng nhập` (khách) và ô `Viết bình luận` (đã đăng nhập) đã nằm sẵn ở sticky bar đáy màn hình, không lặp lại CTA trên cùng một màn. |
| Scope Đóng bình luận | **Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau**<br>Dùng chung cho empty state trong tab, toast khi mở deep link và khi mở từ thông báo. |

### Điểm cần xác nhận khi chạy test

- Thiết kế breakpoint và vị trí khu vực Bình luận trên từng nền tảng.
