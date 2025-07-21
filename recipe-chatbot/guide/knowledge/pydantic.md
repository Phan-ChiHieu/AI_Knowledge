Dưới đây là kiến thức cần biết (cốt lõi + mở rộng) về **Pydantic** – một thư viện cực kỳ phổ biến trong hệ sinh thái Python, đặc biệt là khi làm việc với **FastAPI**, **SQLModel**, hoặc **data validation/parsing**.

## ✅ 1. **Pydantic là gì?**

Pydantic là một thư viện Python giúp **định nghĩa schema (kiểu dữ liệu)** một cách rõ ràng và **tự động kiểm tra - ép kiểu** dữ liệu dựa trên **type hint**.

> Cốt lõi là: **Pydantic = dataclass có validation & parsing thông minh**

## ✅ 2. **Use case phổ biến**

- Tạo schema để validate JSON từ request API (FastAPI)
- Convert dữ liệu từ dict/json sang object Python có type rõ ràng
- Dùng làm tầng trung gian để giao tiếp giữa frontend/backend/database
- Tạo schema cho config, settings (qua `.env`, file JSON, v.v.)

## ✅ 3. **Kiến thức nền tảng cần nắm**

### 3.1. **BaseModel**

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool = True

user = User(id='1', name='Edric')
print(user.id)  # 1 (đã tự ép từ str sang int)
```

> `BaseModel` là cốt lõi, dùng để khai báo model/schema.

### 3.2. **Validation & type coercion**

Pydantic **tự động validate & ép kiểu**:

```python
User(id='1', name='Edric')  # OK: '1' -> 1
User(id='abc', name='Edric')  # ❌ lỗi: không ép được 'abc' -> int
```

### 3.3. **Optional, default, Union**

```python
from typing import Optional, Union, List

class User(BaseModel):
    name: str
    age: Optional[int] = None   # age có thể là None
    tags: List[str]             # bắt buộc là list chứa toàn str
    status: Union[int, str]     # có thể là int hoặc str
```

### 3.4. **Nested model**

```python
class Address(BaseModel):
    city: str

class User(BaseModel):
    name: str
    address: Address

User(name='Edric', address={'city': 'HCM'})  # OK
```

### 3.5. **Custom validator**

```python
from pydantic import validator

class User(BaseModel):
    name: str

    @validator('name')
    def name_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError('Name must not be blank')
        return v
```

## ✅ 4. **Điểm mạnh của Pydantic**

- Tự động ép kiểu cực kỳ mạnh
- Validation dễ mở rộng
- Giao tiếp tốt với FastAPI, SQLModel
- Rất nhanh nhờ dùng Rust bên trong (Pydantic v2)

## ✅ 5. **Sự khác biệt với typing / dataclass**

| So sánh        | typing + dataclass | Pydantic.BaseModel |
| -------------- | ------------------ | ------------------ |
| Validation     | Không              | Có                 |
| Type coercion  | Không              | Có                 |
| Nested model   | Khó                | Dễ                 |
| Error messages | Thô                | Cụ thể, rõ ràng    |
| Hiệu suất      | Tốt (nhẹ)          | Tốt (v2 nhanh hơn) |

## ✅ 6. **Pydantic v1 vs v2**

- `v2` ra mắt 2023, nhanh hơn nhờ Rust
- Cú pháp validator thay đổi một chút
- Tương thích ngược đa số

## ✅ 7. **FastAPI + Pydantic**

```python
from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

app = FastAPI()

@app.post("/users")
def create_user(user: User):
    return user
```

> FastAPI tự dùng Pydantic để parse + validate request JSON vào `user`.

---

---

Trong **Pydantic**, phương thức `.dict()` là cách để **chuyển model thành dictionary (kiểu `dict` của Python)**.

## ✅ Mục đích của `.dict()`

Biến một `BaseModel` thành dict thuần, dùng để:

- Gửi JSON response
- Lưu vào database
- Debug / logging
- Convert sang format khác

## ✅ Ví dụ cơ bản

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool = True

user = User(id=1, name="Edric")

print(user.dict())
# {'id': 1, 'name': 'Edric', 'is_active': True}
```

## ✅ Một số tùy chọn của `.dict()`

### 1. `exclude_unset=True`

Chỉ xuất các field đã được set (dữ liệu đầu vào có khai báo)

```python
class User(BaseModel):
    name: str
    age: int = 18
    city: str = "HCM"

u = User(name="Edric")

print(u.dict())  # {'name': 'Edric', 'age': 18, 'city': 'HCM'}
print(u.dict(exclude_unset=True))  # {'name': 'Edric'}
```

### 2. `exclude_defaults=True`

Loại bỏ các field có giá trị **default** (dù được set)

```python
print(u.dict(exclude_defaults=True))  # {'name': 'Edric'}
```

### 3. `exclude_none=True`

Loại bỏ các field có giá trị là `None`

```python
class User(BaseModel):
    name: str
    nickname: str | None = None

u = User(name="Edric")
print(u.dict(exclude_none=True))  # {'name': 'Edric'}
```

## ✅ So sánh `.dict()` vs `.json()`

| Phương thức | Kết quả trả về | Dùng khi                |
| ----------- | -------------- | ----------------------- |
| `.dict()`   | Python `dict`  | Xử lý nội bộ            |
| `.json()`   | Chuỗi JSON     | Gửi response / lưu file |

```python
print(user.json())  # '{"id": 1, "name": "Edric", "is_active": true}'
```

## ✅ Tổng kết ngắn gọn

- `.dict()` → Trả ra dict Python từ model
- Có thể dùng thêm các tham số như `exclude_unset`, `exclude_defaults`, `exclude_none` để tùy chỉnh
- Rất hữu dụng khi tương tác với DB hoặc serialize data
