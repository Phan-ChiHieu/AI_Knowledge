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

#### 🎯 Bước chi tiết (ví dụ đơn giản):

Mỗi từ sẽ được ánh xạ thành một vector (embedding).

Câu: "I ate an apple"

Ta có:

- "I" → v1
- "ate" → v2
- "an" → v3
- "apple" → v4

#### 💡 Bây giờ giả sử ta đang xử lý từ "apple", ta cần hỏi:

> “Để hiểu 'apple', tôi nên chú ý đến từ nào?”

- Có thể từ “ate” sẽ được chú ý nhiều → vì ăn cái gì?
- an” chỉ là mạo từ → không quan trọng.

Mô hình tính toán các attention score (điểm chú ý) giữa "apple" với từng từ khác:

| Từ so sánh   | Điểm Attention (ví dụ) |
| ------------ | ---------------------- |
| I            | 0.1                    |
| ate          | 0.6 ✅ (quan trọng)    |
| an           | 0.2                    |
| apple (self) | 0.1                    |

➡️ Mô hình biết rằng khi xử lý "apple", cần chú ý nhiều nhất đến "ate" để hiểu mối quan hệ hành động – đối tượng.

➡️ Giúp mô hình “hiểu mối quan hệ giữa các từ trong câu”.

### 3.2. Multi-Head Attention – Nhìn nhiều góc độ

- Một attention head nhìn **mối quan hệ theo kiểu A → B**

- Nhiều head giúp nhìn **đa chiều**: ngữ pháp, nghĩa, cú pháp…

→ Tăng khả năng hiểu ngữ cảnh phức tạp.

### 3.3. Feed Forward Network – Xử lý phi tuyến

Sau Attention, thông tin được đẩy qua các lớp **dense layer phi tuyến** để "nâng cấp" biểu diễn.

### 3.4. Residual + Layer Normalization – Ổn định việc học

- Kỹ thuật giúp mô hình học ổn định, tránh gradient vanishing/exploding.
- Dạng: `output = LayerNorm(x + FeedForward(x))`

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 4. ✅ Output – Sinh từ tiếp theo

- Đầu ra là một vector có độ dài bằng số lượng từ vựng (vocab size)

- Dùng `softmax` để biến thành xác suất

Ví dụ:

```bash

Input: “I want to eat a …”
→ Model dự đoán: [0.01, 0.03, ..., 0.94 (pizza), ..., 0.0001]
→ Chọn từ có xác suất cao nhất: "pizza"
```

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 5. ✅ Huấn luyện mô hình – Dạy máy bằng dữ liệu

- Mô hình được huấn luyện để **dự đoán từ tiếp theo** trên hàng trăm tỷ câu
- Sử dụng:

  - **Loss function**: Cross Entropy

  - **Optimizer**: Adam

  - **Backpropagation**: để điều chỉnh các trọng số

✅ Cuối cùng: `fine-tune` với `Reinforcement Learning from Human Feedback (RLHF)` → làm cho câu trả lời phù hợp, lịch sự, hữu ích hơn

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 📌 Tóm tắt 80/20 (học để hiểu – không học để ghi nhớ):

| Thành phần       | Vai trò                                             |
| ---------------- | --------------------------------------------------- |
| Token            | Chuyển văn bản thành số                             |
| Embedding        | Biểu diễn ý nghĩa từ dưới dạng vector               |
| Transformer      | Hiểu và xử lý ngữ cảnh                              |
| Attention        | Xác định từ nào quan trọng trong câu                |
| Output (Softmax) | Dự đoán từ tiếp theo                                |
| Training (RLHF)  | Làm cho mô hình thông minh & phù hợp với người dùng |
