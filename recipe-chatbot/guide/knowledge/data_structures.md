# Phổ biến

| Kiểu        | Tên tiếng Anh | Mô tả                                 | Ví dụ                  |
| ----------- | ------------- | ------------------------------------- | ---------------------- |
| `list`      | List          | Danh sách có thứ tự, thay đổi được    | `[1, 2, 3]`            |
| `tuple`     | Tuple         | Như list nhưng không sửa được         | `(1, 2, 3)`            |
| `dict`      | Dictionary    | Dạng key–value                        | `{"a": 1, "b": 2}`     |
| `set`       | Set           | Tập hợp, không trùng, không có thứ tự | `{1, 2, 3}`            |
| `frozenset` | Frozen Set    | Giống set nhưng bất biến              | `frozenset([1, 2, 3])` |

## 🔍 So sánh tổng thể

| Thuộc tính              | `tuple`                   | `list`                       | `dict`                                   |
| ----------------------- | ------------------------- | ---------------------------- | ---------------------------------------- |
| **Cú pháp**             | `(1, 2, 3)`               | `[1, 2, 3]`                  | `{"a": 1, "b": 2}`                       |
| **Có thứ tự (ordered)** | ✅ (Python 3.6+)          | ✅                           | ✅ (Python 3.7+)                         |
| **Thay đổi được**       | ❌ (immutable)            | ✅ (mutable)                 | ✅ (mutable)                             |
| **Truy cập phần tử**    | Theo index: `x[0]`        | Theo index: `x[0]`           | Theo key: `x["a"]`                       |
| **Dùng làm key dict**   | ✅                        | ❌                           | ❌                                       |
| **Tốc độ**              | ⚡ Nhanh hơn list/dict    | 🐢 Trung bình                | 🐢 Chậm hơn (do hash & key lookup)       |
| **Dùng cho**            | Dữ liệu cố định (hằng số) | Danh sách cần chỉnh sửa      | Lưu trữ theo cặp key–value               |
| **Unpacking**           | ✅ `a, b = (1, 2)`        | ✅ `a, b = [1, 2]`           | ❌ (phải dùng `.items()`, `.values()`)   |
| **Hàm hỗ trợ**          | Ít (`count()`, `index()`) | Nhiều (`append()`, `sort()`) | Rất nhiều (`get()`, `keys()`, `items()`) |

## 📌 Ví dụ trực tiếp

```python
# Tuple
my_tuple = ("VN", "US", "UK")
print(my_tuple[0])  # VN

# List
my_list = ["VN", "US", "UK"]
my_list.append("JP")
print(my_list)  # ['VN', 'US', 'UK', 'JP']

# Dict
my_dict = {"VN": "Việt Nam", "US": "Hoa Kỳ"}
print(my_dict["VN"])  # Việt Nam

```

## ✅ Tóm gọn khi nào dùng:

| Nhu cầu                         | Nên dùng gì |
| ------------------------------- | ----------- |
| Dữ liệu cố định, không thay đổi | `tuple`     |
| Danh sách có thể thay đổi       | `list`      |
| Tra cứu theo key (lookup table) | `dict`      |

---

---

## Ví dụ thêm về Tuple

### ✅ Truy cập toàn bộ phần tử tuple

#### 1. **Duyệt qua tuple bằng vòng lặp:**

```python
my_tuple = ("VN", "US", "UK")

for country in my_tuple:
    print(country)
```

**Kết quả:**

```
VN
US
UK
```

#### 2. **Dùng slicing (cắt chuỗi):**

```python
print(my_tuple[:])       # ('VN', 'US', 'UK')
print(my_tuple[1:])      # ('US', 'UK')
print(my_tuple[:-1])     # ('VN', 'US')
```

#### 3. **Ép kiểu thành list (nếu muốn dùng hàm như list):**

```python
my_list = list(my_tuple)
my_list.append("JP")
print(my_list)           # ['VN', 'US', 'UK', 'JP']
```

### ❗ Nhưng không được làm gì?

```python
my_tuple[0] = "JP"  # ❌ Lỗi vì tuple không thay đổi được
```

### ✅ Tổng kết:

| Hành động        | `tuple` làm được? |
| ---------------- | ----------------- |
| Truy cập toàn bộ | ✅                |
| Duyệt qua        | ✅                |
| Cắt (slicing)    | ✅                |
| Thêm/sửa/xoá     | ❌                |
