# User Flow — US08 Trả lời bình luận một cấp

> User Story: [US08_TRA_LOI_BINH_LUAN_MOT_CAP.md](US08_TRA_LOI_BINH_LUAN_MOT_CAP.md)

**Platforms:** Phone, Web. Smart TV không áp dụng US08; việc đọc thread chỉ đọc trên TV thuộc US01 (AC11).

```mermaid
flowchart TD
 A["Root có reply"] --> B["Hiển thị Xem n phản hồi, không preload reply trong root list"]
 B --> C{"Platform"}
 C -->|Phone/Web| D["Expand thread inline"]
 C -->|Smart TV| E["Mở trang Thread riêng chỉ đọc — thuộc US01, không có Reply"]
 D --> F["Hiển thị tối đa 3 reply đầu, sort cũ → mới"]
 F --> G{"Còn reply chưa tải?"}
 G -->|"Có"| H["lazy load với n = số reply còn lại"]
 I --> J["Giữ focus tại nút, announce số reply vừa tải qua aria-live, cập nhật lại {n}"]
 D --> K["Tap Trả lời"]
 K --> L["Phone bottom sheet / Web inline composer"]
 L --> M["Reply root hoặc reply khác"]
 M --> N["Nếu reply một reply: tự @nickname nhưng lưu depth=1 dưới root"]
```

## UX đã chốt

- Root list không hiển thị sẵn reply; chỉ action `{n} phản hồi`.
- Khi mở thread, **initial hiển thị tối đa 3 reply**, sort **cũ → mới** (AC9).
- Phần reply còn lại tải dùng infinite scroll/lazy load theo cuộn. Mỗi lần bấm tải **tối đa 10 reply**; nếu phần còn lại <10 thì tải hết (AC10, TC-US08-008). Số `{n}` trên nút được cập nhật lại sau mỗi lần tải;
- Lưu ý phạm vi: **infinite scroll vẫn đúng cho danh sách root comment (US02)**; 
- Có reply mới khi thread mở: indicator `Có {n} phản hồi mới`; user bấm → tải và cuộn tới reply mới đầu tiên.
- Smart TV mở trang thread riêng chỉ đọc (màn `C17`) để xem reply và không có action Trả lời. Phần đọc này thuộc phạm vi US01; US08 không áp dụng trên TV.
