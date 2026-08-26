# User Flow — US04 Đăng bình luận

> User Story: [US04_DANG_BINH_LUAN.md](US04_DANG_BINH_LUAN.md)

**Platforms:** Phone, Web. Smart TV không áp dụng US04.

## Flow

```mermaid
flowchart TD
 A[Chọn Viết bình luận] --> B{Đã login?}
 B -->|Không| C[Auth gate → login → quay lại, user bấm lại]
 B -->|Có| D{Scope mở + không Comment Lock?}
 D -->|Không| E[Hiển thị trạng thái bị chặn]
 D -->|Có| F[Phone: bottom sheet / Web: composer inline]
 F --> G[Nhập text/emoji + Spoiler + timestamp]
 G --> H[Validate 1–1000 grapheme + URL + rate limit]
 H -->|Lỗi| I[Giữ draft + inline error]
 H -->|Hợp lệ| J[AI moderation]
 J -->|Heavy| K[Giữ composer + draft, báo lỗi để sửa]
 J -->|Pending| L[Đóng/clear sau submit + item inline Đang chờ duyệt chỉ tác giả thấy]
 J -->|Public| M[Đóng/clear sau submit + insert public]
```

## UX đã chốt

- Phone mở **bottom sheet**; Web expand composer inline.
- Draft tự lưu khi đóng composer nhưng **chỉ trong phiên hiện tại**; đóng app/reload/kết thúc phiên thì draft mất. Submit thành công clear draft.
- Composer hiển thị content context hiện tại.
- Nickname đổi được ở Profile và có shortcut `Đổi nickname` trong composer.
- Nickname AI timeout/5xx/down: **không đổi nickname**, giữ old/fallback, báo thử lại, không Pending, không vào queue, không tiêu quota đổi nickname.
- Pending comment hiển thị inline chỉ tác giả với nhãn `Đang chờ duyệt`, không tính public count.
- Smart TV không có nút Viết bình luận; hiển thị hướng dẫn + QR để dùng smartphone.
- Smart TV cũng không áp dụng cơ chế Làm mờ của US04: đoạn chữ được làm mờ khi soạn trên Phone/Web sẽ hiển thị nguyên văn khi đọc trên TV.
