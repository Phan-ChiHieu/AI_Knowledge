# RAG (Retrieval-Augmented Generation)

- Là một trong những kỹ thuật quan trọng nhất khi xây dựng ứng dụng thực tế với LLM như ChatGPT, Claude, Gemini.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ WHAT – RAG là gì?

### RAG = Retrieval-Augmented Generation

Là kỹ thuật kết hợp:

- **Truy xuất dữ liệu từ bên ngoài (Retrieval) ➕**
- **Sinh ngôn ngữ từ mô hình LLM (Generation)**

> Giúp mô hình trả lời đúng và cập nhật thông tin mới **mà nó chưa được huấn luyện trước đó**.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ WHY – Tại sao cần RAG?

### 🧠 Vấn đề của LLM:

- LLM như GPT-4 học từ dữ liệu cũ → **không biết thông tin mới**
- Chúng có giới hạn **context window (số token đọc được)** → không đọc hết cả kho tài liệu lớn

### ✅ RAG giải quyết:

- Cho phép **LLM truy cập dữ liệu ngoài** (PDF, database, knowledge base,…)
- **Không cần fine-tune**, vẫn trả lời đúng theo dữ liệu mới
- Giảm hallucination (ảo giác) vì model **dựa trên tài liệu thật**

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ HOW – RAG hoạt động chi tiết (từng bước

### 🧩 BỐ CỤC RAG:

```bash
Câu hỏi (User) → Tìm kiếm ngữ nghĩa → Lấy tài liệu phù hợp → Đưa vào LLM → Sinh câu trả lời
```

### 🔍 Cụ thể các bước:

#### Bước 1: Chuẩn bị dữ liệu

- Chia tài liệu thành các đoạn nhỏ **(chunking)**
- Tạo vector ngữ nghĩa cho từng chunk **(embedding)**
- Lưu vào vector database (Pinecone, Weaviate, FAISS, Chroma, v.v.)

#### Bước 2: Khi có câu hỏi

- `Embedding` câu hỏi thành `vector`
- So sánh gần đúng với các chunk trong vector DB **(semantic search)**
- Lấy ra **K chunk gần nhất** **(top-k retrieval)**

#### Bước 3: Trả về cho LLM

- Kết hợp câu hỏi + các chunk được truy xuất:

```bash
Prompt:
"Câu hỏi: Ai là CEO của OpenAI?
Dữ liệu liên quan: ..."

→ GPT trả lời dựa vào đoạn văn đó.
```

#### Bước 4: Sinh câu trả lời

- LLM dùng các đoạn đã **retrieve** làm **context**
- Dự đoán câu trả lời dựa vào thông tin đó (không cần nhớ từ trước)

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ Ví dụ minh họa (cụ thể, dễ hiểu)

### 🎯 Bài toán: Chatbot nội bộ công ty

Bạn muốn hỏi:

> "Công ty có bao nhiêu ngày nghỉ phép/năm?"

LLM như GPT-4 không biết, vì không được huấn luyện với nội quy công ty bạn.

RAG hoạt động như sau:

1. Chia **file PDF nội quy công ty** thành 100 đoạn nhỏ
2. Tạo embedding cho từng đoạn → Lưu vào vector DB
3. Câu hỏi → tạo embedding → so sánh với 100 đoạn
4. Tìm thấy đoạn:
   > "Mỗi nhân viên được nghỉ 12 ngày phép có lương mỗi năm…"
5. Đưa đoạn này vào prompt → GPT trả lời đúng.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ Tóm tắt 80/20

| Thành phần | Mục đích                                      |
| ---------- | --------------------------------------------- |
| Chunking   | Chia tài liệu thành đoạn nhỏ                  |
| Embedding  | Chuyển đoạn thành vector ngữ nghĩa            |
| Vector DB  | Lưu trữ các vector để tìm kiếm semantic       |
| Retrieval  | Tìm đoạn liên quan đến câu hỏi                |
| Generation | LLM sinh câu trả lời dựa vào đoạn đã tìm được |

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 📌 Lưu ý quan trọng

- RAG ≠ fine-tuning → không thay đổi trọng số mô hình

- RAG chỉ **thêm kiến thức mới vào lúc hỏi**, không cần training lại

- Có thể **cập nhật dữ liệu theo thời gian thực** (tài liệu thay đổi liên tục)
