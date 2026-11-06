# CHANGELOG rà soát V5 — Chốt kịch bản theo thiết kế Figma Phone/Web/Smart TV

**Ngày:** 02/11/2026 · **Phạm vi:** toàn bộ backlog (5 Epic / 20 User Story), URD, thiết kế Figma 3 nền tảng.
**Nguồn:** phiên grilling BA ↔ PO (33 câu hỏi, Q1–Q33), file `feedback_figma_tinh_nang_kich_ban.xlsx` (12 feedback của đội phát triển), inventory Figma ngày 02/11/2026.

> **Quan hệ với [V3](CHANGELOG_RASOAT_V3.md) và [V4](CHANGELOG_RASOAT_V4.md):** V3 (bình luận cấp phim) và V4 (phạm vi theo nền tảng, 26/08/2026) vẫn có hiệu lực trừ các điểm V5 thay thế dưới đây (đáng chú ý: V4 QĐ-C5/E4/G4 về rating chỉ đọc, spoiler và deep link chia sẻ trên TV không còn áp dụng vì US03/US18 Deferred và bỏ định dạng; V4 QĐ-D5 "5 reason" đổi thành 4 reason). Khi mâu thuẫn, V5 là bản có hiệu lực. **Thiết kế Figma là nguồn chính của kịch bản**; tài liệu phải bám theo Figma sau khi Figma đã xử lý xong các ghi chú `[BA]`.

---

## 1. Quyết định mới (QĐ-xx5)

| Mã | Quyết định | Thay thế / bổ sung | Q |
|---|---|---|---|
| **QĐ-A5** | **Danh tính bình luận gắn với account MyTV**, không gắn hồ sơ xem (profile). Đổi profile trong cùng account không đổi danh tính, chế tài, huy hiệu, rate limit. **Hồ sơ Trẻ em ẩn hẳn khu vực Bình luận** (Phone/Web/TV, cả UI lẫn API). | Mới | Q1, Q27 |
| **QĐ-B5** | Xác nhận **bình luận cấp phim** (QĐ-A3). Figma bỏ phân nhánh Phim bộ/Phim lẻ; chỉ khác tab mặc định: phim bộ → `Các tập`, phim lẻ → `Tương tự`. | V3 | Q2, Q31 |
| **QĐ-C5** | **Giới hạn 500 ký tự** cho Comment/Reply/Edit (theo Figma Web). | 1.000 ký tự ở README 5.3 | Q3 |
| **QĐ-D5** | **US03 Đánh giá phim → Deferred.** Engagement Score bỏ thành phần Rating. | README 5.4, 5.13 | Q4, Q20 |
| **QĐ-E5** | **US06 Mốc thời gian → Deferred.** Chuỗi `24:14` hiển thị như text thường; không tương tác player. | README 5.5, QĐ-D3 | Q5 |
| **QĐ-F5** | **US18 Chia sẻ → Deferred.** Bỏ OS share sheet, preview, deep link cài app. **Giữ deep link nội bộ** cho thông báo. Engagement Score bỏ Share. | README 5.12, 5.13 | Q6, Q20 |
| **QĐ-G5** | **Bỏ toàn bộ định dạng văn bản** (Đậm/Nghiêng/Gạch chân/Làm mờ/Link). Nội dung là văn bản thuần. Spoiler xử lý bằng lý do Báo cáo + CMS. | README 5.3 (formatting), US04 | Q7 |
| **QĐ-H5** | **Thông báo có target bình luận**: Phone mở **view Bình luận toàn màn hình** (không player, header Back + tên phim + nút "Xem phim"); Web mở trang phim, auto-scroll + mở thread; TV mở trang phim + thread chỉ đọc. Highlight target 2 giây. | README 4.1 (TV), US09 | Q8, Q22 |
| **QĐ-I5** | **Overlay tối** khi focus ô nhập / mở bottom sheet / dialog / màn Phản hồi trên Phone: chặn mọi tương tác với player và nội dung dưới; **video vẫn phát**; bấm vùng tối = đóng. Web dùng backdrop modal tương tự. | Mới | Q9 |
| **QĐ-J5** | **Reply**: reply của reply → cùng thread, prefill `@tên`; thứ tự **cũ → mới**, reply mới append cuối + cuộn tới. Web: expand inline + ô nhập dưới root; Phone: màn Phản hồi. | US08 | Q10 |
| **QĐ-K5** | **Huy hiệu**: (1) **Ghim không phải huy hiệu** → marker riêng, card có thể có cả Ghim + 1 huy hiệu; (2) tối đa 1 huy hiệu, ưu tiên Custom > Nổi bật > Fan kỳ cựu > Fan tích cực; (3) Custom do Admin đặt tên (vd "Chuyên gia"); (4) bấm chip mở sheet giải thích, **không hiện số liệu tiêu chí**; TV chỉ chip; (5) tên chuẩn: Fan tích cực / Fan kỳ cựu / Nổi bật. | README 5.11 | Q11 |
| **QĐ-L5** | **Lý do báo cáo**: Phone/Web **5 lý do** (Có spoiler / Spam, Quảng cáo / Xúc phạm, ngôn từ công kích / Nội dung không phù hợp / Khác) — **bỏ "Sai thông tin"**. **TV 4 lý do**, không "Khác". "Khác" bắt buộc mô tả 1–500 ký tự nhập **trong cùng sheet/modal**. | README 5.7 (6 reason), 4.1 (TV 5 reason) | Q12, Q26, Q29 |
| **QĐ-M5** | **Luồng xử lý báo cáo & phản hồi** (5 bước): gửi → toast; CMS Bỏ qua / Ẩn / Từ chối / Xóa; **reporter** nhận thông báo "đã được xử lý" (không nêu chế tài, không click); **tác giả** nhận thông báo kèm lý do; **card của tác giả** hiện trạng thái "Đã bị ẩn / Không được chấp thuận" + lý do, chỉ tác giả thấy, chỉ còn Xóa. | US10, US12, US14 | Q13 |
| **QĐ-N5** | **Không có form khiếu nại trong app.** Mọi khiếu nại (Khóa bình luận, Khóa tài khoản) qua Tổng đài 1800 1166; thông báo chế tài hiển thị lý do + thời hạn + hướng dẫn liên hệ. | README 5.10, US16 | Q14 |
| **QĐ-O5** | **Hủy đăng bình luận khi Chờ duyệt** = rút khỏi hàng chờ (soft-delete), không hoàn quota rate limit. **Pending: chỉ Hủy, không Sửa.** | US04, US05 | Q15, Q24 |
| **QĐ-P5** | **Blacklist từ khóa**: 1 danh sách toàn hệ thống trong CMS (US15), có audit log, không override theo phim. Khớp (không phân biệt hoa/thường, chuẩn hóa dấu) → chặn ngay như AI Nặng, **không gọi AI**, copy "Bình luận không được chấp thuận". | US11, US15 | Q16, Q25 |
| **QĐ-Q5** | **Không có nickname riêng** cho cộng đồng. Tên hiển thị = tên tài khoản MyTV; chưa có tên → `0***123`. Avatar = avatar tài khoản, mặc định logo MyTV. Toàn bộ rule nickname (5.3) và chính sách AI nickname → **Deferred**. | README 5.3, 5.8, US04, US11 | Q19 |
| **QĐ-R5** | **@mention không click được** (không có trang hồ sơ công khai); hiển thị text màu cam, không hover-link. | US09 | Q21 |
| **QĐ-S5** | **Bảng loại thông báo → đích đến** (xem §3). Khóa tài khoản không có thông báo in-app. | US09 | Q23 |
| **QĐ-T5** | **Số đếm tab/khu vực = root + reply công khai**; ≥1.000 → `1,2K`, ≥1.000.000 → `1,2M`. | US01, US02 | Q28, Q18e |
| **QĐ-U5** | **Công tắc thông báo cộng đồng → Deferred**; dùng cài đặt thông báo chung của app. | README 5.6 | Q18f |
| **QĐ-V5** | Chốt nhanh UI: bình luận dài cắt 4 dòng + "Xem thêm" (Phone/Web; **TV hiện full**); format thời gian `Vừa xong / {n} phút trước / {n} giờ trước / {n} ngày trước (≤7 ngày) / dd/mm/yyyy`; bình luận của mình có nhãn "Bạn" + ⋮ chỉ Sửa/Xóa; icon đã thích tô đặc cam; nhãn sort "Nổi bật" (bỏ "Nổi bật nhất"). | US01, US02, US05, US07 | Q18, Q29 |
| **QĐ-W5** | **Màn chặn đăng nhập khi Khóa tài khoản** thuộc phân hệ Xác thực, ghi vào URD như thiết kế bổ sung (Phone/Web/TV), không block MVP bình luận. | README 5.6 | Q30 |

### Engagement Score mới (QĐ-D5 + QĐ-F5)

`Engagement = Comment×2 + Reply×2 + Net Like×1` — thành phần `Rating×1` và `Share×2` sẽ bổ sung khi bật lại US03/US18.

---

## 2. Trạng thái 20 User Story sau V5

| ID | Trạng thái | Ghi chú |
|---|---|---|
| US01, US02, US04, US05, US07, US08, US09, US10, US11, US12, US13, US14, US15, US16, US17, US19, US20 | **Active** | Cập nhật theo QĐ-xx5 ở trên |
| **US03** | **Deferred** | Thiết kế giữ hidden trên Figma Phone/Web |
| **US06** | **Deferred** | Thiết kế giữ hidden trên Figma Phone/Web; Web gỡ link `24:14` còn sót ở US08/US10 |
| **US18** | **Deferred** | Thiết kế giữ hidden; Phone gỡ "Chia sẻ bình luận" khỏi menu ⋮ và nhánh deep link cài app |

Ma trận nền tảng (thay bảng 4.1 README và mục 1 của V4):

| Nền tảng | User Story áp dụng |
|---|---|
| Phone | US01, US02, US04, US05, US07, US08, US09, US10, US17 |
| Web | US01, US02, US04, US05, US07, US08, US09, US10, US17 |
| Smart TV | US01 (chỉ đọc, full text), US07, US10 (4 lý do), US17 (chip) |
| CMS | US11, US12, US13, US14, US15 (+blacklist), US16, US19, US20 |

---

## 3. Bảng loại thông báo → đích đến (QĐ-S5)

| Loại | Nội dung | Bấm vào mở |
|---|---|---|
| Reply / Mention | "{Tên} đã trả lời / nhắc đến bạn trong {phim}" | Phone: view Bình luận toàn màn hình; Web: trang phim + scroll + thread; TV: trang phim + thread chỉ đọc |
| Báo cáo đã xử lý (reporter) | "Báo cáo của bạn về một bình luận đã được xử lý" | Không mở gì |
| Bình luận bị ẩn/xóa/từ chối (tác giả) | "Bình luận của bạn đã bị ẩn do: {lý do}" | Phone: Chi tiết thông báo; Web: modal "Vi phạm tiêu chuẩn" |
| Cảnh báo / Khóa bình luận | "…bị khóa bình luận đến {ngày giờ} do: {lý do}. Liên hệ 1800 1166 để khiếu nại" | Chi tiết thông báo / modal |
| Được cấp huy hiệu | "Bạn vừa nhận huy hiệu {tên}" | Sheet/modal Huy hiệu thành viên (TV: không mở) |
| Khóa tài khoản | Không có in-app (có thể push) | Màn hình khóa khi đăng nhập |

---

## 4. Ghi chú `[BA]` đã đặt trên Figma (02/11/2026)

Đặt dưới dạng sticky note màu cam cạnh frame (công cụ không tạo được comment thread). Đội thiết kế xử lý xong thì xóa note.

| File | Mã | Frame / section | Tóm tắt |
|---|---|---|---|
| Phone | P1 | US01 section | Bỏ nhánh Phim bộ/Phim lẻ |
| Phone | P2 | US01 "Deep link comment/thread" | Gỡ nhánh cài app; thêm view Bình luận toàn màn hình từ thông báo |
| Phone | P3 | US01 "Step 1 - Play Comment - Login" | Sort "Nổi bật"; nhãn "Bạn"; Ghim tách slot; Xem thêm; số đếm K/M; format thời gian; tên hiển thị |
| Phone | P4 | US01 "Step 1.5 - Play Close Comment" | Copy state Đóng |
| Phone | P5 | US04 section | Overlay; 500 ký tự + state vượt; bỏ định dạng; giữ blacklist |
| Phone | P6 | US04 state Waiting | Pending chỉ Hủy, ẩn Sửa |
| Phone | P7 | US08 section | Reply 1 cấp, thứ tự cũ→mới, prefill @ |
| Phone | P8 | US09 "Thông báo" | 3 loại thông báo mới; chi tiết thông báo có lý do/thời hạn/hotline |
| Phone | P9 | US10 kebab sheet | Gỡ "Chia sẻ bình luận" |
| Phone | P10 | US10 sheet Báo cáo | Xóa radio trống; "Khác" → textarea 0/500 cùng sheet |
| Phone | P11 | US17 sheet Huy hiệu | Tên chuẩn, Custom có tên mẫu, không hiện số liệu |
| Phone | P12 | US05 section | State card bị ẩn/từ chối cho tác giả |
| Phone | P13 | Component | Badge "Nổi bật"; ẩn Spoiler Fill/Edit Menu; marker Ghim; US03/06/18 giữ hidden |
| Web | W1 | US04 "Step 3.1_Bôi đen" | Bỏ toolbar định dạng + component Format |
| Web | W2 | US08 "Step 2.1" | Gỡ link "24:14" |
| Web | W3 | US01 "Step 1 - Play Comment - Nologin" | Chuẩn hoá card (như P3) + icon đã thích |
| Web | W4 | US02 "Step 2 - Arrange - Login" | "Nổi bật nhất" → "Nổi bật" |
| Web | W5 | US04 "Step 3.6_Chờ xét duyệt" | Thêm Hủy đăng, ẩn Sửa |
| Web | W6 | US09 "Thông báo nhắc tên" | 3 loại thông báo; modal vi phạm có lý do/thời hạn/hotline |
| Web | W7 | US10 "Step 2.1" modal | "Khác" → textarea 0/500 |
| Web | W8 | US04 "Step 3.3_Tag" | @mention không click |
| Web | W9 | US01 section | Hành vi deep link/thông báo trên Web; cấp phim; Trẻ em |
| Web | W10 | US05 section | State card bị ẩn/từ chối |
| TV | T1 | US01 section | Bỏ nhánh phim bộ/lẻ; "cấp 2" → "Xem phản hồi" |
| TV | T2 | Popup Báo cáo | Sửa copy "quảng cáo này"; dọn layer ẩn; 4 lý do |
| TV | T3 | List "VOD Comment" | Ghim tách slot; full text; số đếm; thời gian; tên hiển thị |
| TV | T4 | Component Badge | "Bình luận nổi bật" → "Nổi bật" |

**Màn cần thiết kế mới:** view Bình luận toàn màn hình từ thông báo (Phone); card tác giả bị ẩn (Phone/Web); ô mô tả "Khác" (Phone/Web); state vượt 500 ký tự (Phone); 3 item thông báo mới (Phone/Web); nhãn "Bạn" + marker Ghim (3 nền tảng); màn chặn đăng nhập khi Khóa tài khoản (3 nền tảng).

---

## 5. Tài liệu đã cập nhật

| Nhóm | Tệp |
|---|---|
| Backlog và quyết định | [README.md](README.md) (mục 2, 4.1, 5.x) |
| Tài liệu bàn giao | [TAI_LIEU/URD_content.json](TAI_LIEU/URD_content.json) → `03_BM03_URD_MyTV_Comment.docx` **phiên bản 2.0** (71 trang, 51 hình Phone/Web/TV) |
| User Story | US03, US06, US18 gắn banner Deferred; các US còn lại tham chiếu V5 (chi tiết AC sẽ đồng bộ ở vòng refinement kế tiếp) |

## 6. Điểm còn treo

- SRS (`04_BM04_SRS`) chưa cập nhật theo V5 — làm sau khi Figma xử lý xong ghi chú `[BA]` để lấy ảnh chuẩn.
- `UR_NF33` / `UR_NF48` vẫn chờ số liệu (từ V3).
- Thiết kế CMS chưa có trên Figma.
