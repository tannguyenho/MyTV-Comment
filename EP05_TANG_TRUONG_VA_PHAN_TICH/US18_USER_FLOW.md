# User Flow — US18 Chia sẻ bình luận

> User Story: [US18_CHIA_SE_BINH_LUAN.md](US18_CHIA_SE_BINH_LUAN.md)

**Platforms:** Phone, Web. Smart TV không tạo Share nhưng mở được link chia sẻ tới comment/thread (AC18).

```mermaid
flowchart TD
 A["Menu ⋯ → Chia sẻ"] --> B{"Đã login + target public?"}
 B -->|"Không"| C["Auth/unavailable — không ghi Share event"]
 B -->|"Có + Phone"| D["Mở OS share sheet ngay"]
 B -->|"Có + Web"| G{"Trình duyệt hỗ trợ Web Share API?"}
 G -->|"Có"| D
 G -->|"Không"| H["Fallback: Sao chép liên kết"]
 D --> E{"Share sheet mở thành công?"}
 E -->|"Có"| F["Ghi 1 Share event, có dedup"]
 E -->|"Không"| C
 H --> H2{"Sao chép liên kết thành công?"}
 H2 -->|"Có"| F
 H2 -->|"Không"| C
 F --> I["Recipient mở deep link"]
 I --> J["App nếu có, nếu không MyTV Web"]
 J --> K["Visibility Resolver → target hoặc fallback"]
```

## UX đã chốt

- Share nằm trong menu `⋯`, không phải action ưu tiên cạnh Like/Reply.
- Phone không có preview/confirm trung gian; mở OS share sheet ngay.
- **MVP chỉ dùng OS share sheet, KHÔNG tích hợp SDK/kênh riêng cho bất kỳ mạng xã hội nào** (README mục 5.12, AC13). Web dùng **Web Share API / OS share sheet** khi trình duyệt hỗ trợ; trình duyệt không hỗ trợ thì fallback là **“Sao chép liên kết”**.
- **Mốc ghi nhận Share event — áp dụng cho CẢ Phone và Web** (AC14, AC15):
  - Phone và Web có Web Share API: ghi đúng **1 Share event khi share sheet mở thành công**; user cancel/đóng sau đó không hoàn tác event.
  - Web dùng fallback: ghi đúng **1 Share event khi sao chép liên kết thành công**.
  - Cả hai nhánh đều đi qua cùng một node ghi event và phải **dedup** để retry/lỗi kỹ thuật không làm tăng Share KPI sai.
  - Nhánh bị chặn (chưa login, target non-public, scope Đóng, Account Lock) hoặc mở sheet/copy thất bại thì **không ghi Share event**.
- Vì Share có trọng số ×2 trong Engagement Score (`Comment×2 + Reply×2 + Net Like + Rating + Share×2`), nhánh Web bắt buộc phải ghi event; nếu bỏ sót, dashboard và ranking phim sẽ thiếu điểm mà đối soát hằng ngày không phát hiện được do đối soát cùng nguồn sự kiện.
- Payload/preview không chứa nguyên văn comment, nickname/phone/Spoiler; CTA `Xem nội dung này trên MyTV`.
- Smart TV không có action Chia sẻ, nhưng mở được link chia sẻ trỏ tới comment/thread: mở đúng phim + tab Bình luận, hoặc thread chỉ đọc `C17` nếu target là reply; gate và fallback theo US12 giống Phone/Web.
