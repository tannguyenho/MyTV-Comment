# Yêu cầu chéo: Accessibility (WCAG 2.1 AA) & Bảo mật

Tài liệu này tổng hợp các yêu cầu **cross-cutting** (áp dụng xuyên suốt toàn bộ 20 User Story) về khả năng tiếp cận (accessibility) và bảo mật, dựa trên kết quả một đợt rà soát UX/bảo mật trên backlog MyTV Comment. Theo quy ước tại `CONVENTIONS.md`, các User Story liên quan chỉ dẫn chiếu tới mục tương ứng trong file này thay vì lặp lại toàn bộ nội dung.

## Phần A — Accessibility (WCAG 2.1 AA)

### A.1. Yêu cầu chung

- Toàn bộ tính năng bình luận (web + mobile) phải tuân thủ **WCAG 2.1 mức AA**.
- **Tương phản màu**: tối thiểu **4.5:1** cho văn bản thường, tối thiểu **3:1** cho thành phần UI/đồ họa (bao gồm nền của **đoạn chữ bị làm mờ do Spoiler** và trạng thái focus/underline của **timestamp link**).
- **Touch target**: tối thiểu **44×44pt** cho mọi phần tử tương tác (nút Like, nút Report, timestamp, sao rating, đoạn chữ bị làm mờ do Spoiler, nút "Xem thêm phản hồi"...).
- **Font scaling / Dynamic Type**: hỗ trợ phóng to tới **200%** mà không bị cắt nội dung, không mất chức năng, không chồng chéo layout.
- **Điều hướng bàn phím (web)**: toàn bộ luồng thao tác (đăng comment, reply, like, report, rating, mention, xem thêm phản hồi, seek timestamp) phải thao tác được đầy đủ bằng bàn phím, có thứ tự tab hợp lý và focus indicator rõ ràng.
- **`prefers-reduced-motion`**: animation của optimistic Like (US07) và các hiệu ứng chuyển trạng thái khác phải tôn trọng cờ hệ điều hành này — khi bật, giảm/tắt hiệu ứng chuyển động, giữ nguyên chức năng.

### A.2. Yêu cầu cụ thể theo thành phần

| Thành phần | US liên quan | Yêu cầu |
|---|---|---|
| Nút Like (optimistic UI) | US07 | Dùng thuộc tính `aria-pressed` để phản ánh trạng thái đã Like/chưa Like; có vùng `aria-live="polite"` cho số Like để screen reader đọc số cập nhật; khi client reconcile với BE và phải revert (do lỗi/conflict), phải announce thay đổi qua vùng `aria-live` đó, không âm thầm đổi số trên UI. |
| Đoạn chữ Spoiler (Làm mờ) | US04 | Đoạn chữ bị làm mờ phải đặt `aria-hidden="true"` cho tới khi user chủ động chạm để hiện — **không được để screen reader đọc xuyên qua nội dung spoiler** trước khi user cho phép. Vùng mờ phải là phần tử focusable/bấm được (không phải `<span>` trang trí) với accessible name **"Hiện nội dung có tiết lộ"**; mỗi đoạn mờ trong cùng một comment là một vùng độc lập. |
| Timestamp bấm được | US06 | Phải là phần tử `<button>` thực sự (không dùng `<span>`/`<div>` gắn `onClick`) để đảm bảo focusable và có role đúng theo bàn phím/AT. Accessible name phải ở dạng đọc được, ví dụ **"Xem từ phút {m} giây {s}"**, không phải chuỗi số trần dạng "18:00". |
| Rating 5 sao | US03 | Dùng pattern `radiogroup` (mỗi sao là một `radio`), điều hướng chọn giá trị bằng phím mũi tên trái/phải; mỗi sao có nhãn accessible riêng dạng **"{n} sao"**. |
| Quay lại đúng comment sau login | US01 (AC6) | Sau khi login xong và điều hướng về đúng comment target, phải **chủ động set focus** vào phần tử comment đó (ví dụ bằng `tabindex="-1"` + `.focus()`), không chỉ scroll tới vị trí bằng mắt — nếu không, user dùng screen reader/bàn phím sẽ mất ngữ cảnh. |
| "Xem thêm phản hồi" | US08 (AC10) | Sau khi tải thêm reply xong, giữ nguyên **focus tại nút "Xem thêm phản hồi"** (hoặc chuyển focus tới reply đầu tiên vừa tải, tuỳ thiết kế), đồng thời announce số lượng reply vừa tải qua vùng `aria-live` (ví dụ "Đã tải thêm 10 phản hồi"). |
| Badge | US17 | Badge hiển thị bằng icon phải có **text alternative** là tên huy hiệu (`alt`/`aria-label`, ví dụ "Huy hiệu Fan kỳ cựu"), không được truyền đạt chỉ bằng hình ảnh. |
| Chip trạng thái (Chờ duyệt/Từ chối/Khóa bình luận...) | Toàn bộ US có trạng thái hiển thị dạng chip trên CMS/app | Bắt buộc kết hợp **icon + text**, không được truyền đạt thông tin chỉ bằng màu sắc đơn thuần (theo WCAG 1.4.1 — Use of Color). |

## Phần B — Bảo mật

### B.1. Chống XSS / injection

*US liên quan trực tiếp: US04, US08, US11; ảnh hưởng: US01, US13, US18.*

- Toàn bộ nội dung do user nhập — comment, reply, nickname, note CMS ("Vi phạm khác") — phải được **escape/encode ở mọi bề mặt hiển thị**: web, mobile app, CMS (danh sách + chi tiết), export CSV/XLSX, preview share.
- **Export CSV** phải neutralize **formula injection**: nếu nội dung ô bắt đầu bằng `=`, `+`, `-`, hoặc `@`, phải thêm ký tự thoát (ví dụ prefix `'`) trước khi ghi file, tránh Excel/Sheets tự thực thi công thức khi mở file export.
- Lưu ý quan trọng: **AI moderation phân loại nội dung NGỮ NGHĨA (Nhẹ/Trung bình/Nặng), không phải hàng rào chống injection** — risk "Nhẹ" hoàn toàn không đồng nghĩa với an toàn khi render; việc sanitize/encode là bắt buộc độc lập với kết quả AI moderation.

### B.2. Ký tự đối kháng / Unicode

- Chặn hoặc neutralize trong comment/reply/nickname các nhóm ký tự:
  - **RTL override**: U+202E và các ký tự bidi override tương tự.
  - **Zero-width**: U+200B (zero-width space), U+200D (zero-width joiner) và tương tự — có thể dùng để né bộ lọc từ khoá.
  - **Control character**: U+0000–U+001F.
- **Nickname** phải chặn **homoglyph** (ví dụ ký tự Cyrillic а/о nhìn giống Latin a/o) — không được tạo ra nickname "nhìn giống hệt" một nickname đã tồn tại mà vẫn vượt qua được kiểm tra uniqueness (chuẩn hoá Unicode/so khớp confusable trước khi check unique).

### B.3. IDOR — phân quyền ghi theo scope CMS

*US liên quan: US13, US14, US16.*

- Mọi hành động ghi trên CMS — **Duyệt/Ẩn/Xóa/Undo/bulk moderation/export PII/ghim (Pin)/áp sanction** — phải được kiểm tra quyền và **scope Admin/Moderator ở tầng API**, không chỉ chặn ở lớp UI.
- Một Moderator ngoài scope được cấp, nếu gọi thẳng API bằng ID biết trước (thread/comment/user ID đoán được hoặc rò rỉ), request phải bị **từ chối (403/404 nhất quán)**.
- Response lỗi và metadata **không được để lộ sự tồn tại hay nội dung của record** nằm ngoài scope (tránh oracle cho phép dò/enumerate dữ liệu qua sự khác biệt giữa "không có quyền" và "không tồn tại").

### B.4. PII trong push notification

*US liên quan: US09 (AC13).*

- Payload push notification **không được chứa nguyên văn** nội dung có gắn Spoiler, cũng không chứa PII dạng số điện thoại đầy đủ — vì nội dung push có thể hiển thị trên **màn hình khóa** thiết bị, ngoài tầm kiểm soát truy cập trong app.
- Tên người gửi hiển thị trên push phải dùng **nickname** hoặc **identity đã mask**, không dùng dữ liệu định danh đầy đủ.

### B.5. PII trong gợi ý mention

*US liên quan: US09 (AC3), US04 (AC11).*

- Response API và UI dropdown gợi ý mention **chỉ được chứa nickname hợp lệ hoặc identity đã mask** (dạng `0******124`) — không bao giờ trả về số điện thoại/email đầy đủ.
- Ô mention **không được dùng để enumerate tài khoản** ngoài phạm vi thread/phim hiện tại (không cho phép gõ tự do để dò danh sách toàn bộ user hệ thống).

### B.6. Session và Account Lock

*US liên quan: US16.*

- Khi một **Account Lock** có hiệu lực, **session hiện tại** của user đó phải bị **vô hiệu hoá ngay tại effective time** — không chỉ chặn việc đăng nhập mới, tránh trường hợp user vẫn thao tác được bằng access token còn hạn sau khi đã bị khoá.
- Request được gửi **hợp lệ trước effective time** của Account Lock vẫn được xử lý theo mode/luồng cũ (đúng theo nguyên tắc "grandfathering" đã chốt ở mục nghiệp vụ liên quan).
- Request gửi **sau effective time** phải bị từ chối ở **mọi API** liên quan — Comment, Like, Report, Rating, Share — không chỉ chặn ở tầng UI/app.

## Phần C — Cách các User Story khác tham chiếu file này

Các User Story liên quan trực tiếp (**US01, US03, US04, US06, US07, US08, US09, US13, US14, US16, US17, US18**) dẫn chiếu tới mục tương ứng trong file này thay vì lặp lại toàn bộ yêu cầu.
