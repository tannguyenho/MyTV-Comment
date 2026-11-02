#!/usr/bin/env python3
# Sinh URD_content.json v2.0 từ v1.1 + các quyết định chốt ngày 02/11/2026 (Q1–Q33)
import json, copy

SRC = 'URD_content_v1.1.json'
OUT = 'URD_content.json'
old = json.load(open(SRC))
ob = old['body']

doc = copy.deepcopy(old)
doc['meta']['version'] = '2.0'
doc['meta']['effectiveDate'] = '02/11/2026'
doc['history'].append({
    "no": 3, "version": "2.0", "author": "Business Analyst", "approver": "", "date": "02/11/2026",
    "changes": "Chốt kịch bản theo thiết kế Figma Phone/Web/Smart TV và 12 feedback của đội phát triển: bình luận và danh tính ở cấp phim/tài khoản; giới hạn 500 ký tự; bỏ Đánh giá sao (US03), Mốc thời gian (US06), Chia sẻ (US18), định dạng văn bản và nickname riêng khỏi MVP; bổ sung bước chặn từ khóa, Hủy đăng khi chờ duyệt, luồng xử lý báo cáo và phản hồi, bảng loại thông báo và view bình luận mở từ thông báo; thêm ảnh thiết kế Web và Smart TV; bổ sung danh mục màn hình cần thiết kế thêm."
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

FLOW_NOTE = "lưu đồ trích từ Figma Phone hiện trạng; đồ họa sẽ được cập nhật sau khi đội thiết kế xử lý các ghi chú [BA] ngày 02/11/2026"

body = []

# ======================= I. TỔNG QUAN =======================
body += [h1("TỔNG QUAN"), h2("Mục đích"),
 p("Tài liệu mô tả yêu cầu của người sử dụng đối với tính năng Bình luận trên nền tảng MyTV, bao gồm khu vực thảo luận gắn với từng bộ phim truyện/VOD, cơ chế kiểm duyệt kết hợp AI và kiểm duyệt viên, hệ thống CMS quản trị nội dung và cơ chế huy hiệu khuyến khích cộng đồng."),
 p("Tài liệu là cơ sở để đội phát triển lập tài liệu Đặc tả yêu cầu phần mềm (SRS), thiết kế kiến trúc, xây dựng, kiểm thử và nghiệm thu hệ thống. Phiên bản 2.0 được chốt trên cơ sở bộ thiết kế giao diện Figma cho ba nền tảng Phone, Web và Smart TV (nguồn chính của kịch bản), backlog 5 Epic / 20 User Story, và 12 phản hồi của đội phát triển về thiết kế và kịch bản. Các quyết định chốt được ghi tại CHANGELOG_RASOAT_V5.md trong kho tài liệu dự án."),
 h2("Phạm vi"),
 p("Tài liệu áp dụng cho toàn bộ các bên tham gia dự án Bình luận MyTV: Ban sản phẩm, đội Business Analyst, đội thiết kế UX/UI, đội phát triển ứng dụng (Phone iOS/Android, Web, Smart TV/STB), đội phát triển CMS, đội kiểm thử, bộ phận vận hành kiểm duyệt nội dung và Tổng đài chăm sóc khách hàng."),
 p("Phạm vi nghiệp vụ trong giai đoạn này:", bold=True),
 bullets([
  "Phim truyện/VOD có timeline cố định. Bình luận ở cấp bộ phim: mỗi bộ phim — phim lẻ hay phim bộ — có duy nhất một khu vực bình luận dùng chung cho mọi tập; đổi tập không tải lại danh sách.",
  "Danh tính bình luận gắn với tài khoản MyTV (không gắn với từng hồ sơ xem trong tài khoản). Tên hiển thị là tên tài khoản sẵn có; chưa có tên thì hiển thị số điện thoại đã che dạng 0***123. Hồ sơ Trẻ em không nhìn thấy khu vực bình luận.",
  "Đọc bình luận công khai không cần đăng nhập; phải đăng nhập mới được Bình luận, Trả lời, Thích, Nhắc tên và Báo cáo.",
  "Bình luận và trả lời là văn bản thuần 1–500 ký tự; trả lời chỉ sâu một cấp.",
  "Kiểm duyệt gồm ba lớp: chặn theo danh sách từ khóa, AI phân loại rủi ro hai chế độ, kiểm duyệt viên xử lý hàng chờ; có trạng thái và nhật ký kiểm toán rõ ràng.",
  "Báo cáo vi phạm từ cộng đồng và luồng phản hồi kết quả cho người báo cáo và tác giả.",
  "CMS: tra cứu, xử lý nội dung, ghim, cấu hình theo phim, danh sách từ khóa chặn, chế tài người dùng, khiếu nại và audit log.",
  "Tăng trưởng và phân tích: huy hiệu người dùng, thống kê hoạt động và AI hỗ trợ vận hành.",
  "Smart TV chỉ đọc, Thích/Bỏ thích, Báo cáo (4 lý do) và hiển thị huy hiệu; có hướng dẫn kèm mã QR để chuyển sang điện thoại khi muốn tham gia bình luận.",
 ]),
 p("Ngoài phạm vi giai đoạn này (các hạng mục Deferred được giữ lại trong Figma ở trạng thái ẩn để dùng cho giai đoạn sau):", bold=True),
 table(["Hạng mục", "Lý do loại khỏi phạm vi"], [
  ["Đánh giá sao cho phim (US03)", "Ứng dụng hiện chỉ có đánh giá ứng dụng; đánh giá phim là tính năng mới hoàn toàn, cần thiết kế và nghiệp vụ riêng. Thiết kế đang ẩn trên Figma Phone/Web."],
  ["Bình luận kèm mốc thời gian (US06)", "Thiếu thiết kế highlight và thông báo mốc không hợp lệ; chỉ khả thi với phim lẻ. Chuỗi thời gian trong nội dung hiển thị như văn bản thường."],
  ["Chia sẻ bình luận ra ngoài (US18)", "Bỏ bảng chia sẻ hệ điều hành và deep link cài ứng dụng; chỉ giữ deep link nội bộ phục vụ thông báo."],
  ["Định dạng văn bản (Đậm, Nghiêng, Gạch chân, Làm mờ, Chèn liên kết)", "Đội phát triển đánh giá không cần thiết; thống nhất văn bản thuần trên mọi nền tảng. Spoiler được xử lý bằng lý do báo cáo và kiểm duyệt."],
  ["Nickname riêng cho cộng đồng", "Dùng tên hiển thị sẵn có của tài khoản MyTV; không xây dựng màn đặt/đổi nickname và chính sách AI riêng cho nickname."],
  ["Khiếu nại chế tài trong ứng dụng", "Mọi khiếu nại (Khóa bình luận, Khóa tài khoản) thực hiện qua Tổng đài 1800 1166; thông báo chế tài hiển thị hướng dẫn liên hệ."],
  ["Công tắc thông báo tương tác cộng đồng", "Dùng cài đặt thông báo chung của ứng dụng MyTV."],
  ["Nội dung phát trực tiếp (live)", "Kiểm duyệt thời gian thực là bài toán khác."],
  ["Thể thao / thiếu nhi / giải trí", "Cần chính sách kiểm duyệt riêng theo nhóm khán giả."],
  ["Frame/clip đính kèm bình luận", "Đã chốt loại khỏi MVP."],
  ["Trả lời lồng nhiều cấp", "Quyết định sản phẩm đã khóa: chỉ một cấp."],
  ["Tin nhắn riêng giữa người dùng", "Không thuộc mục tiêu thảo luận quanh nội dung."],
  ["Bộ chuyển Series ↔ Tập phía người xem", "Bình luận đã ở cấp phim nên không cần."],
 ], [40, 60]),
 h2("Tài liệu liên quan"),
 table(["STT", "Tên tài liệu", "Tên file / nguồn"], [
  ["1", "Backlog sản phẩm: 5 Epic, 20 User Story và các quyết định nghiệp vụ đã khóa", "README.md"],
  ["2", "Nhật ký rà soát và quyết định chốt kịch bản V5 (02/11/2026)", "CHANGELOG_RASOAT_V5.md"],
  ["3", "Kiến trúc giải pháp tính năng Bình luận MyTV", "SOLUTION_ARCHITECTURE.md"],
  ["4", "Yêu cầu chéo: Accessibility WCAG 2.1 AA và Bảo mật", "REQUIREMENTS_A11Y_SECURITY.md"],
  ["5", "Bản đồ kiến trúc thông tin và danh mục màn hình", "UX_INFORMATION_ARCHITECTURE_SCREEN_MAP.md"],
  ["6", "Chi tiết 20 User Story kèm tiêu chí chấp nhận và user flow", "EP01 … EP05 (thư mục theo Epic)"],
  ["7", "Thiết kế giao diện Phone — trang “Bình luận App”", "Figma: [Phone] Play Nội dung, node 39753-12055"],
  ["8", "Thiết kế giao diện Web — trang “Tính năng bình luận”", "Figma: [Web] Play Nội dung, node 16065-2741"],
  ["9", "Thiết kế giao diện Smart TV — trang “Bình luận SmartTV”", "Figma: [TV] Trang chủ, node 86-40747"],
  ["10", "Danh sách feedback kịch bản bình luận của đội phát triển", "feedback_figma_tinh_nang_kich_ban.xlsx"],
 ], [7, 55, 38]),
 h2("Giải thích từ ngữ và các chữ viết tắt"),
 table(["Thuật ngữ", "Ý nghĩa"], [
  ["Scope (phạm vi bình luận)", "Đơn vị nội dung mà một khu vực bình luận gắn vào: luôn là một bộ phim (phim lẻ hoặc cả bộ phim bộ)"],
  ["Root comment", "Bình luận gốc, không phải trả lời của bình luận khác"],
  ["Reply", "Trả lời một bình luận gốc; hệ thống chỉ hỗ trợ một cấp"],
  ["Guest", "Người xem chưa đăng nhập; chỉ được đọc bình luận công khai"],
  ["Hồ sơ Trẻ em", "Hồ sơ xem dành cho trẻ em trong tài khoản MyTV; không hiển thị khu vực bình luận"],
  ["Tên hiển thị", "Tên tài khoản MyTV hiện có; nếu rỗng thì số điện thoại đã che dạng 0***123"],
  ["Blacklist từ khóa", "Danh sách từ khóa toàn hệ thống quản lý trên CMS; nội dung khớp bị chặn ngay khi gửi, không gọi AI"],
  ["Chế độ 1 (Mode 1)", "Chế độ kiểm duyệt AI: rủi ro Nhẹ hiển thị ngay, Trung bình vào Chờ duyệt, Nặng bị chặn"],
  ["Chế độ 2 (Mode 2)", "Chế độ kiểm duyệt AI: Nhẹ và Trung bình đều vào Chờ duyệt, Nặng bị chặn"],
  ["Effective Visibility Resolver", "Module dùng chung duy nhất quyết định một nội dung có được hiển thị công khai hay không và lý do"],
  ["Ghim (Pin)", "Bình luận được quản trị viên ghim lên đầu danh sách, tối đa 3 trên một scope; hiển thị bằng marker riêng, không phải huy hiệu"],
  ["Sắp xếp Nổi bật", "Chế độ sắp xếp mặc định dùng Featured Score"],
  ["Huy hiệu Nổi bật", "Huy hiệu tự động cấp toàn MyTV, hiển thị cạnh tên; khác với Ghim và khác với sắp xếp Nổi bật"],
  ["Featured Score", "Điểm nổi bật của bình luận: 0,5×ln(1+Like) + 0,3×ln(1+Reply) + 0,2×e^(-AgeHours/72)"],
  ["Net Like", "Số lượt Thích công khai hiện tại của một bình luận"],
  ["Overlay (màn tối)", "Lớp phủ tối trên trình phát và nội dung bên dưới khi người dùng đang thao tác với bình luận; chặn mọi tương tác với các lớp dưới, video vẫn phát"],
  ["Ẩn", "Trạng thái kiểm duyệt chính thức do CMS/Admin áp; không dùng cho trạng thái tạm"],
  ["Non-public tạm thời", "Trạng thái tạm do Khóa tài khoản hoặc scope Đóng bình luận, không đổi trạng thái kiểm duyệt"],
  ["Khóa bình luận", "Chế tài chặn tạo mới Bình luận, Trả lời, Nhắc tên và Sửa; vẫn cho tự xóa, Thích, Báo cáo"],
  ["Khóa tài khoản (Account Lock)", "Chế tài chặn đăng nhập và sử dụng MyTV; khiếu nại qua Tổng đài 1800 1166"],
  ["Active day", "Ngày người dùng đã đăng nhập mở/đọc khu vực Bình luận đang khả dụng ít nhất một lần; tối đa 1 ngày/tài khoản/ngày"],
  ["SLA", "Cam kết thời gian xử lý: kiểm duyệt 24 giờ, khiếu nại 48 giờ"],
  ["CMS", "Content Management System — hệ thống quản trị nội dung dành cho kiểm duyệt viên và quản trị viên"],
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
  ["3", "MT03", "Giữ môi trường an toàn bằng ba lớp kiểm duyệt (từ khóa, AI, kiểm duyệt viên), có chế tài và khiếu nại minh bạch", "Kiểm duyệt viên, Quản trị viên, Người xem", "Cao"],
  ["4", "MT04", "Cung cấp dữ liệu vận hành để đội nội dung hiểu nội dung nào tạo ra thảo luận", "Đội nội dung, Ban sản phẩm", "Cao"],
  ["5", "MT05", "Tạo cơ chế tăng trưởng qua huy hiệu và AI hỗ trợ vận hành cộng đồng", "Người xem, Quản trị viên", "Trung bình"],
  ["6", "MT06", "Bảo đảm khả năng tiếp cận WCAG 2.1 AA và các yêu cầu bảo mật XSS/IDOR/PII xuyên suốt", "Toàn bộ đối tượng", "Cao"],
  ["7", "MT07", "Trải nghiệm thống nhất trên Phone, Web và Smart TV theo đúng bộ thiết kế Figma đã chốt", "Người xem, Đội thiết kế, Đội phát triển", "Cao"],
 ], [5, 11, 29, 32, 23]),
 h2("Đối tượng người dùng của hệ thống"),
 p("Hệ thống Bình luận là một miền nghiệp vụ mới, tiêu thụ các dịch vụ sẵn có của MyTV (Xác thực/SSO và hồ sơ tài khoản, Dịch vụ Nội dung, Trình phát video, Dịch vụ Push, Nhà cung cấp AI, Kho dữ liệu) chứ không thay thế chúng. Trình phát video chỉ cung cấp ngữ cảnh bộ phim đang xem; hệ thống không điều khiển trình phát."),
 table([{"text": "STT", "rowspan": 2}, {"text": "Tên đối tượng", "rowspan": 2}, {"text": "Mô tả", "rowspan": 2}, {"text": "Tương tác với hệ thống", "colspan": 2}, {"text": "Lợi ích mong đợi", "rowspan": 2}], [
  [{"text": "Vào", "bold": True, "align": "center", "shade": "D9D9D9"}, {"text": "Ra", "bold": True, "align": "center", "shade": "D9D9D9"}],
  ["1", "Người xem chưa đăng nhập (Guest)", "Khán giả đang xem phim truyện/VOD trên MyTV nhưng chưa đăng nhập", "Mở tab/khu vực Bình luận, cuộn danh sách, đổi cách sắp xếp, mở thread phản hồi", "Danh sách bình luận công khai, số lượng bình luận, thanh nhắc đăng nhập", "Tham khảo cảm nhận cộng đồng trước và trong khi xem"],
  ["2", "Người xem đã đăng nhập", "Khán giả có tài khoản MyTV, được thực hiện toàn bộ thao tác tương tác", "Gửi bình luận, trả lời, thích, nhắc tên, báo cáo, sửa, xóa và hủy đăng nội dung của mình", "Bình luận đã đăng kèm trạng thái, thông báo tương tác và kiểm duyệt, huy hiệu", "Bày tỏ cảm nhận, thảo luận với cộng đồng và được ghi nhận đóng góp"],
  ["3", "Hồ sơ Trẻ em", "Hồ sơ xem dành cho trẻ em trong một tài khoản MyTV", "Không có", "Không hiển thị khu vực Bình luận trên mọi nền tảng", "Không tiếp xúc nội dung do người dùng tạo"],
  ["4", "Kiểm duyệt viên (Moderator)", "Nhân sự vận hành xử lý hàng chờ kiểm duyệt trong phạm vi được cấp", "Duyệt, từ chối, ẩn, xóa mềm, hoàn tác, xử lý hàng loạt, bỏ qua báo cáo", "Hàng chờ ưu tiên theo mức rủi ro, cảnh báo quá SLA, kết quả tra cứu", "Kiểm soát chất lượng nội dung đúng SLA 24 giờ"],
  ["5", "Quản trị viên (Admin)", "Nhân sự có thẩm quyền cấu hình, ghim và áp chế tài", "Cấu hình chế độ kiểm duyệt, ngưỡng AI và danh sách từ khóa chặn; ghim bình luận; áp cảnh báo/khóa bình luận/khóa tài khoản; cấp huy hiệu thủ công", "Nhật ký kiểm toán, báo cáo thống kê, kết quả đề xuất của AI", "Vận hành cộng đồng an toàn, đúng quy định và đo lường được"],
  ["6", "Tổng đài chăm sóc khách hàng", "Bộ phận tiếp nhận khiếu nại chế tài qua số 1800 1166", "Nhập khiếu nại Khóa bình luận và Khóa tài khoản của người dùng vào CMS", "Trạng thái và kết quả xử lý khiếu nại", "Giải quyết khiếu nại cho người dùng, kể cả khi không đăng nhập được"],
  ["7", "Đội nội dung và Ban sản phẩm", "Bộ phận theo dõi hiệu quả nội dung và tính năng", "Chọn bộ lọc, khoảng thời gian, kết xuất báo cáo", "Bảng chỉ số Engagement, tỷ lệ an toàn, thời gian xử lý hàng chờ, tệp CSV/XLSX", "Ra quyết định nội dung và đầu tư dựa trên dữ liệu"],
 ], [5, 13, 20, 22, 22, 18], caption="Bảng 1: Đối tượng người dùng và tương tác với hệ thống"),
]

# ======================= III. QUY TRÌNH NGHIỆP VỤ =======================
body += [h1("QUY TRÌNH NGHIỆP VỤ"), h2("Quy trình nghiệp vụ tổng thể"),
 p("Quy trình tổng thể của tính năng Bình luận đi từ lúc người xem mở khu vực bình luận, qua ba lớp kiểm duyệt (từ khóa, AI, kiểm duyệt viên), tới lúc nội dung được hiển thị công khai hoặc bị chặn, kèm nhánh báo cáo, chế tài và khiếu nại."),
 p("Quy ước đánh mã bước quy trình:", bold=True),
 bullets(["Mỗi bước được đánh mã theo dạng CMT.xx.<Tên bước>, với xx chạy từ 01 đến 99.", "Quy trình con mang cả mã quy trình mẹ: CMT.xx.yy.<Tên bước con>."]),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["B01", "Mở khu vực bình luận", "Người xem", "Người xem chọn tab Bình luận (Phone), cuộn tới khu vực Bình luận (Web) hoặc bấm nút Bình luận trên thanh điều khiển (Smart TV). Hệ thống hiển thị số lượng bình luận (gốc + trả lời công khai) và danh sách theo sắp xếp Nổi bật. Hồ sơ Trẻ em không thấy khu vực này."],
  ["B02", "Xác định quyền tương tác", "Hệ thống", "Guest chỉ được đọc. Khi guest chọn một thao tác tương tác, hệ thống điều hướng sang đăng nhập rồi quay lại đúng phim/thread/bình luận, không tự thực hiện lại thao tác cũ."],
  ["B03", "Gửi nội dung", "Người xem đã đăng nhập", "Người dùng gửi bình luận, trả lời hoặc bản sửa dưới dạng văn bản thuần. Hệ thống kiểm tra độ dài 1–500 ký tự, tên miền liên kết, ký tự đối kháng và giới hạn tần suất trước khi kiểm tra từ khóa."],
  ["B04", "Chặn theo danh sách từ khóa", "Hệ thống", "Đối chiếu nội dung với danh sách từ khóa chặn toàn hệ thống (không phân biệt hoa/thường, có chuẩn hóa dấu). Khớp → chặn ngay như mức Nặng, không gọi AI, hiển thị “Bình luận không được chấp thuận”."],
  ["B05", "Phân loại bằng AI", "Hệ thống — AI Adapter", "AI phân loại rủi ro Nhẹ / Trung bình / Nặng. Timeout 5 giây, lỗi hoặc ngôn ngữ ngoài Việt/Anh đều chuyển sang Chờ duyệt."],
  ["B06", "Quyết định hiển thị theo chế độ", "Hệ thống", "Chế độ 1: Nhẹ hiển thị ngay, Trung bình vào Chờ duyệt. Chế độ 2: Nhẹ và Trung bình đều vào Chờ duyệt. Rủi ro Nặng bị chặn ngay tại thời điểm gửi. Nội dung Chờ duyệt hiển thị riêng cho tác giả kèm lựa chọn Hủy đăng."],
  ["B07", "Kiểm duyệt thủ công", "Kiểm duyệt viên", "Kiểm duyệt viên xử lý hàng chờ ưu tiên theo mức rủi ro, SLA 24 giờ. Thao tác gồm Duyệt, Từ chối, Ẩn, Xóa mềm, Hoàn tác và xử lý hàng loạt tối đa 100 mục."],
  ["B08", "Xác định khả năng hiển thị thực tế", "Hệ thống — Effective Visibility Resolver", "Tổng hợp năm cơ chế ẩn theo thứ tự ưu tiên và trả về kết quả hiển thị kèm thông báo tương ứng cho mọi bề mặt đọc và deep link từ thông báo."],
  ["B09", "Hiển thị công khai và tương tác", "Người xem", "Nội dung hợp lệ được hiển thị; người dùng đã đăng nhập có thể Thích, Trả lời, Nhắc tên và Báo cáo. Smart TV chỉ Thích và Báo cáo."],
  ["B10", "Tiếp nhận và xử lý báo cáo vi phạm", "Người xem đã đăng nhập / Kiểm duyệt viên", "Người dùng báo cáo theo bộ lý do chuẩn. Báo cáo không tự động ẩn nội dung. Sau khi CMS xử lý, người báo cáo nhận thông báo đã xử lý (không nêu chế tài), tác giả nhận thông báo kèm lý do nếu nội dung bị ẩn/từ chối/xóa."],
  ["B11", "Áp chế tài", "Quản trị viên", "Cảnh báo, Khóa bình luận tạm thời hoặc Khóa tài khoản, kèm lý do bắt buộc theo taxonomy chung. Thông báo chế tài nêu lý do, thời hạn và hướng dẫn liên hệ Tổng đài."],
  ["B12", "Tiếp nhận khiếu nại", "Người dùng / Tổng đài", "Mọi khiếu nại chế tài thực hiện qua Tổng đài 1800 1166 (miễn phí, 24/7); Tổng đài nhập khiếu nại vào CMS. SLA 48 giờ."],
  ["B13", "Ghi nhận chỉ số và nhật ký", "Hệ thống", "Ghi Engagement Score, chỉ số an toàn và vận hành; ghi nhật ký kiểm toán bất biến lưu 2 năm, độc lập với xóa mềm 90 ngày."],
 ], [10, 20, 18, 52], caption="Bảng 2: Mô tả các bước của quy trình nghiệp vụ tổng thể"),
 p("Thứ tự ưu tiên các cơ chế ẩn (Effective Visibility Resolver): khi một bình luận rơi vào từ hai cơ chế ẩn trở lên cùng lúc, hệ thống dùng thông báo của cơ chế có mức ưu tiên cao nhất."),
 ob[27],
 h2("Quy trình nghiệp vụ chi tiết"),
 note("[Ảnh màn hình trích từ Figma Phone (375×812), Web (1920×1080) và Smart TV (1920×1080) theo hiện trạng ngày 02/11/2026. Các ghi chú [BA] đã đặt trên Figma liệt kê những điểm cần sửa; sau khi đội thiết kế cập nhật, ảnh trong tài liệu sẽ được thay bằng bản mới theo cùng vị trí.]"),
]

# ---- 3.2.1 Đọc ----
body += [h3("Quy trình đọc khu vực bình luận"),
 p("Quy trình mô tả hai nhánh chưa đăng nhập và đã đăng nhập, trạng thái tải khung xương, trạng thái rỗng, trạng thái scope Đóng bình luận và lối vào thread Phản hồi. Khu vực bình luận gắn với bộ phim: phim bộ mặc định mở tab Các tập, phim lẻ mặc định mở tab Tương tự; đổi tập không tải lại bình luận."),
 img(FL+"US01.jpg", 16, cap(f"Lưu đồ đọc khu vực bình luận (US01) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.01.B01", "Mở trang nội dung", "Người xem", "Phone: phim bộ mở tab Các tập, phim lẻ mở tab Tương tự; tab Bình luận hiển thị nhãn “Bình luận ({count})”. Web: khu vực “Bình luận ({count})” nằm trong trang phim, dưới các khối đề xuất. Smart TV: nút Bình luận trên thanh điều khiển mở bảng bình luận bên phải trình phát. Hồ sơ Trẻ em: không hiển thị tab/khu vực/nút."],
  ["CMT.01.B02", "Tải danh sách", "Hệ thống", "Hiển thị khung xương trong lúc tải, sau đó trả 10 bình luận gốc đầu tiên theo sắp xếp Nổi bật (tối đa 3 bình luận ghim đứng đầu), tải thêm 10 mục mỗi lần cuộn. Số đếm = bình luận gốc + trả lời công khai; từ 1.000 viết tắt 1,2K, từ 1.000.000 viết tắt 1,2M."],
  ["CMT.01.B03", "Hiển thị theo trạng thái đăng nhập", "Hệ thống", "Guest thấy thanh “Đăng nhập để bình luận”. Người đã đăng nhập thấy ô soạn bình luận: Phone là thanh nhập cố định đáy màn hình; Web là ô nhập ở đầu khu vực Bình luận. Smart TV luôn hiển thị dải nhắc “Mở ứng dụng MyTV trên thiết bị di động hoặc website để thêm bình luận và trả lời”."],
  ["CMT.01.B04", "Hiển thị card bình luận", "Hệ thống", "Mỗi card gồm avatar, tên hiển thị, nhãn “Bạn” nếu là bình luận của chính mình, marker Ghim (nếu có), tối đa một huy hiệu, thời gian tương đối (Vừa xong / {n} phút trước / {n} giờ trước / {n} ngày trước ≤ 7 ngày / dd/mm/yyyy), nội dung, nút Thích kèm số, nút Trả lời, lối vào “{n} phản hồi”, menu ⋮. Nội dung dài hơn 4 dòng được cắt kèm “Xem thêm” (Phone, Web); Smart TV hiển thị đủ nội dung."],
  ["CMT.01.B05", "Mở thread Phản hồi", "Người xem", "Phone: màn “Phản hồi” riêng; Web: mở rộng inline dưới bình luận gốc, có “Thu gọn”; Smart TV: trang thread chỉ đọc. Thread tải 3 trả lời đầu theo thứ tự cũ → mới, nút “Xem thêm {n} phản hồi” tải tối đa 10 mục mỗi lần."],
  ["CMT.01.B06", "Trạng thái đặc biệt", "Hệ thống", "Chưa có bình luận: trạng thái rỗng “Hãy là người đăng bình luận đầu tiên”. Scope Đóng: giữ tab nhưng bỏ số đếm, ẩn danh sách và ô soạn, hiển thị “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”. Lỗi tải: cho thử lại."],
 ], [12, 20, 16, 52]),
 img(PH+"01_list_nologin.png", 5.2, cap("Phone — Tab Bình luận ở trạng thái chưa đăng nhập, có danh sách công khai và thanh nhắc đăng nhập")),
 img(PH+"03_skeleton.png", 5.2, cap("Phone — Khung xương trong lúc tải danh sách")),
 img(PH+"04_list_login.png", 5.2, cap("Phone — Danh sách bình luận khi đã đăng nhập, ô soạn cố định đáy màn hình")),
 img(PH+"24_empty_state.png", 5.2, cap("Phone — Trạng thái rỗng: chưa có bình luận nào")),
 img(PH+"02_closed_scope.png", 5.2, cap("Phone — Trạng thái scope Đóng bình luận: tab giữ, bỏ số đếm, ẩn danh sách và ô soạn")),
 img(WB+"web_list.jpg", 16, cap("Web — Khu vực Bình luận trong trang phim: ô nhập, nút Sắp xếp theo, danh sách bình luận và lối vào phản hồi")),
 img(TV+"tv_list.jpg", 16, cap("Smart TV — Bảng bình luận bên phải trình phát, chỉ đọc, dải nhắc chuyển sang điện thoại/website")),
 img(TV+"tv_skeleton.jpg", 16, cap("Smart TV — Khung xương trong lúc tải")),
 img(TV+"tv_empty.jpg", 16, cap("Smart TV — Trạng thái rỗng")),
 img(TV+"tv_login_qr.jpg", 16, cap("Smart TV — Hướng dẫn tải ứng dụng kèm mã QR và đăng nhập để tham gia bình luận")),
]

# ---- 3.2.2 Sắp xếp ----
body += [h3("Quy trình sắp xếp và tải thêm bình luận"),
 p("Người xem đổi cách sắp xếp giữa Nổi bật (mặc định), Mới nhất và Nhiều lượt thích. Phone dùng bottom sheet “Sắp xếp theo”, Web dùng dropdown cùng tên; Smart TV không có điều khiển sắp xếp và luôn dùng Nổi bật. Mở một bộ phim khác thì sắp xếp trở về Nổi bật; đổi tập trong cùng bộ phim giữ nguyên."),
 img(FL+"US02.jpg", 11, cap(f"Lưu đồ tải thêm và sắp xếp bình luận (US02) — {FLOW_NOTE}")),
 img(PH+"06_sort_sheet.png", 5.2, cap("Phone — Bottom sheet Sắp xếp theo: Nổi bật, Mới nhất, Nhiều lượt thích")),
 img(WB+"web_sort.jpg", 16, cap("Web — Dropdown Sắp xếp theo")),
]

# ---- 3.2.3 Đăng ----
body += [h3("Quy trình đăng bình luận qua kiểm duyệt"),
 p("Đây là quy trình lõi của hệ thống, quyết định nội dung được hiển thị ngay, vào hàng chờ duyệt hay bị chặn tại thời điểm gửi. Bình luận là văn bản thuần tối đa 500 ký tự; không có định dạng."),
 img(FL+"US04.jpg", 16, cap(f"Lưu đồ đăng bình luận qua kiểm duyệt (US04, US11) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.02.B01", "Mở ô soạn bình luận", "Người xem đã đăng nhập", "Phone: thanh nhập cố định đáy màn hình nở lên tối đa 3 dòng khi bàn phím bật; đồng thời hiện overlay tối chặn tương tác với trình phát và nội dung bên dưới, video vẫn phát; bấm vùng tối để đóng. Web: ô nhập nội tuyến ở đầu khu vực Bình luận."],
  ["CMT.02.B02", "Soạn nội dung", "Người xem đã đăng nhập", "Văn bản thuần, có thể gõ @ để nhắc tên. Bộ đếm ký tự hiển thị khi gần ngưỡng; vượt 500 ký tự thì bộ đếm chuyển đỏ, nút gửi bị vô hiệu và hiện thông báo “Bạn đã vượt quá 500 ký tự”."],
  ["CMT.02.B03", "Kiểm tra hợp lệ tại client", "Hệ thống", "Độ dài 1–500 ký tự, chặn nội dung chỉ có khoảng trắng, chỉ cho liên kết thuộc mytv.com.vn và tên miền con thực, chuẩn hóa ký tự đối kháng."],
  ["CMT.02.B04", "Kiểm tra giới hạn tần suất", "Hệ thống", "Tối đa 5 nội dung Bình luận và Trả lời trong 1 phút cho mỗi người dùng; riêng thao tác Sửa tối đa 5 lần/phút trên mỗi bình luận. Tài khoản đang Khóa bình luận bị chặn tạo mới."],
  ["CMT.02.B05", "Chặn theo danh sách từ khóa", "Hệ thống", "Khớp từ khóa trong danh sách chặn toàn hệ thống → chặn ngay, không gọi AI, không tốn quota AI; hiển thị lỗi nội tuyến “Bình luận không được chấp thuận”, nội dung giữ trong ô để người dùng sửa."],
  ["CMT.02.B06", "Gọi AI phân loại", "Hệ thống — AI Adapter", "Timeout 5 giây; lỗi, dịch vụ không khả dụng, ngôn ngữ ngoài Việt/Anh hoặc độ tin cậy thấp đều chuyển sang Chờ duyệt."],
  ["CMT.02.B07", "Áp quyết định theo chế độ", "Hệ thống", "Chế độ 1: Nhẹ hiển thị ngay, Trung bình vào Chờ duyệt. Chế độ 2: Nhẹ và Trung bình đều vào Chờ duyệt. Nặng bị chặn với cùng thông báo như bước B05."],
  ["CMT.02.B08", "Hiển thị trạng thái Chờ duyệt cho tác giả", "Hệ thống", "Card mờ kèm dòng “Bình luận của bạn sẽ sớm được xuất hiện”, chỉ tác giả thấy. Menu ⋮ chỉ có “Hủy đăng bình luận” (không có Sửa). Hủy → gỡ khỏi hàng chờ, toast “Đã hủy bình luận”, không hoàn quota tần suất."],
  ["CMT.02.B09", "Chờ kiểm duyệt viên xử lý", "Kiểm duyệt viên", "Mục Chờ duyệt vào hàng chờ ưu tiên theo mức rủi ro, SLA 24 giờ. Quá SLA vẫn giữ trạng thái chờ, được đánh dấu Quá SLA và ưu tiên trong hàng chờ."],
  ["CMT.02.B10", "Công khai nội dung", "Hệ thống", "Nội dung được duyệt trở thành công khai, trừ khi còn cơ chế ẩn khác đang có hiệu lực theo Effective Visibility Resolver. Nội dung bị Từ chối: tác giả nhận thông báo kèm lý do và thấy card ở trạng thái “Không được chấp thuận”."],
 ], [12, 20, 16, 52]),
 img(PH+"21_composer_typing.png", 5.2, cap("Phone — Ô soạn khi bàn phím bật, overlay tối phủ trình phát")),
 img(PH+"22_rejected.png", 5.2, cap("Phone — Nội dung bị chặn tại thời điểm gửi: lỗi nội tuyến “Bình luận không được chấp thuận”")),
 img(PH+"23_pending.png", 5.2, cap("Phone — Bình luận đang Chờ duyệt (chỉ tác giả thấy) và menu Hủy đăng bình luận")),
 img(WB+"web_500char_limit.jpg", 16, cap("Web — Trạng thái vượt quá 500 ký tự")),
 img(WB+"web_pending_moderation.jpg", 16, cap("Web — Bình luận chờ xét duyệt")),
]

# ---- 3.2.4 Sửa/Xóa ----
body += [h3("Quy trình sửa, xóa và hủy đăng bình luận"),
 p("Kết quả của một lần sửa phụ thuộc chế độ kiểm duyệt của phim: khi bản mới đang chờ duyệt thì bản cũ vẫn công khai. Bình luận đang Chờ duyệt không được sửa, chỉ được hủy đăng. Người dùng tự xóa bình luận gốc sẽ kéo theo toàn bộ trả lời bị xóa mềm, giữ 90 ngày và quản trị viên không được hoàn tác để công khai lại."),
 img(FL+"US05.jpg", 11, cap(f"Lưu đồ sửa và xóa bình luận (US05) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.04.B01", "Mở menu của bình luận của mình", "Người xem đã đăng nhập", "Card có nhãn “Bạn”; menu ⋮ gồm Chỉnh sửa bình luận và Xóa bình luận (bình luận Chờ duyệt: chỉ Hủy đăng; bình luận bị ẩn/từ chối: chỉ Xóa)."],
  ["CMT.04.B02", "Sửa", "Người xem đã đăng nhập", "Nội dung cũ được nạp vào ô soạn; áp dụng cùng ràng buộc và cùng ba lớp kiểm duyệt như đăng mới. Bản được duyệt mang nhãn “Đã chỉnh sửa”; toast “Chỉnh sửa thành công”."],
  ["CMT.04.B03", "Xóa", "Người xem đã đăng nhập", "Hộp thoại xác nhận: không có trả lời → “Bình luận này sẽ bị xóa và không thể khôi phục lại”; có trả lời → cảnh báo toàn bộ phản hồi liên quan sẽ bị xóa theo. Xác nhận → xóa mềm, toast “Xóa bình luận thành công”."],
  ["CMT.04.B04", "Hủy đăng khi Chờ duyệt", "Người xem đã đăng nhập", "Gỡ nội dung khỏi hàng chờ kiểm duyệt, không tạo bản lưu, không ghi nhật ký kiểm toán, không hoàn quota tần suất; toast “Đã hủy bình luận”."],
 ], [12, 20, 16, 52]),
 img(PH+"16_own_kebab_edit_delete.png", 5.2, cap("Phone — Menu của bình luận của mình: Chỉnh sửa / Xóa")),
 img(PH+"17_delete_dialog.png", 5.2, cap("Phone — Xác nhận xóa bình luận không có trả lời")),
 img(PH+"18_delete_dialog_has_reply.png", 5.2, cap("Phone — Xác nhận xóa bình luận có trả lời: cảnh báo trả lời của người khác sẽ bị xóa theo")),
 img(PH+"19_edited_toast.png", 5.2, cap("Phone — Sửa thành công, bình luận mang nhãn Đã chỉnh sửa")),
 img(WB+"web_editdelete_menu.jpg", 16, cap("Web — Menu Chỉnh sửa / Xóa trên bình luận của mình")),
]

# ---- 3.2.5 Trả lời ----
body += [h3("Quy trình trả lời bình luận một cấp"),
 p("Trả lời chỉ sâu một cấp. Trả lời một trả lời khác vẫn nằm trong cùng thread và ô soạn được điền sẵn @tên tác giả của trả lời đó. Thứ tự trả lời là cũ → mới; trả lời vừa gửi được thêm vào cuối danh sách và tự cuộn tới. Smart TV chỉ đọc thread."),
 img(FL+"US08.jpg", 16, cap(f"Lưu đồ trả lời bình luận một cấp (US08) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.05.B01", "Mở thread", "Người xem", "Phone: bấm nút Trả lời hoặc “{n} phản hồi” mở màn “Phản hồi” (bình luận gốc ở đầu, các trả lời nối bằng đường chỉ). Web: mở rộng inline dưới bình luận gốc, ô nhập trả lời xuất hiện ngay dưới gốc. Smart TV: trang thread chỉ đọc."],
  ["CMT.05.B02", "Soạn trả lời", "Người xem đã đăng nhập", "Ô soạn điền sẵn @tên người được trả lời; cùng ràng buộc 1–500 ký tự và ba lớp kiểm duyệt như bình luận gốc."],
  ["CMT.05.B03", "Hiển thị kết quả", "Hệ thống", "Trả lời hợp lệ xuất hiện cuối thread; số “{n} phản hồi” trên bình luận gốc cập nhật. Trả lời Chờ duyệt chỉ tác giả thấy. Bình luận gốc không công khai thì trả lời cũng không hiển thị độc lập."],
 ], [12, 20, 16, 52]),
 img(PH+"05_reply_view.png", 5.2, cap("Phone — Màn Phản hồi: bình luận gốc và các trả lời một cấp")),
 img(PH+"07_reply_sheet_compose.png", 5.2, cap("Phone — Soạn trả lời với ô nhập điền sẵn @tên người được trả lời")),
 img(WB+"web_reply.jpg", 16, cap("Web — Ô nhập trả lời nội tuyến dưới bình luận gốc")),
 img(TV+"tv_reply_readonly.jpg", 16, cap("Smart TV — Thread phản hồi chỉ đọc")),
]

# ---- 3.2.6 Thích ----
body += [h3("Quy trình thích và bỏ thích bình luận"),
 p("Thích/Bỏ thích dùng giao diện lạc quan: biểu tượng tô đặc màu cam kèm số đếm màu cam khi đã thích, viền xám khi chưa thích. Thao tác được gom theo lô tối đa 5 giây rồi đồng bộ về máy chủ; nhiều lần Thích/Bỏ thích liên tiếp trên cùng đối tượng trong một lô được gộp về trạng thái cuối cùng. Áp dụng trên cả ba nền tảng."),
 img(FL+"US07.jpg", 15, cap(f"Lưu đồ Thích và Bỏ thích bình luận (US07) — {FLOW_NOTE}")),
 img(PH+"20_like_a.png", 5.2, cap("Phone — Bình luận chưa thích")),
 img(PH+"20_like_b.png", 5.2, cap("Phone — Bình luận đã thích, biểu tượng và số đếm chuyển màu cam")),
]

# ---- 3.2.7 Nhắc tên & thông báo ----
body += [h3("Quy trình nhắc tên và nhận thông báo"),
 p("Người dùng gõ @ để nhắc tên; danh sách gợi ý ưu tiên người trong cùng thread rồi đến người đã tham gia bộ phim, chỉ trả về tên hiển thị hoặc định danh đã che. Tên được nhắc hiển thị màu cam nhưng không bấm được (không có trang hồ sơ công khai). Thông báo dùng Trung tâm thông báo sẵn có của ứng dụng và push của hệ điều hành; không có công tắc riêng cho thông báo cộng đồng."),
 img(FL+"US09.jpg", 16, cap(f"Lưu đồ nhắc tên và nhận thông báo (US09) — {FLOW_NOTE}")),
 table(["Loại thông báo", "Nội dung mẫu", "Bấm vào mở", "Nền tảng"], [
  ["Trả lời / Nhắc tên", "“{Tên} đã trả lời bình luận của bạn” / “{Tên} đã nhắc đến bạn trong bộ phim {Tên phim}”", "Phone: view Bình luận toàn màn hình (không trình phát) có nút “Xem phim”; Web: trang phim, tự cuộn tới khu vực Bình luận, mở thread; Smart TV: trang phim + thread chỉ đọc. Bình luận đích được highlight 2 giây.", "Phone, Web, TV"],
  ["Báo cáo đã được xử lý (người báo cáo)", "“Báo cáo của bạn về một bình luận đã được xử lý”", "Không mở màn nào; chỉ đánh dấu đã đọc. Không nêu chế tài.", "Phone, Web, TV"],
  ["Bình luận bị ẩn / từ chối / xóa (tác giả)", "“Bình luận của bạn đã bị ẩn do: {lý do}”", "Phone: màn Chi tiết thông báo; Web: modal “Vi phạm tiêu chuẩn”. Hiển thị lý do và trích nội dung.", "Phone, Web, TV"],
  ["Cảnh báo / Khóa bình luận", "“Tài khoản của bạn bị khóa bình luận đến {ngày giờ} do: {lý do}. Liên hệ 1800 1166 để khiếu nại”", "Màn Chi tiết thông báo / modal Vi phạm tiêu chuẩn.", "Phone, Web, TV"],
  ["Được cấp huy hiệu", "“Bạn vừa nhận huy hiệu {tên huy hiệu}”", "Sheet/modal “Huy hiệu thành viên”. Smart TV: không mở.", "Phone, Web, TV"],
  ["Khóa tài khoản", "Không có thông báo trong ứng dụng (người dùng không đăng nhập được); có thể push nếu thiết bị nhận được.", "Màn hình khóa khi đăng nhập: trạng thái, lý do, số 1800 1166.", "—"],
 ], [20, 30, 36, 14], caption="Bảng 4: Loại thông báo và đích đến khi bấm"),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.06.B01", "Gõ @ và chọn người", "Người xem đã đăng nhập", "Danh sách gợi ý hiện sau ký tự @; chọn một người để chèn @Tên vào nội dung. Ô nhắc tên không được dùng để dò danh sách tài khoản ngoài thread hoặc phim hiện tại."],
  ["CMT.06.B02", "Gửi thông báo", "Hệ thống", "Khi nội dung công khai, người được nhắc tên/trả lời nhận thông báo trong ứng dụng và push (tiêu đề + tên phim, không chứa số điện thoại đầy đủ). Người đang Khóa tài khoản không nhận thông báo cộng đồng; sau mở khóa không bù lại. Thông báo lưu 90 ngày."],
  ["CMT.06.B03", "Mở từ thông báo", "Người xem", "Đích đến theo Bảng 4. Nếu bình luận đích không còn khả dụng, hiển thị thông báo tương ứng của Effective Visibility Resolver ngay tại vị trí đó."],
 ], [12, 20, 16, 52]),
 img(PH+"08_mention_picker.png", 5.2, cap("Phone — Gợi ý nhắc tên khi gõ @")),
 img(PH+"09_push_notification.png", 5.2, cap("Phone — Thông báo đẩy khi được nhắc tên")),
 img(PH+"10_notification_center.png", 5.2, cap("Phone — Trung tâm thông báo")),
 img(PH+"11_notification_detail.png", 5.2, cap("Phone — Chi tiết thông báo (dùng cho thông báo vi phạm và chế tài)")),
 img(WB+"web_notification.jpg", 16, cap("Web — Danh sách thông báo và modal Vi phạm tiêu chuẩn")),
 note("[Cần thiết kế bổ sung: view Bình luận toàn màn hình mở từ thông báo trên Phone (header Quay lại + “Bình luận” + tên phim + nút “Xem phim”); ba mẫu item thông báo mới (báo cáo đã xử lý, bình luận bị ẩn, nhận huy hiệu) trên Phone và Web — xem Bảng 7.]"),
]

# ---- 3.2.8 Báo cáo ----
body += [h3("Quy trình báo cáo vi phạm, xử lý và phản hồi"),
 p("Người dùng báo cáo bình luận vi phạm theo bộ lý do chuẩn; chọn “Khác” bắt buộc nhập mô tả 1–500 ký tự hợp lệ ngay trong cùng bottom sheet/modal. Không được báo cáo nội dung của chính mình. Cùng một đối tượng chỉ được báo cáo lại sau 24 giờ, giới hạn 10 báo cáo trong 1 giờ cho mỗi người dùng. Báo cáo không tự ẩn nội dung; kết quả được phản hồi tới cả người báo cáo và tác giả."),
 img(FL+"US10.jpg", 16, cap(f"Lưu đồ báo cáo bình luận vi phạm (US10) — {FLOW_NOTE}")),
 table(["Mã bước thực hiện", "Tên bước", "Người thực hiện", "Diễn giải bước thực hiện"], [
  ["CMT.07.B01", "Gửi báo cáo", "Người xem đã đăng nhập", "Menu ⋮ của bình luận người khác → Báo cáo bình luận → chọn lý do: Có spoiler / Spam, Quảng cáo / Xúc phạm, ngôn từ công kích / Nội dung không phù hợp / Khác (Phone, Web); Smart TV chỉ 4 lý do đầu. Chọn “Khác” → ô nhập mô tả 0/500 trượt xuống, nút Báo cáo chỉ bật khi có ít nhất 1 ký tự không phải khoảng trắng. Gửi xong: toast “Báo cáo thành công, bình luận sẽ được xem xét” (Smart TV: popup “Quý khách đã gửi báo cáo thành công”)."],
  ["CMT.07.B02", "Xử lý trên CMS", "Kiểm duyệt viên", "Mục bị báo cáo vào hàng chờ kèm lý do và mô tả. Kiểm duyệt viên chọn Bỏ qua báo cáo (không vi phạm) hoặc Ẩn / Từ chối / Xóa mềm kèm lý do; có thể áp chế tài cho tác giả."],
  ["CMT.07.B03", "Phản hồi người báo cáo", "Hệ thống", "Thông báo trong ứng dụng “Báo cáo của bạn về một bình luận đã được xử lý”; không nêu chế tài chi tiết; không bấm mở."],
  ["CMT.07.B04", "Phản hồi tác giả", "Hệ thống", "Nếu nội dung bị Ẩn/Từ chối/Xóa: thông báo “Bình luận của bạn đã bị ẩn do: {lý do}” mở màn chi tiết; nếu bị chế tài: thông báo kèm lý do, thời hạn và hướng dẫn liên hệ 1800 1166."],
  ["CMT.07.B05", "Hiển thị trạng thái trên card của tác giả", "Hệ thống", "Trong danh sách, chỉ tác giả thấy card ở trạng thái “Bình luận đã bị ẩn” / “Không được chấp thuận” kèm lý do, nội dung mờ, menu ⋮ chỉ còn Xóa. Người khác không thấy card."],
 ], [12, 20, 16, 52]),
 img(PH+"12_kebab_menu.png", 5.2, cap("Phone — Menu của bình luận người khác (mục Chia sẻ sẽ được gỡ theo ghi chú [BA])")),
 img(PH+"13_report_sheet.png", 5.2, cap("Phone — Bottom sheet chọn lý do báo cáo")),
 img(PH+"14_report_toast.png", 5.2, cap("Phone — Toast báo cáo thành công")),
 img(WB+"web_report.jpg", 16, cap("Web — Modal Báo cáo bình luận")),
 img(TV+"tv_report.jpg", 16, cap("Smart TV — Popup báo cáo với 4 lý do")),
 img(TV+"tv_report_success.jpg", 16, cap("Smart TV — Thông báo gửi báo cáo thành công")),
 note("[Cần thiết kế bổ sung: ô nhập mô tả khi chọn “Khác” (Phone, Web); trạng thái card bị ẩn/từ chối cho tác giả (Phone, Web) — xem Bảng 7.]"),
]

# ---- 3.2.9 Huy hiệu ----
body += [h3("Quy trình hiển thị và giải thích huy hiệu"),
 p("Huy hiệu được hệ thống tự động xét hằng ngày (Fan tích cực, Fan kỳ cựu, Nổi bật) hoặc do quản trị viên cấp thủ công (Custom, ví dụ “Chuyên gia”). Mỗi card hiển thị tối đa một huy hiệu theo thứ tự ưu tiên Custom > Nổi bật > Fan kỳ cựu > Fan tích cực. Ghim là marker riêng, không chiếm vị trí huy hiệu. Bấm chip huy hiệu mở sheet/modal “Huy hiệu thành viên” giải thích ý nghĩa, không hiển thị số liệu tiêu chí; Smart TV chỉ hiển thị chip."),
 img(FL+"US17.jpg", 12, cap(f"Lưu đồ huy hiệu người dùng (US17) — {FLOW_NOTE}")),
 img(PH+"15_badge_sheet.png", 5.2, cap("Phone — Sheet Huy hiệu thành viên")),
 img(WB+"web_badge.jpg", 16, cap("Web — Modal Huy hiệu thành viên")),
 img(TV+"tv_badge_list.jpg", 16, cap("Smart TV — Chip huy hiệu cạnh tên trong danh sách")),
]

# ---- 3.2.10 CMS ----
cms = copy.deepcopy(ob[68])
cms['rows'] = [
  ["CMT.08.B01", "Mở hàng chờ kiểm duyệt", "Kiểm duyệt viên", "Hàng chờ mặc định xếp mục rủi ro cao trước; cùng mức rủi ro thì mục chờ lâu hơn xếp trước. Mục bị báo cáo hiển thị lý do và mô tả báo cáo."],
  ["CMT.08.B02", "Tra cứu và lọc", "Kiểm duyệt viên", "Tra cứu theo phim, người dùng, trạng thái, mức rủi ro và khoảng thời gian; kết xuất CSV và XLSX theo bộ lọc."],
  ["CMT.08.B03", "Xử lý nội dung", "Kiểm duyệt viên", "Duyệt không cần lý do. Từ chối, Ẩn và Xóa bắt buộc chọn lý do theo taxonomy chuẩn; lý do “Vi phạm khác” bắt buộc ghi chú 1–500 ký tự. Bỏ qua báo cáo không cần lý do. Kết quả được thông báo tới tác giả và người báo cáo theo Bảng 4."],
  ["CMT.08.B04", "Xử lý hàng loạt", "Kiểm duyệt viên", "Chỉ hỗ trợ Duyệt, Từ chối, Ẩn và Xóa mềm, tối đa 100 mục mỗi lần, cho phép thành công một phần."],
  ["CMT.08.B05", "Hoàn tác", "Kiểm duyệt viên", "Từ chối trở về Chờ duyệt, Ẩn trở về Hiển thị, Xóa mềm trở về trạng thái ngay trước khi xóa. Hoàn tác không tự khôi phục Ghim hoặc huy hiệu đã mất."],
  ["CMT.08.B06", "Ghim và cấu hình theo phim", "Quản trị viên", "Tối đa 3 bình luận ghim trên mỗi bộ phim, kéo thả vị trí 1–3, có thể đặt thời hạn. Cấu hình chế độ, ngưỡng AI và trạng thái Đóng bình luận kế thừa theo thứ tự override cấp phim → mặc định hệ thống."],
  ["CMT.08.B07", "Quản lý danh sách từ khóa chặn", "Quản trị viên", "Một danh sách toàn hệ thống, thêm/sửa/xóa từ khóa có audit log; không có override theo phim. Khớp từ khóa chặn nội dung ngay khi gửi."],
  ["CMT.08.B08", "Áp chế tài", "Quản trị viên", "Nhẹ áp Cảnh báo; Trung bình áp Khóa bình luận tạm thời; Nặng cho phép chọn Khóa bình luận hoặc Khóa tài khoản tùy bối cảnh. Thông báo gửi người dùng nêu lý do, thời hạn và hướng dẫn liên hệ Tổng đài."],
  ["CMT.08.B09", "Xử lý khiếu nại", "Quản trị viên / Tổng đài", "Mọi khiếu nại chế tài đi qua Tổng đài 1800 1166 và được Tổng đài nhập vào CMS. SLA 48 giờ; quá hạn vẫn giữ chế tài, đánh dấu Quá SLA và ưu tiên hàng chờ."],
  ["CMT.08.B10", "Ghi nhật ký kiểm toán", "Hệ thống", "Mọi thao tác quản trị được ghi bất biến và lưu 2 năm, độc lập với thời hạn xóa mềm 90 ngày."],
]
body += [h3("Quy trình kiểm duyệt và chế tài trên CMS"),
 note("[Thiết kế giao diện CMS chưa có trên Figma; mục này mô tả ở cấp nghiệp vụ. Lưu đồ và ảnh màn hình CMS sẽ được bổ sung khi có thiết kế.]"),
 cms]

# ======================= IV. YÊU CẦU CHỨC NĂNG =======================
URH = ['STT', 'Mã yêu cầu', 'Tên yêu cầu', 'Mô tả', 'Mức độ ưu tiên', 'Mức độ quan trọng', 'Đối tượng liên quan']
URW = [4, 8, 14, 42, 8, 8, 16]
def ur(stt, code, name, pb, inp, out, proc, exc, pri, imp, who):
    desc = "Phát biểu yêu cầu: " + pb + "\nThông tin đầu vào:\n" + "\n".join("- " + i for i in inp) + "\nThông tin đầu ra: " + out + "\nChức năng xử lý: " + proc + "\nCác ngoại lệ: " + exc
    return [str(stt), code, name, desc, pri, imp, who]
def deferred(stt, code, name, reason, who):
    desc = ("Phát biểu yêu cầu: Deferred — không triển khai trong giai đoạn này. " + reason +
            "\nThông tin đầu vào: N/A\nThông tin đầu ra: N/A\nChức năng xử lý: N/A — thiết kế giữ ở trạng thái ẩn trên Figma để dùng cho giai đoạn sau.\nCác ngoại lệ: N/A")
    return [str(stt), code, name, desc, "Thấp", "Thấp", who]

body += [h1("YÊU CẦU CHỨC NĂNG"),
 p("Hệ thống được chia thành 5 phân hệ tương ứng 5 Epic của backlog sản phẩm. Mỗi yêu cầu chức năng mang một mã UR duy nhất và được tham chiếu lại tại chương Tiêu chuẩn nghiệm thu. Các yêu cầu Deferred (UR03, UR06, UR18) giữ mã để không đánh số lại các tài liệu phụ thuộc."),
 table(["Phân hệ", "Tên phân hệ", "Mã yêu cầu", "Nền tảng áp dụng"], [
  ["PH01", "Trải nghiệm bình luận", "UR01 – UR06 (UR03, UR06 Deferred)", "Phone, Web; Smart TV chỉ đọc"],
  ["PH02", "Tương tác cộng đồng", "UR07 – UR09", "Phone, Web; Smart TV chỉ Thích/Bỏ thích"],
  ["PH03", "An toàn và kiểm duyệt", "UR10 – UR12", "Phone, Web, Smart TV (Báo cáo 4 lý do), CMS"],
  ["PH04", "CMS quản trị bình luận", "UR13 – UR16", "Chỉ Web/Desktop"],
  ["PH05", "Tăng trưởng và phân tích", "UR17 – UR20 (UR18 Deferred)", "Phone, Web, Smart TV (hiển thị huy hiệu), CMS"],
 ], [12, 30, 28, 30], caption="Bảng 5: Cây chức năng tổng thể hệ thống"),
 table(["Màn hình / thành phần", "Phone", "Web", "Smart TV", "User Story"], [
  ["Danh sách bình luận (tab/khu vực/bảng) + số đếm", "Có", "Có", "Có", "US01, US02"],
  ["Khung xương, trạng thái rỗng, trạng thái scope Đóng", "Có", "Có", "Có (rỗng, khung xương; Đóng dạng thông báo)", "US01, US12"],
  ["Thanh nhắc đăng nhập / hướng dẫn QR", "Thanh “Đăng nhập để bình luận”", "Card “Request Login”", "Màn hướng dẫn QR + hotline", "US01"],
  ["Điều khiển sắp xếp", "Bottom sheet", "Dropdown", "Không", "US02"],
  ["Ô soạn bình luận + overlay", "Thanh nhập đáy màn hình, overlay tối", "Ô nhập nội tuyến, backdrop modal", "Không", "US04"],
  ["Trạng thái vượt 500 ký tự / bị chặn / Chờ duyệt + Hủy đăng", "Có (vượt 500: cần vẽ)", "Có (Hủy đăng: cần vẽ)", "Không", "US04, US05"],
  ["Menu ⋮ (Sửa/Xóa — Báo cáo), hộp thoại xóa, nhãn Đã chỉnh sửa, nhãn Bạn", "Có (nhãn Bạn: cần vẽ)", "Có (nhãn Bạn: cần vẽ)", "Chỉ Báo cáo", "US05, US10"],
  ["Thread Phản hồi + ô trả lời điền sẵn @", "Màn Phản hồi", "Mở rộng inline", "Trang thread chỉ đọc", "US08"],
  ["Thích / Bỏ thích", "Có", "Có", "Có", "US07"],
  ["Gợi ý nhắc tên", "Có", "Có", "Không", "US09"],
  ["Trung tâm thông báo, push, chi tiết thông báo / modal vi phạm", "Có", "Có", "Mục thông báo sẵn có của TV", "US09, US10, US16"],
  ["View Bình luận toàn màn hình mở từ thông báo", "Cần vẽ", "Dùng trang phim + cuộn", "Trang phim + thread", "US09, US12"],
  ["Sheet/modal Báo cáo + ô mô tả “Khác”", "Có (ô mô tả: cần vẽ)", "Có (ô mô tả: cần vẽ)", "Popup 4 lý do", "US10"],
  ["Card bị ẩn / không được chấp thuận (tác giả)", "Cần vẽ", "Cần vẽ", "Không", "US12, US14"],
  ["Chip huy hiệu, marker Ghim, sheet/modal Huy hiệu thành viên", "Có (marker Ghim: cần vẽ)", "Có (marker Ghim: cần vẽ)", "Chip (marker Ghim: cần vẽ)", "US15, US17"],
  ["Màn hình chặn đăng nhập khi Khóa tài khoản", "Cần vẽ", "Cần vẽ", "Cần vẽ (text + hotline)", "US16"],
 ], [34, 20, 20, 14, 12], caption="Bảng 6: Ma trận màn hình theo nền tảng (trạng thái thiết kế Figma ngày 02/11/2026)"),
]

# ---- PH01 ----
body += [h2("Phân hệ Trải nghiệm bình luận"),
 p("Phân hệ cung cấp khu vực thảo luận gắn với từng bộ phim, gồm đọc, sắp xếp, đăng, sửa, xóa và hủy đăng bình luận."),
 table(URH, [
  ur(1, "UR01", "Đọc khu vực bình luận",
     "Cho phép mọi người xem, kể cả chưa đăng nhập, đọc bình luận công khai của bộ phim đang xem trên Phone, Web và Smart TV.",
     ["Mã phim (*): lấy từ ngữ cảnh trang nội dung; phim bộ dùng chung một scope cho mọi tập", "Trạng thái đăng nhập và loại hồ sơ của phiên hiện tại"],
     "Số lượng bình luận (gốc + trả lời công khai, viết tắt K/M từ 1.000), danh sách 10 bình luận gốc đầu tiên theo sắp xếp Nổi bật với tối đa 3 bình luận ghim đứng đầu, lối vào “{n} phản hồi”, thanh nhắc đăng nhập hoặc ô soạn bình luận tùy trạng thái đăng nhập; Smart TV hiển thị dải nhắc chuyển sang điện thoại/website.",
     "Xác định scope theo bộ phim; đổi tập không tải lại; gọi Effective Visibility Resolver để lọc nội dung; hiển thị khung xương trong lúc tải; tải thêm 10 bình luận mỗi lần cuộn; card gồm avatar, tên hiển thị, nhãn “Bạn”, marker Ghim, tối đa một huy hiệu, thời gian tương đối, nội dung cắt 4 dòng kèm “Xem thêm” (Smart TV hiển thị đủ); thread tải 3 trả lời đầu theo thứ tự cũ → mới và thêm tối đa 10 trả lời mỗi lần.",
     "Hồ sơ Trẻ em không hiển thị khu vực bình luận; scope đang Đóng thì giữ tab nhưng bỏ số đếm, ẩn danh sách, ô soạn và các thao tác, hiện “Khu vực bình luận hiện không khả dụng. Vui lòng quay lại sau”; chưa có bình luận nào thì hiển thị trạng thái rỗng; lỗi tải danh sách thì cho thử lại.",
     "Cao", "Cao", "Người xem"),
  ur(2, "UR02", "Xem số lượng và sắp xếp bình luận",
     "Cho phép người xem đổi cách sắp xếp danh sách bình luận và tải thêm nội dung khi cuộn.",
     ["Chế độ sắp xếp (*): Nổi bật, Mới nhất hoặc Nhiều lượt thích", "Vị trí cuộn hiện tại của danh sách"],
     "Danh sách bình luận theo chế độ đã chọn, nhãn chế độ sắp xếp hiện hành (“Nổi bật” khi mặc định), số lượng bình luận.",
     "Sắp xếp Nổi bật là mặc định, dùng Featured Score 0,5×ln(1+Like) + 0,3×ln(1+Reply) + 0,2×e^(-AgeHours/72) với Like là Net Like công khai hiện tại; tối đa 3 bình luận ghim luôn đứng đầu và không tham gia tính Featured Score; tải 10 bình luận gốc mỗi lần; trả lời không xuất hiện trong danh sách gốc; mở bộ phim khác thì sắp xếp trở về Nổi bật, đổi tập giữ nguyên.",
     "Smart TV không có điều khiển sắp xếp; không còn dữ liệu để tải thêm; lỗi mạng khi tải thêm thì giữ danh sách hiện có và cho thử lại; bình luận ghim của tài khoản đang bị khóa tạm bị ẩn và giữ metadata.",
     "Cao", "Cao", "Người xem"),
  deferred(3, "UR03", "Đánh giá phim", "Đánh giá sao cho phim là tính năng mới cần thiết kế riêng (ứng dụng hiện chỉ có đánh giá ứng dụng). Khi bật lại sẽ áp dụng ở cấp phim, một đánh giá hiện hành mỗi tài khoản, không xóa đánh giá.", "Người xem đã đăng nhập"),
  ur(4, "UR04", "Đăng bình luận",
     "Cho phép người xem đã đăng nhập gửi bình luận dạng văn bản thuần cho bộ phim đang xem, đi qua ba lớp kiểm duyệt.",
     ["Nội dung bình luận (*): 1–500 ký tự văn bản thuần, cho phép chỉ có emoji, không chấp nhận chỉ khoảng trắng, có thể chứa @nhắc tên", "Mã phim (*)"],
     "Bình luận ở trạng thái công khai hoặc Chờ duyệt (card mờ “Bình luận của bạn sẽ sớm được xuất hiện”, chỉ tác giả thấy, có Hủy đăng); lỗi nội tuyến “Bình luận không được chấp thuận” khi bị chặn; bộ đếm ký tự và thông báo “Bạn đã vượt quá 500 ký tự”.",
     "Phone: ô soạn cố định đáy màn hình nở tối đa 3 dòng, hiện overlay tối chặn tương tác với trình phát và nội dung bên dưới, video vẫn phát; Web: ô nhập nội tuyến. Kiểm tra độ dài, ký tự đối kháng và tên miền liên kết (chỉ mytv.com.vn và tên miền con thực); giới hạn 5 nội dung Bình luận và Trả lời trong 1 phút cho mỗi người dùng; đối chiếu danh sách từ khóa chặn toàn hệ thống (khớp → chặn ngay, không gọi AI); gọi AI phân loại; áp quyết định theo Chế độ 1 hoặc Chế độ 2; tên hiển thị trên card là tên tài khoản MyTV hoặc số điện thoại đã che.",
     "Nội dung rỗng hoặc chỉ khoảng trắng; vượt 500 ký tự thì nút gửi vô hiệu; vượt giới hạn tần suất; khớp từ khóa chặn hoặc AI trả rủi ro Nặng thì chặn tại thời điểm gửi và giữ nội dung trong ô; AI timeout 5 giây, lỗi hoặc ngôn ngữ ngoài tiếng Việt và tiếng Anh thì chuyển sang Chờ duyệt; tài khoản đang bị Khóa bình luận thì chặn tạo mới; scope Đóng ẩn ô soạn; Smart TV không có ô soạn.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  ur(5, "UR05", "Sửa, xóa và hủy đăng bình luận của mình",
     "Cho phép người dùng sửa hoặc xóa bình luận và trả lời do chính mình tạo, và hủy đăng nội dung đang Chờ duyệt.",
     ["Mã bình luận hoặc mã trả lời (*)", "Nội dung mới khi sửa (*): áp dụng cùng ràng buộc như khi đăng mới", "Xác nhận của người dùng khi xóa (*)"],
     "Bản sửa được duyệt mang nhãn “Đã chỉnh sửa” và toast “Chỉnh sửa thành công”; hộp thoại xác nhận xóa nêu rõ hệ quả (có/không có trả lời); toast “Xóa bình luận thành công”; toast “Đã hủy bình luận” khi hủy đăng.",
     "Card của mình có nhãn “Bạn”, menu ⋮ gồm Chỉnh sửa và Xóa; bình luận Chờ duyệt chỉ có Hủy đăng; bình luận bị ẩn/từ chối chỉ có Xóa. Kết quả một lần sửa phụ thuộc chế độ kiểm duyệt — Chế độ 1 với rủi ro Nhẹ thì bản mới công khai ngay, Chế độ 1 với rủi ro Trung bình hoặc Chế độ 2 thì bản mới vào Chờ duyệt và bản cũ vẫn công khai trong lúc chờ; giới hạn 5 lần sửa mỗi phút trên mỗi bình luận; tự xóa bình luận gốc kéo theo toàn bộ trả lời bị xóa mềm và giữ 90 ngày; hủy đăng gỡ mục khỏi hàng chờ, không tạo bản lưu, không hoàn quota.",
     "Từ khóa chặn hoặc rủi ro Nặng bị chặn tại thời điểm gửi và bản cũ giữ nguyên; Khóa bình luận chặn sửa mới nhưng vẫn cho tự xóa; người dùng không xem được lịch sử phiên bản, chỉ CMS và nhật ký kiểm toán xem được; quản trị viên không được hoàn tác để công khai lại nội dung người dùng tự xóa; Smart TV không có Sửa/Xóa.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  deferred(6, "UR06", "Bình luận kèm mốc thời gian", "Chỉ khả thi với phim lẻ, thiếu thiết kế highlight và thông báo mốc không hợp lệ. Trong giai đoạn này chuỗi thời gian trong nội dung hiển thị như văn bản thường, không bấm được và hệ thống không tương tác với trình phát.", "Người xem đã đăng nhập"),
 ], URW),
]

# ---- PH02 ----
body += [h2("Phân hệ Tương tác cộng đồng"),
 p("Phân hệ cung cấp các thao tác tương tác giữa người xem với nhau: Thích, Trả lời một cấp và Nhắc tên kèm thông báo."),
 table(URH, [
  ur(1, "UR07", "Thích và bỏ thích bình luận",
     "Cho phép người dùng đã đăng nhập bày tỏ sự tán thành với một bình luận hoặc trả lời trên Phone, Web và Smart TV.",
     ["Mã bình luận hoặc mã trả lời (*)", "Trạng thái Thích hiện tại của người dùng trên đối tượng đó"],
     "Biểu tượng Thích đổi trạng thái ngay lập tức (tô đặc màu cam và số đếm màu cam khi đã thích; viền xám khi chưa) và số lượt Thích cập nhật theo, viết tắt K/M từ 1.000.",
     "Giao diện cập nhật lạc quan trước, client gom thao tác theo lô tối đa 5 giây rồi đồng bộ về máy chủ, đẩy sớm khi rời màn hình hoặc chuyển nền; nhiều lần Thích và Bỏ thích liên tiếp trên cùng đối tượng trong một lô được gộp về trạng thái cuối cùng; máy chủ là nguồn chân lý; người dùng được Thích nội dung của chính mình.",
     "Chưa đăng nhập thì điều hướng sang đăng nhập và không tự thực hiện lại thao tác; đồng bộ thất bại thì hoàn nguyên trạng thái trên giao diện và thông báo cho công nghệ hỗ trợ đọc màn hình; lượt Thích do tài khoản đang bị khóa tạo ra vẫn giữ bản ghi nhưng tạm không tính vào Net Like công khai.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  ur(2, "UR08", "Trả lời bình luận một cấp",
     "Cho phép người dùng trả lời một bình luận gốc hoặc một trả lời khác trong cùng thread, chỉ sâu một cấp.",
     ["Mã bình luận gốc (*) và, nếu trả lời một trả lời, mã trả lời được nhắc", "Nội dung trả lời (*): 1–500 ký tự, cùng ràng buộc như bình luận"],
     "Trả lời hiển thị cuối thread theo thứ tự cũ → mới và tự cuộn tới; số lượng trên lối vào “{n} phản hồi” được cập nhật; trả lời Chờ duyệt chỉ tác giả thấy.",
     "Phone: màn “Phản hồi” riêng với bình luận gốc ở đầu; Web: mở rộng inline dưới bình luận gốc với ô nhập trả lời ngay dưới gốc và nút “Thu gọn”; Smart TV: trang thread chỉ đọc. Ô soạn điền sẵn @tên người được trả lời; trả lời một trả lời vẫn nằm trong cùng thread, không tạo cấp hai; thread tải 3 trả lời đầu và thêm tối đa 10 trả lời mỗi lần, phần còn lại dưới 10 thì tải hết; đi qua cùng ba lớp kiểm duyệt như bình luận gốc.",
     "Bình luận gốc đang không công khai thì trả lời cũng không hiển thị độc lập; quản trị viên ẩn bình luận gốc hoặc tác giả gốc bị khóa tài khoản làm toàn thread tạm không công khai nhưng không đổi trạng thái kiểm duyệt của trả lời do người khác tạo; Smart TV không có ô nhập trả lời.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  ur(3, "UR09", "Nhắc tên và nhận thông báo",
     "Cho phép người dùng nhắc tên người khác trong bình luận hoặc trả lời và nhận thông báo về các tương tác, kiểm duyệt và chế tài liên quan.",
     ["Ký tự @ kèm chuỗi tìm kiếm trong ô soạn", "Lựa chọn người dùng từ danh sách gợi ý (*)"],
     "@Tên hiển thị màu cam trong nội dung, không bấm được; thông báo trong ứng dụng và push cho người được nhắc tên/trả lời; các loại thông báo và đích đến theo Bảng 4.",
     "Gợi ý ưu tiên người dùng trong cùng thread, sau đó người đã tham gia bộ phim, chỉ trả về tên hiển thị hoặc định danh đã che; dùng Trung tâm thông báo và cài đặt thông báo sẵn có của ứng dụng, không có công tắc riêng cho thông báo cộng đồng; thông báo trong ứng dụng lưu 90 ngày; bấm thông báo có bình luận đích thì Phone mở view Bình luận toàn màn hình (không trình phát, có nút “Xem phim”), Web mở trang phim và tự cuộn tới khu vực Bình luận mở sẵn thread, Smart TV mở trang phim và thread chỉ đọc; bình luận đích được highlight 2 giây; thông báo kiểm duyệt, chế tài và kết quả báo cáo là bắt buộc.",
     "Gợi ý không bao giờ trả số điện thoại hay email đầy đủ; ô nhắc tên không được dùng để dò danh sách tài khoản ngoài phạm vi thread hoặc phim hiện tại; khi người dùng đang bị khóa tài khoản thì không tạo thông báo cộng đồng mới và sau khi mở khóa không bù lại; bình luận đích không còn khả dụng thì hiển thị thông báo của Effective Visibility Resolver ngay trong view; Smart TV không có nhắc tên.",
     "Trung bình", "Trung bình", "Người xem đã đăng nhập"),
 ], URW),
]

# ---- PH03 ----
body += [h2("Phân hệ An toàn và kiểm duyệt"),
 p("Phân hệ bảo đảm nội dung hiển thị công khai đã qua kiểm soát, gồm báo cáo vi phạm từ cộng đồng kèm phản hồi kết quả, ba lớp kiểm duyệt (từ khóa, AI hai chế độ, kiểm duyệt viên) và quản lý trạng thái cùng phạm vi hiển thị."),
 table(URH, [
  ur(1, "UR10", "Báo cáo bình luận vi phạm và nhận phản hồi",
     "Cho phép người dùng đã đăng nhập báo cáo một bình luận hoặc trả lời vi phạm quy tắc cộng đồng và nhận phản hồi khi báo cáo được xử lý.",
     ["Mã bình luận hoặc mã trả lời (*)", "Lý do báo cáo (*): Có spoiler, Spam/Quảng cáo, Xúc phạm/ngôn từ công kích, Nội dung không phù hợp, Khác (Phone, Web); Smart TV chỉ 4 lý do đầu", "Mô tả bổ sung: bắt buộc 1–500 ký tự hợp lệ khi chọn lý do Khác, nhập ngay trong cùng bottom sheet/modal"],
     "Toast “Báo cáo thành công, bình luận sẽ được xem xét” (Smart TV: popup “Quý khách đã gửi báo cáo thành công”); thông báo trong ứng dụng “Báo cáo của bạn về một bình luận đã được xử lý” khi CMS xử lý xong.",
     "Mục Báo cáo chỉ hiện trong menu ⋮ của bình luận người khác; nút Báo cáo chỉ bật khi đã chọn lý do và, với Khác, có ít nhất một ký tự không phải khoảng trắng; đưa mục bị báo cáo vào hàng chờ kiểm duyệt kèm lý do và mô tả nhưng không tự động ẩn hoặc xóa dù số lượng báo cáo lớn; giới hạn 10 báo cáo trong 1 giờ cho mỗi người dùng; cùng một đối tượng chỉ được báo cáo lại sau 24 giờ; sau khi CMS kết luận, người báo cáo nhận thông báo đã xử lý và tác giả nhận thông báo kèm lý do nếu nội dung bị Ẩn/Từ chối/Xóa.",
     "Không được báo cáo nội dung của chính mình; mô tả chỉ có khoảng trắng khi chọn lý do Khác bị từ chối; người báo cáo chỉ nhận thông tin đã xử lý, không được biết chi tiết chế tài áp lên người khác; thông báo cho người báo cáo không bấm mở.",
     "Cao", "Cao", "Người xem đã đăng nhập"),
  ur(2, "UR11", "Kiểm duyệt tự động: danh sách từ khóa và AI hai chế độ",
     "Hệ thống tự động chặn hoặc phân loại rủi ro của mọi nội dung do người dùng gửi trước khi hiển thị công khai.",
     ["Toàn bộ văn bản của bình luận, trả lời hoặc bản sửa", "Danh sách từ khóa chặn toàn hệ thống", "Chế độ và ngưỡng AI áp dụng cho bộ phim tương ứng"],
     "Kết quả chặn ngay (khớp từ khóa hoặc AI Nặng), công khai (AI Nhẹ ở Chế độ 1) hoặc Chờ duyệt; mức rủi ro lưu kèm nội dung để xếp hàng chờ.",
     "Đối chiếu từ khóa không phân biệt hoa/thường, có chuẩn hóa dấu; khớp → chặn ngay như mức Nặng, không gọi AI, không tốn quota; không khớp → AI phân loại Nhẹ/Trung bình/Nặng. Chế độ 1 cho Nhẹ hiển thị ngay và Trung bình vào Chờ duyệt; Chế độ 2 cho cả Nhẹ và Trung bình vào Chờ duyệt; Nặng luôn bị chặn; ngưỡng kế thừa theo thứ tự override cấp phim → mặc định hệ thống và mọi thay đổi đều được ghi nhật ký; quản trị viên có thao tác phản hồi “AI phân loại sai” để lưu kết quả đã hiệu chỉnh.",
     "Timeout 5 giây, lỗi hoặc dịch vụ AI không khả dụng thì chuyển sang Chờ duyệt; ngôn ngữ ngoài Việt/Anh hoặc độ tin cậy thấp chuyển sang Chờ duyệt; AI phân loại theo ngữ nghĩa nên không thay thế việc làm sạch và mã hóa nội dung khi hiển thị; không có chính sách AI riêng cho nickname vì không có nickname riêng.",
     "Cao", "Cao", "Hệ thống, Kiểm duyệt viên"),
  ur(3, "UR12", "Quản lý trạng thái và phạm vi hiển thị",
     "Hệ thống phải có một nguồn chân lý duy nhất trả lời câu hỏi một nội dung có được hiển thị công khai hay không và nếu không thì vì sao.",
     ["Trạng thái kiểm duyệt của nội dung và của bình luận gốc", "Trạng thái khóa tài khoản của tác giả và của tác giả bình luận gốc", "Trạng thái đóng hoặc mở của khu vực bình luận trên bộ phim", "Danh tính người xem (để quyết định có hiển thị card bị ẩn cho chính tác giả hay không)"],
     "Kết quả cho phép hiển thị hoặc không, kèm thông báo tương ứng dùng chung cho mọi bề mặt đọc và cho đích đến của thông báo; với chính tác giả, nội dung bị Ẩn/Từ chối/Xóa do CMS hiển thị dạng card mờ kèm nhãn trạng thái và lý do.",
     "Áp dụng thứ tự ưu tiên tại Bảng 3; phân biệt rõ trạng thái kiểm duyệt chính thức với trạng thái không công khai tạm thời do khóa tài khoản hoặc đóng khu vực bình luận; mở khóa hoặc mở lại khu vực bình luận thì tự động khôi phục hiển thị cho các mục còn hợp lệ; hồ sơ Trẻ em không nhận bất kỳ nội dung bình luận nào.",
     "Nội dung do người dùng tự xóa hoặc hủy đăng không bao giờ hiển thị lại; khóa tài khoản vĩnh viễn giữ trạng thái không công khai vô thời hạn và không tự xóa mềm nội dung; card bị ẩn chỉ hiển thị cho tác giả, không hiển thị cho người khác dưới bất kỳ hình thức nào.",
     "Cao", "Cao", "Hệ thống, Người xem"),
 ], URW),
]

# ---- PH04 ----
ur15 = ur(3, "UR15", "Quản lý bình luận ghim, cấu hình theo phim và danh sách từ khóa chặn",
   "Cho phép quản trị viên ghim bình luận tiêu biểu, cấu hình chế độ kiểm duyệt cho từng bộ phim và quản lý danh sách từ khóa chặn toàn hệ thống.",
   ["Mã bình luận cần ghim và vị trí mong muốn từ 1 đến 3", "Thời hạn ghim (tùy chọn)", "Chế độ kiểm duyệt và ngưỡng AI ở cấp phim hoặc mặc định hệ thống", "Trạng thái đóng hoặc mở khu vực bình luận và thời điểm hiệu lực", "Từ khóa chặn (*): thêm, sửa, xóa"],
   "Danh sách bình luận ghim theo thứ tự đã đặt, hiển thị trên ứng dụng bằng marker Ghim riêng (không chiếm vị trí huy hiệu); cấu hình đang áp dụng cho từng bộ phim; danh sách từ khóa chặn hiện hành; bản ghi nhật ký kiểm toán.",
   "Tối đa 3 bình luận ghim trên mỗi bộ phim, cho phép kéo thả vị trí; cấu hình kế thừa theo thứ tự override cấp phim → mặc định hệ thống; chuyển từ Chế độ 2 sang Chế độ 1 thì mục đang chờ có kết quả AI Nhẹ tự hiển thị còn mức Trung bình tiếp tục chờ; chuyển từ Chế độ 1 sang Chế độ 2 thì nội dung đã hiển thị vẫn giữ nguyên và chế độ mới chỉ áp dụng cho dữ liệu phát sinh từ thời điểm hiệu lực; danh sách từ khóa là một danh sách toàn hệ thống, không có override theo phim, mọi thay đổi có audit log và có hiệu lực cho nội dung gửi sau thời điểm lưu.",
   "Ghim trên nội dung của tài khoản đang bị khóa chỉ tạm ẩn và giữ thông tin, tự hiện lại khi mở khóa nếu còn hợp lệ; thao tác kiểm duyệt Ẩn, Xóa hoặc Từ chối làm mất ghim; đóng khu vực bình luận vẫn giữ hàng chờ nhưng mục được duyệt chưa công khai cho tới khi mở lại; thay đổi danh sách từ khóa không áp dụng hồi tố cho nội dung đã công khai.",
   "Cao", "Cao", "Quản trị viên")
ur16 = ur(4, "UR16", "Quản lý người dùng vi phạm và nhật ký kiểm toán",
   "Cho phép quản trị viên áp chế tài với người dùng vi phạm, xử lý khiếu nại do Tổng đài nhập và tra cứu nhật ký kiểm toán.",
   ["Mã tài khoản người dùng (*)", "Loại chế tài (*): Cảnh báo, Khóa bình luận tạm thời hoặc Khóa tài khoản", "Lý do theo taxonomy chung (*) và ghi chú 1–500 ký tự khi chọn “Vi phạm khác”", "Thời hạn chế tài với các mức 10 phút, 1 giờ, 1 ngày, 3 ngày, 7 ngày, 1 tháng hoặc tùy chọn", "Khiếu nại do Tổng đài nhập (*)"],
   "Trạng thái chế tài của tài khoản; thông báo gửi tới người dùng nêu lý do, thời hạn và hướng dẫn liên hệ 1800 1166; kết quả xử lý khiếu nại; nhật ký kiểm toán bất biến.",
   "Mức Nhẹ áp Cảnh báo, Trung bình áp Khóa bình luận tạm, Nặng cho phép chọn Khóa bình luận hoặc Khóa tài khoản; Khóa bình luận chặn tạo mới Bình luận, Trả lời, Nhắc tên và Sửa nhưng vẫn cho tự xóa, Thích và Báo cáo; Khóa tài khoản chặn đăng nhập và hiển thị màn hình khóa kèm trạng thái, lý do và số Tổng đài 1800 1166 (Phone, Web, Smart TV); mọi khiếu nại đi qua Tổng đài và được nhập vào CMS; nhật ký kiểm toán lưu 2 năm, độc lập với thời hạn xóa mềm 90 ngày.",
   "Không có Khóa bình luận vĩnh viễn; không có form khiếu nại trong ứng dụng; SLA khiếu nại 48 giờ, quá hạn vẫn giữ chế tài, đánh dấu Quá SLA và ưu tiên hàng chờ; khi khóa tài khoản có hiệu lực thì phiên đăng nhập hiện tại phải bị vô hiệu hóa ngay, không chỉ chặn đăng nhập mới.",
   "Cao", "Cao", "Quản trị viên, Tổng đài")
body += [h2("Phân hệ CMS quản trị bình luận"),
 p("Phân hệ dành cho kiểm duyệt viên và quản trị viên, chỉ thiết kế cho Web/Desktop. Mọi hành động ghi phải được kiểm tra quyền và phạm vi ở tầng API, không chỉ chặn ở giao diện."),
 table(URH, [ob[84]['rows'][0], ob[84]['rows'][1], ur15, ur16], URW),
]

# ---- PH05 ----
body += [h2("Phân hệ Tăng trưởng và phân tích"),
 p("Phân hệ tạo động lực đóng góp cho cộng đồng và cung cấp dữ liệu vận hành cho đội nội dung."),
 table(URH, [
  ur(1, "UR17", "Huy hiệu người dùng",
     "Ghi nhận đóng góp của người dùng tích cực bằng huy hiệu hiển thị cạnh tên trên Phone, Web và Smart TV.",
     ["Số ngày hoạt động, số bình luận và trả lời hợp lệ, số lượt Thích nhận được trong cửa sổ trượt", "Quyết định cấp huy hiệu thủ công của quản trị viên kèm tên huy hiệu Custom (ví dụ “Chuyên gia”) và thời hạn tùy chọn"],
     "Chip huy hiệu cạnh tên (tối đa một chip); sheet/modal “Huy hiệu thành viên” giải thích ý nghĩa Fan tích cực, Fan kỳ cựu, Nổi bật và các huy hiệu độc quyền khác, không hiển thị số liệu tiêu chí; thông báo khi được cấp huy hiệu.",
     "Fan tích cực yêu cầu 30 ngày gần nhất có tối thiểu 7 ngày hoạt động và 10 bình luận hoặc trả lời hợp lệ; Fan kỳ cựu yêu cầu 90 ngày gần nhất có tối thiểu 30 ngày hoạt động, 30 bình luận hoặc trả lời hợp lệ và 30 lượt Thích nhận được; huy hiệu Nổi bật cấp khi nội dung công khai đạt tối thiểu 20 Net Like công khai, 5 trả lời và nằm trong nhóm 10% Featured Score cao nhất toàn MyTV trong 30 ngày; đánh giá lại hằng ngày, có 7 ngày ân hạn trước khi thu hồi huy hiệu Fan; thứ tự ưu tiên hiển thị Custom > Nổi bật > Fan kỳ cựu > Fan tích cực; Ghim là marker riêng và không chiếm vị trí huy hiệu; bấm chip mở sheet/modal giải thích trên Phone và Web, Smart TV chỉ hiển thị chip.",
     "Ngày hoạt động chỉ tính khi người dùng đã đăng nhập mở khu vực bình luận đang khả dụng, tối đa một ngày cho mỗi tài khoản mỗi ngày; khách chưa đăng nhập, hồ sơ Trẻ em và scope đang Đóng không tạo ngày hoạt động; người dùng tự xóa bình luận gốc làm mất đóng góp của các trả lời bị xóa theo; sau khi đã cấp, huy hiệu Nổi bật không tự thu hồi khi chỉ số giảm, chỉ mất khi nội dung nguồn bị kiểm duyệt; tắt một loại huy hiệu thì ẩn trên giao diện nhưng giữ lịch sử.",
     "Thấp", "Trung bình", "Người xem đã đăng nhập, Quản trị viên"),
  deferred(2, "UR18", "Chia sẻ bình luận", "Bỏ bảng chia sẻ hệ điều hành, bản xem trước và deep link cài ứng dụng khỏi giai đoạn này. Deep link nội bộ phục vụ thông báo được mô tả tại UR09 và UR12.", "Người xem đã đăng nhập"),
  ur(3, "UR19", "Thống kê hoạt động bình luận",
     "Cung cấp bảng chỉ số về mức độ tham gia, an toàn nội dung và hiệu quả vận hành.",
     ["Bộ lọc theo phim và khoảng thời gian"],
     "Engagement Score, số người bình luận duy nhất, tỷ lệ báo cáo được xác nhận, tỷ lệ nội dung bị ẩn/xóa/từ chối, tỷ lệ nội dung bị chặn bởi từ khóa, tỷ lệ nội dung an toàn được tự động hiển thị, thời gian xử lý hàng chờ; tệp kết xuất CSV và XLSX.",
     "Engagement Score tính theo công thức Bình luận×2 + Trả lời×2 + Net Like×1 (thành phần Đánh giá và Chia sẻ sẽ bổ sung khi bật lại UR03/UR18); bảng chỉ số có độ trễ tối đa 5 phút và được đối soát hằng ngày để tự sửa sai lệch; hiển thị song song tổng số lượt Thích và Net Like công khai, trong đó Engagement chỉ dùng Net Like công khai; hệ thống không lưu nền tảng nguồn của bình luận, lượt Thích và báo cáo.",
     "Chỉ bốn nguyên nhân loại nội dung khỏi chỉ số công khai gồm kiểm duyệt Ẩn/Từ chối/Xóa, người dùng tự xóa kéo theo, quản trị viên xử lý bình luận gốc kéo theo và khóa tài khoản; việc đóng khu vực bình luận không loại nội dung khỏi chỉ số vì đó là biện pháp vận hành chứ không phải chế tài nội dung; nội dung hủy đăng khi Chờ duyệt không tính vào bất kỳ chỉ số nào.",
     "Cao", "Cao", "Đội nội dung, Ban sản phẩm"),
  ob[87]['rows'][3],
 ], URW),
 table(["STT", "Màn hình / trạng thái cần thiết kế", "Nền tảng", "Mô tả yêu cầu", "Tham chiếu"], [
  ["1", "View Bình luận toàn màn hình mở từ thông báo", "Phone", "Header: Quay lại + tiêu đề “Bình luận” + tên phim nhỏ + nút “Xem phim” (mở trình phát). Thân: bình luận gốc và các trả lời; bình luận đích highlight 2 giây; fallback thông báo không khả dụng.", "UR09, UR12"],
  ["2", "Card bị ẩn / không được chấp thuận (chỉ tác giả thấy)", "Phone, Web", "Nội dung mờ, nhãn trạng thái “Bình luận đã bị ẩn” / “Không được chấp thuận”, dòng lý do, menu ⋮ chỉ còn Xóa.", "UR10, UR12, UR14"],
  ["3", "Ô nhập mô tả khi chọn lý do “Khác”", "Phone, Web", "Trượt xuống trong cùng bottom sheet/modal, bộ đếm 0/500, nút Báo cáo bật khi có ký tự hợp lệ; bàn phím bật thì sheet đẩy lên.", "UR10"],
  ["4", "Trạng thái vượt 500 ký tự", "Phone", "Bộ đếm đỏ 500/500, nút gửi vô hiệu, thông báo “Bạn đã vượt quá 500 ký tự” (Web đã có).", "UR04"],
  ["5", "Nút Hủy đăng khi Chờ duyệt", "Web", "Bổ sung trong menu của bình luận chờ xét duyệt, ẩn Chỉnh sửa (Phone đã có).", "UR05"],
  ["6", "Nhãn “Bạn” và marker Ghim", "Phone, Web, Smart TV", "Nhãn nhỏ sau tên trên bình luận của mình; marker Ghim (icon + chữ) ở đầu card, tách khỏi vị trí huy hiệu.", "UR01, UR15, UR17"],
  ["7", "Ba mẫu item thông báo mới", "Phone, Web", "Báo cáo đã xử lý; bình luận bị ẩn kèm lý do; nhận huy hiệu. Chi tiết thông báo chế tài hiển thị lý do, thời hạn và dòng “Liên hệ 1800 1166 để khiếu nại”.", "UR09, UR10, UR16"],
  ["8", "Màn hình chặn đăng nhập khi Khóa tài khoản", "Phone, Web, Smart TV", "Thuộc phân hệ Xác thực: trạng thái khóa, lý do, thời hạn (nếu có), số 1800 1166; Smart TV chỉ cần văn bản và hotline. Không chặn nghiệm thu tính năng bình luận.", "UR16"],
  ["9", "Sửa thiết kế hiện có theo ghi chú [BA] trên Figma", "Phone, Web, Smart TV", "Bỏ phân nhánh phim bộ/phim lẻ, gỡ Chia sẻ và deep link cài app, gỡ định dạng văn bản và link mốc thời gian, nhãn sắp xếp “Nổi bật”, sửa copy popup báo cáo Smart TV, đổi tên variant huy hiệu “Nổi bật”, xóa dòng radio trống trong sheet báo cáo.", "Toàn bộ"],
 ], [5, 25, 14, 44, 12], caption="Bảng 7: Danh mục thiết kế bổ sung và chỉnh sửa cần có trước khi phát triển"),
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
 "UR_NF05": "Toàn bộ nội dung do người dùng nhập phải được làm sạch và mã hóa ở mọi bề mặt hiển thị: web, ứng dụng di động, Smart TV, CMS và tệp kết xuất. Kết quả phân loại của AI và danh sách từ khóa không thay thế cho việc làm sạch này.",
 "UR_NF07": "Chặn hoặc trung hòa các nhóm ký tự đối kháng trong bình luận và trả lời: ký tự đảo chiều văn bản U+202E, ký tự độ rộng bằng không U+200B và U+200D, ký tự điều khiển U+0000–U+001F. Việc đối chiếu từ khóa chặn phải thực hiện sau bước chuẩn hóa này.",
 "UR_NF08": "Nội dung thông báo đẩy không chứa số điện thoại đầy đủ; tên người gửi hiển thị bằng tên hiển thị của tài khoản hoặc định danh đã che dạng 0***123.",
})
sec['rows'].append(["UR_NF10a", "Tên hiển thị lấy từ hồ sơ tài khoản MyTV; khi tài khoản chưa đặt tên, hệ thống chỉ hiển thị số điện thoại đã che (giữ số 0 đầu và 3 số cuối, che toàn bộ số giữa bằng *). Không có API nào trả số điện thoại đầy đủ cho ứng dụng."])
sec['rows'].append(["UR_NF10b", "Hồ sơ Trẻ em không được gọi bất kỳ API đọc/ghi bình luận nào; việc ẩn khu vực bình luận phải được bảo đảm ở cả giao diện và tầng API theo loại hồ sơ của phiên."])

usab = nf_rows(ob[94], repl={
 "UR_NF16": "Tương phản màu tối thiểu 4,5:1 cho văn bản thường và 3:1 cho thành phần giao diện, bao gồm trạng thái card Chờ duyệt/bị ẩn (nội dung mờ) và tên được nhắc màu cam.",
 "UR_NF17": "Vùng chạm tối thiểu 44×44pt cho mọi phần tử tương tác: nút Thích, nút Trả lời, menu ⋮, chip huy hiệu, nút Xem thêm và nút xem thêm phản hồi.",
})
usab['rows'].append(["UR_NF22a", "Khi overlay tối đang hiển thị trên Phone, mọi phần tử bên dưới (trình phát, tab, danh sách) phải bị loại khỏi thứ tự tiêu điểm của công nghệ hỗ trợ; bấm vùng tối hoặc nút Đóng đều đóng được lớp phủ."])

perf = nf_rows(ob[98], repl={
 "UR_NF28": "Thời gian phản hồi khi gửi bình luận hoặc trả lời dưới 1 giây ở phân vị 95 (không tính thời gian gọi AI), đo tại tầng API và không tính độ trễ mạng của thiết bị đầu cuối.",
})
perf['rows'].append(["UR_NF33a", "Bước đối chiếu danh sách từ khóa chặn phải hoàn thành dưới 50 ms ở phân vị 95 với danh sách tới 5.000 từ khóa."])

design = nf_rows(ob[102], repl={
 "UR_NF40": "Nội dung bình luận và trả lời được lưu dưới dạng văn bản thuần (không có dải định dạng); vị trí các @nhắc tên lưu kèm mã tài khoản được nhắc để hiển thị và gửi thông báo.",
 "UR_NF41": "Không có chức năng định dạng văn bản (Đậm, Nghiêng, Gạch chân, Làm mờ) và không có chức năng chèn siêu liên kết trong luồng soạn bình luận; chỉ URL thuộc mytv.com.vn gõ trực tiếp được tự nhận dạng.",
 "UR_NF42": "Hệ thống không điều khiển trình phát video; khi overlay thao tác bình luận hiển thị, video vẫn tiếp tục phát và trình phát không nhận tương tác cho tới khi overlay đóng.",
 "UR_NF43": "Danh tính bình luận gắn với tài khoản MyTV, không gắn với hồ sơ xem; chuyển hồ sơ trong cùng tài khoản không thay đổi danh tính, chế tài, huy hiệu hay giới hạn tần suất.",
 "UR_NF45": "Smart TV không tạo Bình luận, Trả lời, Nhắc tên, không Sửa/Xóa, không đổi cách sắp xếp; chỉ đọc (hiển thị đủ nội dung, không cắt), Thích/Bỏ thích, Báo cáo với 4 lý do và hiển thị chip huy hiệu. Smart TV hiển thị hướng dẫn kèm mã QR để chuyển sang điện thoại khi người dùng muốn tham gia bình luận.",
})
design['rows'].append(["UR_NF45a", "Thiết kế Figma Phone, Web và Smart TV là nguồn chuẩn cho bố cục và nội dung chữ trên giao diện; mọi khác biệt giữa tài liệu này và Figma phải được giải quyết bằng ghi chú [BA] trên Figma trước khi phát triển."])

iface = nf_rows(ob[104], repl={
 "UR_NF47": "Giao tiếp người dùng: toàn bộ giao diện bằng tiếng Việt, phông chữ Unicode; thời gian tương đối hiển thị Vừa xong / {n} phút trước / {n} giờ trước / {n} ngày trước (tối đa 7 ngày) rồi dd/mm/yyyy; số đếm từ 1.000 viết tắt dạng 1,2K và từ 1.000.000 dạng 1,2M. Ô soạn bình luận trên điện thoại là thanh nhập cố định ở đáy màn hình, nở lên tối đa 3 dòng khi bàn phím bật; trên web là ô nhập nội tuyến; Smart TV không có ô nhập.",
 "UR_NF51": "Giao tiếp phần mềm — hệ thống bên ngoài: xác thực và đọc tên hiển thị, avatar, loại hồ sơ qua MyTV Auth/SSO; lấy siêu dữ liệu phim từ Dịch vụ Nội dung; gửi thông báo qua Dịch vụ Push (APNs/FCM) và Trung tâm thông báo sẵn có; gọi Nhà cung cấp AI để phân loại nội dung; đẩy dữ liệu sang Kho dữ liệu báo cáo doanh nghiệp.",
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
 p("Hệ thống được nghiệm thu theo từng giai đoạn triển khai. Điều kiện nghiệm thu chung như sau:"),
 {"type": "number", "items": [
  "Hệ thống được thiết kế và vận hành đúng như mô tả trong tài liệu này, đáp ứng trên 90% các yêu cầu chức năng có mức độ ưu tiên Cao tại Chương IV (UR01, UR02, UR04, UR05, UR07, UR08, UR10, UR11, UR12, UR13, UR14, UR15, UR16, UR19).",
  "Giao diện Phone, Web và Smart TV khớp bộ thiết kế Figma sau khi đội thiết kế xử lý xong các ghi chú [BA] ngày 02/11/2026 và các màn hình bổ sung tại Bảng 7; đội thiết kế và BA xác nhận bằng biên bản Design QA.",
  "Toàn bộ yêu cầu phi chức năng có mức độ ưu tiên Cao tại Chương V được kiểm chứng và có biên bản kiểm thử kèm theo, đặc biệt là nhóm bảo mật UR_NF01–UR_NF10b và nhóm khả năng tiếp cận UR_NF15–UR_NF22a.",
  "Module quyết định khả năng hiển thị được kiểm thử đầy đủ với cả năm cơ chế ẩn và các trường hợp chồng lấn theo Bảng 3, kể cả card bị ẩn chỉ hiển thị cho tác giả; không xảy ra rò rỉ nội dung đã bị ẩn trên bất kỳ bề mặt đọc nào, kể cả đích đến của thông báo và hồ sơ Trẻ em.",
  "Ba lớp kiểm duyệt (từ khóa, AI, kiểm duyệt viên) và luồng phản hồi báo cáo tới người báo cáo và tác giả được kiểm thử đầu cuối trên Phone, Web và Smart TV.",
  "Hệ thống được hiệu chỉnh sau khi triển khai thử nghiệm trên nhóm phim thí điểm và đạt các tiêu chí thoát của giai đoạn thí điểm do Ban sản phẩm thống nhất.",
  "Tổ chức đào tạo và bàn giao tài liệu hướng dẫn cho kiểm duyệt viên, quản trị viên và Tổng đài chăm sóc khách hàng; các đối tượng này thao tác thành thạo sau khóa đào tạo.",
  "Toàn bộ tài liệu và mã nguồn được bàn giao đầy đủ cho Tổng công ty Truyền thông.",
 ]},
 note("[Ghi chú: UR03, UR06, UR18 ở trạng thái Deferred và không thuộc phạm vi nghiệm thu giai đoạn này. Các yêu cầu có mức độ ưu tiên Thấp (UR17, UR20) thuộc giai đoạn Tăng trưởng và không phải điều kiện bắt buộc để nghiệm thu giai đoạn ra mắt giới hạn.]"),
]

doc['body'] = body
json.dump(doc, open(OUT, 'w'), ensure_ascii=False, indent=2)
print("blocks:", len(body), "figures:", fig[0])
