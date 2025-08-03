# Semantic Search

là một khái niệm quan trọng trong AI, đặc biệt trong các ứng dụng như RAG, chatbot, tìm kiếm thông minh,...

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ WHAT – Semantic Search là gì?

**Semantic Search** (Tìm kiếm ngữ nghĩa) là kỹ thuật **tìm kiếm theo ý nghĩa**, chứ không chỉ theo từ khoá.

> 🧠 Nó giúp máy **tìm những đoạn có ý nghĩa gần giống**, ngay cả khi **không có chung từ**.

### 🔍 Ví dụ:

Bạn hỏi:

> "Ai là giám đốc điều hành của Apple?"

Document chứa:

> "Tim Cook là CEO hiện tại của Apple Inc."

➡️ ❌ Keyword Search sẽ KHÔNG tìm thấy vì không có chữ “giám đốc điều hành”.

➡️ ✅ `Semantic Search` sẽ TÌM ĐƯỢC vì hiểu “CEO = giám đốc điều hành”

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ WHY – Tại sao cần Semantic Search?

### Keyword search (tìm theo từ khoá) có giới hạn:

- Không tìm được nếu từ khóa khác biệt
- Không hiểu ngữ cảnh, ý nghĩa
- Không chống được ngôn ngữ tự nhiên phức tạp

→ Semantic Search **hiểu được ý nghĩa sâu hơn của câu hỏi và tài liệu**, rất phù hợp với các hệ thống hỏi-đáp tự nhiên (QA, chatbot, trợ lý AI,...)

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ HOW – Semantic Search hoạt động như thế nào?

### Gồm 3 bước chính:

### 🔹 Bước 1: Biểu diễn văn bản bằng vector ngữ nghĩa (Embedding)

- Câu hỏi và các đoạn tài liệu đều được **chuyển thành vector** (vd: 768 chiều)
- Sử dụng mô hình embedding (vd: OpenAI Embedding, BERT, Instructor, Cohere, v.v.)

Ví dụ:

```bash
Câu hỏi: "CEO của Apple?" → [0.12, -0.55, ..., 0.88]
Đoạn: "Tim Cook là giám đốc..." → [0.13, -0.53, ..., 0.89]
```

---

### 🔹 Bước 2: Tính độ tương đồng vector (Similarity Search)

- Dùng **cosine similarity** để đo “độ gần nhau” giữa các vector
- Đoạn nào gần **vector câu hỏi nhất** thì được xem là liên quan

---

### 🔹 Bước 3: Trả về đoạn liên quan nhất

- Thường trả về **top-k** đoạn phù hợp nhất
- Dùng trong:
  - Chatbot nội bộ
  - Hỏi đáp tài liệu PDF
  - Search thông minh trên website
  - RAG (Retrieval-Augmented Generation)

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ Hình dung trực quan:

🔍 **Keyword Search** giống như tìm file có chứa từ “CEO”

🧠 `Semantic Search` giống như hỏi một người thông minh: “Ai là người đứng đầu Apple?” → Người đó sẽ trả lời: “Tim Cook”

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ Tóm tắt 80/20:

| Thành phần | Vai trò                            |
| ---------- | ---------------------------------- |
| Embedding  | Chuyển text thành vector ngữ nghĩa |
| Vector DB  | Lưu các vector để tìm kiếm         |
| Similarity | Tìm đoạn gần nhất với câu hỏi      |
| Output     | Trả về top-k đoạn liên quan nhất   |
