# Generative AI (Trí tuệ nhân tạo sinh)

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ❓ What – Generative AI là gì?

`Generative AI` là một nhánh của trí tuệ nhân tạo `(AI)` có khả năng **tạo ra nội dung mới** thay vì chỉ phân tích hay dự đoán. Nội dung mới này có thể là:

- **Văn bản** (bài viết, đoạn hội thoại, code, v.v.)

- **Hình ảnh** (ảnh chân dung, tranh vẽ, thiết kế, v.v.)

- **Âm thanh** (nhạc, giọng nói)

- **Video**, 3D, v.v.

👉 Ví dụ: ChatGPT, DALL·E, Midjourney, Stable Diffusion, Sora của OpenAI,...

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 💡 Why – Tại sao gọi là “generative”?

- Từ **"generate"** nghĩa là **sinh ra, tạo ra**. Khác với AI truyền thống (rule-based, classification, prediction), `Generative AI` không chỉ học từ dữ liệu quá khứ mà còn **dự đoán xác suất để tạo ra dữ liệu mới trông "có vẻ thật"** (realistic / natural).

- Nó không **sao chép dữ liệu gốc** mà **dự đoán token tiếp theo**, pixel tiếp theo,... từ mô hình xác suất.

- Ví dụ: Khi bạn gõ "The sun is", ChatGPT dự đoán từ tiếp theo hợp lý nhất có thể là "shining", "hot", "a star", v.v. tùy ngữ cảnh

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ⚙️ How – Nó hoạt động như thế nào? (Bản chất kỹ thuật)

Bản chất lõi của `Generative AI` hiện đại là sử dụng các mô hình học sâu **(deep learning)**, cụ thể là:

- **🔹 Mô hình nền tảng (Foundation Models)**

  - Dạng: Transformer, đặc biệt là **Large Language Models (LLMs)** như GPT, BERT, T5, v.v.
  - Học từ hàng tỷ token (chữ, ảnh, âm thanh…) và tìm ra **cấu trúc ẩn** trong dữ liệu

- **🔹 Cơ chế tạo sinh**

  - **Text**: Sinh token từng bước → câu → đoạn văn
  - **Image**: Sinh ảnh bằng cách nhiễu hóa rồi khử nhiễu _(diffusion models)_
  - **Audio/Video**: Dùng dạng tuần tự hoặc mạng thời gian.

- **🔹 Cốt lõi toán học**

  - **Xác suất có điều kiện (Conditional probability)**
  - **Học biểu diễn (Representation learning)**: hiểu được "ý nghĩa" trừu tượng của từ, ảnh, âm thanh.
  - **Fine-tune + Reinforcement Learning (với phản hồi con người - RLHF)**: như ChatGPT, sau khi pretrain xong thì tinh chỉnh để đáp ứng mục tiêu cụ thể.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 🎯 Tóm gọn theo nguyên tắc 80/20

| Yếu tố cốt lõi    | Nội dung giải thích ngắn gọn               |
| ----------------- | ------------------------------------------ |
| Mục tiêu          | Tạo nội dung mới giống người               |
| Phương pháp chính | Deep learning với Transformer              |
| Dữ liệu           | Hàng tỷ văn bản, ảnh, âm thanh             |
| Quy trình         | Học xác suất → Sinh đầu ra hợp lý          |
| Ví dụ ứng dụng    | ChatGPT (text), DALL·E (ảnh), Sora (video) |
