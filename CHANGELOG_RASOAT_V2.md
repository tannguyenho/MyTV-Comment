# Nhật ký thay đổi — Áp dụng rà soát vòng 2

> **Ghi chú:** đây là hồ sơ của vòng rà soát V2. Quyết định **QĐ-A** dưới đây (phim bộ bình luận và đánh giá theo từng tập) **đã được thay thế** tại [CHANGELOG_RASOAT_V3.md](CHANGELOG_RASOAT_V3.md). Khi hai tài liệu mâu thuẫn, V3 là bản có hiệu lực.


**Ngày:** 19/08/2026 · **Áp lên:** `e1c71a0`
**Căn cứ:** Báo cáo rà soát vòng 2 (19 phát hiện) + 4 quyết định PO chốt ngày 19/08/2026

Mỗi mục dưới đây ghi: vấn đề gốc → thay đổi → file bị ảnh hưởng. Dùng để review từng điểm mà không cần đọc lại báo cáo.

---

## Phần 0 — Bốn quyết định PO làm căn cứ

| Mã | Quyết định | Phương án bị loại |
|---|---|---|
| **QĐ-A** | **Bỏ hẳn scope Series phía người xem.** Phim lẻ: comment/rating cấp phim. Phim bộ: chỉ theo tập hiện tại. CMS **vẫn giữ** cấu hình cấp series (US15). | Giữ scope Series phía người xem theo README cũ |
| **QĐ-B** | **Không cho xóa rating.** Chỉ đổi mức sao, không có `DELETE rating` trong MVP. | Cho xóa theo README cũ |
| **QĐ-C** | **Nickname không bao giờ có trạng thái Chờ duyệt.** AI timeout / ngôn ngữ ngoài Việt-Anh / low-confidence đều xử lý giống nhau: chặn, giữ tên cũ, cho thử lại, không queue, **không tiêu quota**. | Đưa về hàng chờ Admin; hoặc cho qua nếu ngoài Việt-Anh |
| **QĐ-D** | Sửa toàn bộ 19 điểm của báo cáo, kèm nhật ký này. | Chỉ sửa nhóm chặn + Cao |

---

## Phần 1 — Ba điểm chặn

### 1.1. Scope Series bị bỏ nửa vời (QĐ-A)

**Vấn đề:** US02 AC1 và US03 AC3 đã bỏ scope Series phía người xem, nhưng `README:67` — nằm trong mục *"Các quyết định nghiệp vụ đã khóa"* — vẫn ghi "Rating có cả cấp series và episode". IA còn màn `C03 Comment Area — Series scope` **ghi nguồn là US02/US03**, chính hai file phủ định sự tồn tại của nó.

**Thay đổi:**

| File | Thay đổi |
|---|---|
| `README.md` | Mục 2: mô tả phạm vi theo phim lẻ/phim bộ. Mục 5.1: bỏ "rating cấp series"; **thêm câu mới** nêu rõ CMS vẫn giữ cấu hình cấp series (US15) để không ai hiểu nhầm là bỏ luôn cấu hình |
| `SOLUTION_ARCHITECTURE.md` | Mục 2.2 phạm vi; mục 9 đổi "chuyển series↔episode" thành "cách hiển thị context phim/tập đang xem" |
| `US17_HUY_HIEU_NGUOI_DUNG.md` | Phạm vi tính Top 10%: "gộp mọi scope (cả cấp series và cấp episode)" → "gộp toàn bộ phim lẻ và tập phim trên hệ thống". Sửa cả trong `TC-US17-027` |
| `UX_INFORMATION_ARCHITECTURE_SCREEN_MAP.md` | Viết lại IA-02; **gỡ màn `C03` và `C04`**; sửa Exit của C02, entry points, route model, deep-link, navigation rule; gỡ "Scope Series/Episode" khỏi đợt wireframe P0 |
| `UX_FIGMA_WIREFRAMES.md` | Câu context Series/Episode → mô hình phim/tập hiện tại |

**Giữ nguyên có chủ đích:** 4 vị trí trong IA (CMS Search/Pin/Config) và các chỗ trong README/SOLUTION_ARCHITECTURE nói về **cấu hình CMS cấp series** — đây là chuyện khác, vẫn đúng.

### 1.2. Rating xóa được hay không (QĐ-B)

**Vấn đề:** `README:100` nói "user được xóa rating", US03 nói "không hỗ trợ xóa rating". BE đọc README sẽ mở `DELETE /rating` mà FE không có UI bảo vệ — gọi trực tiếp được để hạ tổng lượt rating công khai.

**Thay đổi:** `README.md` mục 5.4 sửa thành "user **không được xóa rating**, chỉ được đổi mức sao; không có thao tác DELETE rating trong MVP (xem US03)". US03 và `US03_USER_FLOW.md` vốn đã đúng, giữ nguyên.

### 1.3. Nickname khi AI timeout hoặc ngôn ngữ ngoài Việt-Anh (QĐ-C)

**Vấn đề:** `TC-US11-007` ghi đích danh *"Gửi content/**nickname**"* → *"Dữ liệu vào Chờ duyệt"*, mâu thuẫn với 5 chỗ khác trong cùng file khẳng định nickname không có Chờ duyệt. Riêng trường hợp nickname ngoài Việt-Anh thì **chưa dòng nào trong repo xử lý**.

**Thay đổi trong `US11_AI_KIEM_DUYET_THEO_HAI_CHE_DO.md`:**

- Mục Phạm vi, **AC6**, **AC7**: giới hạn rõ chỉ áp cho Comment/Reply/Edit, thêm mệnh đề loại trừ nickname dẫn tới mục "Global policy — Nickname"
- **AC9**: "nickname queue item" → "nickname decision"
- Rule "Fallback AI lỗi luôn fail-safe về queue": tách rõ content → queue; nickname → chặn + retry, không queue
- **Mục "Global policy — Nickname"**: thêm 2 mục mới — timeout/ngoài Việt-Anh/low-confidence xử lý giống nhau; và quy tắc **không tiêu quota** khi bị chặn (trước đây quy tắc này chỉ tồn tại ở file user flow, chưa có trong backlog)
- `TC-US11-007`, `TC-US11-008`, `TC-US11-012`: bỏ nickname khỏi kỳ vọng "vào Chờ duyệt"
- **3 test case mới:** `TC-US11-014` (nickname tiếng Hàn), `TC-US11-015` (low-confidence), `TC-US11-016` (nickname AI timeout)

**Kèm theo trong `US04_DANG_BINH_LUAN.md`:** AC10 thêm chữ **"thành công"** vào quota nickname (trước đây đọc riêng AC10 sẽ hiểu mọi submission đều tiêu quota, ngược với rule ở 3 chỗ khác), và bổ sung trường hợp timeout/ngoài Việt-Anh/low-confidence cũng không tiêu quota.

---

## Phần 2 — Sáu lỗi Cao

### 2.1. US12 tự mâu thuẫn với chính mình

**Vấn đề:** bảng ưu tiên gate ghi *"gate 2/3 thắng gate 4, gate 4 thắng gate 5"*, nhưng cách đó 28 dòng trong cùng file vẫn còn rule cũ: *"Deep link trong scope Đóng dùng fallback **theo scope**, không dùng thông báo của target bị **moderation riêng**"* — tức scope thắng moderation, ngược hoàn toàn.

**Thay đổi:** rule đó được viết lại để tuân theo Resolver — nếu target **chỉ** bị gate scope Đóng thì dùng thông báo scope; nếu còn moderation riêng / Admin root cascade / Account Lock thì dùng thông báo của gate ưu tiên cao hơn. AC10 bổ sung mệnh đề điều kiện tương ứng. `TC-US12-009` mở rộng thành 3 trường hợp (chỉ scope / + moderation riêng / + Account Lock) với chuỗi thông báo khớp từng trường hợp.

### 2.2. Hồi quy: US02 mất 56% nội dung

**Vấn đề:** commit `bee9501` rút gọn US02 từ 103 → 45 dòng, làm mất phần bổ sung của vòng rà trước. Commit `e1c71a0` khôi phục US04/US07/US08 nhưng bỏ sót US02/US03.

**Thay đổi — US02: 45 → 114 dòng, test case 7 → 21**

- Khôi phục mục **Ưu tiên** (`Must`) — US02 từng là file **duy nhất trong 20 file** thiếu mục này
- Đổi heading `### Business rules` → `### Quy tắc nghiệp vụ` — US02 từng là file duy nhất dùng tiếng Anh
- Khôi phục **Giá trị, Điều kiện tiên quyết, Phụ thuộc, Điểm cần PO chốt, Phân tích kiểm thử, Microcopy**
- Khôi phục rule tường minh loại trừ Account Lock (kể cả reply cascade) và scope Đóng khỏi public count, diễn đạt theo Effective Visibility Resolver, kèm ghi chú **không ảnh hưởng KPI** (US19)
- Khôi phục `TC-US02-005` (counter exclusion) và `TC-US02-010` (tính tay Featured Score)

**Thay đổi — US03: 55 → 85 dòng, test case 8 → 13.** Bổ sung các mục cấu trúc chuẩn, dẫn chiếu a11y (`radiogroup`), test case mới cho Comment Lock, làm tròn, scope Đóng, phim lẻ, idempotency.

> **Sửa lỗi số học:** test case tính tay Featured Score ở bản `d3706a9` có giá trị sai. Đã tính lại và xác minh bằng Python — bốn bộ dữ liệu `(0,0,0)→0.2000`, `(10,5,24)→1.8798`, `(10,5,72)→1.8101`, `(100,0,168)→2.3270`, sai số dưới 0,0001.

**Không khôi phục có chủ đích:** test case cũ về xóa rating (trái QĐ-B — thay bằng test verify **không** tồn tại action xóa/endpoint DELETE); test case cũ giả định scope Series (viết lại theo mô hình phim lẻ/phim bộ).

### 2.3. US08_USER_FLOW đổi cơ chế tải reply, phá cam kết a11y

**Vấn đề:** flow mô tả "cuộn gần cuối → lazy load 10 reply/batch" (infinite scroll), trong khi US08 AC10 + README + `TC-US08-008` + `REQUIREMENTS_A11Y_SECURITY` đều yêu cầu nút **"Xem thêm {n} phản hồi"**. Infinite scroll không có `<button>` → người dùng bàn phím/screen reader mất điểm dừng focus, nội dung tự chèn không announce.

**Thay đổi:** khôi phục initial 3 reply + nút `[Xem thêm {n} phản hồi]`, mỗi lần tải tối đa 10 (còn <10 tải hết), vòng lặp cập nhật `{n}` và ẩn nút khi hết. Thêm ghi chú a11y: giữ focus tại nút, announce qua `aria-live`, dùng `<button>` thật, touch target 44×44pt. **Ghi rõ** infinite scroll vẫn đúng cho danh sách root comment (US02) — chỉ reply mới dùng nút.

### 2.4. US18_USER_FLOW thêm kênh chia sẻ riêng + mất Share event

**Vấn đề A:** flow có nhánh Web mở dialog **Facebook / Zalo**, trái `README:205` *"MVP dùng OS share sheet, không direct SDK Facebook/Zalo/TikTok"*.

**Vấn đề B (nặng hơn):** chỉ nhánh Phone đi qua node ghi Share event; nhánh Web đi thẳng, **không ghi**. Một tập có 500 share Web + 100 Phone → dashboard chỉ ghi 100 → Engagement Score thiếu 800 điểm, ranking phim sai. Đối soát hằng ngày không phát hiện được vì nó đối soát với chính nguồn sự kiện vốn không được ghi.

**Thay đổi:** gỡ hoàn toàn Facebook/Zalo; Web rẽ nhánh theo khả năng hỗ trợ Web Share API → OS share sheet, nếu không thì fallback "Sao chép liên kết". **Cả hai nhánh Web đều đi qua node ghi Share event**, với mốc ghi nhận rõ ràng (sheet mở thành công, hoặc copy link thành công với fallback), kèm khử trùng lặp và liệt kê các trường hợp không ghi nhận.

### 2.5. US07_USER_FLOW bỏ cơ chế gom batch

**Vấn đề:** flow mô tả "auto retry đúng 1 lần → vẫn lỗi thì revert", trong khi README mục 5.6 + US07 AC4/5/6 yêu cầu gom batch 5 giây + coalesce + flush sớm. Kịch bản hỏng: user đi thang máy Like 4 comment → revert cả 4 tim và bắn 4 toast lỗi.

**Thay đổi:** chèn node gom batch + coalesce theo target về state cuối; flush khi đủ 5 giây **hoặc** rời màn hình/background. Kết quả từ BE rẽ ba nhánh: thành công (giữ state BE) / mismatch-từ chối (revert + announce, đúng AC7) / **lỗi mạng (giữ batch, KHÔNG revert, tự retry khi có mạng)**. Thêm nhánh force-kill app → reconcile theo BE.

### 2.6. README chưa đồng bộ điều kiện Undo

**Vấn đề:** `README:163` ghi "Undo **khi còn retention**" áp cho cả ba hành động, trong khi `US14` AC1 đã tách đúng: Từ chối/Ẩn không giới hạn thời gian; chỉ Xóa mềm giới hạn 90 ngày.

**Thay đổi:** README mục 5.9 tách rõ ánh xạ state và điều kiện thời gian, khớp US14 AC1, ghi rõ 90 ngày tính theo retention của **ROOT**.

---

## Phần 3 — Sáu vấn đề Trung bình

| # | Vấn đề | Thay đổi |
|---|---|---|
| 3.1 | **IA không có một dòng nào về SmartTV** (grep = 0) dù 6 file khác yêu cầu. IA quy định mỗi frame Figma phải gắn Screen ID lấy từ chính nó → SmartTV không màn nào được wireframe | Thêm mục `## SmartTV / 10-foot UI`; thêm **cột Platform** cho cả 3 bảng màn hình/state; thêm màn `C17 Thread — SmartTV read-only` (US08) + node trong sơ đồ; thêm state `S13` (không tạo nội dung, hướng dẫn + QR — US01/04/09/10/18); thêm Platform vào handoff checklist |
| 3.2 | IA liệt kê **3 quyết định đã chốt** vào mục "chưa chốt" → gây vòng review thừa và rủi ro thiết kế ngược | Gỡ khỏi mục "chưa chốt", chuyển thành phát biểu khẳng định: Comment Area = **tab riêng**; composer Phone = bottom sheet / Web = inline; truncate **3 dòng**. Kèm theo: đổi mô hình count từ "Header" sang **nhãn tab**; state scope Đóng nay ghi rõ *"giữ tab `Bình luận` nhưng bỏ count"* (trước đây thiếu → wireframe sẽ vẫn hiện `Bình luận (128)` ở khu vực không khả dụng) |
| 3.3 | IA nói sort persist "chưa khóa", trong khi US02 AC3 đã khóa reset về `Nổi bật`. Nằm trong mục IA đặt tên "Navigation rules quan trọng" — nơi dev tin cậy nhất | Thay bằng phát biểu khẳng định theo US02 AC3 |
| 3.4 | `UX_FIGMA_WIREFRAMES` **thiếu `S04`** (Account Lock). Dev sẽ tái dùng frame `S03` → hiện "Bình luận **không còn** khả dụng" thay vì "**hiện không** khả dụng" → user hiểu nhầm bị gỡ vĩnh viễn | Thêm hàng `S04`; thêm nhánh Account Lock vào connected flow; thêm rule **"3 chuỗi fallback = 3 frame khác nhau"**; IA liệt kê S03 và S04 là hai frame riêng trong P0 kèm lý do |
| 3.5 | IA thiếu state cho rate limit comment/edit/nickname; màn `C09 Nickname Settings` có trong bảng nhưng **không nằm ở P0/P1/P2** → không đợt nào vẽ | Thêm `S14` (5 nội dung/phút), `S15` (5 edit/phút/target), `S16` (nickname bị chặn), `S17` (hết quota 24h); đưa `C09` + S16/S17 vào **P0**; bổ sung C09 vào hàng US11 của ma trận coverage |
| 3.6 | `US14_USER_FLOW` chỉ cho 1 reason chung, mất quyền override từng item (US14 AC5 cho phép). 40 comment gồm 38 Spam + 2 Spoiler → cả 40 bị ghi sai lý do, audit sai căn cứ chế tài | Cập nhật: reason chung cho batch → **override reason/note từng item** → item có reason cuối "Vi phạm khác" bắt note 1–500 → bước xem trước per-item → Apply → partial success |

---

## Phần 4 — Bốn điểm Thấp

| # | Vấn đề | Thay đổi |
|---|---|---|
| 4.1 | Nhãn sort lệch: IA ghi "Nhiều lượt thích **nhất**", US02 và flow ghi "Nhiều lượt thích" | Sửa IA cho khớp |
| 4.2 | `US10_USER_FLOW` dùng chuỗi cooldown thiếu `{n} giờ` → user bấm lại sau 1h và sau 23h đều thấy cùng một câu | Trích đúng chuỗi đã chốt của US10 |
| 4.3 | `US04` AC10 thiếu chữ "thành công" trong quota nickname | Đã sửa (gộp trong mục 1.3) |
| 4.4 | Tiêu đề US02/US03 trong file đã đổi nhưng bảng mục lục README vẫn tên cũ | Cập nhật bảng mục lục khớp H1 thực tế; mở rộng ghi chú filename legacy gồm US02 (`SERIES_TAP`), US03 (`SERIES`), US15 (`NOI_BAT`) bên cạnh US06/US18 |

---

## Phần 5 — Kiểm chứng đã chạy

| Kiểm tra | Kết quả |
|---|---|
| `grep "cấp series\|Series scope"` ngoài ngữ cảnh CMS | rỗng |
| `grep "được xóa rating"` | chỉ còn các câu phủ định ("**không** được xóa rating") |
| `grep "nickname queue item"` | rỗng |
| `grep "fallback theo scope"` trong US12 | rỗng |
| `grep "Undo khi còn retention"` trong README | rỗng |
| `grep "Facebook\|Zalo"` trong US18_USER_FLOW | rỗng |
| `grep "Nhiều lượt thích nhất"` | rỗng |
| `grep "SmartTV"` trong IA | 26 kết quả |
| Mục `### Ưu tiên` ở cả 20 file US | đủ |
| Heading `### Business rules` (tiếng Anh) | rỗng |
| ID test case trùng lặp | không có *(TC-US13-010 trong US16 là tham chiếu chéo hợp lệ)* |
| Bảng markdown lệch cột | không có |
| **Sơ đồ Mermaid render thử** | **35/35 OK** |
| Phép toán Featured Score trong `TC-US02-010` | xác minh bằng Python, sai số < 0,0001 |

---

## Phần 6 — Ba điểm còn mở, cần Design/PO xử lý tiếp

Đây **không phải lỗi** — là việc phát sinh tự nhiên sau các thay đổi trên, không tự quyết được:

1. **Frame `S04` chưa tồn tại trong file Figma.** IA và `UX_FIGMA_WIREFRAMES` đã khai báo state này, nhưng chưa có `node-id`. Tài liệu ghi *"(frame chưa dựng trong file Figma)"* thay vì bịa link. **Cần Design dựng frame và điền link.**
2. **Microcopy cho `S17` (nickname hết quota 24 giờ) chưa tồn tại** ở bất kỳ US nào. Tài liệu chỉ mô tả state, chưa đặt chuỗi hiển thị — cố tình không bịa. **Cần UX Writer bổ sung.**
3. **SmartTV chưa có trong `UX_FIGMA_WIREFRAMES.md`.** File đó tự khai báo phạm vi là *P0 Mobile v1*, nên không tự thêm mục TV vào. IA đã có sẵn Screen ID (`C17`, `S13`) để dựng khi Design mở đợt TV. **Cần Design quyết thời điểm mở đợt.**

Ngoài ra, một điểm nhỏ đáng cân nhắc: `SOLUTION_ARCHITECTURE.md` phần mô tả AI Adapter nêu đúng invariant nickname nhưng chưa nhắc "cho thử lại / không tiêu quota / không queue". Không sai, chỉ là chưa đầy đủ bằng US11 — có thể bổ sung ở lần cập nhật kiến trúc tới.
