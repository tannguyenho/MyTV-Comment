# US02 — Xem bình luận, số lượng và sắp xếp

> Thuộc EP01 — Trải nghiệm bình luận và đánh giá  
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md) · [User Flow →](US02_USER_FLOW.md)

### User Story

**Là người xem**, tôi muốn xem đúng bình luận của bộ phim hiện tại và sắp xếp theo nhu cầu, để không lẫn thảo luận giữa các phim.

### Giá trị

- Tránh lẫn thảo luận giữa các bộ phim khác nhau.
- Giúp người dùng nhanh chóng tìm được bình luận đáng chú ý hoặc mới nhất.
- Tăng khả năng khám phá các cuộc thảo luận có tương tác cao.

### Ưu tiên

**Must**

### Điều kiện tiên quyết

- Bộ phim đã được định danh chính xác trên hệ thống nội dung.
- Khu vực bình luận của content scope hiện tại đang được bật (không ở trạng thái Đóng bình luận).

### Acceptance Criteria

1. **Phạm vi bình luận là bộ phim.** Phim lẻ và phim bộ đều dùng scope cấp phim; mỗi bộ phim có duy nhất một khu vực bình luận.
2. Phim bộ đổi tập **không** làm đổi phạm vi bình luận: rating, public comment count, Pin và list giữ nguyên.
3. Khi mở một bộ phim khác, hệ thống load rating, public comment count, Pin và list của phim đó; sort reset về `Nổi bật`.
4. Tab hiển thị `Bình luận ({public_count})`; count gồm root + reply có effective visibility public.
5. Có 3 sort: `Nổi bật`, `Mới nhất`, `Nhiều lượt thích`; mặc định `Nổi bật`, chọn qua dropdown.
6. Tối đa 3 comment Ghim luôn hiển thị trên cùng **trong mọi sort**, ngoài quota root batch và không trùng trong list thường; hiển thị icon + chữ `Đã ghim`.
7. FeaturedScore của root không ghim: `0.5×ln(1+Like) + 0.3×ln(1+Reply) + 0.2×e^(-AgeHours/72)`; tie → comment mới hơn → `comment_id`.
8. `Mới nhất`: root mới → cũ. `Nhiều lượt thích`: public Net Like giảm dần, tie → mới hơn.
9. Initial load **10 root**; cuộn gần cuối lazy load **10 root/batch**, không trùng/bỏ sót.
10. Comment dài tối đa 3 dòng → `Xem thêm` / `Thu gọn`.
11. Root list không preload Reply; nếu có reply hiển thị lối vào thread `{n} phản hồi` và đi US08.
12. Có comment mới khi đang đọc: không tự chèn; hiện `Có {n} bình luận mới`. Khi refresh, `Nổi bật`/`Nhiều lượt thích` luôn giữ đúng ranking; `Mới nhất` có thể đưa tới comment mới đầu tiên.
13. Rời tab rồi quay lại cùng phiên giữ scroll/sort/thread/expand state và refresh ngầm không reset context.
14. SmartTV cho đọc, đổi sort và lazy load bằng remote.

### Quy tắc nghiệp vụ

- Reply được tính vào tổng số bình luận nhưng không được trộn thành bình luận gốc trong danh sách root.
- Tổng số công khai = số comment/reply có **effective visibility = public tại thời điểm đọc** (xem Effective Visibility Resolver, US12). Comment ở trạng thái **Chờ duyệt, Từ chối, Ẩn hoặc Xóa** không được tính vào tổng số công khai và không tham gia Featured Score.
- Nội dung tạm non-public do **Account Lock** của tác giả/root author (kể cả reply cascade theo root) và do **scope Đóng bình luận** cũng **KHÔNG** được tính vào tổng số công khai hiển thị cho end-user tại thời điểm đọc. Đây là **visibility gate** theo thứ tự ưu tiên của Effective Visibility Resolver (US12) — chỉ ảnh hưởng phần hiển thị/đếm cho người xem, **không** ảnh hưởng KPI/Engagement Score trên dashboard Admin (US19) và **không** đổi `moderation_state` lưu trữ của comment.
- Like trong công thức FeaturedScore = **public Net Like hiện tại**, không phải tổng Like record bất kể trạng thái account của người Like.
- Like của account đang Account Lock giữ record nhưng tạm không tính vào public Net Like, Featured Score và ranking; khi unlock được tính lại nếu Like record và target vẫn hợp lệ.
- Like của chính tác giả là Like hợp lệ và được tính vào Featured Score theo US07, trừ khi account tạo Like đang bị Account Lock.
- `AgeHours` tính từ thời điểm comment được đăng; hệ số decay freshness là 72 giờ.
- Hard max Pin = 3 cho mỗi content scope, không cho cấu hình vượt mức này. Nhóm ghim nằm ngoài quota 10 root của lần tải đầu và bị loại khỏi danh sách xếp theo sort để tránh hiển thị trùng; tổng số công khai vẫn đếm comment ghim đúng 1 lần.

### Phụ thuộc

- US07 — Like và Unlike bình luận.
- US08 — Trả lời bình luận.
- US12 — Quản lý trạng thái và phạm vi hiển thị bình luận (Effective Visibility Resolver).
- US15 — Quản lý bình luận ghim và cấu hình theo phim.
- US16 — Quản lý người dùng vi phạm và Account Lock.

---

## Phân tích kiểm thử

### Mục tiêu

Kiểm tra phân tách dữ liệu theo bộ phim, tổng số công khai, hard max ghim, Featured Score và lazy load 10 item không lặp/bỏ sót.

### Rủi ro chính

- Trộn bình luận giữa các bộ phim khi chuyển ngữ cảnh.
- Tính nội dung không công khai (Chờ duyệt/Từ chối/Ẩn/Xóa, Account Lock, scope Đóng) vào count/ranking.
- Tính Like của account đang bị Account Lock vào Net Like/ranking công khai.
- Vượt hard max 3 comment ghim hoặc pin bị lặp trong list thường.
- Featured Score/tie-break sai hoặc lazy load tạo bản ghi trùng/bỏ sót.

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US02-001 | Scope | Phim bộ S1 có comment, đang xem tập E1 | Chuyển sang tập E2 rồi mở tab Bình luận | Danh sách, count, rating và Pin **giữ nguyên** vì bình luận thuộc về bộ phim S1; không có bộ chọn phạm vi bình luận trên UI và API người xem. |
| TC-US02-002 | Scope phim lẻ | Phim lẻ M1 có comment | Mở tab Bình luận của M1 | Comment nằm ở scope cấp phim, cùng mô hình với phim bộ. |
| TC-US02-003a | Sort giữ khi đổi tập | Phim bộ S1, đang ở sort `Mới nhất`, đã cuộn vài batch, đang xem tập E1 | Chuyển sang tập E2 rồi mở lại tab Bình luận | Sort vẫn là `Mới nhất`, danh sách và vị trí cuộn không bị reset, không phát sinh request load lại scope mới. |
| TC-US02-003 | Navigation | Đang đọc phim M1 với sort `Mới nhất` và đã cuộn vài batch | Chuyển sang phim M2 rồi refresh | Load rating, public count, Pin và list của M2; sort reset về `Nổi bật`; không giữ cache comment của M1. |
| TC-US02-004 | Counter | Scope có comment/reply công khai và cả Chờ duyệt/Từ chối/Ẩn/Xóa | Đối chiếu số trên tab `Bình luận ({public_count})` | Chỉ root + reply có effective visibility public được tính. |
| TC-US02-005 | Counter exclusion | Root comment của tác giả đang Account Lock có reply hợp lệ; một content khác đang scope Đóng bình luận | Đọc tổng số công khai ở cả hai trường hợp và đối chiếu dashboard Admin | Comment/reply thuộc root bị Account Lock (kể cả reply cascade theo root) và toàn bộ comment/reply trong scope Đóng **không** được tính vào tổng số công khai hiển thị cho end-user; KPI/Engagement Score trên dashboard Admin không bị ảnh hưởng (đối chiếu US19). |
| TC-US02-006 | Sorting | Có dữ liệu đủ cho ba chế độ | Mở lần đầu và mở dropdown sort | Mặc định là `Nổi bật`; dropdown có đúng ba lựa chọn `Nổi bật` / `Mới nhất` / `Nhiều lượt thích`. |
| TC-US02-007 | Pin | Scope có 3 comment Ghim và >10 root thường | Đổi lần lượt qua cả ba sort | 3 pin luôn ở trên cùng trong mọi sort, có icon + chữ `Đã ghim`, không lặp lại trong list thường và nằm ngoài quota root batch. |
| TC-US02-008 | Pin boundary | Scope đã có 3 comment ghim | Thử ghim comment thứ 4 qua CMS (US15) | Không thể có quá 3 comment ghim trong cùng scope; tổng số công khai vẫn đếm comment ghim đúng 1 lần. |
| TC-US02-009 | Featured formula | Các root không ghim khác nhau về Like/Reply/AgeHours | Tính score thủ công và mở sort `Nổi bật` | Thứ tự khớp công thức 50% Like, 30% Reply, 20% freshness với decay 72 giờ. |
| TC-US02-010 | Featured formula (tính tay) | Bộ dữ liệu (Like, Reply, AgeHours): (0,0,0), (10,5,24), (10,5,72), (100,0,168) | Tính `FeaturedScore = 0.5×ln(1+Like)+0.3×ln(1+Reply)+0.2×e^(-AgeHours/72)` cho từng bộ và đối chiếu giá trị hệ thống trả về | Giá trị số phải khớp: (0,0,0)→0.2000; (10,5,24)≈1.1989+0.5375+0.1433≈1.8798; (10,5,72)≈1.1989+0.5375+0.0736≈1.8101; (100,0,168)≈2.3076+0+0.0194≈2.3270 (sai số cho phép ≤0.001 — verify giá trị số chứ không chỉ verify thứ tự). |
| TC-US02-011 | Featured tie | Hai root có Featured Score bằng nhau | Mở sort `Nổi bật` | Comment mới hơn đứng trước; nếu vẫn bằng nhau thì `comment_id` tạo thứ tự ổn định giữa các lần load. |
| TC-US02-012 | Latest | Có root đăng ở nhiều thời điểm khác nhau, kèm reply | Chọn sort `Mới nhất` | Root sắp từ mới đến cũ; reply không bị trộn thành item gốc trong list. |
| TC-US02-013 | Most liked | Có root với Net Like khác nhau và trường hợp Net Like bằng nhau | Chọn sort `Nhiều lượt thích` | Public Net Like cao hơn đứng trước; bằng nhau thì comment mới hơn đứng trước. |
| TC-US02-014 | Initial load | Scope có >10 root | Mở khu vực bình luận | Lần đầu trả đúng 10 root (không tính nhóm ghim). |
| TC-US02-015 | Lazy load | Còn >20 root sau lần tải đầu | Cuộn liên tục tới gần cuối nhiều lần | Mỗi batch thêm tối đa 10 root; không trùng/bỏ sót và dừng đúng cuối danh sách; chỉ lấy dữ liệu trong scope hiện tại. |
| TC-US02-016 | Locked liker | U1 đã Like C1; sau đó U1 bị Account Lock rồi được mở khóa | Đối chiếu Net Like/Featured Score/ranking trước khóa, khi khóa và sau mở khóa | Khi khóa, Like của U1 tạm bị loại khỏi public Net Like/Featured Score/ranking nhưng record không mất; mở khóa tính lại nếu Like record và target vẫn hợp lệ. |
| TC-US02-017 | New comments | Đang đọc ở sort `Nổi bật`, `Nhiều lượt thích` và `Mới nhất`; có comment mới được đăng | Quan sát list rồi bấm indicator | Không tự chèn comment mới vào list; hiện `Có {n} bình luận mới`. Khi refresh, `Nổi bật`/`Nhiều lượt thích` giữ đúng ranking; `Mới nhất` có thể đưa user tới comment mới đầu tiên. |
| TC-US02-018 | Truncate | Có comment dài hơn 3 dòng | Mở list và bấm `Xem thêm` rồi `Thu gọn` | Mặc định rút gọn tối đa 3 dòng; `Xem thêm`/`Thu gọn` hoạt động đúng. |
| TC-US02-019 | Reply preview | Root có reply và root không có reply | Mở list root | Không preload reply; root có reply hiển thị `{n} phản hồi` (không dùng nhãn khác như “{n} bình luận”) và mở thread theo US08. |
| TC-US02-020 | Session context | Rời tab Bình luận rồi quay lại trong cùng phiên | Quay lại tab | Giữ scroll/sort/thread/expand state; refresh ngầm không reset context. |
| TC-US02-021 | SmartTV | Thiết bị SmartTV, scope có >20 root | Dùng remote để đọc, mở dropdown đổi sort và cuộn lazy load | Đọc, đổi sort và lazy load thực hiện được đầy đủ bằng remote. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Nhãn control sort đang chọn | Dùng **đúng tên chế độ**, không thêm hậu tố: `Nổi bật` / `Mới nhất` / `Nhiều lượt thích`. Không dùng biến thể “Nổi bật nhất”. |
| Tiêu đề sheet chọn sort | **Sắp xếp theo** |
| Lối vào thread trên root card | **{n} phản hồi** |
| Lựa chọn sort `Nổi bật` | **Nổi bật**<br>Ưu tiên bình luận được ghim và có tương tác cao, còn mới.<br>`[Chọn]` |
| Lựa chọn sort `Mới nhất` | **Mới nhất**<br>Hiển thị bình luận theo thời gian đăng, mới nhất lên đầu.<br>`[Chọn]` |
| Lựa chọn sort `Nhiều lượt thích` | **Nhiều lượt thích**<br>Hiển thị bình luận có số lượt thích công khai cao nhất lên đầu.<br>`[Chọn]` |
