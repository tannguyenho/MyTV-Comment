# User Flow — US20 AI hỗ trợ vận hành cộng đồng

> User Story: [US20_AI_HO_TRO_VAN_HANH_CONG_DONG.md](US20_AI_HO_TRO_VAN_HANH_CONG_DONG.md)

**Platform:** CMS Web/Desktop only

```mermaid
flowchart TD
 A[Admin mở Content Operations của phim] --> B[AI đề xuất]
 B --> C[System chỉ lấy input trong scope hiện tại]
 C --> D{Loại đề xuất}
 D -->|Comment đáng chú ý| E[Rank candidates public hợp lệ]
 E --> F[Admin review]
 F -->|Accept| G[Đi flow Pin US15]
 F -->|Discard| H[Không thay đổi public state]
 D -->|Câu hỏi/chủ đề| I[AI sinh proposal + safety/spoiler check]
 I --> J[Admin review/edit]
 J -->|Approve/Post| K[Public sau xác nhận Admin]
 J -->|Discard| H
```

## UX đã chốt

- `AI đề xuất` nằm ngay trong **Content Operations của bộ phim hiện tại**, không có top-level AI Ops riêng.
- Không auto-run, auto-pin, auto-publish.
- Admin luôn review/confirm trước thay đổi public.
