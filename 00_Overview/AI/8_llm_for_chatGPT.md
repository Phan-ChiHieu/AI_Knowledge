## 🔧 Các thành phần cốt lõi của một mô hình ngôn ngữ như GPT

1.  **Token**

2.  **Embedding**

3.  **Transformer**

    - Attention (Self-Attention)

    - Multi-Head Attention

    - Feed Forward

    - Residual + LayerNorm

4.  **Output (Softmax + Dự đoán từ tiếp theo)**

5.  **Huấn luyện (Training: Loss function, Optimizer, RLHF)**

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 1. ✅ Token – Từ không phải là từ

**Vấn đề**: Máy không hiểu chữ như người → phải chuyển text thành số.

#### 🔹 Token là đơn vị nhỏ của văn bản được "băm ra":

- Có thể là chữ cái, âm tiết, từ, hoặc đoạn từ (tùy tokenizer).

- Ví dụ: `"ChatGPT"` → `[‘Chat’, ‘G’, ‘PT’]` → `[32001, 12, 754]`

#### 👉 `Text` → `Token (số nguyên)` là bước đầu tiên của mọi mô hình NLP.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 2. ✅ Embedding – Chuyển token thành vector hiểu được

🔹 Token (số nguyên) không có ý nghĩa toán học → cần chuyển thành vector nhiều chiều.

- Mỗi token được ánh xạ thành một vector số thực (vd: 768 chiều)

- Gọi là Embedding Vector

Ví dụ:

```bash
Token “king” → [0.12, -0.23, ..., 0.55] (768 số)
Token “queen” → vector gần giống
```

#### 📌 Mục tiêu: các từ "gần nghĩa" nằm gần nhau trong không gian vector.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 3. ✅ Transformer – Bộ não của mô hình

Transformer là **kiến trúc cốt lõi** (xuất hiện từ paper năm 2017: Attention is All You Need). Nó thay thế hoàn toàn RNN, LSTM cũ.

### Gồm 3 khối chính:

### 3.1. Attention – “Tôi nên chú ý vào từ nào?”

- Một từ không thể hiểu đơn lẻ, nó cần **ngữ cảnh**.
- Ví dụ: "apple" trong "I ate an apple" vs "Apple released a new iPhone"

✅ Self-Attention: mỗi từ sẽ tính mức độ quan trọng (attention score) đối với các từ khác trong câu.

➡️ Giúp mô hình “hiểu mối quan hệ giữa các từ trong câu”.
