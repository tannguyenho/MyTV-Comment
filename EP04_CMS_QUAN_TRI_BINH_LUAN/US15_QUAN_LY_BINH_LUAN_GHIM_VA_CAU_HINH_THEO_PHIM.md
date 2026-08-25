# US15 — Quản lý bình luận ghim và cấu hình theo phim

> Thuộc EP04 — CMS quản trị bình luận
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là Admin vận hành nội dung**, tôi muốn ghim bình luận và cấu hình moderation theo từng phim, để định hướng thảo luận và áp dụng mức kiểm soát phù hợp.

### Ưu tiên

**Must**

### Acceptance Criteria — Bình luận ghim

1. Admin chỉ ghim comment đang Hiển thị và đang public tại thời điểm ghim.
2. Mỗi scope có **hard max 3 comment ghim**; không có cấu hình vượt quá 3.
3. Khi đã đủ 3, Admin phải bỏ ghim/thay thế trước khi ghim item mới.
4. Admin **kéo-thả để sắp xếp thủ công vị trí 1–3**; thứ tự ghim không phụ thuộc Featured Score/thời gian ghim.
5. Mỗi comment ghim có thể có **ngày/giờ hết hạn tùy chọn**; nếu không đặt thì giữ đến khi Admin bỏ ghim hoặc comment không còn hợp lệ.
6. Khi hết hạn hoặc comment bị moderation **Ẩn/Xóa/Từ chối**, item mất Pin và không còn public ở vùng ghim.
7. Nếu tác giả comment bị **Account Lock**, comment tạm không public và **Pin tạm ẩn nhưng metadata Pin được giữ**. Khi mở khóa, Pin tự hiển thị lại nếu comment vẫn hợp lệ, chưa bị moderation riêng và Pin chưa hết hạn.
8. Nếu trong thời gian Account Lock comment bị moderation Ẩn/Xóa/Từ chối riêng, Pin bị mất theo moderation và **không tự khôi phục** khi account mở khóa.
9. Nếu Admin Undo action moderation đã làm mất Pin, Undo chỉ khôi phục content state; **không tự khôi phục Pin**. Admin phải ghim lại nếu muốn.
10. Ghim/bỏ ghim/reorder/set expiry và thay đổi Pin do lifecycle đều lưu audit phù hợp.

### Acceptance Criteria — Cấu hình moderation

1. Mỗi phim có thể cấu hình Chế độ 1, Chế độ 2 hoặc Đóng bình luận; phim không có config riêng thì kế thừa default hệ thống.
2. Cấu hình Mở/Đóng và moderation mode áp cho **toàn bộ phim**, kể cả mọi tập của phim bộ.
3. AI threshold cũng theo inheritance: override cấp phim → default hệ thống theo US11; **nickname không dùng inheritance này** vì dùng global AI policy riêng.
4. Rule “sau X giờ” cho phép Admin chọn mốc. **Phim lẻ:** giờ phát hành MyTV, giờ phát sóng thực tế hoặc mốc Admin nhập thủ công. **Phim bộ:** chỉ giờ phát hành MyTV hoặc mốc Admin nhập thủ công.
5. Admin thấy rõ config hiệu lực, inheritance source và effective time trước khi lưu.
6. Khi thay đổi mode/Đóng, cách xử lý item đang Hiển thị/Chờ duyệt tuân US12.
7. Đóng bình luận không xóa dữ liệu cũ.
8. AI tại US20 chỉ đề xuất; Admin là người quyết định ghim.

### Quy tắc nghiệp vụ

- Hard max pin = 3.
- Pin order là editorial order thủ công.
- Phim override default hệ thống; không có override thì inherit.
- Account Lock chỉ **tạm ẩn Pin**; moderation invalidation thực sự làm mất Pin.
- Undo moderation không tự tạo lại Pin đã mất; khác với unlock Account Lock, vốn có thể khôi phục Pin metadata tạm ẩn nếu còn hợp lệ/chưa hết hạn.
- Scheduled config phải audit before/after, actor, effective time và loại mốc.

*Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục Bảo mật — kiểm soát quyền cấu hình theo phạm vi Admin.*

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US15-001 | Pin | C1 public | Ghim C1 | C1 vào vùng ghim và audit. |
| TC-US15-002 | Hard max | Đã có C1/C2/C3 ghim | Ghim C4 | Không thể vượt 3; yêu cầu thay thế/bỏ ghim. |
| TC-US15-003 | Reorder | Có 3 ghim | Drag vị trí 3→1 | Web/mobile dùng đúng thứ tự thủ công mới. |
| TC-US15-004 | Expiry | C1 ghim có expiry | Kiểm tra trước/sau expiry | Trước hạn còn ghim; hết hạn tự bỏ khỏi vùng ghim và giữ audit. |
| TC-US15-005 | Invalid pin | C1 pending/Ẩn/Xóa/Từ chối | Ghim qua UI/API | Bị chặn. |
| TC-US15-006 | Account Lock pin | C1 đang Pin; tác giả U1 bị Account Lock rồi mở khóa trước expiry | Kiểm tra vùng ghim | Khi khóa Pin tạm ẩn nhưng metadata còn; mở khóa tự hiện lại nếu C1 vẫn hợp lệ. |
| TC-US15-007 | Account Lock + moderation | C1 đang Pin; U1 bị Account Lock; sau đó Admin Ẩn/Xóa/Từ chối C1 | Mở khóa U1 | Pin không tự trở lại vì source đã bị moderation riêng. |
| TC-US15-008 | Undo moderation pin | C1 từng Pin rồi bị Admin Ẩn/Xóa làm mất Pin | Undo moderation | Content state có thể phục hồi nhưng Pin không tự phục hồi; cần Admin ghim lại. |
| TC-US15-009 | Inheritance | Default hệ thống Mode1, phim M1 không override, phim M2 override Mode2 | Gửi nội dung ở M1 và M2 | M1 dùng Mode1 từ default; M2 dùng Mode2. |
| TC-US15-010 | Đóng bình luận | Phim M1 Mở, phim M2 Đóng | Mở tab Bình luận của M1 và M2 | M1 hoạt động; M2 ẩn toàn khu vực và chặn interaction theo US12, áp cho mọi tập của M2. |
| TC-US15-011 | AI threshold inheritance | Default hệ thống và override cấp phim khác nhau | Gửi cùng mẫu content | Dùng đúng override cấp phim → default; nickname không bị ảnh hưởng. |
| TC-US15-012 | X-hours | Phim lẻ cấu hình lần lượt 3 loại mốc; phim bộ mở màn hình cấu hình mốc | Kiểm tra effective transition ở phim lẻ; kiểm tra danh sách loại mốc khả dụng ở phim bộ | Phim lẻ dùng đúng loại mốc Admin chọn. Phim bộ chỉ hiển thị 2 lựa chọn (giờ phát hành MyTV, mốc thủ công); API từ chối nếu ép giá trị “giờ phát sóng thực tế”. |
| TC-US15-013 | Mode transition | Có item public/pending | Đổi Mode1↔Mode2/Đóng | Hành vi đúng US12, không mất lịch sử. |
| TC-US15-014 | Audit | Pin/reorder/expiry/config/lifecycle Pin | Tra history | Có actor/time/before-after/effective data phù hợp. |
| TC-US15-015 | Xác nhận trước khi lưu | Admin thay đổi threshold cho phim đang inherit từ default hệ thống | Mở màn hình xác nhận trước khi lưu | Hiển thị rõ: config đang hiệu lực, nguồn kế thừa (inherit từ default hay override riêng), config sau khi lưu, effective time kèm timezone. |
