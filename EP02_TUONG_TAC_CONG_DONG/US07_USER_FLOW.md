# User Flow — US07 Like / Unlike

> User Story: [US07_LIKE_VA_UNLIKE_BINH_LUAN.md](US07_LIKE_VA_UNLIKE_BINH_LUAN.md)

**Platforms:** Phone, Web, Smart TV

```mermaid
flowchart TD
 A["Tap Like/Unlike"] --> B{"Đã login + target public?"}
 B -->|Guest| C["Auth gate → login → quay lại, không auto-like"]
 B -->|"Không public"| D["Action unavailable"]
 B -->|"Hợp lệ"| E["Optimistic update state + count ngay lập tức"]
 E --> F["Đưa thao tác vào batch queue của client"]
 F --> G["Coalesce theo target: chỉ giữ state cuối cùng trong batch window"]
 G --> H{"Điều kiện flush batch"}
 H -->|"Chưa tới hạn"| G
 H -->|"Đủ tối đa 5 giây"| I["Sync batch xuống BE"]
 H -->|"Rời màn hình hoặc app chuyển background: flush sớm"| I
 I --> J{"Kết quả BE"}
 J -->|"Success"| K["Giữ state theo BE là source of truth"]
 J -->|"BE trả mismatch hoặc từ chối"| L["Reconcile revert state/count + báo lỗi + announce aria-live"]
 J -->|"Lỗi mạng hoặc offline"| M["Giữ nguyên batch chưa gửi, KHÔNG revert UI, không báo lỗi"]
 M --> N["Có mạng lại → tự retry/flush lại batch, BE nhận state cuối đúng một lần"]
 N --> I
 M --> O["Force-kill app trước khi flush → mở lại app reconcile theo state hiện hành ở BE"]
```

## UX đã chốt

- Hiển thị `👍 {count}` trực tiếp cạnh Like.
- **Không có reaction âm trên bất kỳ nền tảng nào:** chỉ có duy nhất một nút Like dạng bật/tắt. Smart TV cũng dùng đúng một nút Like toggle, **không có nút `Dislike` riêng**.
- **Optimistic update ngay lập tức**, sau đó client **gom batch tối đa 5 giây** rồi mới sync BE, không gửi từng thao tác riêng lẻ tức thì (AC3–AC4).
- **Flush sớm** khi user rời màn hình hoặc app chuyển background trước khi hết 5 giây (AC5).
- Nhiều Like/Unlike liên tiếp trên **cùng một target** trong cùng batch window được **coalesce về state cuối cùng**; các state trung gian không được gửi lên BE và không làm sai Net Like (AC6). BE phải idempotent/dedup để double-click hoặc retry không nhân đôi Like (AC8).
- **Chỉ revert khi BE trả mismatch hoặc từ chối** (AC7): client reconcile về state BE và hiển thị microcopy “Chưa lưu được lượt thích.”
- **Lỗi mạng tạm thời KHÔNG revert UI và không bắn toast lỗi**: batch chưa gửi được giữ lại, client tự retry/flush khi có mạng lại và BE nhận đúng state cuối cùng đúng một lần (TC-US07-014a). Nếu app bị force-kill trước khi flush, lần mở lại UI reconcile theo state hiện hành trên BE thay vì giữ optimistic state đã mất (TC-US07-014b).
- Smart TV áp dụng US07 đầy đủ: Like/Unlike bằng remote nhưng vẫn yêu cầu login.
