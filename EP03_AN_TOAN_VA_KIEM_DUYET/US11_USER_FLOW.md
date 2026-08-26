# User Flow — US11 AI kiểm duyệt theo hai chế độ

> User Story: [US11_AI_KIEM_DUYET_THEO_HAI_CHE_DO.md](US11_AI_KIEM_DUYET_THEO_HAI_CHE_DO.md)

**Platform:** CMS Web/Desktop only (cấu hình + vận hành). Việc phân loại AI do backend xử lý phía sau; ứng dụng Phone/Web/Smart TV chỉ hiển thị kết quả trạng thái đã có, không phát sinh chức năng mới trên app.

```mermaid
flowchart TD
 A[Submit Comment/Reply/Edit] --> B[Snapshot mode + scope]
 B --> C[AI classify ≤5s]
 C -->|Heavy| D[Block; giữ composer/draft để sửa]
 C -->|Medium| E[Pending]
 C -->|Light + Mode2| E
 C -->|Light + Mode1| F[Displayed]
 C -->|Timeout/5xx/low confidence/other language| E
 E --> G[Inline Đang chờ duyệt chỉ tác giả]
 G --> H[CMS queue SLA 24h]
 H -->|Approve| I[Displayed nếu Resolver cho public]
 H -->|Reject| J[Non-public + notification]
```

## Nickname invariant đã chốt

Nickname dùng global policy riêng, không Mode1/2 và **không có Pending**. Safe/Light → save; Medium/Heavy → block. AI timeout/5xx/down → không đổi nickname, giữ old/fallback, retryable error, không queue và không tiêu quota đổi nickname.

## UX đã chốt

- Heavy content: giữ nguyên composer và draft, cho sửa/gửi lại.
- Pending item hiển thị inline chỉ tác giả.
- Pending item vẫn được edit; version pending cũ được thay bằng version mới, chạy moderation lại.
