# User Flow — US14 Xử lý nội dung trên CMS

> User Story: [US14_XU_LY_NOI_DUNG_TREN_CMS.md](US14_XU_LY_NOI_DUNG_TREN_CMS.md)

**Platform:** CMS Web/Desktop only

```mermaid
flowchart TD
 A[Chọn item trong Detail panel] --> B[Server check current state + scope]
 B --> C{Action}
 C -->|Duyệt| D[Không reason]
 C -->|Từ chối/Ẩn/Xóa mềm| E[Reason; Vi phạm khác bắt note 1–500]
 D --> F[Apply + audit]
 E --> F
 F --> G[Success → tự chuyển item kế tiếp trong queue, giữ filter/search]
 H[Item bị Admin khác cập nhật] --> I[Không chạy action cũ; báo conflict + refresh state]
 J["Bulk"] --> K["Checkbox từng row/header Select all, max 100"]
 K --> L{"Bulk Duyệt/Từ chối/Ẩn/Xóa mềm"}
 L -->|"Duyệt"| P
 L -->|"Từ chối/Ẩn/Xóa mềm"| M["Chọn 1 reason chung cho cả batch"]
 M --> M1["Cho phép override reason/note riêng từng item"]
 M1 --> M2{"Reason cuối cùng của item là Vi phạm khác?"}
 M2 -->|"Có"| M3["Bắt buộc note 1–500 ký tự cho chính item đó"]
 M2 -->|"Không"| M4["Note tùy chọn"]
 M3 --> P["Xem trước danh sách per-item: reason/note cuối của từng item"]
 M4 --> P
 P --> Q["Apply"]
 Q --> N["Validate từng item + partial success summary"]
```

## UX đã chốt

- Report không tab riêng; Detail panel hiển thị report context.
- Bulk action bar chỉ hiện khi có selection.
- Sau single action thành công tự chuyển item kế tiếp; hết queue thì empty queue, không tự đổi filter.
- Optimistic concurrency: nếu stale, không overwrite im lặng.
- **Bulk reason (AC5–AC6 Bulk moderation, README mục 5.9):** Admin chọn **một reason chung cho batch** và **có thể override reason riêng cho từng item** trước khi Apply — không ép cả batch mang cùng một reason. Ví dụ chọn 40 comment gồm 38 Spam và 2 Spoiler: đặt reason chung "Spam/quảng cáo" rồi override 2 item sang "Spoiler", để thông báo gửi tác giả và audit log ghi đúng căn cứ chế tài của từng item.
- **Note theo reason cuối cùng của từng item**, không dùng 1 note chung: item nào có reason cuối là **"Vi phạm khác"** thì bắt buộc note **1–500 ký tự** hợp lệ (không chỉ khoảng trắng); item override sang reason khác không bị bắt note.
- Trước khi Apply, CMS hiển thị **bước xem trước danh sách per-item** (item — reason cuối — note) để Admin rà lại; sau Apply vẫn giữ **partial success summary** theo từng item.
