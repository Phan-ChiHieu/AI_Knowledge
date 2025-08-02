# Transformer là một kiến trúc deep learning dùng để xử lý chuỗi dữ liệu

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 🚀 WHAT – Bên trong Transformer là gì?

Transformer là một kiến trúc **deep learning** dùng để **xử lý chuỗi dữ liệu** (ví dụ: văn bản). Nó được giới thiệu trong paper nổi tiếng _"Attention is All You Need" (2017)._

Cấu trúc Transformer gồm 2 khối chính:

1. `Encoder` (mã hoá) → dùng trong BERT, dịch máy.

2. `Decoder` (giải mã) → dùng trong GPT, sinh văn bản.

> GPT chỉ dùng Decoder stack (Uni-directional).<br />
> BERT chỉ dùng Encoder stack (Bi-directional).<br /> > _Tóm lại: LLM = nhiều lớp Transformer Decoder (trong GPT)_

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 🧠 WHY – Vì sao Transformer mạnh?

Trước Transformer, người ta dùng các kiến trúc: RNN, LSTM để xử lý chuỗi → nhưng các mô hình này **khó học ngữ cảnh xa và không song song hoá được**.

Transformer dùng `Attention` (Tập trung) để:

- Nhìn toàn bộ chuỗi 1 lúc (không tuần tự như RNN)
- Tự chọn phần nào của chuỗi đầu vào là "quan trọng"
- Song song hóa cực nhanh trên GPU → huấn luyện mô hình cực lớn

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ⚙️ HOW – Transformer hoạt động thế nào? (Chi tiết dễ hiểu)

### Tổng thể kiến trúc một Decoder layer (của GPT):

```bash
Input tokens → Embedding → Positional Encoding
↓
Layer 1:
  Self-Attention → Add & Norm
  FeedForward → Add & Norm
↓
Layer 2:
  ...
↓
Output logits → chọn từ tiếp theo

```

### 1. **Input Token & Embedding**

- Văn bản: `"The cat sat"` → Token hóa → `[101, 232, 674]`
- Ánh xạ token thành vector (embedding) → ví dụ `101 → [0.2, 0.5, -0.1, ...]`

### 2. **Positional Encoding**

- Vì Transformer không xử lý tuần tự như RNN nên cần thêm vị trí token để hiểu ngữ cảnh (dùng sin/cos hoặc embedding vị trí).

### 3. **Self-Attention (Cốt lõi)**

#### Mục tiêu:

> Mỗi từ cần **"nhìn lại" toàn bộ câu** để quyết định phần nào quan trọng.

#### Cách làm:

- Với mỗi token, tạo ra 3 vector: **Query (Q), Key (K), Value (V)**
- Tính attention score:
  $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) \cdot V$

→ Giống như:

> “Tôi là token `sat`, tôi muốn biết từ nào quan trọng với tôi → dùng Q, K để tính mức độ liên quan → sau đó cộng các V theo trọng số.”

### 4. **FeedForward Network**

- Mỗi token sau attention sẽ qua 1 MLP nhỏ (giống fully-connected layer).

### 5. **Residual + LayerNorm**

- Mỗi bước đều có:
  `Output = LayerNorm(x + SubLayer(x))`
  → giúp ổn định và gradient không bị mất.

## 🔁 Stack N lần các layer trên

Ví dụ GPT-3 có **96 layers**, GPT-4 còn nhiều hơn → mô hình có thể học được mối liên hệ ngôn ngữ rất phức tạp.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 🧪 Ví dụ minh họa Attention

Câu:

> "The cat sat on the mat because it was tired."

→ Token `"it"` sẽ **tự động học được** rằng "it" liên quan đến "the cat", chứ không phải "the mat".
→ Vì attention sẽ gán trọng số cao cho "cat" khi tính từ `"it"`.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## Tổng kết theo nguyên tắc 80/20:

| Thành phần              | Ý nghĩa                                |
| ----------------------- | -------------------------------------- |
| **Embedding**           | Chuyển token → vector                  |
| **Positional Encoding** | Thêm thông tin vị trí                  |
| **Self-Attention**      | Tính mối liên hệ giữa các token        |
| **FeedForward**         | Ánh xạ phi tuyến từng token            |
| **Stack Layers**        | Lặp lại nhiều lần để học biểu diễn sâu |
