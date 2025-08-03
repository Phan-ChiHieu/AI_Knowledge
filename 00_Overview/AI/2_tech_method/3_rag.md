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
