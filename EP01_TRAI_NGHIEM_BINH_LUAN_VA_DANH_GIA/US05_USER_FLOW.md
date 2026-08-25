# User Flow — US05 Sửa và xóa bình luận

> User Story: [US05_SUA_VA_XOA_BINH_LUAN.md](US05_SUA_VA_XOA_BINH_LUAN.md)

**Platforms:** Phone, Web

```mermaid
flowchart TD
 A[Menu ⋯ trên content của mình] --> B{Chỉnh sửa / Xóa}
 B -->|Chỉnh sửa| C{Comment Lock hoặc >5 edit/phút/target?}
 C -->|Có| D[Chặn edit]
 C -->|Không| E[Mở editor]
 E --> F[Sửa text/emoji + Spoiler + timestamp]
 F --> G[Submit version mới → moderation theo mode của phim]
 G -->|Chế độ 1 + AI Nhẹ| I[Public ngay + toast Chỉnh sửa thành công + nhãn Đã chỉnh sửa]
 G -->|Chế độ 1 + AI Trung bình hoặc Chế độ 2| H[Giữ version public cũ; version mới Chờ duyệt + toast Đã gửi bản chỉnh sửa, đang chờ duyệt]
 G -->|AI Nặng hoặc bị Từ chối| J[Giữ version public gần nhất]
 H -->|Admin Duyệt| I
 B -->|Xóa reply| K[Confirm → self-delete reply]
 B -->|Xóa root| L[Confirm cảnh báo cascade reply kèm số phản hồi]
 L --> M[Self-delete root + toàn reply; không Undo public]
 N[Content của mình đang Chờ duyệt] --> O[Menu ⋯ → Hủy đăng bình luận]
 O --> P[Confirm Hủy đăng bình luận này?]
 P --> Q[Xóa khỏi UI + gỡ khỏi moderation queue; không hoàn quota; không ghi audit]
```

## UX đã chốt

- Action của chính user nằm trong menu `⋯` (kebab mở bottom sheet).
- Edit được sửa toàn bộ text/emoji, đoạn Làm mờ (Spoiler), timestamp.
- **Kết quả của một lần sửa phụ thuộc chế độ kiểm duyệt của phim**, không phải luôn public ngay; hai toast phân biệt rõ: `Chỉnh sửa thành công` và `Đã gửi bản chỉnh sửa, đang chờ duyệt`.
- Pending content vẫn được edit; version pending cũ được thay bằng version mới, không tạo nhiều pending song song.
- Edit limit 5/phút/target.
- **Hủy đăng nội dung đang Chờ duyệt** là lifecycle riêng: không hoàn lại quota 5 nội dung/phút, không ghi audit log, gỡ khỏi moderation queue ngay, không có đường khôi phục.
- Self-delete root khác CMS delete; user không có Undo public.
