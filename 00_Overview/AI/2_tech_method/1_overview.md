## ✅ Câu trả lời ngắn gọn:

### 🔸 Các thuật ngữ như:

- `chunking`
- `semantic search`
- `prompt caching`
- `retrieval augmentation`
  → **KHÔNG phải là phần lõi của mô hình (như GPT, Transformer, Attention...)**

➡️ Chúng là **kỹ thuật bổ trợ/phụ trợ** để **sử dụng mô hình tốt hơn trong ứng dụng thực tế**, đặc biệt là các hệ thống như:

- RAG (Retrieval-Augmented Generation)
- Chatbot với context lớn
- Search engine thông minh

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ Phân loại rõ ràng: "Core" vs "Usage"

| Loại                                        | Thành phần                                                 | Giải thích                                     |
| ------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------- |
| **Lõi mô hình (core)**                      | Token, Embedding, Transformer, Attention, Softmax, Loss... | Là cấu trúc bên trong GPT/Claude/Gemini        |
| **Bổ trợ cho ứng dụng (application-level)** | Chunking, Semantic Search, Prompt Caching, RAG             | Là kỹ thuật khi dùng mô hình trong app thực tế |

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ Giải thích từng thuật ngữ bạn hỏi

### 1. 🔹 **Chunking**

- **Là gì?**: Chia văn bản lớn thành các đoạn nhỏ (chunk) để xử lý từng phần
- **Vì sao cần?**: LLM như GPT chỉ đọc được số lượng token giới hạn → cần chia nhỏ tài liệu để đưa vào từng phần
- **Ứng dụng**: Làm search, RAG, tóm tắt tài liệu dài

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

### 2. 🔹 **Semantic Search**

- **Là gì?**: Tìm kiếm dựa trên ý nghĩa, không dựa vào từ khoá
- **Cốt lõi**: So sánh vector embedding của câu hỏi và tài liệu
- **Dùng trong đâu?**: RAG, chatbot hỏi đáp tài liệu nội bộ

Ví dụ:

> Câu hỏi: “CEO của Apple là ai?” → tìm đoạn chứa “Tim Cook” dù không chứa từ “CEO”

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

### 3. 🔹 **Prompt Caching**

- **Là gì?**: Lưu lại kết quả của một prompt để không cần gọi lại LLM lần nữa
- **Dùng để?**: Tăng tốc, giảm chi phí
- **Phạm vi?**: Không liên quan đến mô hình GPT, mà là tầng ứng dụng

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

### 4. 🔹 **Semantic Embedding**

- Là vector biểu diễn ngữ nghĩa của một đoạn text
- Là nền tảng cho các kỹ thuật như semantic search, clustering, hoặc RAG

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

### 5. 🔹 **RAG (Retrieval-Augmented Generation)** – Cực kỳ quan trọng

- Kết hợp mô hình sinh (LLM) + truy xuất thông tin (vector DB)
- Giải bài toán: “LLM không nhớ kiến thức ngoài training set”
- Ứng dụng: Chatbot nội bộ, QA tài liệu doanh nghiệp

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ Tóm tắt 80/20

| Nhóm               | Gồm các thuật ngữ                        | Mục đích                                        |
| ------------------ | ---------------------------------------- | ----------------------------------------------- |
| **Lõi mô hình**    | token, embedding, transformer, attention | Dự đoán ngôn ngữ                                |
| **Bổ trợ sử dụng** | chunking, semantic, prompt caching, RAG  | Kéo dài context, giảm chi phí, thêm dữ liệu mới |
