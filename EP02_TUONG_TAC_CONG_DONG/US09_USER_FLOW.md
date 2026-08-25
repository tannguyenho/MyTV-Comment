# User Flow — US09 Mention và thông báo

> User Story: [US09_MENTION_VA_NHAN_THONG_BAO.md](US09_MENTION_VA_NHAN_THONG_BAO.md)

**Platforms:** Phone, Web. SmartTV chỉ hiển thị mention trong nội dung.

```mermaid
flowchart TD
 A[Gõ @ trong composer] --> B[Gợi ý user trong thread trước]
 B --> C[Sau đó user đã tham gia bộ phim hiện tại]
 C --> D[Chọn user → lưu mention theo account ID]
 D --> E[Submit content → moderation]
 E -->|Pending| F[Chưa gửi community notification]
 E -->|Public| G{Self / Account Lock / switch off?}
 G -->|Có| H[Không gửi community notification]
 G -->|Không| I[Tạo notification theo hệ thống MyTV hiện có]
 I --> J[Tap notification → deep link + Visibility Resolver]
```

## UX đã chốt

- Không tìm kiếm toàn bộ user MyTV; ưu tiên thread rồi content scope hiện tại.
- Notification Center **giữ nguyên 1 feed hiện có của MyTV**; flow này không thiết kế IA/tab/filter mới.
- Notification moderation/sanction/appeal/report-result vẫn bắt buộc theo business rule.
- SmartTV hiển thị `@nickname` để đọc nhưng không tạo Mention.
