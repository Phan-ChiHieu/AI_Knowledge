# LLM (Large Language Model – Mô hình ngôn ngữ lớn)

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## WHAT – LLM là gì? (Bản chất)

`LLM` (Large Language Model – Mô hình ngôn ngữ lớn) là **một loại mô hình AI** được huấn luyện trên **khối lượng văn bản cực lớn** (Internet, sách, báo, mã nguồn, v.v) để học cách **dự đoán từ tiếp theo trong một câu**. Bản chất là một mô hình xác suất:

> Cho chuỗi đầu vào, LLM sẽ tính xác suất từ kế tiếp nào là hợp lý nhất.

### Cốt lõi của LLM:

- Là **mô hình học sâu (deep learning)**, thường sử dụng kiến trúc **Transformer**.
- Không có tri thức thật sự như con người. Nó chỉ "học thuộc" các mẫu ngôn ngữ thống kê.
- Đầu vào là **tokens** (biểu diễn từ dưới dạng số), đầu ra là xác suất của các token tiếp theo.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## WHY – Tại sao LLM quan trọng?

LLM là đột phá vì:

1. **Hiểu và sinh ngôn ngữ tự nhiên (Natural Language)** ở cấp độ chưa từng có: có thể viết, dịch, tóm tắt, trả lời câu hỏi.

2. **Không cần huấn luyện chuyên biệt cho từng tác vụ** – chỉ cần `prompt` đúng là làm được nhiều việc khác nhau (zero-shot, few-shot).

3. **Tăng hiệu suất lao động** trong lập trình, viết lách, nghiên cứu, chăm sóc khách hàng, v.v.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## HOW – LLM hoạt động như thế nào?

1. **Tiền xử lý (Preprocessing)**

- Văn bản được token hóa (chuyển thành chuỗi số).
- Ví dụ: "Hello world" → [15496, 995]

2. **Mô hình học (Training):**

- Mô hình học cách **dự đoán token tiếp theo** cho mỗi chuỗi đầu vào.
- Dựa vào kiến trúc `Transformer`: dùng cơ chế `Attention` để "hiểu ngữ cảnh"

3. **Sinh văn bản (Inference):**

- Khi bạn nhập một prompt, mô hình sẽ lần lượt dự đoán từng token kế tiếp → sinh ra câu hoàn chỉnh.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ỨNG DỤNG – LLM dùng để làm gì?

| Ứng dụng             | Cụ thể                                                       |
| -------------------- | ------------------------------------------------------------ |
| ✅ Chatbot           | ChatGPT, Claude, Gemini – trả lời câu hỏi, hỗ trợ khách hàng |
| ✅ Viết lách         | Viết bài, tóm tắt, dịch thuật, chỉnh sửa ngữ pháp            |
| ✅ Lập trình         | Code completion, debugging, giải thích mã                    |
| ✅ Giáo dục          | Dạy học cá nhân hoá, giải bài tập, trợ giảng                 |
| ✅ Phân tích văn bản | Tóm tắt tài liệu, trích xuất thông tin từ văn bản dài        |
| ✅ Sáng tạo nội dung | Viết truyện, thơ, nhạc, kịch bản...                          |
| ✅ Tìm kiếm nâng cao | Dựa trên ngữ nghĩa thay vì chỉ từ khoá                       |

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## Tóm tắt nhanh theo nguyên tắc 80/20:

- **20% cốt lõi**: LLM là mô hình học xác suất dự đoán từ tiếp theo trong chuỗi, dùng kiến trúc Transformer.

- **80% ứng dụng**: giao tiếp ngôn ngữ, sáng tạo, hỗ trợ lập trình, phân tích văn bản...
