# US03 — Đánh giá phim

> Thuộc EP01 — Trải nghiệm bình luận và đánh giá  
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md) · [User Flow →](US03_USER_FLOW.md)

### User Story

**Là người dùng đã đăng nhập**, tôi muốn đánh giá nội dung đang xem bằng thang điểm 5 sao và có thể thay đổi đánh giá, để thể hiện cảm nhận hiện tại của mình với cộng đồng.

### Giá trị

- Cho cộng đồng một tín hiệu chất lượng nhanh, gọn ngay đầu khu vực Bình luận.
- Cho phép người dùng cập nhật cảm nhận theo thời gian mà không làm nhiễu tổng lượt đánh giá.

### Ưu tiên

**Must**

### Điều kiện tiên quyết

- Bộ phim đã được định danh chính xác trên hệ thống nội dung.
- Khu vực Bình luận của content scope hiện tại đang được bật (rating nằm trong khu vực này).

### Acceptance Criteria

1. Rating nằm ở **khối thông tin phim**, không nằm trong tab Bình luận. Khối này hiển thị điểm trung bình và mở được bottom sheet đánh giá; bottom sheet hiển thị điểm trung bình, tổng số lượt đánh giá và thang điểm 5 sao.
2. Guest xem được aggregate nhưng phải login để đánh giá; login quay lại đúng content và không auto-rating.
3. Rating ở **cấp phim** cho cả phim lẻ và phim bộ: một account có tối đa một rating hiện hành trên mỗi bộ phim.
4. Mỗi account chỉ có một rating hiện hành trên mỗi content scope.
5. User được thay đổi rating 1–5 sao; đổi rating không tăng tổng lượt.
6. **Không hỗ trợ xóa rating** sau khi đã đánh giá.
7. Chọn số sao rồi xác nhận bằng nút **Gửi đánh giá**; nút ở trạng thái disabled cho tới khi user chọn ít nhất 1 sao. Trước khi bấm Gửi, user được đổi lựa chọn tự do và không có bản ghi rating nào được tạo.
8. Submit/update lỗi → giữ/revert về rating hợp lệ trước đó; không tạo state nửa chừng và không tự retry.
9. Average hiển thị 1 chữ số thập phân và luôn làm tròn lên đến 0.1 gần nhất, ví dụ `4.21 → 4.3`, `4.20 → 4.2`.
10. Account Lock tạm loại rating khỏi cả average và public total; unlock tính lại nếu record còn. Comment Lock không loại rating.
11. **Scope Đóng bình luận không ảnh hưởng rating**: điểm trung bình, tổng số lượt và thao tác đánh giá vẫn hoạt động bình thường khi phim đang Đóng bình luận. Đóng bình luận chỉ gate danh sách comment/reply, không gate rating.
12. SmartTV cho user đã login đánh giá 1–5 sao bằng remote và thay đổi rating.

### Quy tắc nghiệp vụ

- Giá trị rating: integer 1–5.
- Một account đóng góp tối đa một current rating/content scope.
- Rating record không bị xóa do Account Lock; khóa/mở khóa chỉ ảnh hưởng việc rating có được tính vào aggregate công khai hay không.
- Bộ rating dùng để tính **average** và **total count công khai** phải nhất quán: rating của account đang Account Lock không tham gia cả hai chỉ số.
- Không có thao tác DELETE rating ở UX/API product contract MVP; con đường duy nhất để thay đổi là chọn lại mức sao 1–5 rồi bấm Gửi đánh giá.
- Rating là thành phần của **khối thông tin phim**, không thuộc khu vực Bình luận; vì vậy rating **không** nằm trong phạm vi gate của scope Đóng bình luận tại US12.
- Rating chỉ được ghi khi user bấm Gửi đánh giá; việc chạm chọn sao là state cục bộ của UI.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) — rating 5 sao dùng `radiogroup`, điều hướng phím mũi tên, nhãn "{n} sao".*

### Phụ thuộc

- US12 — Quản lý trạng thái và phạm vi hiển thị bình luận (scope Đóng **không** gate rating).
- US16 — Quản lý người dùng vi phạm và Account Lock.

---

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US03-001 | Guest | Content đã có rating; phiên khách | Mở khối thông tin phim, mở bottom sheet đánh giá rồi chạm vào sao | Guest thấy 5 sao + average + total; chạm sao ra auth gate; login xong quay lại đúng content và không auto-rating (không tự bấm Gửi đánh giá). |
| TC-US03-002 | Boundary | U1 đã đăng nhập | Gửi 1★ và 5★; thử 0, 6 và giá trị thập phân qua UI/API | Chỉ integer 1–5 hợp lệ; các giá trị còn lại bị từ chối nhất quán ở cả hai bề mặt. |
| TC-US03-003 | Scope | Phim bộ S1 đang xem tập E1 | U1 đánh giá 4★ ở E1 rồi chuyển sang E2 và mở lại bottom sheet | Bottom sheet ở E2 hiển thị đúng rating 4★ đã chấm và tổng lượt không tăng: rating thuộc về bộ phim S1, không theo tập. |
| TC-US03-004 | Update | U1 đã có 3★ trên content | Chọn lại 5★ | Rating hiện hành đổi thành 5★; tổng lượt không tăng; average được tính lại. |
| TC-US03-005 | No delete | U1 đã có rating trên content | Rà UI (chạm lại đúng sao đang chọn, long-press, menu ngữ cảnh, đóng sheet giữa chừng) và rà API contract | Không có action xóa/toggle-to-empty trên UI và không có endpoint DELETE rating; rating chỉ có thể đổi sang mức 1–5 sao. Đóng sheet mà chưa bấm Gửi đánh giá thì rating cũ giữ nguyên. |
| TC-US03-014 | Submit gate | U1 đăng nhập, chưa từng đánh giá content | Mở sheet và quan sát nút Gửi đánh giá trước/sau khi chọn sao; chọn 3★ rồi đổi sang 5★ trước khi bấm Gửi | Nút Gửi disabled khi chưa chọn sao; đổi lựa chọn trước khi Gửi không tạo bản ghi nào; chỉ mức sao tại thời điểm bấm Gửi được lưu và tổng lượt tăng đúng 1. |
| TC-US03-015 | Rating hiện hành | U1 đã đánh giá content ở mức 4★ | Mở lại bottom sheet đánh giá | Sheet hiển thị sẵn 4★ đang chọn (không phải 0 sao) và nút Gửi đánh giá cho phép xác nhận mức mới. |
| TC-US03-006 | Error | U1 có rating hợp lệ; mock lỗi khi update | Chọn mức sao mới và để request thất bại | Revert về rating hợp lệ trước đó + thông báo lỗi; không tạo state nửa chừng và không tự retry ngầm. |
| TC-US03-007 | Account Lock | U1 có rating; khóa rồi mở khóa toàn bộ account U1 | Đối chiếu average và total công khai ở ba mốc | Khi khóa, rating U1 bị loại khỏi **cả average và total công khai** mà không xóa record; mở khóa tính lại nếu record vẫn còn. |
| TC-US03-008 | SmartTV | U1 đã đăng nhập trên SmartTV | Chọn số sao bằng remote rồi đổi sang mức khác | Submit và update rating hoạt động như Phone/Web. |
| TC-US03-009 | Comment Lock | U1 bị Khóa bình luận nhưng account không bị khóa | Đối chiếu aggregate | Rating của U1 vẫn được tính trong cả average và total count công khai. |
| TC-US03-010 | Rounding | Average thô lần lượt 4.20, 4.21, 4.29, 4.31 | Đối chiếu hiển thị UI và API public | Kết quả lần lượt 4.2, 4.3, 4.3, 4.4 — luôn làm tròn lên đến 0.1 gần nhất, hiển thị đúng 1 chữ số thập phân. |
| TC-US03-011 | Scope Đóng | Content đang ở trạng thái Đóng bình luận, đã có rating trước đó | Mở trang phim; gửi rating mới qua UI và API; sau đó Admin mở lại scope | Khi Đóng: khối thông tin phim vẫn hiển thị average/total, bottom sheet vẫn mở được và rating mới **vẫn được nhận** ở cả UI và API; chỉ danh sách comment/reply bị ẩn kèm thông báo “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”. Khi mở lại scope: rating và aggregate không thay đổi do việc đóng/mở. |
| TC-US03-012 | Scope phim lẻ | Phim lẻ M1 | U1 đánh giá M1 rồi đổi mức sao | Rating nằm ở cấp phim; U1 chỉ có một rating hiện hành trên M1. |
| TC-US03-013 | Idempotency | U1 gửi/đổi rating với retry và request lỗi giữa chừng | Gửi lặp cùng thao tác nhiều lần | Chỉ tồn tại một rating hiện hành hợp lệ; tổng lượt không bị sai lệch do retry. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Guest chạm sao | **Đăng nhập để đánh giá**<br>Đăng nhập để chấm điểm nội dung này.<br>`[Đăng nhập]` |
| Tiêu đề bottom sheet | **Đánh giá bộ phim từ cộng đồng** |
| Câu hỏi chọn sao | **Bạn đánh giá bộ phim mấy sao?** |
| Nút xác nhận | `[Gửi đánh giá]` — disabled khi chưa chọn sao |
| Gửi/cập nhật thành công | **Cảm ơn bạn đã để lại đánh giá** |
| Submit/update lỗi | **Không thể cập nhật đánh giá. Vui lòng thử lại sau** |
