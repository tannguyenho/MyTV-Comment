# US19 — Thống kê hoạt động bình luận

> Thuộc EP05 — Tăng trưởng và phân tích
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là quản lý sản phẩm/Admin vận hành**, tôi muốn theo dõi KPI bình luận và tương tác theo phim và thời gian, để đánh giá hiệu quả và ưu tiên vận hành.

### Ưu tiên

**Must**

### Engagement Score

`Engagement Score = Comment × 2 + Reply × 2 + Net Like × 1 + Rating × 1 + Share × 2`

- Chỉ tính Comment/Reply **đang đủ điều kiện public trong dữ liệu chính thức**; nội dung/thread non-public do moderation, lifecycle hoặc Account Lock visibility gate tạm không được tính.
- Engagement dùng **Net Like công khai hiện tại**, không dùng tổng số lần bấm Like lịch sử.
- `Rating` = **số lượng rating hợp lệ hiện hành** trong scope/thời gian đang tính; mỗi account có một rating hợp lệ đóng góp **+1**, bất kể rating 1★ hay 5★.
- `Share` = số **Share event hợp lệ khi OS share sheet mở thành công** theo US18; không cần callback xác nhận user đã gửi sang ứng dụng đích.

### KPI MVP

- Comment gốc mới/công khai.
- Reply mới/công khai.
- Unique commenters trên dữ liệu công khai theo scope/time.
- Net Like công khai hiện tại + tổng thao tác Like/Unlike lịch sử.
- Rating: số rating hợp lệ hiện hành + điểm rating trung bình/tổng lượt hiển thị theo US03.
- Share: số share sheet mở thành công theo rule US18.
- Report + tỷ lệ Report được xác nhận vi phạm.
- Nội dung Ẩn/Xóa/Từ chối.
- Tỷ lệ AI tự Hiển thị ở Mode1.
- Thời gian xử lý moderation queue/SLA.
- Engagement Score và ranking phim.

### Acceptance Criteria

1. Dashboard filter theo phim và khoảng thời gian.
2. **Unique commenters**: trong một khoảng thời gian + scope filter, mỗi account chỉ tính **1 lần** nếu có ít nhất một Comment/Reply đang đủ điều kiện được tính trong public KPI; đổi filter thì tính lại unique trong scope mới.
3. Dashboard cập nhật với độ trễ tối đa **5 phút** và hiển thị thời điểm cập nhật gần nhất.
4. Ranking phim dùng Engagement Score đã chốt; tie-break phải ổn định.
5. Dashboard hiển thị Net Like và tổng thao tác Like/Unlike; Engagement chỉ dùng **Net Like công khai**.
6. Trong Engagement, **mỗi rating hợp lệ hiện hành = 1 đơn vị Rating**, không nhân theo số sao; điểm sao/average là KPI chất lượng riêng.
7. Trong Engagement, **mỗi lần OS share sheet mở thành công = 1 Share**; cancel/đóng sheet sau đó không hoàn tác event đã ghi; retry/lỗi kỹ thuật phải dedup.
8. Khi comment/reply/thread trở thành non-public do **Ẩn/Từ chối/Xóa, self-delete cascade, Admin root moderation cascade hoặc Account Lock visibility**, score/KPI public được điều chỉnh ở pipeline/đối soát tiếp theo. Danh sách nguyên nhân loại KPI ở trên **KHÔNG bao gồm scope Đóng bình luận**. Scope Đóng bình luận là gate hiển thị vận hành (chống spoiler/thời điểm nhạy cảm), KHÔNG phải chế tài nội dung — KPI/Engagement Score của dữ liệu đã phát sinh trước và trong thời gian Đóng được GIỮ NGUYÊN, không bị loại trừ chỉ vì scope đang Đóng. Khi scope mở lại, không cần tính lại KPI vì KPI chưa từng bị loại.
9. Nếu **Account Lock** làm content của user tạm non-public, contribution public của content đó tạm bị loại; khi mở khóa, contribution được tính lại nếu source còn hợp lệ.
10. Nếu user bị Account Lock là **root author**, toàn bộ thread tạm non-public nên Comment/Reply contribution của cả thread, kể cả reply hợp lệ của user khác, tạm bị loại khỏi public KPI/Engagement; reply user khác không bị đổi moderation state.
11. Like do account đang Account Lock tạo vẫn giữ record nhưng tạm bị loại khỏi **Net Like công khai, Featured Score/ranking và Engagement**; mở khóa tính lại nếu record/target còn hợp lệ.
12. Nếu user **self-delete root**, root + toàn bộ reply cascade soft-delete theo US05 và bị loại khỏi public KPI/Engagement; đây không phải visibility tạm thời và không được Admin Undo public lại.
13. Nếu Admin **Ẩn/Xóa root**, toàn thread non-public nên public KPI/Engagement của thread bị loại; state/eligibility badge của reply user khác tuân US14/US17 và không được suy ra trực tiếp từ KPI public.
14. Có job **đối soát tự động mỗi ngày** với dữ liệu nguồn; phát hiện lệch thì tự hiệu chỉnh aggregate và ghi log reconciliation.
15. Hỗ trợ export dashboard/report theo filter + khoảng thời gian hiện tại ở cả **CSV + XLSX**.
16. Retry/duplicate event không làm tăng KPI sai.
17. Quyền dữ liệu/export tuân US13; báo cáo không tự đưa PII nếu không cần.
18. Dashboard có empty/error state rõ ràng.

### Quy tắc nghiệp vụ

- Data dictionary phải định nghĩa rõ Comment/Reply hợp lệ/public, Net Like công khai, Unique commenter và denominator của các tỷ lệ; semantics Rating/Share trong Engagement đã khóa tại US này.
- Rating 1★ và 5★ có cùng trọng số interaction `+1 Rating`; chất lượng rating được phản ánh ở KPI average riêng, không làm thay đổi trọng số Engagement của một hành động rating.
- Share event được ghi tại mốc share sheet mở thành công; không phụ thuộc callback hoàn tất share của OS/app đích.
- Nội dung Chờ duyệt chưa được tính vào public KPI.
- **Account Lock là visibility gate tạm thời đối với public KPI**, không tự xóa source record; unlock có thể phục hồi aggregate nếu source vẫn hợp lệ.
- Public KPI/Engagement và badge eligibility là hai semantic khác nhau: reply user khác có thể tạm bị loại public KPI do root non-public nhưng vẫn giữ badge eligibility trong các case được US17 quy định.
- Self-delete root là lifecycle soft-delete thật toàn thread nên khác Account Lock/Admin Hide visibility cascade.
- Daily reconciliation là lớp bảo đảm tính đúng dài hạn cho pipeline gần real-time 5 phút.

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US19-001 | Metrics | Có event Comment/Reply/Like/Rating/Share | Mở dashboard | Các KPI đúng scope/time. |
| TC-US19-002 | Engagement | C=2, R=3, NetLike=4, Rating hợp lệ hiện hành=5, Share sheet-open=6 | Tính score | Khớp `2C + 2R + NetLike + Rating + 2Share = 31`. |
| TC-US19-003 | Rating semantics | U1 rating 1★, U2 rating 5★ đều hợp lệ hiện hành | Tính Engagement | Rating đóng góp tổng **2**, không phải 6; average rating được tính riêng theo US03. |
| TC-US19-004 | Rating lock | U1 có rating rồi Account Lock | Refresh sau pipeline | Rating U1 bị loại khỏi count Rating dùng cho Engagement và aggregate public; mở khóa tính lại nếu record còn. |
| TC-US19-005 | Share semantics | User mở share sheet thành công rồi cancel | Kiểm tra KPI | Share tăng 1; không cần callback hoàn tất gửi. |
| TC-US19-006 | Moderation invalid content | Comment/reply đang tính score rồi bị Ẩn/Từ chối/Xóa | Refresh sau pipeline/reconciliation | Nội dung/thread liên quan bị loại khỏi score public theo lifecycle đã chốt. |
| TC-US19-007 | Like semantics | Like rồi Unlike nhiều lần | Kiểm tra dashboard | Có thể thấy tổng action history; Engagement chỉ dùng Net Like công khai hiện hành. |
| TC-US19-008 | Locked liker | U1 đã Like C1 rồi Account Lock | Refresh Net Like/ranking/Engagement; sau đó unlock | Like record giữ; khi lock bị loại public aggregate; unlock tính lại nếu hợp lệ. |
| TC-US19-009 | Account Lock content | U1 có C1/R1 public | Khóa U1 rồi unlock | Khi khóa contribution content U1 tạm bị loại public KPI/Engagement; unlock tính lại item hợp lệ. |
| TC-US19-010 | Locked root thread | U1 root C1; U2 có R1 hợp lệ | Account Lock U1 | Cả C1/R1 tạm bị loại public KPI/Engagement; R1 không đổi moderation state. |
| TC-US19-011 | Admin root hide/delete | Root C1 có reply user khác | Admin Ẩn/Xóa C1 | Toàn thread bị loại public KPI/Engagement trong thời gian/non-public lifecycle tương ứng. |
| TC-US19-012 | Self-delete root | U1 self-delete C1 có R1/R2 | Refresh analytics | Root + replies cascade soft-delete và bị loại public KPI; không được khôi phục qua Admin Undo. |
| TC-US19-013 | Unique | U1 có nhiều comment/reply public trong cùng filter | Tính Unique commenters | U1 chỉ tính 1. |
| TC-US19-014 | Unique visibility | U1 chỉ có content bị Account Lock/non-public | Tính Unique commenters | U1 không được tính trong public Unique commenters cho filter đó; unlock có thể tính lại nếu content hợp lệ. |
| TC-US19-015 | Filter scope | U1 tham gia nhiều phim | Đổi filter | Unique được tính lại trong từng scope, không cộng sai ở dashboard tổng. |
| TC-US19-016 | Freshness | Phát sinh event/state change mới | Refresh | Dữ liệu/aggregate thay đổi trong tối đa 5 phút; UI có last-updated. |
| TC-US19-017 | Reconciliation | Cố tình tạo aggregate lệch | Chạy daily job | Job phát hiện, tự sửa và ghi reconciliation log. |
| TC-US19-018 | Export | Có filter/time range | Export CSV/XLSX | File khớp dashboard/data dictionary và filter hiện tại. |
| TC-US19-019 | Extended KPI | Có Report/AI/moderation data | Mở KPI | Có confirmed-report rate, hidden/deleted/rejected, AI auto-display rate, queue time. |
| TC-US19-020 | Dedup | Event retry/duplicate, gồm Share retry do lỗi kỹ thuật | Nạp pipeline | Event không bị tính lặp ngoài định nghĩa; Engagement không tăng sai. |
| TC-US19-021 | Closed scope giữ nguyên KPI | Phim M1 đang có Engagement Score = X với dữ liệu Comment/Reply/Like/Rating/Share đã phát sinh | Admin Đóng bình luận M1; kiểm tra dashboard trong suốt thời gian Đóng; sau đó mở lại scope | Engagement Score/KPI của M1 KHÔNG tụt xuống 0 và KHÔNG bị loại trừ chỉ vì scope Đóng; dữ liệu lịch sử hiển thị nguyên vẹn trên dashboard trong suốt thời gian Đóng; khi mở lại, KPI không cần tính lại vì chưa từng bị loại. |
| TC-US19-022 | Dashboard empty/error/stale state | (a) Filter phim và khoảng thời gian không có dữ liệu; (b) pipeline aggregate lỗi hoặc quá 5 phút chưa cập nhật; (c) export bị lỗi giữa chừng | (a) Áp filter không có data; (b) giả lập pipeline lỗi/trễ; (c) chạy export rồi ngắt giữa chừng | (a) Hiển thị empty state rõ ràng, không hiện số 0 gây hiểu nhầm mất dữ liệu; (b) hiển thị error/stale state kèm thời điểm last-updated, không âm thầm hiển thị số liệu cũ như đang mới; (c) báo lỗi export rõ ràng, không sinh file rỗng hoặc file dở bị hiểu nhầm là kết quả hợp lệ. |

### Microcopy

| Trạng thái | Nội dung hiển thị |
|---|---|
| Empty state — filter không có dữ liệu | **Chưa có dữ liệu cho lựa chọn này**<br>Không có hoạt động nào khớp với phim và khoảng thời gian đã chọn.<br>`[Đổi bộ lọc]` |
| Error/stale state — pipeline lỗi hoặc quá 5 phút chưa cập nhật | **Dữ liệu có thể chưa mới nhất**<br>Hệ thống đang gặp sự cố cập nhật. Cập nhật gần nhất: {last-updated}.<br>`[Thử tải lại]` |
| Error state — export lỗi giữa chừng | **Xuất báo cáo không thành công**<br>Đã có lỗi trong quá trình tạo file, vui lòng thử lại. File không hợp lệ sẽ không được tải xuống.<br>`[Thử lại]` |
