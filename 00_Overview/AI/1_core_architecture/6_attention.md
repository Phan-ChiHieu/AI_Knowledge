# Attention

- Là phần cốt lõi nhất của Transformer và cũng là nơi mà LLM học được “ngữ cảnh”

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ✅ WHAT – Attention là gì? (Bản chất)

> **Attention = cơ chế cho phép mô hình tập trung vào những phần quan trọng trong chuỗi đầu vào khi xử lý một từ.**

### Nói cách khác:

- Với mỗi từ (token), **mô hình nhìn lại toàn bộ các từ khác trong câu**.
- Sau đó, **gán trọng số (attention weights)** cho từng từ đó, để tính ra “ý nghĩa tổng hợp” của từ đang xét.

→ Attention chính là **“trọng số hóa ngữ cảnh”** để biểu diễn thông minh hơn.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 🔍 WHY – Tại sao cần Attention?

### So với RNN:

- `RNN` xử lý từng từ theo thứ tự → khó nhớ thông tin xa (long-term dependencies)
- `Attention` nhìn toàn bộ một lúc, không phụ thuộc thứ tự

→ Giải quyết được vấn đề:

> “Ở từ **it**, tôi phải nhớ rằng nó đang nói về **the cat** cách xa mấy từ trước đó.”

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## ⚙️ HOW – Attention hoạt động như thế nào?

### Bước 1: Với mỗi token → tạo 3 vector:

- **Query (Q)**: vector đại diện cho "nội dung tôi muốn tìm"
- **Key (K)**: vector đại diện cho "tôi có gì để người khác tra cứu"
- **Value (V)**: vector đại diện cho "nội dung thực tế"

> Mỗi token sẽ có Q, K, V của chính nó.

### Bước 2: Tính điểm tương quan giữa Q và K

→ dùng dot-product: $Q \cdot K^T$

→ Cho biết mức độ **liên quan** giữa token hiện tại (Q) và từng token khác (K)

### Bước 3: Softmax → chuẩn hóa thành **trọng số (α)**

### Bước 4: Nhân trọng số với V → rồi cộng lại

### 🧮 Công thức tổng quát:

$$
\text{Attention}(Q, K, V) = \text{softmax}\left( \frac{QK^T}{\sqrt{d_k}} \right) \cdot V
$$

- $Q, K, V \in \mathbb{R}^{d_k}$
- $\sqrt{d_k}$: dùng để ổn định gradient (tránh số quá lớn)

## 📌 Tóm lại ý tưởng:

> **Tôi là từ “sat”**
> Tôi tạo vector Q để thể hiện tôi muốn nhìn cái gì.
> Tôi so sánh Q của tôi với K của tất cả từ trong câu để xem tôi liên quan đến từ nào.
> Tôi cộng các V (nội dung của các từ) lại theo trọng số tôi vừa tính.
> → Kết quả: tôi có được **biểu diễn mới** mang ý nghĩa toàn câu.

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## 🧠 **Ví dụ đơn giản:**

Câu: `"The animal didn't cross the street because it was tired"`

→ Từ `"it"` có thể tham chiếu đến `"animal"` hoặc `"street"`

→ Attention sẽ học trọng số cao với `"animal"` chứ không phải `"street"`

→ Điều này không lập trình tay, mà **mô hình học được qua huấn luyện**!

## 🔄 Multi-Head Attention?

→ Thay vì 1 cặp Q-K-V → dùng **nhiều cặp Q-K-V song song**, mỗi cái học một kiểu quan hệ khác nhau
→ Sau đó ghép kết quả lại

━━━━━━━━━━━━━━━━━━ ∘◦ ✧ ✦ ✧ ◦∘ ━━━━━━━━━━━━━━━━━━

## Tổng kết 80/20:

| Thành phần           | Ý nghĩa                                            |
| -------------------- | -------------------------------------------------- |
| **Q** (Query)        | “Tôi muốn tìm gì”                                  |
| **K** (Key)          | “Tôi có gì để so sánh”                             |
| **V** (Value)        | “Thông tin tôi mang”                               |
| **QKᵀ + softmax**    | Độ liên quan giữa token hiện tại và các token khác |
| **Attention Output** | Tổng hợp ngữ cảnh có trọng số                      |
