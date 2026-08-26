# User Flow — US02 Số lượng và sắp xếp bình luận theo nội dung hiện tại

> User Story: [US02_XEM_BINH_LUAN_SO_LUONG_VA_SAP_XEP.md](US02_XEM_BINH_LUAN_SO_LUONG_VA_SAP_XEP.md)

**Platforms:** Phone, Web. Smart TV không áp dụng US02.

## Flow

```mermaid
flowchart TD
 A[Mở tab Bình luận] --> B[Xác định content scope hiện tại]
 B --> C[Phạm vi bình luận = bộ phim]
 C --> D[Load public count + rating + pin + root list]
 D --> E[Sort mặc định Nổi bật]
 E --> F[Hiển thị tối đa 3 Pin luôn ở trên cùng]
 F --> G[Load 10 root đầu]
 G --> H{Cuộn gần cuối?}
 H -->|Có| I[Lazy load tối đa 10 root/batch]
 I --> H
 G --> J{Đổi sort?}
 J --> K[Dropdown: Nổi bật / Mới nhất / Nhiều lượt thích]
 K --> G
 L[Phim bộ đổi tập] --> M[Giữ nguyên sort, count, rating, Pin và list]
```

## UX đã chốt

- **Phạm vi bình luận là bộ phim.** Phim lẻ và phim bộ dùng chung mô hình; đổi tập không đổi phạm vi bình luận.
- Pin tối đa 3, luôn ở đầu trong mọi sort, có `📌 Đã ghim`, không lặp trong list thường.
- Sort control dạng dropdown `Nổi bật ▼`.
- Root comment lazy load **10/batch**.
- Khi user bấm indicator comment mới: `Nổi bật` và `Nhiều lượt thích` luôn giữ ranking đúng, không ép comment mới lên đầu; `Mới nhất` có thể đưa user tới comment mới đầu tiên.
- Smart TV không đổi sort: TV không render control sort, danh sách cố định thứ tự `Nổi bật` và kế thừa quy tắc count/pin/lazy load của US02 (xem US01 AC10).

## States

Loading/skeleton · Empty · Loading more · End list · New-content indicator · Sort menu.
