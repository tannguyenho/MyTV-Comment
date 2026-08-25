# User Flow — US13 Tra cứu bình luận trên CMS

> User Story: [US13_TRA_CUU_BINH_LUAN_TREN_CMS.md](US13_TRA_CUU_BINH_LUAN_TREN_CMS.md)

**Platform:** Web/Desktop only

```mermaid
flowchart TD
 A[Mở Moderation] --> B[Server auth role + scope]
 B -->|OK| C[Một screen: Table/List trái + Detail panel phải]
 C --> D[Search + filter + saved views]
 D --> E[Chờ duyệt / Bị Report / Đã xử lý / phim / thời gian / AI / Spoiler]
 E --> F[Chọn row → xem Detail không rời list]
 F --> G[Giữ nguyên queue/filter/search context]
 C --> H[Export theo filter hiện tại]
```

## UX đã chốt

- Queue và Search **không tách navigation**; nằm trong một Moderation screen.
- Report là filter/saved view, không module riêng.
- Desktop only; không thiết kế CMS smartphone/tablet.
- Queue mặc định risk cao trước, cùng risk item chờ lâu hơn trước.
