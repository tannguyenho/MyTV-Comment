# User Flow — US12 Trạng thái và phạm vi hiển thị

> User Story: [US12_QUAN_LY_TRANG_THAI_VA_PHAM_VI_HIEN_THI_BINH_LUAN.md](US12_QUAN_LY_TRANG_THAI_VA_PHAM_VI_HIEN_THI_BINH_LUAN.md)

```mermaid
flowchart TD
 A[Admin mở Content Operations] --> B[Chọn Mode1 / Mode2 / Đóng]
 B --> C[Review before/after + effective time]
 C --> D[Save + audit]
 D --> E{Phim bộ?}
 E -->|Có| F[Config mặc định cấp phim bộ; tập có thể override]
 E -->|Không| G[Config cấp phim]
 D --> H{Đóng?}
 H -->|Có| I[User tab Bình luận vẫn hiện nhưng bỏ count]
 I --> J[Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau]
 H -->|Không| K[Render theo Effective Visibility Resolver]
```

## UX/Scope đã chốt

- User-facing **không có scope Series**. Phim bộ chỉ đọc/comment/rating theo tập hiện tại.
- CMS vẫn có cấu hình mặc định cấp phim bộ để vận hành, từng tập override Mode1/Mode2/Đóng.
- Scope Đóng: tab `Bình luận` vẫn tồn tại, không count, không list/composer/interaction; rating vẫn hoạt động.
- Deep link vào scope Đóng mở đúng phim/tập + tab Bình luận + fallback.
- Resolver priority: self-delete → own moderation → Admin root cascade → Account Lock → scope Closed.
