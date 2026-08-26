# User Flow — US16 Vi phạm, sanction và appeal

> User Story: [US16_QUAN_LY_NGUOI_DUNG_VI_PHAM_VA_AUDIT_LOG.md](US16_QUAN_LY_NGUOI_DUNG_VI_PHAM_VA_AUDIT_LOG.md)

**Platform:** CMS Web/Desktop only (Admin ra quyết định). Account Lock do backend áp dụng trên mọi nền tảng gồm Smart TV; app chỉ hiển thị màn khóa và các state đã đặc tả.

```mermaid
flowchart TD
 A[CMS Users & Appeals] --> B[User history + sanction]
 B --> C{Warning / Comment Lock / Account Lock}
 C --> D[Apply reason/duration + audit + notification]
 D -->|Comment Lock| E[User vẫn vào MyTV; chặn Comment/Reply/Mention/Edit]
 E --> F[Tab Bình luận + Profile hiển thị lock status]
 F --> G[Appeal: Nội dung khiếu nại bắt buộc ≤500]
 G --> H[Submit → Đã gửi khiếu nại + Case ID + SLA 48h]
 H --> I[CMS Appeal Queue trong Users & Appeals]
 I --> J[Approve/Reject]
 J --> K[Chỉ gửi notification kết quả; không cần lưu result history riêng trong Profile]
 D -->|Account Lock| L[Invalidate session + chặn toàn MyTV]
 L --> M[Locked screen: reason/duration/Case ID/1800 1166]
```

## UX đã chốt

- Comment Lock không banner toàn app; hiển thị trong tab Bình luận và Profile/Cài đặt.
- Appeal Comment Lock: 1 textarea bắt buộc tối đa 500; system tự attach case/sanction context.
- Sau submit hiển thị Case ID + `MyTV sẽ phản hồi trong vòng 48 giờ`.
- Kết quả appeal chỉ qua notification; không xây màn lịch sử appeal riêng.
- Account Lock áp dụng mọi platform, gồm SmartTV; appeal Account Lock qua Tổng đài MyTV 1800 1166.
