# US07 — Like và Unlike bình luận

> Thuộc EP02 — Tương tác cộng đồng
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là người dùng đã đăng nhập**, tôi muốn Like hoặc Unlike một bình luận/reply, để thể hiện sự đồng tình hoặc yêu thích đối với ý kiến đó.

### Ưu tiên

**Must**

### Acceptance Criteria

1. User đăng nhập có thể Like/Unlike comment hoặc reply đang Hiển thị, kể cả **comment/reply của chính mình**.
2. Mỗi tài khoản chỉ có một trạng thái Like hiện hành trên mỗi comment/reply.
3. UI áp dụng **optimistic update ngay lập tức** sau thao tác Like/Unlike.
4. Client gom các thay đổi Like/Unlike và đồng bộ xuống BE theo batch sau tối đa **5 giây** thay vì gửi từng thao tác riêng lẻ ngay lập tức.
5. Nếu user rời màn hình hoặc app chuyển background trước 5 giây, client **flush batch sớm**.
6. Trong cùng batch window, nhiều thao tác liên tiếp trên cùng target phải được **coalesce về state cuối cùng cần đồng bộ**, không tạo Net Like sai do các trạng thái trung gian.
7. BE là nguồn trạng thái cuối cùng; nếu kết quả server khác optimistic state, client reconcile về trạng thái BE.
8. Double-click/retry không làm tăng/giảm trùng Like.
9. Guest chọn Like được chuyển sang login; không tạo Like trước xác thực.
10. Comment bị Ẩn/Xóa hoặc user không còn quyền xem không thể nhận Like mới.
11. Net Like hiện tại được dùng cho sort Được yêu thích/Featured Score; lịch sử thao tác Like/Unlike có thể được tracking riêng cho US19.
12. Nếu account đã tạo Like sau đó bị **Khóa tài khoản**, Like record **không bị xóa**, nhưng trong thời gian khóa Like đó tạm bị loại khỏi **Net Like công khai, Featured Score/ranking và Engagement Score**. Khi account được mở khóa, Like được tính lại nếu record và target vẫn hợp lệ.
13. Việc một liker bị Account Lock **không làm thay đổi Fan kỳ cựu eligibility của người đã nhận Like đó**; badge dùng semantics riêng tại US17 để tránh badge của recipient dao động theo lock/unlock của past liker.

### Quy tắc nghiệp vụ

- Self-like là hợp lệ và được tính như Like khác.
- Một account, một Like hiện hành trên một comment/reply.
- Optimistic UI không thay đổi nguyên tắc BE là source of truth.
- Batch window 5 giây là rule client; phải hỗ trợ idempotency/dedup ở BE.
- Coalescing không ngăn analytics ghi nhận lịch sử thao tác UI nếu data dictionary US19 cần; Net Like cuối cùng vẫn dựa trên state hiện hành ở BE.
- **Public Net Like** loại Like của account đang Account Lock; đây là rule cho public aggregate/ranking/Engagement, không phải xóa Like record.
- Badge eligibility của recipient là một data semantic riêng theo US17 và cố ý không dao động theo trạng thái khóa của liker.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục A.2 — nút Like dùng `aria-pressed`, vùng `aria-live` cho số Like, announce khi reconcile revert.*

---

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US07-001 | Functional | U1 đăng nhập; C1/R1 public | Like C1/R1 | UI đổi trạng thái ngay, mỗi target có đúng một Like của U1. |
| TC-US07-002 | Self-like | U1 là tác giả C1 | U1 Like C1 | Được phép; Net Like tăng như bình thường. |
| TC-US07-003 | Unlike | U1 đã Like C1 | Unlike | UI giảm ngay; state cuối BE không còn Like U1. |
| TC-US07-004 | Batch timing | Thực hiện nhiều Like/Unlike | Theo dõi request trong 5 giây | UI phản hồi ngay nhưng client gom request và sync batch tối đa sau 5 giây. |
| TC-US07-005 | Early flush | Có batch chưa gửi | Rời màn hình/chuyển background trước 5 giây | Batch được flush sớm, không mất state. |
| TC-US07-006 | Coalescing | C1 ban đầu chưa Like | Trong <5 giây bấm Like → Unlike → Like C1 | UI theo thao tác tức thời; batch đồng bộ state cuối là **Liked**; BE có đúng một Like hiện hành, Net Like không tăng/giảm theo state trung gian. |
| TC-US07-007 | Reconcile | Mock BE từ chối/mismatch | Like optimistic rồi nhận response | UI reconcile theo BE và thông báo lỗi phù hợp. |
| TC-US07-008 | Idempotency | Double-click/retry | Gửi thao tác lặp | Không nhân đôi Like/event hợp lệ. |
| TC-US07-009 | Authentication | Guest | Chọn Like | Yêu cầu login, không tạo Like trước auth. |
| TC-US07-010 | Invalid target | C1 Ẩn/Xóa | Like qua UI/API | Bị chặn; Net Like public không đổi. |
| TC-US07-011 | Integration | Net Like thay đổi | Mở sort Được yêu thích/Nổi bật | Ranking dùng Net Like công khai hiện hành sau reconcile. |
| TC-US07-012 | Account Lock aggregate | U1 đã Like C1, sau đó U1 bị Account Lock | Kiểm tra Like record, Net Like/ranking/Engagement rồi mở khóa | Record vẫn tồn tại; khi khóa Like U1 bị loại public aggregate; mở khóa được tính lại nếu hợp lệ. |
| TC-US07-013 | Badge exception | U1 đã Like content của U2 rồi U1 bị Account Lock | Chạy badge job của U2 | Like vẫn được tính vào Fan kỳ cựu eligibility của U2 theo US17 dù tạm không nằm trong public Net Like. |
| TC-US07-014 | Mất mạng hoàn toàn trước flush | U1 thao tác Like/Unlike tạo batch chưa gửi | (a) Mất mạng ngay trước khi batch kịp gửi, đợi có mạng lại; (b) force-kill app trước khi batch gửi, mở lại app; (c) kiểm tra Net Like công khai/Featured Score ở cả 2 nhánh | (a) Client tự retry/flush batch khi có mạng lại; BE nhận đúng state cuối cùng đúng một lần, không nhân đôi Like/Unlike; (b) Sau khi mở lại app, UI reconcile lại đúng theo state hiện hành trên BE (không giữ optimistic state đã mất); (c) Net Like công khai và Featured Score khớp với BE ở mọi nhánh, không bị lệch tạm thời hay vĩnh viễn. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Reconcile thất bại/mismatch với BE | **Chưa lưu được lượt thích.**<br>Vui lòng thử lại.<br>`[Thử lại]` |
