# CHANGELOG rà soát V3 — Chuẩn hóa phạm vi bình luận về cấp phim

**Ngày:** 25/08/2026 · **Phạm vi:** toàn bộ backlog (5 Epic / 20 User Story), tài liệu UX, kiến trúc và bộ tài liệu URD/SRS.

> **Quan hệ với [CHANGELOG_RASOAT_V2.md](CHANGELOG_RASOAT_V2.md):** V2 là hồ sơ của một vòng rà soát đã diễn ra và được giữ nguyên. Quyết định **QĐ-A** của V2 (*phim bộ bình luận và đánh giá theo từng tập*) **đã bị thay thế** bởi QĐ-A3 dưới đây. Khi hai tài liệu mâu thuẫn, V3 là bản có hiệu lực.

---

## 1. Quyết định mới

| Mã | Quyết định | Thay thế cho |
|---|---|---|
| **QĐ-A3** | **Bình luận ở cấp phim.** Mỗi bộ phim — phim lẻ hay phim bộ — có duy nhất một khu vực bình luận dùng chung cho mọi tập. | QĐ-A của V2 |
| **QĐ-B3** | **Đánh giá cũng ở cấp phim.** Một account có tối đa một rating hiện hành trên mỗi bộ phim; đổi tập không đổi rating. | — |
| **QĐ-C3** | **CMS cấu hình ở cấp phim.** Chế độ kiểm duyệt, ngưỡng AI và trạng thái Đóng bình luận kế thừa theo thứ tự **override cấp phim → default hệ thống**. | Inheritance 3 cấp của V2 |
| **QĐ-D3** | **US06 mốc thời gian chỉ áp dụng cho phim lẻ.** Phim bộ không có mốc bấm được và API không nhận trường timestamp. | — |
| **QĐ-E3** | **Mốc neo “sau X giờ”:** phim lẻ giữ đủ 3 loại (giờ phát hành MyTV / giờ phát sóng thực tế / mốc thủ công); **phim bộ chỉ còn 2 loại** (giờ phát hành MyTV / mốc thủ công). | — |

### Lý do QĐ-D3 và QĐ-E3

Hai quyết định này là hệ quả bắt buộc của QĐ-A3, không phải lựa chọn độc lập:

- **QĐ-D3:** khi bình luận nằm ở cấp phim, một chuỗi `24:14` trong bình luận của phim bộ không xác định được thuộc tập nào. Giữ tính năng mà không có mã tập sẽ tạo hành vi mơ hồ cho người đọc đang ở tập khác.
- **QĐ-E3:** cấu hình ở cấp phim trong khi mỗi tập có giờ phát sóng riêng, nên mốc “giờ phát sóng thực tế” không phân giải được ở cấp phim đối với phim bộ.

---

## 2. Hệ quả hành vi cần chú ý khi implement

| Hành vi | Trước | Sau |
|---|---|---|
| Phim bộ đổi tập | Reload count/rating/Pin/list, sort reset về `Nổi bật` | **Giữ nguyên** toàn bộ, không phát sinh request load scope mới |
| Mở một bộ phim khác | — | Load dữ liệu của phim đó, sort reset về `Nổi bật` |
| Rating trên phim bộ | Mỗi tập một điểm | Một điểm cho cả bộ phim |
| Cấu hình AI/Đóng bình luận | 3 cấp kế thừa | 2 cấp: override cấp phim → default hệ thống |
| Mốc thời gian trên phim bộ | Có | **Không** — chuỗi thời gian hiển thị là text thường |

---

## 3. Đổi tên file

Filename được đưa về khớp nội dung; toàn bộ liên kết trong repo đã cập nhật (**đã kiểm tra 138 liên kết markdown, 0 liên kết gãy**).

| Tên cũ | Tên mới |
|---|---|
| `US02_XEM_BINH_LUAN_THEO_SERIES_TAP_SO_LUONG_VA_SAP_XEP.md` | [`US02_XEM_BINH_LUAN_SO_LUONG_VA_SAP_XEP.md`](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US02_XEM_BINH_LUAN_SO_LUONG_VA_SAP_XEP.md) |
| `US03_DANH_GIA_SERIES_VA_TAP_PHIM.md` | [`US03_DANH_GIA_PHIM.md`](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US03_DANH_GIA_PHIM.md) |
| `US06_BINH_LUAN_KEM_CANH_PHIM.md` | [`US06_BINH_LUAN_KEM_MOC_THOI_GIAN.md`](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US06_BINH_LUAN_KEM_MOC_THOI_GIAN.md) |
| `US15_QUAN_LY_BINH_LUAN_NOI_BAT_VA_CAU_HINH_THEO_PHIM.md` | [`US15_QUAN_LY_BINH_LUAN_GHIM_VA_CAU_HINH_THEO_PHIM.md`](EP04_CMS_QUAN_TRI_BINH_LUAN/US15_QUAN_LY_BINH_LUAN_GHIM_VA_CAU_HINH_THEO_PHIM.md) |
| `US18_CHIA_SE_BINH_LUAN_VA_CANH_PHIM.md` | [`US18_CHIA_SE_BINH_LUAN.md`](EP05_TANG_TRUONG_VA_PHAN_TICH/US18_CHIA_SE_BINH_LUAN.md) |

Cùng với đổi tên, các ghi chú *“filename giữ tên legacy”* đã được gỡ khỏi README gốc, US02, US03 và US02_USER_FLOW vì không còn đúng.

---

## 4. Tài liệu đã cập nhật

| Nhóm | Tệp |
|---|---|
| Backlog và quyết định | [README.md](README.md) |
| Kiến trúc | [SOLUTION_ARCHITECTURE.md](SOLUTION_ARCHITECTURE.md) |
| UX | [UX_USER_FLOWS.md](UX_USER_FLOWS.md), [UX_INFORMATION_ARCHITECTURE_SCREEN_MAP.md](UX_INFORMATION_ARCHITECTURE_SCREEN_MAP.md) |
| Epic README | EP01, EP04, EP05 |
| User Story | US01–US06, US09–US13, US15, US17–US20 |
| User Flow | US01, US02, US03, US05, US06, US09, US12, US13, US15, US18, US19, US20 |
| Tài liệu bàn giao | [TAI_LIEU/URD_content.json](TAI_LIEU/URD_content.json), [TAI_LIEU/SRS_content.json](TAI_LIEU/SRS_content.json) và hai tệp `.docx` sinh ra từ chúng (đều lên **phiên bản 1.1**) |

---

## 5. Lỗi và mâu thuẫn phát hiện trong rà soát, đã sửa

### 5.1. Mâu thuẫn nội tại

| # | Vị trí | Vấn đề | Cách sửa |
|---|---|---|---|
| 1 | `TC-US02-003` | Vẫn mô tả “đổi tập → reload + sort reset”, **trái AC2 của chính US02** | Viết lại thành chuyển giữa hai bộ phim M1 → M2; bổ sung `TC-US02-003a` kiểm chứng đổi tập **giữ nguyên** sort và danh sách |
| 2 | `TC-US11-006` | “E1 Mode1, E2 Mode2” — hai tập không thể khác chế độ khi cấu hình ở cấp phim | Đổi thành hai bộ phim M1/M2 có chế độ khác nhau |
| 3 | SRS | Thiếu hẳn ràng buộc “mốc thời gian chỉ phim lẻ” trong khi URD đã có → hai tài liệu lệch nhau | Bổ sung vào Bảng 2 (trường Mốc thời gian), ma trận truy vết UR06 và **yêu cầu phi chức năng mới SRS_NF45a** |

### 5.2. Sai lệch tiêu đề và trích dẫn

| # | Vị trí | Vấn đề | Cách sửa |
|---|---|---|---|
| 4 | US02 tiêu đề H1 | Không khớp tên trong bảng mục lục README | Thống nhất thành *“Xem bình luận, số lượng và sắp xếp”* |
| 5 | US06 tiêu đề H1 | Chưa nêu giới hạn phim lẻ | Đổi thành *“Bình luận kèm mốc thời gian (chỉ phim lẻ)”* |
| 6 | US06 mục *Phạm vi MVP* | Giới hạn phim lẻ chỉ nằm lẫn trong AC4 | Thêm gạch đầu dòng đầu tiên nêu rõ; tách AC4 thành AC4 (phạm vi) và AC5 (kiểm tra giá trị), đánh số lại AC5–AC10 thành AC6–AC11 |
| 7 | Screen map dòng 45 | Trích “US02 AC3” cho phát biểu thực ra thuộc AC2 | Sửa thành AC2 |
| 8 | `TC-US06-001/005`, `TC-US20-002`, `TC-US01`, `TC-US18` | Còn dùng định danh `E1/E2` (mã tập) làm mã nội dung | Đổi sang `M1/M2` (mã phim) |

### 5.3. Khoảng trống nghiệp vụ mới phát sinh

| # | Vấn đề | Cách sửa |
|---|---|---|
| 9 | Mốc neo “sau X giờ” không phân giải được với phim bộ | Áp QĐ-E3 vào US12 AC11, US15 AC4, `TC-US15-012` và README mục 5.8 |
| 10 | Không có test case xác minh phim bộ **không** có mốc thời gian | Bổ sung `TC-US06-001a` kiểm tra cả UI và API |

---

## 6. Kiểm chứng đã chạy

| Hạng mục | Kết quả |
|---|---|
| Liên kết markdown toàn repo | 138 liên kết, **0 gãy** |
| Dấu vết mô hình cấp tập trong tài liệu spec | **0** (các chỗ còn chữ “tập” đều là ngữ cảnh phát hợp lệ: tab `Danh sách tập`, Dịch vụ Nội dung, hoặc từ ghép như “tập trung”, “biên tập viên”) |
| Tham chiếu chéo AC (`USxx ACn`) | 13 tham chiếu, đích đến đều đúng nội dung được trích |
| Tính hợp lệ của `URD_content.json` / `SRS_content.json` | JSON hợp lệ |
| Hai tệp `.docx` sinh lại | zip hợp lệ, toàn bộ XML well-formed |

---

## 7. Điểm còn treo — không thuộc phạm vi rà soát này

Hai chỗ trong URD/SRS để dấu `<...>` vì chưa có số liệu chính thức, cần các bên cung cấp:

| Mã | Nội dung | Người chốt |
|---|---|---|
| `UR_NF33` / `SRS_NF33` | Số người dùng đồng thời mục tiêu cho giai đoạn thí điểm | Ban sản phẩm |
| `UR_NF48` / `SRS_NF48` | Danh sách thiết bị và phiên bản tối thiểu để kiểm thử | Đội kỹ thuật |

Các mục “cần chốt” trong [SOLUTION_ARCHITECTURE.md](SOLUTION_ARCHITECTURE.md) mục 9 là quyết định đầu tư và vận hành có từ trước, không phát sinh từ vòng rà soát này.

Ngoài ra, thiết kế giao diện cho **Website, Smart TV và CMS** vẫn đang chờ hoàn thiện. Hai tài liệu URD/SRS đã ghi rõ trạng thái này và chừa sẵn vị trí để bổ sung ảnh màn hình theo cùng chuẩn trình bày như bộ thiết kế Phone đã có.
