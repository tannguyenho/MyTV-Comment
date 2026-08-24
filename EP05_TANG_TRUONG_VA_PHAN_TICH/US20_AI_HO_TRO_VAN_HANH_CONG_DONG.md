# US20 — AI hỗ trợ vận hành cộng đồng

> Thuộc EP05 — Tăng trưởng và phân tích
> [← Quay lại README của Epic](README.md) · [← Backlog MyTV](../README.md)

### User Story

**Là Admin/biên tập viên nội dung**, tôi muốn chủ động yêu cầu AI đề xuất comment đáng chú ý hoặc câu hỏi thảo luận, để giảm thời gian vận hành nhưng vẫn kiểm soát hoàn toàn nội dung được ghim/đăng.

### Ưu tiên

**Could**

### Acceptance Criteria — Cách gọi AI

1. AI không tự chạy để public nội dung; Admin chủ động bấm **“AI đề xuất”**.
2. Nút AI đề xuất luôn khả dụng cho role được quyền trong scope sản phẩm hiện tại; **không cần toggle bật/tắt tính năng theo KPI**.
3. AI chỉ dùng dữ liệu trong **phim/tập hiện tại**: comment, reply, Like, Rating, Report và metadata nội dung liên quan.
4. Không dùng lịch sử hành vi user trên toàn MyTV hoặc dữ liệu ngoài MyTV làm input cho feature này.

### Acceptance Criteria — Đề xuất comment nổi bật

1. AI chỉ xét comment đang Hiển thị.
2. Tín hiệu ưu tiên: **chất lượng nội dung + mức liên quan tới phim/tập + Like + Reply**.
3. Loại khỏi candidate các comment Chờ duyệt/Từ chối/Ẩn/Xóa; hoặc comment đang có **AI risk = Nặng**; hoặc đã được CMS **gắn Flag nghiêm trọng**.
4. **Report chưa được xác minh không tự loại candidate chỉ dựa trên số lượng Report**, kể cả có nhiều Report; Report vẫn là tín hiệu để AI/Admin tham khảo nhưng không phải kết luận vi phạm.
5. AI trả rationale/tín hiệu chính để Admin đánh giá.
6. AI **không tự ghim**. Admin xem đề xuất rồi quyết định ghim qua US15 hoặc bỏ qua.
7. Không chỉnh sửa text comment của user khi ghim; nếu cần xử lý nội dung phải đi moderation/edit flow phù hợp.

### Acceptance Criteria — Đề xuất câu hỏi/chủ đề

1. Admin bấm “AI đề xuất” để sinh câu hỏi/chủ đề gắn đúng series/tập.
2. AI proposal phải qua safety/Spoiler check.
3. Admin có thể **chỉnh sửa → duyệt → đăng** ngay; **không cần Admin thứ hai phê duyệt**.
4. Nếu Admin không xác nhận, AI proposal không được public.

### KPI chất lượng AI

- Tỷ lệ Admin **chấp nhận** đề xuất.
- Tỷ lệ Admin **chỉnh sửa** trước khi đăng.
- Tỷ lệ Admin **bỏ** đề xuất.

Các KPI dùng để theo dõi chất lượng, không tự động disable tính năng.

### Quy tắc nghiệp vụ

> *Xem thêm: [REQUIREMENTS_A11Y_SECURITY.md](../REQUIREMENTS_A11Y_SECURITY.md) mục liên quan — an toàn dữ liệu đầu vào AI (PII, phạm vi dữ liệu) và kiểm soát nội dung do AI đề xuất.*

- Human-in-the-loop bắt buộc: AI đề xuất, Admin quyết định.
- Input bị giới hạn theo phim/tập hiện tại để giảm rủi ro privacy/context leakage.
- Candidate exclusion vì mức nghiêm trọng chỉ dựa trên **AI Nặng** hoặc **CMS Flag nghiêm trọng**; unverified Report count không tự tạo exclusion.
- AI không tự pin, không tự publish.
- Mọi accept/edit/discard/pin/post liên quan proposal phải tracking để US19 đo hiệu quả.

## Test Cases

| ID | Loại | Tiền điều kiện / dữ liệu | Bước kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| TC-US20-001 | Trigger | Admin có quyền | Không bấm AI đề xuất rồi theo dõi | Không có proposal/public action tự phát. |
| TC-US20-002 | Input scope | E1 có dữ liệu và account có lịch sử ở E2/khác | Bấm AI đề xuất ở E1 | Input/output chỉ dựa dữ liệu E1/phim hiện tại theo scope được phép. |
| TC-US20-003 | Candidate | Có comment khác nhau quality/relevance/Like/Reply | Bấm AI đề xuất | Ranking proposal phản ánh bốn nhóm tín hiệu và có rationale. |
| TC-US20-004 | State exclusion | Có pending/rejected/hidden/deleted | Bấm AI đề xuất | Các item không Hiển thị bị loại khỏi candidate list. |
| TC-US20-005 | Severe exclusion | C1 public AI Nặng; C2 public có CMS Flag nghiêm trọng | Bấm AI đề xuất | C1 và C2 đều bị loại khỏi candidate list. |
| TC-US20-006 | Unverified reports | C3 public có nhiều Report chưa xác minh, không AI Nặng và không Flag nghiêm trọng | Bấm AI đề xuất | C3 **không bị loại chỉ vì Report count**; Report có thể xuất hiện trong rationale/tín hiệu để Admin cân nhắc. |
| TC-US20-007 | No auto-pin | Có candidate tốt | Không thao tác Admin | Không thay đổi pin state. |
| TC-US20-008 | Pin decision | Admin chấp nhận candidate | Ghim qua US15 | Pin chỉ thay đổi sau thao tác Admin; text user không bị rewrite. |
| TC-US20-009 | Question workflow | Admin bấm AI đề xuất câu hỏi | Edit → Approve → Post | Nội dung chỉ public sau Admin xác nhận; không cần reviewer thứ hai. |
| TC-US20-010 | Safety | Proposal câu hỏi có Spoiler/risk | Chạy safety/Spoiler check | Proposal không được public trước khi qua check và Admin xác nhận; kết quả safety được hiển thị để Admin xử lý theo policy. |
| TC-US20-011 | KPI tracking | Accept/edit/discard nhiều proposal | Mở metric | Tính đúng ba tỷ lệ KPI chất lượng. |
| TC-US20-012 | No disable | KPI discard cao | Kiểm tra CMS | Feature không tự disable và không có toggle quality-based trong scope hiện tại. |
