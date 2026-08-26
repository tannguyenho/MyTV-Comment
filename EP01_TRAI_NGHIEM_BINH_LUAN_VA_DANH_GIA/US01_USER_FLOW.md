# User Flow — US01 Đọc khu vực bình luận

> User Story: [US01_DOC_KHU_VUC_BINH_LUAN.md](US01_DOC_KHU_VUC_BINH_LUAN.md)

**Platforms:** Phone, Web, Smart TV  
**Actor:** Guest / User đăng nhập

## Flow

```mermaid
flowchart TD
 A[Mở trang phim] --> B[Trang giữ tab mặc định hiện hành]
 B --> C[User chọn Bình luận count]
 C --> D{Scope đang mở?}
 D -->|Không| E[Tab vẫn hiện tên Bình luận, bỏ count + trạng thái không khả dụng]
 D -->|Có| F[Loading skeleton rating + sort + 3 comment]
 F --> G[Hiển thị public comment theo Effective Visibility]
 G --> H{Guest chọn interaction?}
 H -->|Có| I[Auth gate]
 I --> J[Login thành công → quay lại đúng context, không auto action]
 H -->|Không| K[Tiếp tục đọc]
 L[Deep link comment/thread] --> M[Mở đúng phim + active tab Bình luận]
 M --> N{Target public?}
 N -->|Có| O[Focus đúng target]
 N -->|Không| P[Fallback an toàn theo Visibility Resolver]
```

## UX đã chốt

- Comment là **tab riêng**. Phim bộ mặc định tab `Danh sách tập`; phim lẻ mặc định tab `Đề xuất`. User chủ động chọn tab Bình luận.
- Tab mở hiển thị `Bình luận ({public_count})`; scope Đóng chỉ hiển thị `Bình luận`.
- Comment dài tối đa **3 dòng** → `Xem thêm` / `Thu gọn`.
- Rời tab rồi quay lại trong cùng phiên: giữ scroll, sort, thread mở, trạng thái expand/collapse; refresh dữ liệu ngầm không reset context.
- Có dữ liệu mới khi đang đọc: không tự chèn; hiện `Có {n} bình luận mới` để user chủ động refresh.
- Guest được đọc public content; login chỉ khi tương tác.
- Empty: logged-in có CTA viết đầu tiên; Guest có CTA login; SmartTV có hướng dẫn + QR chuyển sang smartphone.
- **Smart TV chỉ áp dụng US01, US07, US10 và US17.** TV đọc danh sách gốc, mở trang thread chỉ đọc để xem reply, Thích/Bỏ thích, Báo cáo bình luận và hiển thị huy hiệu. Không composer, không Trả lời/Sửa/Xóa/Nhắc tên/Chia sẻ, không đổi sort, không chấm sao, không seek timestamp.
- Danh sách trên Smart TV kế thừa quy tắc render của US02 (count trên tab, tối đa 3 pin trên cùng, thứ tự `Nổi bật`, lazy load 10 root/batch) nhưng không có control sort.
- Smart TV không áp dụng cơ chế Làm mờ: nội dung comment hiển thị nguyên văn, không có dải mờ.

## States

Loading skeleton · Empty · Populated · Auth gate · Scope Closed · Target unavailable · Background refresh.
