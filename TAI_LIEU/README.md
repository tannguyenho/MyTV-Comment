# Tài liệu URD và SRS — Tính năng Bình luận MyTV

## Sản phẩm

| Tệp | Nội dung |
|---|---|
| `03_BM03_URD_MyTV_Comment.docx` | Đặc tả yêu cầu người sử dụng (BM03_URD), phiên bản 1.1 — 6 chương, 20 yêu cầu chức năng UR01–UR20, 64 yêu cầu phi chức năng, 22 ảnh Figma |
| `04_BM04_SRS_MyTV_Comment.docx` | Đặc tả yêu cầu phần mềm (BM04_SRS), phiên bản 1.1 — 5 phân hệ, 8 module, 14 chức năng, 34 bảng tình huống sử dụng, 27 ảnh Figma |

Mở bằng Word rồi nhấn **Ctrl+A → F9** để cập nhật số trang trong mục lục.

## Nguồn để chỉnh sửa

Hai tệp `.docx` được **sinh ra** từ hai tệp JSON dưới đây, không sửa trực tiếp trong Word
nếu muốn giữ khả năng tái tạo:

| Tệp nguồn | Sinh ra |
|---|---|
| `URD_content.json` | `03_BM03_URD_MyTV_Comment.docx` |
| `SRS_content.json` | `04_BM04_SRS_MyTV_Comment.docx` |

Lệnh sinh lại:

```bash
node .claude/skills/urd-docx/scripts/build-docx.js \
     TAI_LIEU/URD_content.json \
     .claude/skills/urd-docx/assets/BM03_URD_template.docx \
     TAI_LIEU/03_BM03_URD_MyTV_Comment.docx

node .claude/skills/srs-docx/scripts/build-docx.js \
     TAI_LIEU/SRS_content.json \
     .claude/skills/srs-docx/assets/BM04_SRS_template.docx \
     TAI_LIEU/04_BM04_SRS_MyTV_Comment.docx
```

Kiểm tra sau khi sinh:

```bash
node .claude/skills/urd-docx/scripts/inspect-docx.js <file.docx> --check   # zip + XML hợp lệ
node .claude/skills/urd-docx/scripts/inspect-docx.js <file.docx>           # in lại cấu trúc
```

## Ảnh thiết kế

Ảnh trong `assets/` được trích xuất từ Figma, file **[Phone] Play Nội dung**, canvas
**T8 Bình luận** (`node-id=39753-12055`).

| Thư mục | Nội dung |
|---|---|
| `assets/flow/` | 11 lưu đồ theo User Story (US01–US10, US17), đã tự cắt bỏ viền nền thừa |
| `assets/screen/` | 45 ảnh màn hình 375×812 xuất ở tỉ lệ 2× |

## Trạng thái thiết kế theo nền tảng

| Nền tảng | Trạng thái | Ghi chú |
|---|---|---|
| Phone (iOS, Android) | Đã hoàn thiện | Đã đưa vào cả hai tài liệu |
| Website | Chờ hoàn thiện | Bổ sung vào các mục "Yêu cầu giao diện" tương ứng khi có |
| Smart TV / STB | Chờ hoàn thiện | Phạm vi rút gọn: chỉ đọc, Thích, Đánh giá, Sắp xếp, hiện đoạn Làm mờ, nhảy mốc thời gian |
| CMS (Web/Desktop) | Chờ hoàn thiện | Ảnh hưởng mục "Yêu cầu giao diện" của phân hệ CMS và Tăng trưởng |

Cả hai tài liệu đã ghi rõ trạng thái này (URD: ghi chú tại Chương III và IV; SRS: Phụ lục B).
Khi bổ sung thiết kế của một nền tảng, cần thêm một dòng vào `history` trong tệp JSON
tương ứng và tăng số phiên bản trước khi sinh lại.

## Phạm vi bình luận

Bình luận và đánh giá đều ở **cấp phim**: mỗi bộ phim, dù là phim lẻ hay phim bộ, có duy nhất một khu vực bình luận và một điểm đánh giá dùng chung cho mọi tập. Cấu hình kiểm duyệt trên CMS cũng ở cấp phim (override cấp phim → mặc định hệ thống). Mốc thời gian (US06) chỉ áp dụng cho phim lẻ.

## Điểm cần các bên chốt

Hai chỗ trong tài liệu để dấu `<...>` vì chưa có số liệu chính thức:

- **UR_NF33 / SRS_NF33** — số người dùng đồng thời mục tiêu cho giai đoạn thí điểm (cần Ban sản phẩm).
- **UR_NF48 / SRS_NF48** — danh sách thiết bị và phiên bản tối thiểu để kiểm thử (cần đội kỹ thuật).
