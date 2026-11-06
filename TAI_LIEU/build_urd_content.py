#!/usr/bin/env python3
# Sinh URD_content.json v2.1 từ v1.1 + quyết định V5 (02/11/2026) + phản hồi PO 06/11/2026
import json, copy, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'URD_content_v1.1.json')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'URD_content.json')
old = json.load(open(SRC))
ob = old['body']

doc = copy.deepcopy(old)
doc['meta']['version'] = '2.1'
doc['meta']['effectiveDate'] = '06/11/2026'
doc['history'].append({
    "no": 3, "version": "2.0", "author": "Business Analyst", "approver": "", "date": "02/11/2026",
    "changes": "Chốt kịch bản theo thiết kế Figma Phone/Web/Smart TV và 12 feedback của đội phát triển: bình luận và danh tính ở cấp phim/tài khoản; giới hạn 500 ký tự; bỏ Đánh giá sao, Mốc thời gian, Chia sẻ, định dạng văn bản và nickname riêng khỏi giai đoạn này; bổ sung bước chặn từ khóa, Hủy đăng khi chờ duyệt, luồng xử lý báo cáo, bảng loại thông báo; thêm ảnh thiết kế Web và Smart TV."
})
doc['history'].append({
    "no": 4, "version": "2.1", "author": "Business Analyst", "approver": "", "date": "06/11/2026",
    "changes": "Thu hẹp tài liệu về đúng các luồng có thiết kế trên Figma: Phone/Web gồm US01, US02, US04, US05, US07, US08, US09, US10, US17; Smart TV gồm US01, US17; các luồng còn lại (CMS, Thích/Báo cáo trên TV, Đánh giá, Mốc thời gian, Chia sẻ) ghi nhận cho giai đoạn sau. Cập nhật tiêu chí huy hiệu không còn phụ thuộc ngày hoạt động. Cập nhật theo phản hồi của Ban sản phẩm trên bảng feedback: thiết kế Xem thêm bình luận dài, màn Bình luận của nội dung mở từ thông báo, định dạng thời gian tương đối 6 mức, không phân biệt giao diện bình luận của mình, nhắc tên không bấm được."
})

def h1(t): return {"type": "h1", "text": t}
def h2(t): return {"type": "h2", "text": t}
def h3(t): return {"type": "h3", "text": t}
def p(t, **kw): d = {"type": "p", "text": t}; d.update(kw); return d
def note(t): return {"type": "note", "text": t}
def bullets(items): return {"type": "bullet", "items": items}
def img(path, w, cap): return {"type": "image", "path": path, "widthCm": w, "caption": cap}
def table(header, rows, widths, caption=None):
    d = {"type": "table", "header": header, "rows": rows, "widths": widths}
    if caption: d["caption"] = caption
    return d

PH = 'assets/phone/'; WB = 'assets/web/'; TV = 'assets/tv/'; FL = 'assets/flow/'
fig = [0]
def cap(t):
    fig[0] += 1
    return f"Hình {fig[0]}: {t}"

FLOW_NOTE = "lưu đồ trích từ Figma Phone; đồ họa sẽ được cập nhật khi đội thiết kế xử lý xong các ghi chú [BA] còn lại"
TIME_FMT = "Vừa mới xong (dưới 1 phút) / {X} phút trước (1–59 phút) / {X} giờ trước (1–23 giờ) / {X} ngày trước (1–29 ngày) / {X} tháng trước (1–11 tháng) / {X} năm trước (từ 1 năm)"
PW = 5.2  # phone image width cm

body = []

# ======================= I. TỔNG QUAN =======================
body += [h1("TỔNG QUAN"), h2("Mục đích"),
 p("Tài liệu mô tả yêu cầu của người sử dụng đối với tính năng Bình luận trên nền tảng MyTV: khu vực thảo luận gắn với từng bộ phim truyện/VOD trên Phone, Web và Smart TV, các thao tác tương tác của người xem, cơ chế kiểm duyệt tự động khi đăng và huy hiệu khuyến khích cộng đồng."),
 p("Tài liệu là cơ sở để đội phát triển lập tài liệu Đặc tả yêu cầu phần mềm (SRS), thiết kế kiến trúc, xây dựng, kiểm thử và nghiệm thu hệ thống. Phiên bản 2.1 chỉ đặc tả các luồng đã có thiết kế giao diện trên Figma (nguồn chính của kịch bản); các luồng chưa có thiết kế được liệt kê tại mục Phạm vi dưới nhãn “Giai đoạn sau” để không bị bỏ sót khi lập kế hoạch tiếp theo. Các quyết định chốt được ghi tại CHANGELOG_RASOAT_V5.md và bảng feedback kịch bản bình luận trong kho tài liệu dự án."),
 h2("Phạm vi"),
 p("Tài liệu áp dụng cho toàn bộ các bên tham gia dự án Bình luận MyTV: Ban sản phẩm, đội Business Analyst, đội thiết kế UX/UI, đội phát triển ứng dụng (Phone iOS/Android, Web, Smart TV/STB), đội phát triển dịch vụ phía máy chủ, đội kiểm thử và bộ phận vận hành nội dung."),
 p("Phạm vi giai đoạn này — theo nền tảng và User Story có thiết kế trên Figma:", bold=True),
 table(["Nền tảng", "User Story trong phạm vi", "Ghi chú"], [
  ["Phone (iOS/Android)", "US01 Đọc khu vực bình luận; US02 Số lượng và sắp xếp; US04 Đăng bình luận; US05 Sửa và xóa bình luận; US07 Thích và Bỏ thích; US08 Trả lời một cấp; US09 Nhắc tên và nhận thông báo; US10 Báo cáo bình luận vi phạm; US17 Huy hiệu người dùng", "Thiết kế: Figma [Phone] Play Nội dung, trang “Bình luận App”"],
  ["Web (MyTV Web)", "US01, US02, US04, US05, US07, US08, US09, US10, US17 (như Phone)", "Thiết kế: Figma [Web] Play Nội dung, trang “Tính năng bình luận”"],
  ["Smart TV / STB", "US01 Đọc khu vực bình luận (chỉ đọc); US17 Huy hiệu người dùng (hiển thị chip)", "Thiết kế: Figma [TV] Trang chủ, trang “Bình luận SmartTV”. Thích và Báo cáo trên TV chuyển giai đoạn sau"],
 ], [20, 50, 30], caption="Bảng 1: Phạm vi User Story theo nền tảng"),
 p("Các nguyên tắc nghiệp vụ áp dụng chung trong phạm vi:", bold=True),
 bullets([
  "Phim truyện/VOD có timeline cố định. Bình luận ở cấp bộ phim: mỗi bộ phim — phim lẻ hay phim bộ — có duy nhất một khu vực bình luận dùng chung cho mọi tập; đổi tập không tải lại danh sách.",
  "Danh tính bình luận gắn với tài khoản MyTV (không gắn với từng hồ sơ xem). Tên hiển thị là tên tài khoản sẵn có; chưa có tên thì hiển thị số điện thoại đã che dạng 0***123. Hồ sơ Trẻ em không nhìn thấy khu vực bình luận.",
  "Đọc bình luận công khai không cần đăng nhập; phải đăng nhập mới được Bình luận, Trả lời, Thích, Nhắc tên và Báo cáo.",
  "Bình luận và trả lời là văn bản thuần 1–500 ký tự, không định dạng; trả lời chỉ sâu một cấp.",
  "Khi đăng, nội dung đi qua kiểm duyệt tự động (danh sách từ khóa chặn và AI phân loại) trước khi hiển thị công khai hoặc vào trạng thái Chờ duyệt.",
  "Smart TV chỉ đọc; có hướng dẫn kèm mã QR để chuyển sang điện thoại/website khi muốn tham gia bình luận.",
 ]),
 p("Giai đoạn sau — các luồng chưa có thiết kế trên Figma hoặc đã quyết định hoãn (ghi nhận để lập kế hoạch, không đặc tả chi tiết trong tài liệu này):", bold=True),
 table(["Hạng mục", "Lý do / ghi chú"], [
  ["US03 Đánh giá phim", "Ứng dụng hiện chỉ có đánh giá ứng dụng; đánh giá phim là tính năng mới cần thiết kế và nghiệp vụ riêng. Thiết kế đang ẩn trên Figma Phone/Web."],
  ["US06 Bình luận kèm mốc thời gian", "Chưa có thiết kế highlight và thông báo mốc không hợp lệ. Chuỗi thời gian trong nội dung hiển thị như văn bản thường, không bấm được."],
  ["US18 Chia sẻ bình luận", "Bỏ bảng chia sẻ hệ điều hành và deep link cài ứng dụng; chỉ giữ deep link nội bộ phục vụ thông báo (US09)."],
  ["US07 Thích và US10 Báo cáo trên Smart TV", "Thiết kế đã ẩn trên Figma TV; Smart TV giai đoạn này chỉ đọc và hiển thị huy hiệu."],
  ["Phân hệ CMS quản trị bình luận: US11 Kiểm duyệt AI hai chế độ (phần cấu hình), US12 Quản lý trạng thái và phạm vi hiển thị (phần công cụ), US13 Tra cứu và xử lý nội dung, US14 Xử lý hàng chờ, US15 Ghim/cấu hình/từ khóa chặn, US16 Chế tài và nhật ký kiểm toán", "Chưa có thiết kế giao diện CMS. Các hành vi phía máy chủ mà luồng Đăng bình luận (US04) và Báo cáo (US10) phụ thuộc — kiểm duyệt tự động, trạng thái Chờ duyệt, tiếp nhận báo cáo — được mô tả ngay trong UR04 và UR10 ở mức cần thiết; việc xử lý thủ công, chế tài, khiếu nại và phản hồi kết quả tới người dùng thuộc giai đoạn sau."],
  ["US19 Thống kê hoạt động, US20 AI hỗ trợ vận hành", "Thuộc CMS/phân tích, chưa có thiết kế."],
  ["Định dạng văn bản (Đậm, Nghiêng, Gạch chân, Làm mờ, Chèn liên kết)", "Đội phát triển và Ban sản phẩm thống nhất không làm trong giai đoạn này; văn bản thuần trên mọi nền tảng."],
  ["Nickname riêng cho cộng đồng", "Dùng tên hiển thị sẵn có của tài khoản MyTV."],
  ["Khiếu nại chế tài trong ứng dụng; công tắc thông báo cộng đồng; màn hình chặn đăng nhập khi khóa tài khoản", "Phụ thuộc phân hệ CMS và Xác thực; chưa có thiết kế."],
  ["Nội dung phát trực tiếp; thể thao/thiếu nhi/giải trí; frame/clip đính kèm; trả lời lồng nhiều cấp; tin nhắn riêng", "Ngoài mục tiêu sản phẩm của tính năng Bình luận phim truyện/VOD."],
 ], [40, 60], caption="Bảng 2: Hạng mục giai đoạn sau"),
 h2("Tài liệu liên quan"),
 table(["STT", "Tên tài liệu", "Tên file / nguồn"], [
  ["1", "Backlog sản phẩm: 5 Epic, 20 User Story và các quyết định nghiệp vụ đã khóa", "README.md"],
  ["2", "Nhật ký rà soát và quyết định chốt kịch bản V5 (02/11/2026)", "CHANGELOG_RASOAT_V5.md"],
  ["3", "Bảng feedback kịch bản bình luận của đội phát triển kèm phản hồi của Ban sản phẩm (06/11/2026)", "feedback_figma_tinh_nang_kich_ban.xlsx (Google Sheets)"],
  ["4", "Kiến trúc giải pháp tính năng Bình luận MyTV", "SOLUTION_ARCHITECTURE.md"],
  ["5", "Yêu cầu chéo: Accessibility WCAG 2.1 AA và Bảo mật", "REQUIREMENTS_A11Y_SECURITY.md"],
  ["6", "Bản đồ kiến trúc thông tin và danh mục màn hình", "UX_INFORMATION_ARCHITECTURE_SCREEN_MAP.md"],
  ["7", "Chi tiết 20 User Story kèm tiêu chí chấp nhận và user flow", "EP01 … EP05 (thư mục theo Epic)"],
  ["8", "Thiết kế giao diện Phone — trang “Bình luận App”", "Figma: [Phone] Play Nội dung, node 39753-12055"],
  ["9", "Thiết kế giao diện Web — trang “Tính năng bình luận”", "Figma: [Web] Play Nội dung, node 16065-2741"],
  ["10", "Thiết kế giao diện Smart TV — trang “Bình luận SmartTV”", "Figma: [TV] Trang chủ, node 86-40747"],
  ["11", "Danh sách ghi chú [BA] đã đặt trên Figma", "FIGMA_BA_NOTES.md"],
 ], [7, 55, 38]),
 h2("Giải thích từ ngữ và các chữ viết tắt"),
 table(["Thuật ngữ", "Ý nghĩa"], [
  ["Scope (phạm vi bình luận)", "Đơn vị nội dung mà một khu vực bình luận gắn vào: luôn là một bộ phim (phim lẻ hoặc cả bộ phim bộ)"],
  ["Root comment", "Bình luận gốc, không phải trả lời của bình luận khác"],
  ["Reply", "Trả lời một bình luận gốc; hệ thống chỉ hỗ trợ một cấp"],
  ["Guest", "Người xem chưa đăng nhập; chỉ được đọc bình luận công khai"],
  ["Hồ sơ Trẻ em", "Hồ sơ xem dành cho trẻ em trong tài khoản MyTV; không hiển thị khu vực bình luận"],
  ["Tên hiển thị", "Tên tài khoản MyTV hiện có; nếu rỗng thì số điện thoại đã che dạng 0***123"],
  ["Blacklist từ khóa", "Danh sách từ khóa toàn hệ thống; nội dung khớp bị chặn ngay khi gửi, không gọi AI"],
  ["Chế độ 1 (Mode 1)", "Chế độ kiểm duyệt AI: rủi ro Nhẹ hiển thị ngay, Trung bình vào Chờ duyệt, Nặng bị chặn"],
  ["Chế độ 2 (Mode 2)", "Chế độ kiểm duyệt AI: Nhẹ và Trung bình đều vào Chờ duyệt, Nặng bị chặn"],
  ["Chờ duyệt", "Trạng thái nội dung đã gửi nhưng chưa công khai, chỉ tác giả thấy; chờ xử lý thủ công"],
  ["Ghim (Pin)", "Bình luận được quản trị viên ghim lên đầu danh sách, tối đa 3 trên một scope; hiển thị bằng marker riêng cạnh tên, không phải huy hiệu"],
  ["Sắp xếp Nổi bật", "Chế độ sắp xếp mặc định dùng Featured Score"],
  ["Huy hiệu Nổi bật", "Huy hiệu tự động cấp toàn MyTV, hiển thị cạnh tên; khác với Ghim và khác với sắp xếp Nổi bật"],
  ["Featured Score", "Điểm nổi bật của bình luận: 0,5×ln(1+Like) + 0,3×ln(1+Reply) + 0,2×e^(-AgeHours/72)"],
  ["Net Like", "Số lượt Thích công khai hiện tại của một bình luận"],
  ["Overlay (màn tối)", "Lớp phủ tối trên trình phát và nội dung bên dưới khi người dùng đang thao tác với bình luận; chặn mọi tương tác với các lớp dưới, video vẫn phát"],
  ["Màn Bình luận của nội dung", "Màn toàn màn hình (không trình phát) hiển thị thẻ phim và danh sách bình luận của phim, mở từ thông báo"],
  ["Khóa bình luận (scope Đóng)", "Quản trị viên đóng khu vực bình luận của một bộ phim; ứng dụng hiển thị trạng thái “Bình luận đang bị khóa”"],
  ["CMS", "Content Management System — hệ thống quản trị nội dung (giai đoạn sau)"],
  ["STB", "Set-top box — đầu thu truyền hình MyTV"],
  ["PII", "Personally Identifiable Information — thông tin định danh cá nhân"],
  ["WCAG 2.1 AA", "Bộ tiêu chuẩn khả năng tiếp cận nội dung web, mức AA"],
 ], [26, 74]),
]

# ======================= II. TỔNG QUAN HỆ THỐNG =======================
body += [h1("TỔNG QUAN HỆ THỐNG"), h2("Mục tiêu hệ thống"),
 table(["STT", "Mã mục tiêu", "Tên mục tiêu", "Đối tượng liên quan", "Mức độ ưu tiên"], [
  ["1", "MT01", "Tạo không gian thảo luận quanh nội dung, tăng thời lượng xem và tần suất quay lại", "Người xem, Ban sản phẩm", "Cao"],
  ["2", "MT02", "Chuyển đổi người xem thụ động thành người dùng có tài khoản (đọc tự do, đăng nhập để tương tác)", "Người xem chưa đăng nhập, Ban sản phẩm", "Cao"],
  ["3", "MT03", "Giữ môi trường an toàn bằng kiểm duyệt tự động khi đăng (từ khóa, AI) và cơ chế báo cáo từ cộng đồng", "Người xem, Bộ phận vận hành nội dung", "Cao"],
  ["4", "MT04", "Tạo cơ chế ghi nhận đóng góp qua huy hiệu", "Người xem", "Trung bình"],
  ["5", "MT05", "Bảo đảm khả năng tiếp cận WCAG 2.1 AA và các yêu cầu bảo mật XSS/IDOR/PII xuyên suốt", "Toàn bộ đối tượng", "Cao"],
  ["6", "MT06", "Trải nghiệm thống nhất trên Phone, Web và Smart TV theo đúng bộ thiết kế Figma đã chốt", "Người xem, Đội thiết kế, Đội phát triển", "Cao"],
 ], [5, 11, 29, 32, 23]),
 h2("Đối tượng người dùng của hệ thống"),
 p("Hệ thống Bình luận là một miền nghiệp vụ mới, tiêu thụ các dịch vụ sẵn có của MyTV (Xác thực/SSO và hồ sơ tài khoản, Dịch vụ Nội dung, Trình phát video, Dịch vụ Push, Nhà cung cấp AI) chứ không thay thế chúng. Trình phát video chỉ cung cấp ngữ cảnh bộ phim đang xem; hệ thống không điều khiển trình phát."),
 table([{"text": "STT", "rowspan": 2}, {"text": "Tên đối tượng", "rowspan": 2}, {"text": "Mô tả", "rowspan": 2}, {"text": "Tương tác với hệ thống", "colspan": 2}, {"text": "Lợi ích mong đợi", "rowspan": 2}], [
  [{"text": "Vào", "bold": True, "align": "center", "shade": "D9D9D9"}, {"text": "Ra", "bold": True, "align": "center", "shade": "D9D9D9"}],
  ["1", "Người xem chưa đăng nhập (Guest)", "Khán giả đang xem phim truyện/VOD trên MyTV nhưng chưa đăng nhập", "Mở tab/khu vực Bình luận, cuộn danh sách, đổi cách sắp xếp, mở thread phản hồi, bung bình luận dài", "Danh sách bình luận công khai, số lượng bình luận, thanh nhắc đăng nhập", "Tham khảo cảm nhận cộng đồng trước và trong khi xem"],
  ["2", "Người xem đã đăng nhập", "Khán giả có tài khoản MyTV, được thực hiện toàn bộ thao tác tương tác", "Gửi bình luận, trả lời, thích, nhắc tên, báo cáo, sửa, xóa và hủy đăng nội dung của mình", "Bình luận đã đăng kèm trạng thái, thông báo tương tác, huy hiệu", "Bày tỏ cảm nhận, thảo luận với cộng đồng và được ghi nhận đóng góp"],
  ["3", "Người xem trên Smart TV", "Khán giả xem trên Smart TV/STB, đã hoặc chưa đăng nhập", "Mở bảng bình luận, cuộn, chọn card để xem đủ nội dung và thread phản hồi", "Danh sách bình luận chỉ đọc, chip huy hiệu, hướng dẫn QR chuyển sang điện thoại", "Theo dõi thảo luận ngay trên màn hình lớn"],
  ["4", "Hồ sơ Trẻ em", "Hồ sơ xem dành cho trẻ em trong một tài khoản MyTV", "Không có", "Không hiển thị khu vực Bình luận trên mọi nền tảng", "Không tiếp xúc nội dung do người dùng tạo"],
  ["5", "Bộ phận vận hành nội dung", "Nhân sự xử lý hàng chờ Chờ duyệt và báo cáo vi phạm (công cụ CMS thuộc giai đoạn sau)", "Duyệt/từ chối nội dung chờ duyệt, xử lý báo cáo, ghim bình luận, cấu hình chế độ kiểm duyệt và từ khóa chặn", "Kết quả xử lý phản ánh lên ứng dụng qua trạng thái nội dung", "Kiểm soát chất lượng nội dung"],
 ], [5, 13, 20, 22, 22, 18], caption="Bảng 3: Đối tượng người dùng và tương tác với hệ thống"),
]

# ======================= III. QUY TRÌNH NGHIỆP VỤ =======================
body += [h1("QUY TRÌNH NGHIỆP VỤ"), h2("Quy trình nghiệp vụ tổng thể"),
 p("Quy trình tổng thể đi từ lúc người xem mở khu vực bình luận, qua kiểm duyệt tự động khi đăng, tới lúc nội dung được hiển thị công khai, kèm các nhánh tương tác (thích, trả lời, nhắc tên, báo cáo) và huy hiệu. Các bước xử lý thủ công trên CMS thuộc giai đoạn sau và chỉ được nhắc tới như điểm tiếp nhận."),
 p("Quy ước đánh mã bước quy trình:", bold=True),
 bullets(["Mỗi bước được đánh mã theo dạng CMT.xx.<Tên bước>, với xx chạy từ 01 đến 99.", "Quy trình con mang cả mã quy trình mẹ: CMT.xx.yy.<Tên bước con>."]),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["B01", "Mở khu vực bình luận", "Người xem", "Người xem chọn tab Bình luận (Phone), cuộn tới khu vực Bình luận (Web) hoặc bấm nút Bình luận trên thanh điều khiển (Smart TV). Hệ thống hiển thị số lượng bình luận (gốc + trả lời công khai) và danh sách theo sắp xếp Nổi bật. Hồ sơ Trẻ em không thấy khu vực này."],
  ["B02", "Xác định quyền tương tác", "Hệ thống", "Guest chỉ được đọc. Khi guest chọn một thao tác tương tác, hệ thống điều hướng sang đăng nhập rồi quay lại đúng phim/thread/bình luận, không tự thực hiện lại thao tác cũ. Smart TV chỉ đọc với mọi trạng thái đăng nhập."],
  ["B03", "Gửi nội dung", "Người xem đã đăng nhập", "Người dùng gửi bình luận, trả lời hoặc bản sửa dưới dạng văn bản thuần. Hệ thống kiểm tra độ dài 1–500 ký tự, tên miền liên kết, ký tự đối kháng và giới hạn tần suất."],
  ["B04", "Chặn theo danh sách từ khóa", "Hệ thống", "Đối chiếu nội dung với danh sách từ khóa chặn toàn hệ thống (không phân biệt hoa/thường, có chuẩn hóa dấu). Khớp → chặn ngay, không gọi AI, hiển thị “Bình luận không được chấp thuận”."],
  ["B05", "Phân loại bằng AI", "Hệ thống — AI Adapter", "AI phân loại rủi ro Nhẹ / Trung bình / Nặng. Timeout 5 giây, lỗi hoặc ngôn ngữ ngoài Việt/Anh đều chuyển sang Chờ duyệt."],
  ["B06", "Quyết định hiển thị theo chế độ", "Hệ thống", "Chế độ 1: Nhẹ hiển thị ngay, Trung bình vào Chờ duyệt. Chế độ 2: Nhẹ và Trung bình đều vào Chờ duyệt. Nặng bị chặn ngay tại thời điểm gửi. Nội dung Chờ duyệt hiển thị riêng cho tác giả kèm lựa chọn Chỉnh sửa hoặc Hủy đăng."],
  ["B07", "Xử lý nội dung chờ duyệt", "Bộ phận vận hành nội dung", "Điểm tiếp nhận của giai đoạn sau (CMS): nội dung Chờ duyệt được duyệt hoặc từ chối; kết quả phản ánh lên ứng dụng qua trạng thái nội dung."],
  ["B08", "Hiển thị công khai và tương tác", "Người xem", "Nội dung hợp lệ được hiển thị; người dùng đã đăng nhập trên Phone/Web có thể Thích, Trả lời, Nhắc tên và Báo cáo."],
  ["B09", "Tiếp nhận báo cáo vi phạm", "Người xem đã đăng nhập / Bộ phận vận hành nội dung", "Người dùng báo cáo theo bộ lý do chuẩn; hệ thống ghi nhận và báo thành công. Báo cáo không tự động ẩn nội dung; việc xử lý và phản hồi kết quả thuộc giai đoạn sau."],
  ["B10", "Gửi thông báo", "Hệ thống", "Người được trả lời/nhắc tên nhận thông báo trong ứng dụng và push; bấm thông báo mở màn Bình luận của nội dung hoặc thread tương ứng."],
  ["B11", "Xét và hiển thị huy hiệu", "Hệ thống", "Hằng ngày xét tiêu chí Fan tích cực (7 ngày), Fan kỳ cựu (30 ngày) và Nổi bật; hiển thị tối đa một chip huy hiệu cạnh tên trên mọi nền tảng."],
 ], [10, 20, 18, 52], caption="Bảng 4: Mô tả các bước của quy trình nghiệp vụ tổng thể"),
 h2("Quy trình nghiệp vụ chi tiết"),
 note("[Ảnh màn hình trích từ Figma Phone (375×812), Web (1920×1080) và Smart TV (1920×1080) theo hiện trạng ngày 06/11/2026. Một số ghi chú [BA] trên Figma vẫn đang chờ đội thiết kế xử lý; khi thiết kế cập nhật, ảnh sẽ được thay theo cùng vị trí.]"),
]

# ---- 3.2.1 US01 Đọc ----
body += [h3("US01 — Quy trình đọc khu vực bình luận"),
 p("Quy trình mô tả hai nhánh chưa đăng nhập và đã đăng nhập, trạng thái tải khung xương, trạng thái rỗng, trạng thái scope bị khóa, bình luận dài kèm “Xem thêm” và lối vào thread Phản hồi. Khu vực bình luận gắn với bộ phim: phim bộ mặc định mở tab Các tập, phim lẻ mặc định mở tab Tương tự; đổi tập không tải lại bình luận."),
 img(FL+"US01.jpg", 16, cap(f"Lưu đồ đọc khu vực bình luận (US01) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.01.B01", "Mở trang nội dung", "Người xem", "Phone: phim bộ mở tab Các tập, phim lẻ mở tab Tương tự; tab Bình luận hiển thị nhãn “Bình luận ({count})”. Web: khu vực “Bình luận ({count})” nằm trong trang phim. Smart TV: nút Bình luận trên thanh điều khiển mở bảng bình luận bên phải trình phát với tiêu đề “Bình luận · {count}”. Hồ sơ Trẻ em: không hiển thị tab/khu vực/nút."],
  ["CMT.01.B02", "Tải danh sách", "Hệ thống", "Hiển thị khung xương trong lúc tải, sau đó trả 10 bình luận gốc đầu tiên theo sắp xếp Nổi bật (tối đa 3 bình luận ghim đứng đầu), tải thêm 10 mục mỗi lần cuộn. Số đếm = bình luận gốc + trả lời công khai; từ 1.000 viết tắt 1,2K, từ 1.000.000 viết tắt 1,2M."],
  ["CMT.01.B03", "Hiển thị theo trạng thái đăng nhập", "Hệ thống", "Guest thấy thanh “Đăng nhập để bình luận”. Người đã đăng nhập thấy ô soạn bình luận: Phone là thanh nhập cố định đáy màn hình; Web là ô nhập ở đầu khu vực Bình luận. Smart TV luôn hiển thị dải nhắc “Mở ứng dụng MyTV trên thiết bị di động hoặc website để thêm bình luận và trả lời”."],
  ["CMT.01.B04", "Hiển thị card bình luận", "Hệ thống", "Mỗi card gồm avatar, tên hiển thị, marker Ghim (nếu có), tối đa một huy hiệu, thời gian tương đối (" + TIME_FMT + "), nội dung, nút Thích kèm số, nút Trả lời, lối vào “{n} Phản hồi”, menu ⋮. Không có dấu hiệu riêng phân biệt bình luận của chính mình; sự khác biệt chỉ nằm ở menu ⋮ (Sửa/Xóa thay vì Báo cáo)."],
  ["CMT.01.B05", "Bình luận dài — Xem thêm", "Người xem", "Phone và Web: nội dung dài hơn 4 dòng được cắt, cuối dòng 4 có liên kết “Xem thêm”; bấm để bung đủ nội dung ngay tại chỗ, không có “Thu gọn”. Smart TV: card trong danh sách cắt nội dung bằng “…”; chọn card để mở trang Phản hồi hiển thị đủ nội dung."],
  ["CMT.01.B06", "Mở thread Phản hồi", "Người xem", "Phone: màn “Phản hồi” riêng; Web: mở rộng inline dưới bình luận gốc, có “Thu gọn”; Smart TV: trang Phản hồi chỉ đọc. Thread tải 3 trả lời đầu theo thứ tự cũ → mới, nút “Xem thêm {n} phản hồi” tải tối đa 10 mục mỗi lần."],
  ["CMT.01.B07", "Trạng thái đặc biệt", "Hệ thống", "Chưa có bình luận: trạng thái rỗng “Hãy là người đăng bình luận đầu tiên”. Scope bị khóa: giữ tab nhưng bỏ số đếm, ẩn danh sách và ô soạn, hiển thị minh họa ổ khóa kèm “Bình luận đang bị khóa. Vui lòng thử lại sau”. Lỗi tải: cho thử lại."],
 ], [12, 20, 16, 52]),
 img(PH+"01_list_nologin.png", PW, cap("Phone — Tab Bình luận ở trạng thái chưa đăng nhập, có danh sách công khai và thanh nhắc đăng nhập")),
 img(PH+"03_skeleton.png", PW, cap("Phone — Khung xương trong lúc tải danh sách")),
 img(PH+"04_list_login.png", PW, cap("Phone — Danh sách bình luận khi đã đăng nhập, ô soạn cố định đáy màn hình")),
 img(PH+"24_empty_state.png", PW, cap("Phone — Trạng thái rỗng: chưa có bình luận nào")),
 img(PH+"40229_30039.png", PW, cap("Phone — Trạng thái khu vực bình luận bị khóa")),
 img(PH+"xemthem_1_41153_21376.png", PW, cap("Phone — Bình luận dài được cắt 4 dòng kèm liên kết Xem thêm")),
 img(PH+"xemthem_2_41153_21710.png", PW, cap("Phone — Bình luận dài sau khi bấm Xem thêm, bung đủ nội dung tại chỗ")),
 img(WB+"16107_22582.jpg", 16, cap("Web — Khu vực Bình luận trong trang phim khi chưa đăng nhập: thẻ nhắc đăng nhập, Sắp xếp theo, danh sách và liên kết Xem thêm")),
]

# ---- US01 trên Smart TV ----
TW = 15
body += [p("Giao diện Smart TV — US01 Đọc khu vực bình luận", bold=True),
 p("Trên Smart TV người xem điều khiển bằng remote: nút Bình luận nằm trên thanh điều khiển của trình phát; bảng bình luận mở ở nửa phải màn hình, video thu nhỏ bên trái và tiếp tục phát. Tiêu điểm (focus) di chuyển theo thứ tự dải nhắc → các card; nhấn Click trên card mở trang Phản hồi; nhấn BACK quay lại. Luồng cho phim bộ và phim lẻ giống nhau (chỉ khác tiêu đề có số tập) vì bình luận ở cấp phim. Quản trị viên đóng bình luận của phim thì thanh điều khiển không hiển thị nút Bình luận."),
 img(TV+"us01_overview.jpg", 16, cap("Smart TV — Lưu đồ Figma US01 Đọc khu vực bình luận (các nhánh phim bộ/phim lẻ, phản hồi, xem thêm, hướng dẫn mở ứng dụng)")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.01.TV.B01", "Mở bảng bình luận", "Người xem", "Trên thanh điều khiển trình phát, di chuyển tiêu điểm tới nút “Bình luận” và nhấn Click. Nếu quản trị viên đã đóng bình luận của phim thì nút này không xuất hiện."],
  ["CMT.01.TV.B02", "Tải danh sách", "Hệ thống", "Video thu nhỏ sang trái, bảng “Bình luận · {count}” hiện bên phải với khung xương trong lúc tải; sau đó hiển thị dải nhắc “Mở ứng dụng MyTV trên thiết bị di động hoặc website để thêm bình luận và trả lời” (tiêu điểm mặc định) và danh sách card theo sắp xếp Nổi bật, tải thêm khi cuộn tới cuối."],
  ["CMT.01.TV.B03", "Duyệt card", "Người xem", "Di chuyển tiêu điểm xuống từng card (card có tiêu điểm nền sáng). Card hiển thị avatar, tên, chip huy hiệu hoặc marker Ghim, thời gian tương đối, nội dung (cắt bằng “…” khi dài), số lượt thích và số phản hồi. Chưa có bình luận → trạng thái rỗng “Hãy là người đầu tiên bình luận về nội dung này”."],
  ["CMT.01.TV.B04", "Xem phản hồi / xem đủ nội dung", "Người xem", "Nhấn Click trên card mở trang “Phản hồi”: bình luận gốc hiển thị đủ nội dung ở đầu, bên dưới là các phản hồi một cấp (chỉ đọc). Nhấn Click trên một phản hồi mở trang Phản hồi của phản hồi đó (chỉ có nội dung, không có phản hồi con). Nhấn BACK quay lại danh sách."],
  ["CMT.01.TV.B05", "Hướng dẫn tham gia bình luận", "Người xem", "Nhấn Click trên dải nhắc mở trang “Cách thêm bình luận và phản hồi”: bước 1 quét mã QR tải ứng dụng MyTV SmartPhone, bước 2 đăng nhập và tham gia bình luận; hiển thị tổng đài 1800 1166. Nhấn BACK quay lại."],
 ], [14, 20, 14, 52]),
 img(TV+"tv_us01_r1_c1_71_3221.jpg", TW, cap("Smart TV — Trình phát phim bộ với nút Bình luận trên thanh điều khiển")),
 img(TV+"tv_us01_r1_c2_73_7691.jpg", TW, cap("Smart TV — Nút Bình luận đang có tiêu điểm")),
 img(TV+"tv_us01_r2_c2_78_10112.jpg", TW, cap("Smart TV — Phim đã đóng bình luận: thanh điều khiển không có nút Bình luận")),
 img(TV+"tv_us01_r1_c3_79_22313.jpg", TW, cap("Smart TV — Khung xương trong lúc tải bảng bình luận")),
 img(TV+"tv_us01_r1_c4_71_3916.jpg", TW, cap("Smart TV — Bảng bình luận, tiêu điểm mặc định ở dải nhắc chuyển sang điện thoại/website")),
 img(TV+"tv_us01_r1_c5_78_10487.jpg", TW, cap("Smart TV — Tiêu điểm chuyển xuống card bình luận đầu tiên")),
 img(TV+"tv_us01_r2_c3_84_40002.jpg", TW, cap("Smart TV — Trạng thái rỗng: chưa có bình luận")),
 img(TV+"tv_us01_r5_c5_233_4295.jpg", TW, cap("Smart TV — Card có tiêu điểm với nội dung dài bị cắt bằng dấu ba chấm")),
 img(TV+"tv_us01_r6_c5_233_4296.jpg", TW, cap("Smart TV — Trang Phản hồi hiển thị đủ nội dung bình luận gốc dài")),
 img(TV+"tv_us01_r2_c4_148_4134.jpg", TW, cap("Smart TV — Trang Phản hồi của bình luận chưa có phản hồi nào")),
 img(TV+"tv_us01_r5_c1_82_32806.jpg", TW, cap("Smart TV — Trang Phản hồi: bình luận gốc và các phản hồi một cấp")),
 img(TV+"tv_us01_r5_c2_82_32931.jpg", TW, cap("Smart TV — Tiêu điểm trên một phản hồi trong trang Phản hồi")),
 img(TV+"tv_us01_r5_c3_82_33242.jpg", TW, cap("Smart TV — Nhấn Click trên phản hồi: trang Phản hồi của phản hồi đó (không có phản hồi con)")),
 img(TV+"tv_us01_r2_c5_78_10689.jpg", TW, cap("Smart TV — Trang Phản hồi theo thiết kế hiện tại; các nút Thích và Báo cáo trên bình luận gốc thuộc giai đoạn sau")),
 img(TV+"tv_us01_r3_c1_79_23737.jpg", TW, cap("Smart TV — Trình phát phim lẻ: luồng giống phim bộ, chỉ khác tiêu đề không có số tập")),
 img(TV+"tv_us01_r6_c1_86_40605.jpg", TW, cap("Smart TV — Nhấn Click trên dải nhắc để mở hướng dẫn")),
 img(TV+"tv_us01_r6_c2_86_40747.jpg", TW, cap("Smart TV — Trang Cách thêm bình luận và phản hồi: mã QR tải ứng dụng, đăng nhập, tổng đài 1800 1166")),
]

# ---- US02 Sắp xếp ----
body += [h3("US02 — Quy trình xem số lượng và sắp xếp bình luận"),
 p("Người xem đổi cách sắp xếp giữa Nổi bật (mặc định), Mới nhất và Nhiều lượt thích. Phone dùng bottom sheet “Sắp xếp theo”, Web dùng dropdown cùng tên; Smart TV không có điều khiển sắp xếp và luôn dùng Nổi bật. Mở một bộ phim khác thì sắp xếp trở về Nổi bật; đổi tập trong cùng bộ phim giữ nguyên."),
 img(FL+"US02.jpg", 11, cap(f"Lưu đồ tải thêm và sắp xếp bình luận (US02) — {FLOW_NOTE}")),
 img(PH+"06_sort_sheet.png", PW, cap("Phone — Bottom sheet Sắp xếp theo: Nổi bật, Mới nhất, Nhiều lượt thích")),
 img(WB+"web_sort.jpg", 16, cap("Web — Dropdown Sắp xếp theo")),
]

# ---- US04 Đăng ----
body += [h3("US04 — Quy trình đăng bình luận qua kiểm duyệt tự động"),
 p("Đây là quy trình lõi của hệ thống, quyết định nội dung được hiển thị ngay, vào trạng thái Chờ duyệt hay bị chặn tại thời điểm gửi. Bình luận là văn bản thuần tối đa 500 ký tự; không có định dạng. Phần xử lý thủ công nội dung Chờ duyệt thuộc giai đoạn sau."),
 img(FL+"US04.jpg", 16, cap(f"Lưu đồ đăng bình luận qua kiểm duyệt (US04) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.02.B01", "Mở ô soạn bình luận", "Người xem đã đăng nhập", "Phone: thanh nhập cố định đáy màn hình nở lên tối đa 3 dòng khi bàn phím bật; đồng thời hiện overlay tối chặn tương tác với trình phát và nội dung bên dưới, video vẫn phát; bấm vùng tối để đóng. Web: ô nhập nội tuyến ở đầu khu vực Bình luận."],
  ["CMT.02.B02", "Soạn nội dung", "Người xem đã đăng nhập", "Văn bản thuần, có thể gõ @ để nhắc tên. Bộ đếm ký tự hiển thị khi gần ngưỡng; vượt 500 ký tự thì bộ đếm chuyển đỏ, nút gửi bị vô hiệu và hiện thông báo “Bạn đã vượt quá 500 ký tự”."],
  ["CMT.02.B03", "Kiểm tra hợp lệ tại client", "Hệ thống", "Độ dài 1–500 ký tự, chặn nội dung chỉ có khoảng trắng, chỉ cho liên kết thuộc mytv.com.vn và tên miền con thực, chuẩn hóa ký tự đối kháng."],
  ["CMT.02.B04", "Kiểm tra giới hạn tần suất", "Hệ thống", "Tối đa 5 nội dung Bình luận và Trả lời trong 1 phút cho mỗi người dùng; riêng thao tác Sửa tối đa 5 lần/phút trên mỗi bình luận."],
  ["CMT.02.B05", "Chặn theo danh sách từ khóa", "Hệ thống", "Khớp từ khóa trong danh sách chặn toàn hệ thống → chặn ngay, không gọi AI; hiển thị lỗi nội tuyến “Bình luận không được chấp thuận”, nội dung giữ trong ô để người dùng sửa."],
  ["CMT.02.B06", "Gọi AI phân loại", "Hệ thống — AI Adapter", "Timeout 5 giây; lỗi, dịch vụ không khả dụng, ngôn ngữ ngoài Việt/Anh hoặc độ tin cậy thấp đều chuyển sang Chờ duyệt."],
  ["CMT.02.B07", "Áp quyết định theo chế độ", "Hệ thống", "Chế độ 1: Nhẹ hiển thị ngay, Trung bình vào Chờ duyệt. Chế độ 2: Nhẹ và Trung bình đều vào Chờ duyệt. Nặng bị chặn với cùng thông báo như bước B05."],
  ["CMT.02.B08", "Hiển thị trạng thái Chờ duyệt cho tác giả", "Hệ thống", "Card mờ kèm dòng “Bình luận của bạn sẽ sớm được xuất hiện”, chỉ tác giả thấy. Menu ⋮ gồm “Chỉnh sửa bình luận” (bản sửa thay thế bản đang chờ và đi lại kiểm duyệt) và “Hủy đăng bình luận” (gỡ khỏi hàng chờ, toast “Đã hủy bình luận”, không hoàn quota tần suất)."],
  ["CMT.02.B09", "Công khai nội dung", "Hệ thống", "Nội dung Nhẹ ở Chế độ 1 công khai ngay; nội dung Chờ duyệt công khai sau khi được duyệt (giai đoạn sau). Số đếm trên tab cập nhật ở lần tải kế tiếp."],
 ], [12, 20, 16, 52]),
 img(PH+"21_composer_typing.png", PW, cap("Phone — Ô soạn khi bàn phím bật, overlay tối phủ trình phát")),
 img(PH+"22_rejected.png", PW, cap("Phone — Nội dung bị chặn tại thời điểm gửi: lỗi nội tuyến “Bình luận không được chấp thuận”")),
 img(PH+"40195_82744.png", PW, cap("Phone — Bình luận đang Chờ duyệt (chỉ tác giả thấy) và menu Chỉnh sửa / Hủy đăng")),
 img(WB+"web_500char_limit.jpg", 16, cap("Web — Trạng thái vượt quá 500 ký tự")),
 img(WB+"web_pending_moderation.jpg", 16, cap("Web — Bình luận chờ xét duyệt")),
]

# ---- US05 Sửa/Xóa ----
body += [h3("US05 — Quy trình sửa và xóa bình luận"),
 p("Kết quả của một lần sửa phụ thuộc chế độ kiểm duyệt của phim: khi bản mới đang chờ duyệt thì bản cũ vẫn công khai. Người dùng tự xóa bình luận gốc sẽ kéo theo toàn bộ trả lời bị xóa mềm, giữ 90 ngày."),
 img(FL+"US05.jpg", 11, cap(f"Lưu đồ sửa và xóa bình luận (US05) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.03.B01", "Mở menu của bình luận của mình", "Người xem đã đăng nhập", "Menu ⋮ của bình luận do chính mình tạo gồm Chỉnh sửa bình luận và Xóa bình luận; bình luận của người khác chỉ có Báo cáo bình luận."],
  ["CMT.03.B02", "Sửa", "Người xem đã đăng nhập", "Nội dung cũ được nạp vào ô soạn; áp dụng cùng ràng buộc và cùng kiểm duyệt tự động như đăng mới. Bản được công khai mang nhãn “Đã chỉnh sửa”; toast “Chỉnh sửa thành công”."],
  ["CMT.03.B03", "Xóa", "Người xem đã đăng nhập", "Hộp thoại xác nhận: không có trả lời → “Bình luận này sẽ bị xóa và không thể khôi phục lại”; có trả lời → cảnh báo toàn bộ phản hồi liên quan sẽ bị xóa theo. Xác nhận → xóa mềm, toast “Xóa bình luận thành công”."],
 ], [12, 20, 16, 52]),
 img(PH+"16_own_kebab_edit_delete.png", PW, cap("Phone — Menu của bình luận của mình: Chỉnh sửa / Xóa")),
 img(PH+"17_delete_dialog.png", PW, cap("Phone — Xác nhận xóa bình luận không có trả lời")),
 img(PH+"18_delete_dialog_has_reply.png", PW, cap("Phone — Xác nhận xóa bình luận có trả lời")),
 img(PH+"19_edited_toast.png", PW, cap("Phone — Sửa thành công, bình luận mang nhãn Đã chỉnh sửa")),
 img(WB+"web_editdelete_menu.jpg", 16, cap("Web — Menu Chỉnh sửa / Xóa trên bình luận của mình")),
]

# ---- US07 Thích ----
body += [h3("US07 — Quy trình thích và bỏ thích bình luận"),
 p("Thích/Bỏ thích trên Phone và Web dùng giao diện lạc quan: biểu tượng tô đặc màu cam kèm số đếm màu cam khi đã thích, viền xám khi chưa thích. Thao tác được gom theo lô tối đa 5 giây rồi đồng bộ về máy chủ; nhiều lần Thích/Bỏ thích liên tiếp trên cùng đối tượng trong một lô được gộp về trạng thái cuối cùng. Smart TV chỉ hiển thị số lượt thích (thao tác Thích trên TV thuộc giai đoạn sau)."),
 img(FL+"US07.jpg", 15, cap(f"Lưu đồ Thích và Bỏ thích bình luận (US07) — {FLOW_NOTE}")),
 img(PH+"20_like_a.png", PW, cap("Phone — Bình luận chưa thích")),
 img(PH+"20_like_b.png", PW, cap("Phone — Bình luận đã thích, biểu tượng và số đếm chuyển màu cam")),
]

# ---- US08 Trả lời ----
body += [h3("US08 — Quy trình trả lời bình luận một cấp"),
 p("Trả lời chỉ sâu một cấp. Trả lời một trả lời khác vẫn nằm trong cùng thread và ô soạn được điền sẵn @tên tác giả của trả lời đó. Thứ tự trả lời là cũ → mới; trả lời vừa gửi được thêm vào cuối danh sách và tự cuộn tới."),
 img(FL+"US08.jpg", 16, cap(f"Lưu đồ trả lời bình luận một cấp (US08) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.04.B01", "Mở thread", "Người xem", "Phone: bấm nút Trả lời hoặc “{n} Phản hồi” mở màn “Phản hồi” (bình luận gốc ở đầu, các trả lời nối bằng đường chỉ). Web: mở rộng inline dưới bình luận gốc, ô nhập trả lời xuất hiện ngay dưới gốc."],
  ["CMT.04.B02", "Soạn trả lời", "Người xem đã đăng nhập", "Ô soạn điền sẵn @tên người được trả lời; cùng ràng buộc 1–500 ký tự và cùng kiểm duyệt tự động như bình luận gốc."],
  ["CMT.04.B03", "Hiển thị kết quả", "Hệ thống", "Trả lời hợp lệ xuất hiện cuối thread; số “{n} Phản hồi” trên bình luận gốc cập nhật. Trả lời Chờ duyệt chỉ tác giả thấy. Bình luận gốc không công khai thì trả lời cũng không hiển thị độc lập."],
 ], [12, 20, 16, 52]),
 img(PH+"05_reply_view.png", PW, cap("Phone — Màn Phản hồi: bình luận gốc và các trả lời một cấp")),
 img(PH+"07_reply_sheet_compose.png", PW, cap("Phone — Soạn trả lời với ô nhập điền sẵn @tên người được trả lời")),
 img(WB+"web_reply.jpg", 16, cap("Web — Ô nhập trả lời nội tuyến dưới bình luận gốc")),
]

# ---- US09 Nhắc tên & thông báo ----
body += [h3("US09 — Quy trình nhắc tên và nhận thông báo"),
 p("Người dùng gõ @ để nhắc tên; danh sách gợi ý ưu tiên người trong cùng thread rồi đến người đã tham gia bộ phim, chỉ trả về tên hiển thị hoặc định danh đã che. Tên được nhắc hiển thị màu cam nhưng không bấm được; nhắc tên chỉ có tác dụng gửi thông báo. Bấm thông báo mở màn “Bình luận của nội dung” toàn màn hình, không có trình phát, để người dùng đọc đúng bình luận mà không phải tải trang phim."),
 img(FL+"US09.jpg", 16, cap(f"Lưu đồ nhắc tên và nhận thông báo (US09) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.05.B01", "Gõ @ và chọn người", "Người xem đã đăng nhập", "Danh sách gợi ý hiện sau ký tự @; chọn một người để chèn @Tên vào nội dung. Ô nhắc tên không được dùng để dò danh sách tài khoản ngoài thread hoặc phim hiện tại."],
  ["CMT.05.B02", "Gửi thông báo", "Hệ thống", "Khi nội dung công khai, người được nhắc tên/trả lời nhận thông báo trong ứng dụng và push (tiêu đề + tên phim, không chứa số điện thoại đầy đủ). Thông báo lưu 90 ngày; dùng Trung tâm thông báo và cài đặt thông báo sẵn có của ứng dụng."],
  ["CMT.05.B03", "Mở từ thông báo — Phone", "Người xem", "Mở màn “Bình luận của nội dung”: thẻ phim (poster, tên phim tối đa 2 dòng, nút “Xem ngay” để sang trình phát), điều khiển sắp xếp, danh sách bình luận của phim; bình luận đích được cuộn tới và highlight 2 giây. Bấm “{n} Phản hồi” mở màn “Phản hồi” toàn màn hình (có nút Quay lại). Bình luận đích không còn khả dụng → hiển thị “Bình luận không còn khả dụng” tại vị trí đó."],
  ["CMT.05.B04", "Mở từ thông báo — Web", "Người xem", "Mở trang phim, tự cuộn tới khu vực Bình luận, mở sẵn thread chứa bình luận đích và highlight 2 giây (trang phim web vốn tải trình phát sẵn)."],
  ["CMT.05.B05", "Mở từ thông báo — Smart TV", "Người xem", "Mở trang phim và bảng bình luận/trang Phản hồi chỉ đọc chứa bình luận đích."],
 ], [12, 20, 16, 52]),
 table(["Loại thông báo", "Nội dung mẫu", "Bấm vào mở", "Giai đoạn"], [
  ["Trả lời / Nhắc tên", "“{Tên} đã trả lời bình luận của bạn” / “{Tên} đã nhắc đến bạn trong bộ phim {Tên phim}”", "Phone: màn Bình luận của nội dung → Phản hồi; Web: trang phim + thread; Smart TV: trang phim + Phản hồi chỉ đọc", "Giai đoạn này"],
  ["Được cấp huy hiệu", "“Bạn vừa nhận huy hiệu {tên huy hiệu}”", "Sheet/modal Huy hiệu thành viên (Smart TV: không mở)", "Giai đoạn này"],
  ["Kết quả báo cáo; nội dung bị ẩn/từ chối; cảnh báo và chế tài", "Phụ thuộc xử lý thủ công trên CMS", "—", "Giai đoạn sau"],
 ], [22, 34, 30, 14], caption="Bảng 5: Loại thông báo và đích đến khi bấm"),
 img(PH+"08_mention_picker.png", PW, cap("Phone — Gợi ý nhắc tên khi gõ @")),
 img(PH+"noti_click_1_40217_96295.png", PW, cap("Phone — Thông báo đẩy khi được nhắc tên")),
 img(PH+"noti_click_2_40217_96311.png", PW, cap("Phone — Màn Bình luận của nội dung mở từ thông báo: thẻ phim kèm nút Xem ngay và danh sách bình luận")),
 img(PH+"noti_click_3_41209_35118.png", PW, cap("Phone — Màn Bình luận của nội dung với tên phim dài 2 dòng")),
 img(PH+"noti_click_4_41209_35408.png", PW, cap("Phone — Màn Phản hồi toàn màn hình mở từ thông báo")),
 img(PH+"10_notification_center.png", PW, cap("Phone — Trung tâm thông báo")),
 img(WB+"noti_click_16782_40718.jpg", 16, cap("Web — Danh sách thông báo (Tất cả / Chưa đọc) với thông báo nhắc tên")),
]

# ---- US10 Báo cáo ----
body += [h3("US10 — Quy trình báo cáo bình luận vi phạm"),
 p("Người dùng đã đăng nhập trên Phone và Web báo cáo bình luận vi phạm theo bộ lý do chuẩn; chọn “Khác” bắt buộc nhập mô tả 1–500 ký tự hợp lệ ngay trong cùng bottom sheet/modal. Không được báo cáo nội dung của chính mình. Cùng một đối tượng chỉ được báo cáo lại sau 24 giờ, giới hạn 10 báo cáo trong 1 giờ cho mỗi người dùng. Báo cáo không tự ẩn nội dung; việc xử lý và phản hồi kết quả thuộc giai đoạn sau."),
 img(FL+"US10.jpg", 16, cap(f"Lưu đồ báo cáo bình luận vi phạm (US10) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.06.B01", "Mở menu Báo cáo", "Người xem đã đăng nhập", "Menu ⋮ của bình luận người khác chỉ có “Báo cáo bình luận”. Guest chọn Báo cáo → điều hướng đăng nhập."],
  ["CMT.06.B02", "Chọn lý do", "Người xem đã đăng nhập", "Có spoiler / Spam, Quảng cáo / Xúc phạm, ngôn từ công kích / Nội dung không phù hợp / Khác. Chọn “Khác” → ô nhập mô tả 0/500 trượt xuống trong cùng sheet; nút Báo cáo chỉ bật khi đã chọn lý do và, với Khác, có ít nhất 1 ký tự không phải khoảng trắng."],
  ["CMT.06.B03", "Gửi báo cáo", "Hệ thống", "Ghi nhận báo cáo kèm lý do và mô tả; toast “Báo cáo thành công, bình luận sẽ được xem xét”. Nội dung bị báo cáo được đưa vào hàng chờ xử lý (công cụ xử lý thuộc giai đoạn sau)."],
 ], [12, 20, 16, 52]),
 img(PH+"40220_29447.png", PW, cap("Phone — Menu của bình luận người khác: Báo cáo bình luận")),
 img(PH+"40220_31205.png", PW, cap("Phone — Bottom sheet chọn lý do báo cáo")),
 img(PH+"14_report_toast.png", PW, cap("Phone — Toast báo cáo thành công")),
 img(WB+"web_report.jpg", 16, cap("Web — Modal Báo cáo bình luận")),
]

# ---- US17 Huy hiệu ----
body += [h3("US17 — Quy trình hiển thị và giải thích huy hiệu"),
 p("Huy hiệu được hệ thống tự động xét hằng ngày theo hành vi trong cửa sổ thời gian gần nhất (Fan tích cực: 7 ngày; Fan kỳ cựu: 30 ngày; Nổi bật: theo bình luận) hoặc do quản trị viên cấp thủ công (Custom, ví dụ “Chuyên gia”). Mỗi card hiển thị tối đa một huy hiệu theo thứ tự ưu tiên Custom > Nổi bật > Fan kỳ cựu > Fan tích cực. Ghim là marker riêng, không chiếm vị trí huy hiệu. Bấm chip huy hiệu mở sheet/modal “Huy hiệu thành viên” giải thích ý nghĩa, không hiển thị số liệu tiêu chí; Smart TV chỉ hiển thị chip."),
 img(FL+"US17.jpg", 12, cap(f"Lưu đồ huy hiệu người dùng (US17) — {FLOW_NOTE}")),
 table(["Huy hiệu", "Tiêu chí xét (tự động, hằng ngày)", "Cửa sổ xét"], [
  ["Fan tích cực", "Có ít nhất 10 bình luận hoặc trả lời hợp lệ (công khai, chưa bị xóa) VÀ đã Thích ít nhất 20 bình luận/trả lời khác nhau", "7 ngày gần nhất"],
  ["Fan kỳ cựu", "Có ít nhất 30 bình luận hoặc trả lời hợp lệ VÀ có ít nhất 1 bình luận nhận từ 10 lượt Thích trở lên", "30 ngày gần nhất"],
  ["Nổi bật", "Có bình luận công khai đạt tối thiểu 20 Net Like, 5 trả lời và nằm trong nhóm 10% Featured Score cao nhất toàn MyTV", "30 ngày gần nhất"],
  ["Custom (ví dụ “Chuyên gia”)", "Quản trị viên cấp thủ công kèm tên huy hiệu và thời hạn tùy chọn", "Theo thời hạn cấp"],
 ], [20, 60, 20], caption="Bảng 6: Tiêu chí huy hiệu"),
 img(PH+"40227_34309.png", PW, cap("Phone — Sheet Huy hiệu thành viên")),
 img(WB+"web_badge.jpg", 16, cap("Web — Modal Huy hiệu thành viên")),
]
body += [p("Giao diện Smart TV — US17 Huy hiệu người dùng", bold=True),
 p("Trên Smart TV huy hiệu chỉ hiển thị dưới dạng chip cạnh tên trong card (tối đa một chip; marker Ghim hiển thị riêng); không có trang giải thích huy hiệu và không có thao tác trên chip."),
 img(TV+"us17_overview.jpg", 16, cap("Smart TV — Lưu đồ Figma US17 Huy hiệu người dùng")),
 img(TV+"tv_us17_r1_c2_89_41320.jpg", 15, cap("Smart TV — Danh sách bình luận với marker Ghim và các chip Fan tích cực, Fan kỳ cựu, Nổi bật")),
 img(TV+"tv_us17_r1_c1_84_39415.jpg", 15, cap("Smart TV — Card có tiêu điểm mang chip Fan kỳ cựu")),
]

# ======================= IV. YÊU CẦU CHỨC NĂNG =======================
URH = ['STT', 'Mã yêu cầu', 'Tên yêu cầu', 'Mô tả', 'Mức độ ưu tiên', 'Mức độ quan trọng', 'Đối tượng liên quan']
URW = [4, 8, 14, 42, 8, 8, 16]
def ur(stt, code, name, pb, inp, out, proc, exc, pri, imp, who):
    desc = "Phát biểu yêu cầu: " + pb + "\nThông tin đầu vào:\n" + "\n".join("- " + i for i in inp) + "\nThông tin đầu ra: " + out + "\nChức năng xử lý: " + proc + "\nCác ngoại lệ: " + exc
    return [str(stt), code, name, desc, pri, imp, who]
def later(stt, code, name, reason, who):
    desc = ("Phát biểu yêu cầu: Giai đoạn sau — không đặc tả trong tài liệu này. " + reason +
            "\nThông tin đầu vào: N/A\nThông tin đầu ra: N/A\nChức năng xử lý: N/A\nCác ngoại lệ: N/A")
    return [str(stt), code, name, desc, "Thấp", "Thấp", who]

body += [h1("YÊU CẦU CHỨC NĂNG"),
 p("Hệ thống được chia thành 5 phân hệ tương ứng 5 Epic của backlog sản phẩm. Mỗi yêu cầu chức năng mang một mã UR duy nhất và được tham chiếu lại tại chương Tiêu chuẩn nghiệm thu. Các yêu cầu thuộc giai đoạn sau giữ mã để không đánh số lại các tài liệu phụ thuộc."),
 table(["Phân hệ", "Tên phân hệ", "Mã yêu cầu trong giai đoạn này", "Giai đoạn sau"], [
  ["PH01", "Trải nghiệm bình luận", "UR01, UR02, UR04, UR05", "UR03, UR06"],
  ["PH02", "Tương tác cộng đồng", "UR07, UR08, UR09", "—"],
  ["PH03", "An toàn và kiểm duyệt", "UR10 (gửi báo cáo); phần kiểm duyệt tự động mô tả trong UR04", "UR11, UR12 (công cụ CMS)"],
  ["PH04", "CMS quản trị bình luận", "—", "UR13 – UR16"],
  ["PH05", "Tăng trưởng và phân tích", "UR17", "UR18, UR19, UR20"],
 ], [12, 28, 36, 24], caption="Bảng 7: Cây chức năng tổng thể hệ thống"),
 table(["Màn hình / thành phần", "Phone", "Web", "Smart TV", "User Story"], [
  ["Danh sách bình luận (tab/khu vực/bảng) + số đếm", "Có", "Có", "Có", "US01, US02"],
  ["Khung xương, trạng thái rỗng, trạng thái bị khóa", "Có", "Có", "Có (rỗng, khung xương; bị khóa = ẩn nút Bình luận)", "US01"],
  ["Bình luận dài — Xem thêm", "Có (bung tại chỗ)", "Có (bung tại chỗ)", "Có (cắt “…”, chọn card xem đủ)", "US01"],
  ["Thanh nhắc đăng nhập / hướng dẫn QR", "Thanh “Đăng nhập để bình luận”", "Thẻ “Đăng nhập để bình luận”", "Dải nhắc + trang hướng dẫn QR, hotline", "US01"],
  ["Điều khiển sắp xếp", "Bottom sheet", "Dropdown", "Không", "US02"],
  ["Ô soạn bình luận + overlay", "Thanh nhập đáy màn hình, overlay tối", "Ô nhập nội tuyến, backdrop modal", "Không", "US04"],
  ["Trạng thái vượt 500 ký tự / bị chặn / Chờ duyệt", "Có (vượt 500: cần vẽ)", "Có (Hủy đăng: cần vẽ)", "Không", "US04"],
  ["Menu ⋮ (Sửa/Xóa — Báo cáo), hộp thoại xóa, nhãn Đã chỉnh sửa", "Có", "Có", "Không", "US05, US10"],
  ["Thread Phản hồi + ô trả lời điền sẵn @", "Màn Phản hồi", "Mở rộng inline", "Trang Phản hồi chỉ đọc (Click vào card; BACK quay lại)", "US08, US01"],
  ["Thích / Bỏ thích", "Có", "Có", "Chỉ hiển thị số", "US07"],
  ["Gợi ý nhắc tên", "Có", "Có", "Không", "US09"],
  ["Trung tâm thông báo, push", "Có", "Có", "Mục thông báo sẵn có", "US09"],
  ["Màn Bình luận của nội dung + Phản hồi mở từ thông báo", "Có", "Dùng trang phim + cuộn", "Trang phim + Phản hồi", "US09"],
  ["Sheet/modal Báo cáo + ô mô tả “Khác”", "Có (ô mô tả: cần vẽ)", "Có (ô mô tả: cần vẽ)", "Không", "US10"],
  ["Chip huy hiệu, marker Ghim, sheet/modal Huy hiệu thành viên", "Có", "Có", "Chip", "US17"],
 ], [34, 20, 20, 14, 12], caption="Bảng 8: Ma trận màn hình theo nền tảng (trạng thái thiết kế Figma ngày 06/11/2026)"),
]

CARD = "card gồm avatar, tên hiển thị (tên tài khoản MyTV hoặc số điện thoại đã che), marker Ghim nếu có, tối đa một huy hiệu, thời gian tương đối theo 6 mức (" + TIME_FMT + "), nội dung cắt 4 dòng kèm “Xem thêm” bung tại chỗ, nút Thích kèm số, nút Trả lời, lối vào “{n} Phản hồi” và menu ⋮; không có dấu hiệu riêng phân biệt bình luận của chính mình"

# ---- PH01 ----
body += [h2("Phân hệ Trải nghiệm bình luận"),
 p("Phân hệ cung cấp khu vực thảo luận gắn với từng bộ phim, gồm đọc, sắp xếp, đăng, sửa và xóa bình luận."),
 table(URH, [
  ur(1, "UR01", "Đọc khu vực bình luận",
     "Cho phép mọi người xem, kể cả chưa đăng nhập, đọc bình luận công khai của bộ phim đang xem trên Phone, Web và Smart TV.",
     ["Mã phim (*): lấy từ ngữ cảnh trang nội dung; phim bộ dùng chung một scope cho mọi tập", "Trạng thái đăng nhập và loại hồ sơ của phiên hiện tại"],
     "Số lượng bình luận (gốc + trả lời công khai, viết tắt K/M từ 1.000), danh sách 10 bình luận gốc đầu tiên theo sắp xếp Nổi bật với tối đa 3 bình luận ghim đứng đầu, lối vào “{n} Phản hồi”, thanh nhắc đăng nhập hoặc ô soạn bình luận tùy trạng thái đăng nhập; Smart TV hiển thị dải nhắc chuyển sang điện thoại/website.",
     "Xác định scope theo bộ phim; đổi tập không tải lại; hiển thị khung xương trong lúc tải; tải thêm 10 bình luận mỗi lần cuộn; " + CARD + "; Smart TV cắt nội dung dài bằng “…” và mở trang Phản hồi hiển thị đủ khi chọn card; thread tải 3 trả lời đầu theo thứ tự cũ → mới và thêm tối đa 10 trả lời mỗi lần.",
     "Hồ sơ Trẻ em không hiển thị khu vực bình luận; scope bị khóa thì giữ tab nhưng bỏ số đếm, ẩn danh sách, ô soạn và các thao tác, hiện minh họa ổ khóa kèm “Bình luận đang bị khóa. Vui lòng thử lại sau”; chưa có bình luận nào thì hiển thị trạng thái rỗng “Hãy là người đăng bình luận đầu tiên”; lỗi tải danh sách thì cho thử lại.",
     "Cao", "Cao", "Người xem"),
  ur(2, "UR02", "Xem số lượng và sắp xếp bình luận",
     "Cho phép người xem trên Phone và Web đổi cách sắp xếp danh sách bình luận và tải thêm nội dung khi cuộn.",
     ["Chế độ sắp xếp (*): Nổi bật, Mới nhất hoặc Nhiều lượt thích", "Vị trí cuộn hiện tại của danh sách"],
     "Danh sách bình luận theo chế độ đã chọn, nhãn chế độ sắp xếp hiện hành, số lượng bình luận.",
     "Sắp xếp Nổi bật là mặc định, dùng Featured Score 0,5×ln(1+Like) + 0,3×ln(1+Reply) + 0,2×e^(-AgeHours/72) với Like là Net Like công khai hiện tại; tối đa 3 bình luận ghim luôn đứng đầu và không tham gia tính Featured Score; tải 10 bình luận gốc mỗi lần; trả lời không xuất hiện trong danh sách gốc; mở bộ phim khác thì sắp xếp trở về Nổi bật, đổi tập giữ nguyên.",
     "Smart TV không có điều khiển sắp xếp, luôn dùng Nổi bật; không còn dữ liệu để tải thêm; lỗi mạng khi tải thêm thì giữ danh sách hiện có và cho thử lại.",
     "Cao", "Cao", "Người xem"),
  later(3, "UR03", "Đánh giá phim", "Ứng dụng hiện chỉ có đánh giá ứng dụng; đánh giá phim cần thiết kế và nghiệp vụ riêng. Thiết kế đang ẩn trên Figma.", "Người xem đã đăng nhập"),
  ur(4, "UR04", "Đăng bình luận qua kiểm duyệt tự động",
     "Cho phép người xem đã đăng nhập trên Phone và Web gửi bình luận dạng văn bản thuần cho bộ phim đang xem; nội dung đi qua kiểm duyệt tự động trước khi hiển thị.",
     ["Nội dung bình luận (*): 1–500 ký tự văn bản thuần, cho phép chỉ có emoji, không chấp nhận chỉ khoảng trắng, có thể chứa @nhắc tên", "Mã phim (*)", "Danh sách từ khóa chặn toàn hệ thống; chế độ và ngưỡng AI áp dụng cho bộ phim"],
     "Bình luận ở trạng thái công khai hoặc Chờ duyệt (card mờ “Bình luận của bạn sẽ sớm được xuất hiện”, chỉ tác giả thấy, menu ⋮ có Chỉnh sửa và Hủy đăng); lỗi nội tuyến “Bình luận không được chấp thuận” khi bị chặn; bộ đếm ký tự và thông báo “Bạn đã vượt quá 500 ký tự”.",
     "Phone: ô soạn cố định đáy màn hình nở tối đa 3 dòng, hiện overlay tối chặn tương tác với trình phát và nội dung bên dưới, video vẫn phát; Web: ô nhập nội tuyến. Kiểm tra độ dài, ký tự đối kháng và tên miền liên kết (chỉ mytv.com.vn và tên miền con thực); giới hạn 5 nội dung Bình luận và Trả lời trong 1 phút cho mỗi người dùng; đối chiếu danh sách từ khóa chặn (khớp → chặn ngay, không gọi AI); gọi AI phân loại Nhẹ/Trung bình/Nặng; áp quyết định theo Chế độ 1 (Nhẹ công khai, Trung bình chờ duyệt) hoặc Chế độ 2 (Nhẹ và Trung bình chờ duyệt); Nặng luôn bị chặn. Hủy đăng gỡ nội dung khỏi hàng chờ, toast “Đã hủy bình luận”, không hoàn quota; chỉnh sửa khi chờ duyệt thay thế bản đang chờ và đi lại kiểm duyệt.",
     "Nội dung rỗng hoặc chỉ khoảng trắng; vượt 500 ký tự thì nút gửi vô hiệu; vượt giới hạn tần suất; khớp từ khóa chặn hoặc AI trả rủi ro Nặng thì chặn tại thời điểm gửi và giữ nội dung trong ô; AI timeout 5 giây, lỗi hoặc ngôn ngữ ngoài tiếng Việt và tiếng Anh thì chuyển sang Chờ duyệt; scope bị khóa ẩn ô soạn; Smart TV không có ô soạn; việc duyệt thủ công nội dung Chờ duyệt thuộc giai đoạn sau.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  ur(5, "UR05", "Sửa và xóa bình luận của mình",
     "Cho phép người dùng trên Phone và Web sửa hoặc xóa bình luận và trả lời do chính mình tạo.",
     ["Mã bình luận hoặc mã trả lời (*)", "Nội dung mới khi sửa (*): áp dụng cùng ràng buộc như khi đăng mới", "Xác nhận của người dùng khi xóa (*)"],
     "Bản sửa được công khai mang nhãn “Đã chỉnh sửa” và toast “Chỉnh sửa thành công”; hộp thoại xác nhận xóa nêu rõ hệ quả (có/không có trả lời); toast “Xóa bình luận thành công”.",
     "Menu ⋮ của bình luận của mình gồm Chỉnh sửa và Xóa (bình luận của người khác chỉ có Báo cáo). Kết quả một lần sửa phụ thuộc chế độ kiểm duyệt — Chế độ 1 với rủi ro Nhẹ thì bản mới công khai ngay, Chế độ 1 với rủi ro Trung bình hoặc Chế độ 2 thì bản mới vào Chờ duyệt và bản cũ vẫn công khai trong lúc chờ; giới hạn 5 lần sửa mỗi phút trên mỗi bình luận; tự xóa bình luận gốc kéo theo toàn bộ trả lời bị xóa mềm và giữ 90 ngày.",
     "Từ khóa chặn hoặc rủi ro Nặng bị chặn tại thời điểm gửi và bản cũ giữ nguyên; người dùng không xem được lịch sử phiên bản; nội dung đã tự xóa không hiển thị lại; Smart TV không có Sửa/Xóa.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  later(6, "UR06", "Bình luận kèm mốc thời gian", "Chưa có thiết kế highlight và thông báo mốc không hợp lệ. Trong giai đoạn này chuỗi thời gian hiển thị như văn bản thường, không bấm được.", "Người xem đã đăng nhập"),
 ], URW),
]

# ---- PH02 ----
body += [h2("Phân hệ Tương tác cộng đồng"),
 p("Phân hệ cung cấp các thao tác tương tác giữa người xem với nhau trên Phone và Web: Thích, Trả lời một cấp và Nhắc tên kèm thông báo."),
 table(URH, [
  ur(1, "UR07", "Thích và bỏ thích bình luận",
     "Cho phép người dùng đã đăng nhập trên Phone và Web bày tỏ sự tán thành với một bình luận hoặc trả lời.",
     ["Mã bình luận hoặc mã trả lời (*)", "Trạng thái Thích hiện tại của người dùng trên đối tượng đó"],
     "Biểu tượng Thích đổi trạng thái ngay lập tức (tô đặc màu cam và số đếm màu cam khi đã thích; viền xám khi chưa) và số lượt Thích cập nhật theo, viết tắt K/M từ 1.000.",
     "Giao diện cập nhật lạc quan trước, client gom thao tác theo lô tối đa 5 giây rồi đồng bộ về máy chủ, đẩy sớm khi rời màn hình hoặc chuyển nền; nhiều lần Thích và Bỏ thích liên tiếp trên cùng đối tượng trong một lô được gộp về trạng thái cuối cùng; máy chủ là nguồn chân lý; người dùng được Thích nội dung của chính mình.",
     "Chưa đăng nhập thì điều hướng sang đăng nhập và không tự thực hiện lại thao tác; đồng bộ thất bại thì hoàn nguyên trạng thái trên giao diện và thông báo cho công nghệ hỗ trợ đọc màn hình; Smart TV chỉ hiển thị số lượt Thích (thao tác Thích trên TV thuộc giai đoạn sau).",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  ur(2, "UR08", "Trả lời bình luận một cấp",
     "Cho phép người dùng trên Phone và Web trả lời một bình luận gốc hoặc một trả lời khác trong cùng thread, chỉ sâu một cấp.",
     ["Mã bình luận gốc (*) và, nếu trả lời một trả lời, mã trả lời được nhắc", "Nội dung trả lời (*): 1–500 ký tự, cùng ràng buộc như bình luận"],
     "Trả lời hiển thị cuối thread theo thứ tự cũ → mới và tự cuộn tới; số lượng trên lối vào “{n} Phản hồi” được cập nhật; trả lời Chờ duyệt chỉ tác giả thấy.",
     "Phone: màn “Phản hồi” riêng với bình luận gốc ở đầu; Web: mở rộng inline dưới bình luận gốc với ô nhập trả lời ngay dưới gốc và nút “Thu gọn”. Ô soạn điền sẵn @tên người được trả lời; trả lời một trả lời vẫn nằm trong cùng thread, không tạo cấp hai; thread tải 3 trả lời đầu và thêm tối đa 10 trả lời mỗi lần; đi qua cùng kiểm duyệt tự động như bình luận gốc.",
     "Bình luận gốc đang không công khai thì trả lời cũng không hiển thị độc lập; Smart TV chỉ đọc thread, không có ô nhập trả lời.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  ur(3, "UR09", "Nhắc tên và nhận thông báo",
     "Cho phép người dùng nhắc tên người khác trong bình luận hoặc trả lời và nhận thông báo khi được trả lời, nhắc tên hoặc cấp huy hiệu.",
     ["Ký tự @ kèm chuỗi tìm kiếm trong ô soạn", "Lựa chọn người dùng từ danh sách gợi ý (*)"],
     "@Tên hiển thị màu cam trong nội dung, không bấm được; thông báo trong ứng dụng và push cho người được nhắc tên/trả lời; đích đến khi bấm theo Bảng 5.",
     "Gợi ý ưu tiên người dùng trong cùng thread, sau đó người đã tham gia bộ phim, chỉ trả về tên hiển thị hoặc định danh đã che; dùng Trung tâm thông báo và cài đặt thông báo sẵn có của ứng dụng; thông báo trong ứng dụng lưu 90 ngày. Bấm thông báo: Phone mở màn “Bình luận của nội dung” (thẻ phim với poster, tên phim tối đa 2 dòng và nút “Xem ngay”; điều khiển sắp xếp; danh sách bình luận; bình luận đích highlight 2 giây; “{n} Phản hồi” mở màn Phản hồi toàn màn hình có nút Quay lại); Web mở trang phim, tự cuộn tới khu vực Bình luận và mở sẵn thread; Smart TV mở trang phim và trang Phản hồi chỉ đọc.",
     "Gợi ý không bao giờ trả số điện thoại hay email đầy đủ; ô nhắc tên không được dùng để dò danh sách tài khoản ngoài phạm vi thread hoặc phim hiện tại; bình luận đích không còn khả dụng thì hiển thị “Bình luận không còn khả dụng” tại vị trí đó; Smart TV không có nhắc tên; các loại thông báo phụ thuộc xử lý CMS (kết quả báo cáo, nội dung bị ẩn, chế tài) thuộc giai đoạn sau.",
     "Trung bình", "Trung bình", "Người xem đã đăng nhập"),
 ], URW),
]

# ---- PH03 ----
body += [h2("Phân hệ An toàn và kiểm duyệt"),
 p("Trong giai đoạn này phân hệ gồm việc gửi báo cáo vi phạm từ cộng đồng (UR10) và kiểm duyệt tự động khi đăng (đã mô tả trong UR04). Công cụ xử lý thủ công, cấu hình chế độ kiểm duyệt và quản lý trạng thái hiển thị trên CMS (UR11, UR12) thuộc giai đoạn sau."),
 table(URH, [
  ur(1, "UR10", "Báo cáo bình luận vi phạm",
     "Cho phép người dùng đã đăng nhập trên Phone và Web báo cáo một bình luận hoặc trả lời vi phạm quy tắc cộng đồng.",
     ["Mã bình luận hoặc mã trả lời (*)", "Lý do báo cáo (*): Có spoiler, Spam/Quảng cáo, Xúc phạm/ngôn từ công kích, Nội dung không phù hợp, Khác", "Mô tả bổ sung: bắt buộc 1–500 ký tự hợp lệ khi chọn lý do Khác, nhập ngay trong cùng bottom sheet/modal"],
     "Toast “Báo cáo thành công, bình luận sẽ được xem xét”; báo cáo được ghi nhận kèm lý do, mô tả, người báo cáo và thời điểm.",
     "Mục Báo cáo chỉ hiện trong menu ⋮ của bình luận người khác; nút Báo cáo chỉ bật khi đã chọn lý do và, với Khác, có ít nhất một ký tự không phải khoảng trắng; đưa mục bị báo cáo vào hàng chờ xử lý nhưng không tự động ẩn hoặc xóa dù số lượng báo cáo lớn; giới hạn 10 báo cáo trong 1 giờ cho mỗi người dùng; cùng một đối tượng chỉ được báo cáo lại sau 24 giờ.",
     "Không được báo cáo nội dung của chính mình; mô tả chỉ có khoảng trắng khi chọn lý do Khác bị từ chối; guest chọn Báo cáo thì điều hướng đăng nhập; Smart TV không có Báo cáo trong giai đoạn này; việc xử lý báo cáo và phản hồi kết quả cho người báo cáo/tác giả thuộc giai đoạn sau.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  later(2, "UR11", "Kiểm duyệt tự động: cấu hình chế độ và ngưỡng AI", "Hành vi kiểm duyệt tự động khi đăng đã mô tả trong UR04; phần cấu hình chế độ, ngưỡng AI, phản hồi “AI phân loại sai” và danh sách từ khóa chặn là công cụ CMS chưa có thiết kế.", "Bộ phận vận hành nội dung"),
  later(3, "UR12", "Quản lý trạng thái và phạm vi hiển thị", "Ứng dụng chỉ cần tôn trọng trạng thái công khai/Chờ duyệt/bị khóa do máy chủ trả về (đã mô tả trong UR01, UR04). Công cụ quản lý trạng thái, ẩn/khôi phục nội dung và đóng/mở khu vực bình luận thuộc CMS.", "Bộ phận vận hành nội dung"),
 ], URW),
]

# ---- PH04 ----
body += [h2("Phân hệ CMS quản trị bình luận"),
 p("Toàn bộ phân hệ CMS thuộc giai đoạn sau vì chưa có thiết kế giao diện; nội dung nghiệp vụ chi tiết đã được ghi nhận trong backlog (US13–US16) để sử dụng khi lập kế hoạch."),
 table(URH, [
  later(1, "UR13", "Tra cứu và xử lý nội dung", "Công cụ tra cứu theo phim/người dùng/trạng thái và các thao tác Duyệt/Từ chối/Ẩn/Xóa mềm/Hoàn tác.", "Bộ phận vận hành nội dung"),
  later(2, "UR14", "Xử lý hàng chờ kiểm duyệt", "Hàng chờ ưu tiên theo mức rủi ro, SLA 24 giờ, xử lý hàng loạt tối đa 100 mục.", "Bộ phận vận hành nội dung"),
  later(3, "UR15", "Ghim bình luận, cấu hình theo phim và danh sách từ khóa chặn", "Ghim tối đa 3 bình luận mỗi phim; cấu hình chế độ kiểm duyệt và đóng/mở khu vực bình luận; quản lý danh sách từ khóa chặn toàn hệ thống. Ứng dụng đã hiển thị marker Ghim và trạng thái bị khóa theo dữ liệu máy chủ.", "Bộ phận vận hành nội dung"),
  later(4, "UR16", "Chế tài người dùng và nhật ký kiểm toán", "Cảnh báo, Khóa bình luận, Khóa tài khoản, khiếu nại qua Tổng đài 1800 1166, nhật ký kiểm toán lưu 2 năm.", "Bộ phận vận hành nội dung"),
 ], URW),
]

# ---- PH05 ----
body += [h2("Phân hệ Tăng trưởng và phân tích"),
 p("Trong giai đoạn này phân hệ gồm huy hiệu người dùng (UR17). Chia sẻ, thống kê và AI hỗ trợ vận hành thuộc giai đoạn sau."),
 table(URH, [
  ur(1, "UR17", "Huy hiệu người dùng",
     "Ghi nhận đóng góp của người dùng tích cực bằng huy hiệu hiển thị cạnh tên trên Phone, Web và Smart TV.",
     ["Số bình luận và trả lời hợp lệ, số bình luận/trả lời khác nhau đã Thích, số lượt Thích nhận được trên từng bình luận, trong cửa sổ thời gian xét", "Quyết định cấp huy hiệu thủ công của quản trị viên kèm tên huy hiệu Custom (ví dụ “Chuyên gia”) và thời hạn tùy chọn"],
     "Chip huy hiệu cạnh tên (tối đa một chip); sheet/modal “Huy hiệu thành viên” giải thích ý nghĩa Fan tích cực, Fan kỳ cựu, Nổi bật và các huy hiệu độc quyền khác, không hiển thị số liệu tiêu chí; thông báo khi được cấp huy hiệu.",
     "Fan tích cực: trong 7 ngày gần nhất có ít nhất 10 bình luận hoặc trả lời hợp lệ và đã Thích ít nhất 20 bình luận/trả lời khác nhau. Fan kỳ cựu: trong 30 ngày gần nhất có ít nhất 30 bình luận hoặc trả lời hợp lệ và ít nhất 1 bình luận nhận từ 10 lượt Thích trở lên. Nổi bật: có bình luận công khai đạt tối thiểu 20 Net Like, 5 trả lời và nằm trong nhóm 10% Featured Score cao nhất toàn MyTV trong 30 ngày. Hệ thống xét lại hằng ngày; huy hiệu Fan được thu hồi khi không còn đạt tiêu chí sau 7 ngày ân hạn; thứ tự ưu tiên hiển thị Custom > Nổi bật > Fan kỳ cựu > Fan tích cực; Ghim là marker riêng và không chiếm vị trí huy hiệu; bấm chip mở sheet/modal giải thích trên Phone và Web, Smart TV chỉ hiển thị chip.",
     "Chỉ tính bình luận/trả lời công khai, chưa bị xóa; bình luận bị xóa kéo theo (tự xóa bình luận gốc) không được tính; lượt Thích do chính mình tạo trên nội dung của mình không tính vào tiêu chí nhận Thích; sau khi đã cấp, huy hiệu Nổi bật không tự thu hồi khi chỉ số giảm, chỉ mất khi nội dung nguồn không còn công khai; tắt một loại huy hiệu thì ẩn trên giao diện nhưng giữ lịch sử.",
     "Trung bình", "Trung bình", "Người xem đã đăng nhập"),
  later(2, "UR18", "Chia sẻ bình luận", "Bỏ bảng chia sẻ hệ điều hành và deep link cài ứng dụng khỏi giai đoạn này; deep link nội bộ phục vụ thông báo đã mô tả tại UR09.", "Người xem đã đăng nhập"),
  later(3, "UR19", "Thống kê hoạt động bình luận", "Bảng chỉ số Engagement (Bình luận×2 + Trả lời×2 + Net Like×1), an toàn và vận hành; thuộc CMS/phân tích.", "Ban sản phẩm"),
  later(4, "UR20", "AI hỗ trợ vận hành", "Gợi ý ghim, tóm tắt thảo luận, cảnh báo bất thường; thuộc CMS.", "Bộ phận vận hành nội dung"),
 ], URW),
 table(["STT", "Màn hình / trạng thái cần thiết kế", "Nền tảng", "Mô tả yêu cầu", "Tham chiếu"], [
  ["1", "Ô nhập mô tả khi chọn lý do “Khác”", "Phone, Web", "Trượt xuống trong cùng bottom sheet/modal, bộ đếm 0/500, nút Báo cáo bật khi có ký tự hợp lệ; bàn phím bật thì sheet đẩy lên.", "UR10"],
  ["2", "Trạng thái vượt 500 ký tự", "Phone", "Bộ đếm đỏ 500/500, nút gửi vô hiệu, thông báo “Bạn đã vượt quá 500 ký tự” (Web đã có).", "UR04"],
  ["3", "Hủy đăng khi Chờ duyệt", "Web", "Bổ sung trong menu của bình luận chờ xét duyệt (Phone đã có).", "UR04"],
  ["4", "Nhãn sắp xếp", "Phone, Web", "Thống nhất nhãn “Nổi bật” giữa nút sắp xếp và sheet/dropdown “Sắp xếp theo” (Figma đang ghi “Nổi bật nhất” ở nút).", "UR02"],
  ["5", "Ghi chú [BA] còn lại trên Figma", "Phone, Web, Smart TV", "Bỏ phân nhánh phim bộ/phim lẻ trong lưu đồ; ẩn toolbar định dạng và các component Format trên Web; gỡ link mốc thời gian “24:14” còn sót trên Web; đổi tên variant huy hiệu “Bình luận nổi bật” → “Nổi bật”; xóa dòng radio trống trong sheet báo cáo Phone.", "Toàn bộ"],
 ], [5, 25, 14, 44, 12], caption="Bảng 9: Danh mục thiết kế bổ sung và chỉnh sửa còn lại trước khi phát triển"),
]

# ======================= V. PHI CHỨC NĂNG =======================
def nf_rows(block, repl=None, drop=None):
    b = copy.deepcopy(block)
    rows = []
    for r in b['rows']:
        code = r[0] if isinstance(r[0], str) else r[0]['text']
        if drop and code in drop: continue
        if repl and code in repl: rows.append([code, repl[code]])
        else: rows.append(r)
    b['rows'] = rows
    return b

sec = nf_rows(ob[90], repl={
 "UR_NF05": "Toàn bộ nội dung do người dùng nhập phải được làm sạch và mã hóa ở mọi bề mặt hiển thị: web, ứng dụng di động, Smart TV và các công cụ nội bộ. Kết quả phân loại của AI và danh sách từ khóa không thay thế cho việc làm sạch này.",
 "UR_NF07": "Chặn hoặc trung hòa các nhóm ký tự đối kháng trong bình luận và trả lời: ký tự đảo chiều văn bản U+202E, ký tự độ rộng bằng không U+200B và U+200D, ký tự điều khiển U+0000–U+001F. Việc đối chiếu từ khóa chặn phải thực hiện sau bước chuẩn hóa này.",
 "UR_NF08": "Nội dung thông báo đẩy không chứa số điện thoại đầy đủ; tên người gửi hiển thị bằng tên hiển thị của tài khoản hoặc định danh đã che dạng 0***123.",
})
sec['rows'].append(["UR_NF10a", "Tên hiển thị lấy từ hồ sơ tài khoản MyTV; khi tài khoản chưa đặt tên, hệ thống chỉ hiển thị số điện thoại đã che (giữ số 0 đầu và 3 số cuối, che toàn bộ số giữa bằng *). Không có API nào trả số điện thoại đầy đủ cho ứng dụng."])
sec['rows'].append(["UR_NF10b", "Hồ sơ Trẻ em không được gọi bất kỳ API đọc/ghi bình luận nào; việc ẩn khu vực bình luận phải được bảo đảm ở cả giao diện và tầng API theo loại hồ sơ của phiên."])

usab = nf_rows(ob[94], repl={
 "UR_NF16": "Tương phản màu tối thiểu 4,5:1 cho văn bản thường và 3:1 cho thành phần giao diện, bao gồm trạng thái card Chờ duyệt (nội dung mờ) và tên được nhắc màu cam.",
 "UR_NF17": "Vùng chạm tối thiểu 44×44pt cho mọi phần tử tương tác: nút Thích, nút Trả lời, menu ⋮, chip huy hiệu, liên kết Xem thêm và nút xem thêm phản hồi.",
})
usab['rows'].append(["UR_NF22a", "Khi overlay tối đang hiển thị trên Phone, mọi phần tử bên dưới (trình phát, tab, danh sách) phải bị loại khỏi thứ tự tiêu điểm của công nghệ hỗ trợ; bấm vùng tối hoặc nút Đóng đều đóng được lớp phủ."])
usab['rows'].append(["UR_NF22b", "Trên Smart TV, card có nội dung dài phải đọc được đủ bằng remote: chọn card mở trang Phản hồi hiển thị toàn bộ nội dung; thứ tự tiêu điểm đi theo thứ tự danh sách."])

perf = nf_rows(ob[98], repl={
 "UR_NF28": "Thời gian phản hồi khi gửi bình luận hoặc trả lời dưới 1 giây ở phân vị 95 (không tính thời gian gọi AI), đo tại tầng API và không tính độ trễ mạng của thiết bị đầu cuối.",
})
perf['rows'].append(["UR_NF33a", "Bước đối chiếu danh sách từ khóa chặn phải hoàn thành dưới 50 ms ở phân vị 95 với danh sách tới 5.000 từ khóa."])
perf['rows'].append(["UR_NF33b", "Màn “Bình luận của nội dung” mở từ thông báo phải hiển thị danh sách trong vòng 1,5 giây ở phân vị 95 mà không tải trình phát hay siêu dữ liệu đầy đủ của trang phim."])

design = nf_rows(ob[102], repl={
 "UR_NF40": "Nội dung bình luận và trả lời được lưu dưới dạng văn bản thuần (không có dải định dạng); vị trí các @nhắc tên lưu kèm mã tài khoản được nhắc để hiển thị và gửi thông báo.",
 "UR_NF41": "Không có chức năng định dạng văn bản (Đậm, Nghiêng, Gạch chân, Làm mờ) và không có chức năng chèn siêu liên kết trong luồng soạn bình luận; chỉ URL thuộc mytv.com.vn gõ trực tiếp được tự nhận dạng.",
 "UR_NF42": "Hệ thống không điều khiển trình phát video; khi overlay thao tác bình luận hiển thị, video vẫn tiếp tục phát và trình phát không nhận tương tác cho tới khi overlay đóng.",
 "UR_NF43": "Danh tính bình luận gắn với tài khoản MyTV, không gắn với hồ sơ xem; chuyển hồ sơ trong cùng tài khoản không thay đổi danh tính, huy hiệu hay giới hạn tần suất.",
 "UR_NF45": "Smart TV chỉ đọc: không tạo Bình luận, Trả lời, Nhắc tên, không Sửa/Xóa, không đổi cách sắp xếp, không Thích và không Báo cáo trong giai đoạn này; hiển thị số lượt thích, chip huy hiệu, cắt nội dung dài bằng “…” và mở trang Phản hồi để đọc đủ. Smart TV hiển thị hướng dẫn kèm mã QR để chuyển sang điện thoại khi người dùng muốn tham gia bình luận.",
})
design['rows'].append(["UR_NF45a", "Thiết kế Figma Phone, Web và Smart TV là nguồn chuẩn cho bố cục và nội dung chữ trên giao diện; mọi khác biệt giữa tài liệu này và Figma phải được giải quyết bằng ghi chú [BA] trên Figma trước khi phát triển."])

iface = nf_rows(ob[104], repl={
 "UR_NF47": "Giao tiếp người dùng: toàn bộ giao diện bằng tiếng Việt, phông chữ Unicode; thời gian tương đối hiển thị theo 6 mức: " + TIME_FMT + "; số đếm từ 1.000 viết tắt dạng 1,2K và từ 1.000.000 dạng 1,2M. Ô soạn bình luận trên điện thoại là thanh nhập cố định ở đáy màn hình, nở lên tối đa 3 dòng khi bàn phím bật; trên web là ô nhập nội tuyến; Smart TV không có ô nhập.",
 "UR_NF51": "Giao tiếp phần mềm — hệ thống bên ngoài: xác thực và đọc tên hiển thị, avatar, loại hồ sơ qua MyTV Auth/SSO; lấy siêu dữ liệu phim (poster, tên phim) từ Dịch vụ Nội dung cho thẻ phim trên màn Bình luận của nội dung; gửi thông báo qua Dịch vụ Push (APNs/FCM) và Trung tâm thông báo sẵn có; gọi Nhà cung cấp AI để phân loại nội dung.",
})

body += [h1("CÁC YÊU CẦU PHI CHỨC NĂNG"),
 h2("Yêu cầu bảo mật, phân quyền người sử dụng"), sec,
 h2("Yêu cầu sao lưu và phục hồi dữ liệu"), ob[92],
 h2("Yêu cầu về tính khả dụng (Usability)"), usab,
 h2("Yêu cầu về tính ổn định (Reliability)"), ob[96],
 h2("Yêu cầu về hiệu năng (Performance)"), perf,
 h2("Yêu cầu về tính hỗ trợ (Supportability)"), ob[100],
 h2("Yêu cầu các ràng buộc thiết kế (Design constraints)"), design,
 h2("Yêu cầu về giao tiếp (Interfaces)"), iface,
 h2("Các yêu cầu về tài liệu người dùng và hỗ trợ trực tuyến"), ob[106],
 h2("Các thành phần mua ngoài"), ob[108],
 h2("Các yêu cầu pháp lý, bản quyền và ghi chú khác"), ob[110],
 h2("Các tiêu chuẩn áp dụng"), ob[112],
]

# ======================= VI. NGHIỆM THU =======================
body += [h1("TIÊU CHUẨN NGHIỆM THU (*)"),
 p("Hệ thống được nghiệm thu theo từng giai đoạn triển khai. Điều kiện nghiệm thu giai đoạn này như sau:"),
 {"type": "number", "items": [
  "Hệ thống được thiết kế và vận hành đúng như mô tả trong tài liệu này, đáp ứng trên 90% các yêu cầu chức năng có mức độ ưu tiên Cao tại Chương IV (UR01, UR02, UR04, UR05, UR07, UR08, UR10) và đầy đủ UR09, UR17.",
  "Giao diện Phone, Web và Smart TV khớp bộ thiết kế Figma sau khi đội thiết kế xử lý xong các mục tại Bảng 9; đội thiết kế và BA xác nhận bằng biên bản Design QA.",
  "Toàn bộ yêu cầu phi chức năng có mức độ ưu tiên Cao tại Chương V được kiểm chứng và có biên bản kiểm thử kèm theo, đặc biệt là nhóm bảo mật UR_NF01–UR_NF10b và nhóm khả năng tiếp cận UR_NF15–UR_NF22b.",
  "Kiểm duyệt tự động khi đăng (từ khóa, AI, hai chế độ) và trạng thái Chờ duyệt được kiểm thử đầu cuối trên Phone và Web; nội dung Chờ duyệt hoặc bị khóa không rò rỉ trên bất kỳ bề mặt đọc nào, kể cả màn Bình luận của nội dung mở từ thông báo và hồ sơ Trẻ em.",
  "Tiêu chí huy hiệu Fan tích cực (7 ngày), Fan kỳ cựu (30 ngày) và Nổi bật được kiểm thử bằng bộ dữ liệu mẫu; thứ tự ưu tiên hiển thị một chip được kiểm chứng.",
  "Hệ thống được hiệu chỉnh sau khi triển khai thử nghiệm trên nhóm phim thí điểm và đạt các tiêu chí thoát của giai đoạn thí điểm do Ban sản phẩm thống nhất.",
  "Toàn bộ tài liệu và mã nguồn được bàn giao đầy đủ cho Tổng công ty Truyền thông.",
 ]},
 note("[Ghi chú: UR03, UR06, UR11–UR16, UR18–UR20 thuộc giai đoạn sau và không thuộc phạm vi nghiệm thu giai đoạn này. Việc duyệt thủ công nội dung Chờ duyệt cần một công cụ tối thiểu của bộ phận vận hành nội dung trước khi phát hành rộng; điều kiện này được ghi nhận như phụ thuộc của giai đoạn phát hành.]"),
]

doc['body'] = body
json.dump(doc, open(OUT, 'w'), ensure_ascii=False, indent=2)
print("blocks:", len(body), "figures:", fig[0])
