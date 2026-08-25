# User Flow — US15 Pin và cấu hình bình luận

> User Story: [US15_QUAN_LY_BINH_LUAN_GHIM_VA_CAU_HINH_THEO_PHIM.md](US15_QUAN_LY_BINH_LUAN_GHIM_VA_CAU_HINH_THEO_PHIM.md)

**Platform:** Web/Desktop only

```mermaid
flowchart TD
 A[Mở Content Operations của phim] --> B{Bình luận ghim / Cấu hình bình luận}
 B -->|Ghim| C[Chọn public comment]
 C --> D{Đã đủ 3 Pin?}
 D -->|Không| E[Pin + expiry tùy chọn]
 D -->|Có| F[Flow Thay thế bình luận ghim]
 F --> G[Admin chọn 1 Pin hiện tại để bỏ]
 G --> E
 E --> H[Drag & drop reorder vị trí 1–3 + audit]
 B -->|Config| I[Mode1/Mode2/Đóng + threshold + schedule]
 I --> J[Cấu hình cấp phim, kế thừa default hệ thống]
```

## UX đã chốt

- Pin và Config nằm cùng trang **Content Operations**, 2 section.
- Pin max 3; pin thứ 4 phải chọn rõ Pin bị thay, không auto replace.
- Expiry optional, mặc định `Không hết hạn`.
- Reorder bằng drag & drop; save lỗi revert thứ tự server gần nhất.
- Phía user Pin luôn ở đầu mọi sort và có icon + chữ `Đã ghim`.
