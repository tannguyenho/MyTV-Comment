# User Flow — US19 Analytics bình luận

> User Story: [US19_THONG_KE_HOAT_DONG_BINH_LUAN.md](US19_THONG_KE_HOAT_DONG_BINH_LUAN.md)

**Platform:** CMS Web/Desktop only

```mermaid
flowchart TD
 A[Mở Analytics] --> B[Default 30 ngày gần nhất]
 B --> C[Chọn phim + time range]
 C --> D[Load KPI + last updated]
 D --> E{Fresh ≤5 phút?}
 E -->|Không| F[Stale/error + retry]
 E -->|Có| G[Hiển thị KPI]
 G --> H[Engagement Score → Bình luận → Reply → Like → Rating → Share → Report]
 G --> I[Export CSV/XLSX theo filter]
```

## UX đã chốt

- Default time range: **30 ngày gần nhất**.
- KPI order: **Engagement Score → Bình luận → Reply → Like → Rating → Share → Report**.
- Giữ last-updated/stale state và export theo filter hiện tại.
- Scope Đóng không làm KPI lịch sử tự tụt; visibility/sanction/lifecycle áp dụng theo business rules hiện hành.
