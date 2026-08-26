# CHANGELOG rà soát V4 — Chuẩn hóa phạm vi theo nền tảng (Phone / Web / Smart TV / CMS)

**Ngày:** 26/08/2026 · **Phạm vi:** toàn bộ backlog (5 Epic / 20 User Story), tài liệu UX, kiến trúc và yêu cầu chéo A11y. **Chưa chạm** bộ tài liệu URD/SRS.

> **Quan hệ với [CHANGELOG_RASOAT_V3.md](CHANGELOG_RASOAT_V3.md):** V3 chuẩn hóa *phạm vi bình luận* về cấp phim và vẫn có hiệu lực nguyên vẹn. V4 chuẩn hóa một trục khác — *phạm vi theo nền tảng* — nên không thay thế quyết định nào của V3. Chỗ duy nhất V4 đảo ngược tài liệu cũ là mô hình Smart TV, được liệt kê đầy đủ tại mục 5.

---

## 1. Ma trận nền tảng đã chốt

| Nền tảng | User Story áp dụng |
|---|---|
| **Phone** (iOS/Android) | US01, US02, US03, US04, US05, US06, US07, US08, US09, US10, US17, US18 |
| **Web** (MyTV Web) | US01, US02, US03, US04, US05, US06, US07, US08, US09, US10, US17, US18 |
| **Smart TV / STB** | **US01, US07, US10, US17** |
| **CMS Web/Desktop (quản trị)** | US11, US12, US13, US14, US15, US16, US19, US20 |

Ma trận này được ghi thành nguồn chuẩn tại [README.md mục 4.1](README.md), và được dẫn chiếu lại từ US01, IA screen map, UX_USER_FLOWS, SOLUTION_ARCHITECTURE và REQUIREMENTS_A11Y_SECURITY.

---

## 2. Quyết định mới

| Mã | Quyết định | Ảnh hưởng |
|---|---|---|
| **QĐ-A4** | **Smart TV chỉ áp dụng US01, US07, US10, US17.** TV đọc bình luận (gồm trang thread chỉ đọc), Thích/Bỏ thích, Báo cáo bình luận và hiển thị huy hiệu. | Đảo mô hình TV cũ ở 11 vị trí (mục 5) |
| **QĐ-B4** | **Danh sách trên TV kế thừa quy tắc render của US02 nhưng không có control sort.** Count trên tab, tối đa 3 pin trên cùng, thứ tự `Nổi bật`, lazy load 10 root/batch. | US02 AC14, US01 AC10 |
| **QĐ-C4** | **US03 không áp dụng trên TV.** Điểm trung bình và tổng lượt vẫn hiển thị ở khối thông tin phim nhưng **chỉ đọc**; TV không mở sheet chấm sao. | US03 AC12, IA `C08` |
| **QĐ-D4** | **US10 áp dụng trên TV với taxonomy rút gọn 5 reason**, ẩn `Vi phạm khác` vì reason đó bắt buộc nhập mô tả 1–500 ký tự và TV không nhập văn bản. Entry là menu action rút gọn chỉ gồm `Báo cáo`. | US10 AC12–AC14, IA `O03`/`O06`/`S11`/`S12` |
| **QĐ-E4** | **TV không áp dụng cơ chế Làm mờ (spoiler) của US04.** Mọi đoạn chữ hiển thị **nguyên văn**, không có dải mờ và không có thao tác hiện nội dung. | US01 AC13, US04 AC8, IA `O07` |
| **QĐ-F4** | **Mục thông báo của app TV hiển thị đầy đủ notification của account** (Reply/Mention, moderation/chế tài, kết quả Báo cáo, huy hiệu) và **bấm vào thì mở đúng comment** — tab Bình luận hoặc thread chỉ đọc `C17`, fallback theo Effective Visibility Resolver (US12). TV không có màn cấu hình Thông báo cộng đồng; switch nằm ở Phone/Web và có hiệu lực cấp account. | US01 AC14, US09 AC17, US10 AC14, US17 flow, IA `C10` |
| **QĐ-G4** | **TV không tạo Share nhưng mở được deep link** tới comment/thread, từ notification trong app hoặc từ link chia sẻ bên ngoài. | US18 AC18, IA `C16` |
| **QĐ-H4** | **Không có reaction âm trên bất kỳ nền tảng nào.** Bỏ khái niệm nút `Dislike` trên TV; TV dùng đúng một nút Like dạng bật/tắt. | US07 flow |
| **QĐ-I4** | **Hệ thống không lưu nền tảng nguồn** của bình luận, lượt thích và báo cáo. CMS (US13/US14) và dashboard (US19) không phân biệt bản ghi đến từ Phone, Web hay Smart TV. | README 4.1, SOLUTION_ARCHITECTURE 2.2 |
| **QĐ-J4** | **US11, US12, US16 thuộc nhóm CMS/quản trị.** Thao tác là của Admin; hệ quả do backend áp dụng và được hiển thị bằng các state đã đặc tả sẵn trên app, không phát sinh chức năng mới cho FE ứng dụng. | Nhãn nền tảng của US11, US12, US16 |

---

## 3. Hành vi Smart TV: trước → sau

| Hành vi trên TV | Trước (tài liệu cũ) | Sau (V4) |
|---|---|---|
| Đổi cách sắp xếp | Có dropdown, đổi được bằng remote | **Không có control sort**; cố định `Nổi bật` |
| Đánh giá phim | Chấm 1–5 sao bằng remote | **Chỉ đọc** điểm trung bình + tổng lượt |
| Báo cáo bình luận | **Không có Report**, phải dùng Phone/Web | **Có Báo cáo**, 5 reason, ẩn `Vi phạm khác` |
| Đoạn Làm mờ (spoiler) | Bấm để hiện nội dung | Hiển thị **nguyên văn**, không có dải mờ |
| Mốc thời gian | Bấm để seek/phát | Chữ thường, **không bấm được** |
| Trang thread chỉ đọc `C17` | Thuộc US08 | Thuộc **US01** (US08 không áp dụng TV) |
| Mention | "Hiển thị mention" | `@nickname` chỉ là chữ trong nội dung, không phải mention tương tác |
| Thông báo | Không nói tới | Hiển thị **đủ** noti của account, bấm mở đúng comment |
| Link chia sẻ | Không nói tới | **Mở được** deep link, nhưng không tạo Share |
| Nút Dislike | "Dislike = Unlike" | **Bỏ hẳn**, chỉ một nút Like toggle |
| Danh sách bình luận | Ngầm hiểu theo US02 | Ghi rõ kế thừa quy tắc render US02, không có control sort |

---

## 4. Chi tiết thay đổi theo tệp

Tổng: **30 tệp**, 91 lần thay thế nội dung, +143 / −62 dòng. Không thêm hoặc đổi liên kết markdown nào.

### 4.1. EP01 — Trải nghiệm bình luận và đánh giá

| Tệp | Thay đổi |
|---|---|
| [US01_DOC_KHU_VUC_BINH_LUAN.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US01_DOC_KHU_VUC_BINH_LUAN.md) | **+6 AC mới (AC9–AC14):** AC9 phạm vi nền tảng · AC10 danh sách TV kế thừa quy tắc US02, không control sort · AC11 reply đọc ở thread chỉ đọc `C17`, thuộc US01 · AC12 rating chỉ đọc trên TV · AC13 TV không áp dụng spoiler, timestamp là chữ thường · AC14 thông báo trên TV (đủ loại, bấm mở comment, không có màn cấu hình, noti huy hiệu không có CTA). **+2 quy tắc nghiệp vụ:** ma trận nền tảng; nguyên tắc "không áp dụng US" chỉ bỏ *thao tác*, không đổi dữ liệu/quy tắc backend. **+4 test case:** `TC-US01-010` scope TV · `TC-US01-011` thread TV · `TC-US01-012` interaction TV · `TC-US01-013` spoiler TV |
| [US01_USER_FLOW.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US01_USER_FLOW.md) | Platforms → `Phone, Web, Smart TV`. Thay 1 bullet cũ ("TV hỗ trợ Like, Rating, Sort, Timestamp") bằng **3 bullet**: phạm vi 4 US, kế thừa render US02, không áp dụng Làm mờ |
| [US02_XEM_BINH_LUAN_SO_LUONG_VA_SAP_XEP.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US02_XEM_BINH_LUAN_SO_LUONG_VA_SAP_XEP.md) | **AC14 viết lại**: từ "TV đọc, đổi sort và lazy load bằng remote" → "US02 không áp dụng trên Smart TV", nêu rõ phần kế thừa render. **`TC-US02-021` viết lại**: kỳ vọng đổi từ "đổi sort được" thành "**không có** control sort, count/pin/lazy load vẫn đúng" |
| [US02_USER_FLOW.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US02_USER_FLOW.md) | Platforms → `Phone, Web. Smart TV không áp dụng US02.` Bullet "TV vẫn được đổi sort" → "TV không đổi sort" |
| [US03_DANH_GIA_PHIM.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US03_DANH_GIA_PHIM.md) | **AC12 viết lại**: từ "TV chấm sao bằng remote" → "US03 không áp dụng trên TV, chỉ hiển thị điểm chỉ đọc". **`TC-US03-008` viết lại**: kỳ vọng đổi thành không mở được sheet, API không nhận rating từ client TV |
| [US03_USER_FLOW.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US03_USER_FLOW.md) | Platforms + bullet: TV không đánh giá, chỉ hiển thị điểm chỉ đọc |
| [US04_DANG_BINH_LUAN.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US04_DANG_BINH_LUAN.md) | **AC8** thêm câu: cơ chế Làm mờ chỉ áp dụng Phone/Web, TV hiển thị nguyên văn (dẫn chiếu US01 AC13) |
| [US04_USER_FLOW.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US04_USER_FLOW.md) | Platforms → `Smart TV không áp dụng US04`. **+1 bullet** về spoiler hiển thị nguyên văn trên TV |
| [US05_USER_FLOW.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US05_USER_FLOW.md) | Platforms → `Phone, Web. Smart TV không áp dụng US05.` |
| [US06_USER_FLOW.md](EP01_TRAI_NGHIEM_BINH_LUAN_VA_DANH_GIA/US06_USER_FLOW.md) | Platforms → `Smart TV không áp dụng US06`. Bullet "TV bấm timestamp để seek" → "TV không seek, mốc thời gian là chữ thường" |

### 4.2. EP02 — Tương tác cộng đồng

| Tệp | Thay đổi |
|---|---|
| [US07_USER_FLOW.md](EP02_TUONG_TAC_CONG_DONG/US07_USER_FLOW.md) | Platforms → `Phone, Web, Smart TV`. **Bỏ khái niệm `Dislike`**: bullet cũ "Dislike trên SmartTV chỉ có nghĩa Unlike" → "không có reaction âm trên bất kỳ nền tảng nào, TV dùng đúng một nút Like toggle". Bullet TV nói rõ US07 áp dụng đầy đủ |
| [US08_USER_FLOW.md](EP02_TUONG_TAC_CONG_DONG/US08_USER_FLOW.md) | Platforms → `Smart TV không áp dụng US08; đọc thread chỉ đọc trên TV thuộc US01 (AC11)`. Nhãn nhánh mermaid và bullet cuối cập nhật theo |
| [US09_MENTION_VA_NHAN_THONG_BAO.md](EP02_TUONG_TAC_CONG_DONG/US09_MENTION_VA_NHAN_THONG_BAO.md) | **+AC17**: TV không tạo Mention và không có màn cấu hình, nhưng **quy tắc hiển thị + điều hướng notification (AC10–AC13) vẫn áp dụng** cho mục thông báo của app TV. **+`TC-US09-017`**: kiểm 5 loại noti trên TV, điều hướng root → tab Bình luận, reply → `C17`, target chết → fallback US12, noti huy hiệu không có CTA |
| [US09_USER_FLOW.md](EP02_TUONG_TAC_CONG_DONG/US09_USER_FLOW.md) | Platforms ghi rõ phần áp dụng/không áp dụng. Bullet cũ về `@nickname` tách thành **2 bullet**: không tạo Mention + mục thông báo TV hiển thị đủ và điều hướng được |

### 4.3. EP03 — An toàn và kiểm duyệt

| Tệp | Thay đổi |
|---|---|
| [US10_REPORT_BINH_LUAN_VI_PHAM.md](EP03_AN_TOAN_VA_KIEM_DUYET/US10_REPORT_BINH_LUAN_VI_PHAM.md) | **+3 AC:** AC12 taxonomy rút gọn 5 reason trên TV, ẩn `Vi phạm khác` · AC13 entry là menu action rút gọn, các quy tắc cooldown/rate-limit/self-report/guest giữ nguyên · AC14 thông báo kết quả vào mục thông báo TV, bấm mở đúng comment. **+2 quy tắc nghiệp vụ:** taxonomy rút gọn không đổi taxonomy chung (report từ TV không bao giờ có reason `Vi phạm khác`); cooldown và rate limit tính **theo account**, dùng chung quota giữa các thiết bị. **+1 dòng microcopy** cho nhãn 5 lựa chọn trên TV. **+3 test case:** `TC-US10-011` taxonomy TV · `TC-US10-012` cooldown/rate-limit dùng chung quota Phone↔TV · `TC-US10-013` notification kết quả trên TV |
| [US10_USER_FLOW.md](EP03_AN_TOAN_VA_KIEM_DUYET/US10_USER_FLOW.md) | Platforms → `Phone, Web, Smart TV (taxonomy rút gọn 5 reason)`, đảo ngược dòng "SmartTV không Report". **Mermaid thêm nhánh Platform**: TV → 5 reason rồi submit thẳng, Phone/Web giữ nhánh 6 reason + mô tả. **+2 bullet** UX đã chốt |
| [US11_USER_FLOW.md](EP03_AN_TOAN_VA_KIEM_DUYET/US11_USER_FLOW.md) | **Bổ sung nhãn nền tảng** (trước đây thiếu hẳn): `CMS Web/Desktop only`, kèm câu phân loại AI do backend xử lý, app không phát sinh chức năng mới |
| [US12_USER_FLOW.md](EP03_AN_TOAN_VA_KIEM_DUYET/US12_USER_FLOW.md) | **Bổ sung nhãn nền tảng** (trước đây thiếu hẳn): `CMS Web/Desktop only`, kèm câu Effective Visibility Resolver do backend áp dụng cho mọi nền tảng |

### 4.4. EP04 — CMS quản trị

| Tệp | Thay đổi |
|---|---|
| [US13_USER_FLOW.md](EP04_CMS_QUAN_TRI_BINH_LUAN/US13_USER_FLOW.md) · [US14](EP04_CMS_QUAN_TRI_BINH_LUAN/US14_USER_FLOW.md) · [US15](EP04_CMS_QUAN_TRI_BINH_LUAN/US15_USER_FLOW.md) | Chuẩn hóa nhãn: `Platform: Web/Desktop only` → `Platform: CMS Web/Desktop only` |
| [US16_USER_FLOW.md](EP04_CMS_QUAN_TRI_BINH_LUAN/US16_USER_FLOW.md) | Chuẩn hóa nhãn: `CMS: Web/Desktop only` → `Platform: CMS Web/Desktop only`, kèm câu Account Lock do backend áp dụng trên mọi nền tảng gồm Smart TV |

### 4.5. EP05 — Tăng trưởng và phân tích

| Tệp | Thay đổi |
|---|---|
| [US17_USER_FLOW.md](EP05_TANG_TRUONG_VA_PHAN_TICH/US17_USER_FLOW.md) | **Bổ sung nhãn nền tảng** (trước đây thiếu hẳn): `Phone, Web, Smart TV (TV chỉ hiển thị icon + tên)`. Bullet TV thêm: noti cấp huy hiệu vào mục thông báo TV, hiển thị dạng đọc, **không có CTA `Xem huy hiệu`** vì TV không có màn chi tiết huy hiệu |
| [US18_CHIA_SE_BINH_LUAN.md](EP05_TANG_TRUONG_VA_PHAN_TICH/US18_CHIA_SE_BINH_LUAN.md) | **+AC18**: TV không tạo Share nhưng mở được link chia sẻ tới comment/thread; gate và fallback theo US12; lượt mở link từ TV vẫn ghi nhận cho US19 |
| [US18_USER_FLOW.md](EP05_TANG_TRUONG_VA_PHAN_TICH/US18_USER_FLOW.md) | Platforms và bullet cập nhật theo AC18 |

### 4.6. Tài liệu nền

| Tệp | Thay đổi |
|---|---|
| [README.md](README.md) | **Mục 4.1 mới — Ma trận nền tảng**: bảng 4 nền tảng + 6 quy tắc đọc ma trận (Phone≡Web; phạm vi TV; kế thừa render US02; vì sao US11/12/16 ở nhóm CMS; thông báo và deep link trên TV; **không lưu nền tảng nguồn** — ghi rõ là quyết định đã chốt, không phải thiếu sót đặc tả) |
| [UX_USER_FLOWS.md](UX_USER_FLOWS.md) | Nguyên tắc 6 viết lại theo mô hình TV mới. **+Nguyên tắc 10**: ma trận nền tảng |
| [UX_INFORMATION_ARCHITECTURE_SCREEN_MAP.md](UX_INFORMATION_ARCHITECTURE_SCREEN_MAP.md) | **14 dòng bảng + 1 ghi chú + mục 21 viết lại + 2 chỗ khác** — chi tiết ở mục 4.7 |
| [REQUIREMENTS_A11Y_SECURITY.md](REQUIREMENTS_A11Y_SECURITY.md) | **Mục A.3 mới — Smart TV / 10-foot UI** (trước đây file này không có một dòng nào về remote): 9 yêu cầu gồm không phụ thuộc hover/touch, focus order tuyến tính, focus indicator ≥3:1 và không chỉ dùng màu, tiêu chí thay cho touch target 44×44pt, đọc ở khoảng cách xa, announce khi lazy load, accessible name cho Like/Báo cáo/huy hiệu, **không có yêu cầu nhập văn bản trên TV**, spoiler không áp dụng nên không cần vùng focusable "Hiện nội dung có tiết lộ". A.1 đổi "web + mobile" → "web + mobile + Smart TV". Phần C thêm dòng: A.3 áp dụng cho phần TV của US01, US07, US10, US17 |
| [SOLUTION_ARCHITECTURE.md](SOLUTION_ARCHITECTURE.md) | **Thêm client `MyTV Smart TV / STB`** vào sơ đồ kiến trúc mục 4 (trước đây chỉ có Web, Mobile, CMS). Mục 2.2 thêm 1 gạch đầu dòng phạm vi theo nền tảng: TV dùng chung API đọc và endpoint Like/Report, **không có endpoint riêng**, và không lưu nền tảng nguồn |

### 4.7. Chi tiết IA screen map

| Đối tượng | Trước | Sau |
|---|---|---|
| `C01` Content Detail | US01, US06, US18 | thêm `(TV: chỉ US01)` |
| `C02` Comment Area | `US01–US08` | `US01–US08 (TV: US01, US07, US10, US17)`; exit thêm `O03 bản rút gọn` |
| `C08` Rating sheet | `Phone, Web, SmartTV` | `Phone, Web (TV chỉ hiển thị điểm chỉ đọc, không mở sheet)` |
| `C10` Notification Center | `Phone, Web` | thêm mục thông báo app TV hiển thị đủ noti; exit trên TV → `C02`/`C17` |
| `C16` Share Deep-link Landing | `Phone, Web` | thêm `Smart TV (TV chỉ mở link, không tạo Share)` |
| `C17` Thread TV read-only | `US01, US08` | `US01` (Like/Báo cáo/huy hiệu theo US07, US10, US17) |
| Ghi chú "TV không có destination tạo nội dung" | liệt kê `O03–O06` và `C16` | bỏ `C16`, thêm `C14`, `C15`; nêu rõ **`O03` có bản rút gọn** và **`O06` có bản 10-foot** |
| `O01` Auth Gate | `TV: Like/Rating` | `TV: Like/Báo cáo` |
| `O02` Sort selector | `Phone, Web, SmartTV (remote)` | `Phone, Web (không render trên TV)` |
| `O03` Comment action menu | `Phone, Web` | thêm `Smart TV (bản rút gọn chỉ có Báo cáo)`; US `(TV: chỉ US10)` |
| `O06` Report sheet | `Phone, Web` | thêm `Smart TV (10-foot, 5 reason, ẩn Vi phạm khác)` |
| `O07` Spoiler reveal | `Phone, Web, SmartTV` | `Phone, Web (TV không áp dụng: nội dung hiển thị nguyên văn)` |
| `S01` Loading | trigger "mở tab / đổi sort" | thêm `(TV: chỉ mở tab)` |
| `S05` Comment Area closed | — | thêm ghi chú trên TV rating là chỉ đọc |
| `S10` Timestamp unavailable | `Phone, Web, SmartTV` | `Phone, Web (TV không áp dụng US06)` |
| `S11`/`S12` Report cooldown & rate limit | `Phone, Web` | thêm `Smart TV`, ghi rõ tính **theo account** |
| `S13` TV không hỗ trợ tạo nội dung | trigger có Report; giữ "đọc/Like/Rating/Sort/Spoiler/Timestamp" | trigger bỏ Report, thêm đổi sort/chấm sao/mốc thời gian; giữ "đọc (gồm thread chỉ đọc), Like/Unlike, Báo cáo, huy hiệu"; US liên quan cập nhật |
| Mục 21 — SmartTV / 10-foot UI | 2 bullet mô tả mô hình cũ | **7 bullet mới**: ma trận, danh sách hỗ trợ, danh sách không hỗ trợ, `O03`/`O06` bản TV, kế thừa render US02, rating chỉ đọc + spoiler nguyên văn, thông báo và deep link. 3 bullet còn lại (thread, badge, D-pad) cập nhật theo |
| Mục P0 scope | TV chỉ có `C02`, `C17`, `S13` | thêm `O03` bản rút gọn và `O06` Report 10-foot |
| Handoff checklist + ví dụ | `Platform: Phone / Web / SmartTV`; ví dụ `C17 · US08` | thêm `CMS`; ví dụ đổi thành `C17 · US01` |

---

## 5. Mâu thuẫn phát hiện trong rà soát và cách xử lý

### 5.1. Mâu thuẫn trực tiếp với ma trận mới — 11 vị trí, đã sửa hết

| # | Vị trí | Vấn đề | Cách sửa |
|---|---|---|---|
| 1 | US02 AC14 + `TC-US02-021` + flow | TV đổi sort và lazy load bằng remote | QĐ-B4 |
| 2 | US03 AC12 + `TC-US03-008` + flow | TV chấm sao 1–5 bằng remote | QĐ-C4 |
| 3 | US06_USER_FLOW | TV bấm timestamp để seek | Ghi rõ không áp dụng |
| 4 | US08_USER_FLOW + IA `C17` | Màn thread read-only trên TV gắn US08 | Chuyển sở hữu sang US01 AC11 |
| 5 | US09_USER_FLOW | "TV hiển thị mention" | Làm rõ `@nickname` chỉ là chữ trong nội dung |
| 6 | US10_USER_FLOW | **"SmartTV không Report"** — ngược hẳn ma trận | QĐ-D4 |
| 7 | US01_USER_FLOW | TV hỗ trợ Like, **Rating, Sort, Timestamp** | Viết lại thành 3 bullet đúng phạm vi |
| 8 | IA mục 21 + `S13` | TV "không Report", giữ Rating/Sort/Spoiler/Timestamp | Viết lại toàn mục |
| 9 | IA `O01`/`O02`/`O07`/`C08`/`C02`/`S01`/`S10` | Còn gắn Smart TV cho sort/rating/spoiler/timestamp | Sửa từng dòng |
| 10 | IA `S11`/`S12` + `O03`/`O06` + ghi chú dòng 649 | Report sheet, cooldown, rate-limit **không** render trên TV → TV không có đường nào bấm Báo cáo | Mở `O03` bản rút gọn + `O06` bản 10-foot; `S11`/`S12` thêm TV |
| 11 | UX_USER_FLOWS nguyên tắc 6 | TV hỗ trợ Rating, Sort, Spoiler, Timestamp | Viết lại + thêm nguyên tắc 10 |

### 5.2. Mâu thuẫn về nhãn nền tảng — đã chuẩn hóa

| # | Vấn đề | Cách sửa |
|---|---|---|
| 12 | US11, US12, US17 **thiếu hẳn** dòng Platform | Bổ sung cả 3 |
| 13 | Nhãn không đồng nhất: US13–15 `Web/Desktop only`, US19–20 `CMS Web/Desktop only`, US16 dùng label `CMS:` | Đưa hết về `Platform: CMS Web/Desktop only` |

### 5.3. Khoảng trống nghiệp vụ phát sinh từ ma trận mới — đã lấp

| # | Vấn đề | Cách sửa |
|---|---|---|
| 14 | US01 AC2 nói người xem đọc được "toàn bộ bình luận **và reply**", nhưng US08 không áp dụng TV → reply không có đường đọc | Giữ màn `C17` và ghi thành US01 AC11 |
| 15 | Reason `Vi phạm khác` bắt buộc nhập mô tả 1–500 ký tự, mâu thuẫn với nguyên tắc TV không nhập văn bản | QĐ-D4: ẩn reason đó trên TV; ghi cả vào A11y A.3 |
| 16 | US10 AC9 yêu cầu reporter nhận in-app notification, nhưng `C10` Notification Center thuộc US09 — không áp dụng TV | QĐ-F4 |
| 17 | Notification cấp huy hiệu có CTA `Xem huy hiệu` nhưng `C15` badge detail không có trên TV | Ghi rõ noti huy hiệu trên TV không có CTA |
| 18 | Link chia sẻ mở trên app TV chưa được định nghĩa (`C16` chỉ Phone/Web) | QĐ-G4 |
| 19 | Sơ đồ kiến trúc không có client Smart TV | Thêm node và dòng phạm vi ở mục 2.2 |
| 20 | REQUIREMENTS_A11Y_SECURITY không có yêu cầu nào cho remote/D-pad dù IA đòi focus order tuyến tính trên TV | Thêm mục A.3 |

### 5.4. Đã kiểm tra và **không** phải mâu thuẫn

| Vị trí | Kết luận |
|---|---|
| `S07` Comment Lock interaction blocked chỉ `Phone, Web` | Đúng. Theo `TC-US16-005`, Khóa bình luận **không** chặn Like và Report — hai thứ duy nhất TV làm được — nên TV không cần state này |
| `S08` Account Lock full-screen có Smart TV | Đúng. Account Lock do backend áp dụng mọi nền tảng; là state hiển thị, không phải tính năng UI của US16 |
| `C05` Focused Thread ghi `Phone, Web (TV dùng C17)` | Đúng, khớp với QĐ-F4 và QĐ-G4 |
| Phone và Web | Trùng khớp 100% với ma trận, **không có mâu thuẫn nào** ở hai nền tảng này |

---

## 6. Test case mới và test case sửa

| Loại | ID | Nội dung |
|---|---|---|
| Mới | `TC-US01-010` | Scope TV: count trên tab, 3 pin trên cùng, 10 root + lazy load, **không** có control sort / ô nhập / action Trả lời-Sửa-Xóa-Chia sẻ |
| Mới | `TC-US01-011` | Thread TV: mở `C17`, đọc đủ reply công khai, không có ô trả lời |
| Mới | `TC-US01-012` | Interaction TV: Thích / Báo cáo / huy hiệu hoạt động; không có chấm sao, không có control sort, timestamp không bấm được |
| Mới | `TC-US01-013` | Spoiler TV: cùng một comment hiển thị nguyên văn trên TV nhưng vẫn làm mờ đúng 2 đoạn trên Phone |
| Mới | `TC-US09-017` | Notification TV: đủ 5 loại noti; root → tab Bình luận, reply → `C17`, target chết → fallback US12; noti huy hiệu không có CTA; không có màn cấu hình |
| Mới | `TC-US10-011` | Taxonomy TV: menu action chỉ có `Báo cáo`; form đúng 5 reason, không có `Khác`, không có ô mô tả |
| Mới | `TC-US10-012` | Cooldown 24h và rate limit 10/giờ tính theo account, dùng chung quota Phone ↔ TV |
| Mới | `TC-US10-013` | Notification kết quả Report trên TV, không tiết lộ chế tài |
| Sửa | `TC-US02-021` | Kỳ vọng đảo chiều: từ "đổi sort được bằng remote" → "**không có** control sort" |
| Sửa | `TC-US03-008` | Kỳ vọng đảo chiều: từ "submit/update rating hoạt động như Phone/Web" → "không mở được sheet, API không nhận rating từ client TV" |

---

## 7. Điểm còn treo — chưa làm theo yêu cầu

| # | Hạng mục | Trạng thái |
|---|---|---|
| 1 | **Lộ trình triển khai app Smart TV** | 4 US của TV đang nằm rải ở 3 giai đoạn trong [SOLUTION_ARCHITECTURE mục 7.2](SOLUTION_ARCHITECTURE.md): US01 ở GĐ1, US07 và US10 ở GĐ2, US17 ở GĐ3. PO chưa chốt; V4 **không sửa** bảng giai đoạn |
| 2 | **URD/SRS + hai tệp `.docx`** | Vẫn còn mô hình TV cũ: `SRS_content.json` và `URD_content.json` ghi "Smart TV cho đọc, Thích, **Đánh giá, đổi cách sắp xếp, hiện đoạn Làm mờ, nhảy tới mốc thời gian**" và "Smart TV không **Báo cáo**"; `TAI_LIEU/README.md` dòng 59 cũng vậy. Cần cập nhật JSON rồi sinh lại docx và tăng phiên bản tài liệu |
| 3 | **Thiết kế Figma cho Smart TV** | Chưa có frame cho `O03` bản TV (menu chỉ `Báo cáo`) và `O06` Report 10-foot — hai màn mà IA V4 vừa yêu cầu |

---

## 8. Kiểm chứng đã chạy

| Hạng mục | Kết quả |
|---|---|
| Số lần thay thế nội dung | 91 lần, **0 lần thất bại** (mỗi lần đối sánh chuỗi nguyên văn và bắt buộc duy nhất trong tệp, tránh sửa nhầm dòng trùng) |
| Rà lại dấu vết mô hình TV cũ | `grep` toàn repo cho `SmartTV` / `Smart TV` kết hợp các từ khóa `rating`, `sort`, `sắp xếp`, `timestamp`, `mốc thời gian`, `spoiler`, `làm mờ`, `không Report`, `đánh giá` — mọi kết quả còn lại đều là **câu mới đúng theo V4** |
| Kiểm tra tự động sau khi sửa | 6 nhóm kiểm tra: đủ nhãn nền tảng ở cả 20 user flow · 11 mẫu tuyên bố TV cũ không còn xuất hiện · số thứ tự AC liên tục ở 6 spec đã sửa · số cột bảng markdown đồng nhất · fence mermaid đóng đủ · ma trận 4 US của Smart TV khớp giữa README, IA, UX_USER_FLOWS và US01. **Kết quả: pass** |
| Liên kết markdown | Không thêm hoặc đổi liên kết nào trong đợt này |
| Tính nhất quán chéo sau khi sửa | Đối chiếu lại phạm vi TV giữa README 4.1 ↔ US01 AC9–AC14 ↔ IA mục 21 ↔ UX_USER_FLOWS nguyên tắc 6 và 10 ↔ SOLUTION_ARCHITECTURE 2.2 ↔ A11y A.3: khớp nhau |
