# User Flow — US12 Trạng thái và phạm vi hiển thị

> User Story: [US12_QUAN_LY_TRANG_THAI_VA_PHAM_VI_HIEN_THI_BINH_LUAN.md](US12_QUAN_LY_TRANG_THAI_VA_PHAM_VI_HIEN_THI_BINH_LUAN.md)

**Platform:** CMS Web/Desktop only (Admin cấu hình). Effective Visibility Resolver do backend áp dụng cho mọi nền tảng; ứng dụng Phone/Web/Smart TV chỉ render kết quả theo các state đã đặc tả ở US01, không phát sinh chức năng mới trên app.

```mermaid
flowchart TD
 A[Admin mở Content Operations] --> B[Chọn Mode1 / Mode2 / Đóng]
 B --> C[Review before/after + effective time]
 C --> D[Save + audit]
 D --> E{Phim bộ?}
 E -->|Có| F[Config cấp phim, kế thừa default hệ thống]
 E -->|Không| G[Config cấp phim]
 D --> H{Đóng?}
 H -->|Có| I[User tab Bình luận vẫn hiện nhưng bỏ count]
 I --> J[Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau]
 H -->|Không| K[Render theo Effective Visibility Resolver]
```

## UX/Scope đã chốt

- Phạm vi đọc/comment/rating phía người xem là **bộ phim**, áp dụng chung cho phim lẻ và phim bộ.
- CMS cấu hình Mode1/Mode2/Đóng ở **cấp phim**, kế thừa default hệ thống khi không có override.
- Scope Đóng: tab `Bình luận` vẫn tồn tại, không count, không list/composer/interaction; rating vẫn hoạt động.
- Deep link vào scope Đóng mở đúng phim + tab Bình luận + fallback.
- Resolver priority: self-delete → own moderation → Admin root cascade → Account Lock → scope Closed.
