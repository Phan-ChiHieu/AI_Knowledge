# Viết function tự đông tạo ra câu hỏi theo yêu cầu của Question

- Được viết toàn bộ trong một file: homeworks/hw2/generate_synthetic_queries.py

## I. Import thư viện

```python
import json, os
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import pandas as pd
from litellm import completion
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tqdm import tqdm


#  Load biến môi trường
load_dotenv()
# → Load biến OPENAI_API_KEY từ file .env.
```

| Thư viện                             | Tác dụng                                     |
| ------------------------------------ | -------------------------------------------- |
| `json`, `os`, `pathlib`              | Đọc/ghi file, thao tác path, biến môi trường |
| `typing`, `pydantic`                 | Xác định kiểu dữ liệu và validate            |
| `pandas`                             | Xử lý dữ liệu bảng và xuất CSV               |
| `litellm`                            | Gọi LLM model (ở đây là GPT-4o-mini)         |
| `dotenv`                             | Load biến môi trường từ `.env`               |
| `ThreadPoolExecutor`, `as_completed` | Gọi LLM song song (multi-thread)             |
| `tqdm`                               | Hiển thị progress bar khi chạy               |

---

---

## II. Định nghĩa schema dữ liệu bằng Pydantic

```python
# --- Pydantic Models for Structured Output ---
class DimensionTuple(BaseModel):
    DietaryNeedsOrRestrictions: str
    AvailableIngredientsFocus: str
    CuisinePreference: str
    SkillLevelEffort: str
    TimeAvailability: str
    QueryStyleAndDetail: str
```

| Dimension                    | Ý nghĩa                                                          |
| ---------------------------- | ---------------------------------------------------------------- |
| `DietaryNeedsOrRestrictions` | Nhu cầu ăn uống (ăn chay, không gluten, v.v.)                    |
| `AvailableIngredientsFocus`  | Người dùng có sẵn nguyên liệu nào                                |
| `CuisinePreference`          | Họ thích món gì (Thái, Ý, v.v.) hoặc tránh món gì                |
| `SkillLevelEffort`           | Trình độ nấu ăn (dễ, trung bình, khó)                            |
| `TimeAvailability`           | Có bao nhiêu thời gian (dư dả hay gấp)                           |
| `QueryStyleAndDetail`        | Cách họ đặt câu hỏi (ngắn gọn hay chi tiết, có typo, emoji v.v.) |

→ Mỗi "dimension tuple" mô tả một người dùng.

```python
class QueryWithDimensions(BaseModel):
    id: str
    query: str
    dimension_tuple: DimensionTuple
    is_realistic_and_kept: int = 1
    notes_for_filtering: str = ""
```

→ Mỗi truy vấn sẽ đi kèm với dimension_tuple.

```python
class DimensionTuplesList(BaseModel):
    tuples: List[DimensionTuple]

class QueriesList(BaseModel):
    queries: List[str]
```

→ Các class này dùng để parse kết quả JSON trả về từ GPT.

---

---

## III. Config

```python
# --- Configuration ---
MODEL_NAME = "gpt-4o-mini"
NUM_TUPLES_TO_GENERATE = 10
NUM_QUERIES_PER_TUPLE = 5
OUTPUT_CSV_PATH = Path(__file__).parent / "synthetic_queries_for_analysis.csv"
MAX_WORKERS = 5
```

→ Số lượng tuple cần sinh ra, số query mỗi tuple, số luồng xử lý song song.

---

---

## IV. Gọi GPT để sinh ra dữ liệu

```python
def call_llm(messages: List[Dict[str, str]], response_format: Any) -> Any:
    """Make a single LLM call with retries."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = completion(
                model=MODEL_NAME,
                messages=messages,
                response_format=response_format
            )
            return response_format(**json.loads(response.choices[0].message.content))
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)  # Wait before retry
```

Đây là **giải thích chi tiết từng dòng** cho hàm `call_llm`, một hàm quan trọng dùng để **gọi GPT (qua `litellm.completion`) và parse kết quả về một schema cụ thể** (dựa vào `pydantic`).

### ✳️ Mục đích:

Hàm này gửi `messages` (kiểu ChatGPT) đến GPT model và **parse phản hồi thành một object theo `response_format`**.

## 📦 Hàm đầy đủ:

```python
def call_llm(messages: List[Dict[str, str]], response_format: Any) -> Any:
    """Make a single LLM call with retries."""
    max_retries = 3
```

- Nhận 2 tham số:

  - `messages`: danh sách message kiểu ChatML, ví dụ:

    ```python
    [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."}
    ]
    ```

  - `response_format`: một lớp `pydantic` để định nghĩa kiểu dữ liệu đầu ra. VD: `DimensionTuplesList`, `QueriesList`...

- Gọi lại GPT **tối đa 3 lần** nếu gặp lỗi.

### 🔁 Vòng lặp với retry:

```python
    for attempt in range(max_retries):
```

Lặp tối đa 3 lần trong trường hợp GPT bị timeout/lỗi mạng.

### 🎯 Gọi GPT:

```python
        try:
            response = completion(
                model=MODEL_NAME,
                messages=messages,
                response_format=response_format
            )
```

- Gọi hàm `completion()` từ thư viện `litellm`, gửi `messages` và `model` (VD: `"gpt-4o-mini"`).
- `response_format` ở đây là thông tin mô tả kiểu dữ liệu GPT sẽ trả về (dưới dạng JSON string).

### 📦 Parse kết quả:

```python
            return response_format(**json.loads(response.choices[0].message.content))
```

- `response.choices[0].message.content`: nội dung text trả về từ GPT (chuỗi JSON).
- `json.loads(...)`: chuyển từ JSON string thành Python `dict`
- `response_format(**...)`: dùng `pydantic` để tạo object đúng chuẩn schema đầu vào, ví dụ:

  ```python
  response_format = DimensionTuplesList
  ⇒ return DimensionTuplesList(**<dict từ json>)
  ```

### ❌ Nếu lỗi: retry

```python
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)  # Wait before retry
```

- Nếu lỗi (ví dụ lỗi mạng, lỗi JSON parse...), hàm sẽ:

  - **thử lại** nếu chưa đủ 3 lần
  - Nếu đã hết lần thử, **ném lỗi lên** (`raise e`)
  - Chờ 1 giây trước khi thử lại (`time.sleep(1)`)

## ✅ Ví dụ thực tế:

```python
response_format = DimensionTuplesList
messages = [
  {"role": "system", "content": "You are a helpful assistant..."},
  {"role": "user", "content": "Generate 10 dimension tuples..."}
]

result = call_llm(messages, DimensionTuplesList)
print(result.tuples[0].CuisinePreference)  # truy cập dữ liệu như object
```

## 🧠 Tổng kết:

| Thành phần                           | Giải thích                                                                   |
| ------------------------------------ | ---------------------------------------------------------------------------- |
| `completion(...)`                    | Gửi prompt đến GPT model                                                     |
| `response_format(**json.loads(...))` | Parse kết quả GPT thành object Pydantic                                      |
| `retry`                              | Giúp chống lỗi mạng hoặc GPT fail tạm thời                                   |
| `response_format`                    | Tùy biến để tái sử dụng: có thể là `DimensionTuplesList`, `QueriesList`, v.v |

---

---

## V. Gọi GPT để sinh ra dữ liệu

```python
def generate_dimension_tuples() -> List[DimensionTuple]:
    """Generate diverse dimension tuples."""
    prompt = f"""Generate {NUM_TUPLES_TO_GENERATE} diverse combinations of dimension values for a recipe chatbot.
Each combination should represent a different user scenario. Ensure balanced coverage across all dimensions - don't over-represent any particular value or combination.

Important: Aim for an even distribution across all dimensions. For example:
- Don't generate too many dietary restrictions combinations
- Don't focus too heavily on quick recipes
- Don't over-represent any particular cuisine
- Vary the query styles naturally
- Try to use weird combinations of ingredients required in AvailableIngredientsFocus

DietaryNeedsOrRestrictions:
- vegan, vegetarian, gluten-free, dairy-free, keto, paleo, halal, kosher, no restrictions, pescatarian, low-carb, low-sodium, nut-free, egg-free, soy-free, FODMAP, diabetic-friendly, high-protein

AvailableIngredientsFocus:
- must_use_specific: [list of ingredients]
- general_pantry: basic ingredients
- no_specific_ingredients: open to suggestions

CuisinePreference:
- specific_cuisine: [cuisine type]
- any_cuisine
- avoid_specific: [cuisine type]

SkillLevelEffort:
- beginner_easy_low_effort
- intermediate_moderate_effort
- advanced_complex_high_effort

TimeAvailability:
- quick_under_30_mins
- moderate_30_to_60_mins
- flexible_no_time_constraint

QueryStyleAndDetail:
- short_keywords_minimal_detail
- natural_question_moderate_detail
- detailed_request_high_detail

Here are some example dimension tuples that show realistic combinations:

1. Beginner cook with time constraints and specific ingredients:
{{
    "DietaryNeedsOrRestrictions": "no restrictions",
    "AvailableIngredientsFocus": "must_use_specific: chicken breast, rice, vegetables",
    "CuisinePreference": "any_cuisine",
    "SkillLevelEffort": "beginner_easy_low_effort",
    "TimeAvailability": "quick_under_30_mins",
    "QueryStyleAndDetail": "natural_question_moderate_detail"
}}

2. Experienced cook with dietary restrictions and flexible time:
{{
    "DietaryNeedsOrRestrictions": "vegan",
    "AvailableIngredientsFocus": "general_pantry",
    "CuisinePreference": "specific_cuisine: mediterranean",
    "SkillLevelEffort": "advanced_complex_high_effort",
    "TimeAvailability": "flexible_no_time_constraint",
    "QueryStyleAndDetail": "detailed_request_high_detail"
}}

3. Busy parent with dietary needs and pantry ingredients:
{{
    "DietaryNeedsOrRestrictions": "gluten_free",
    "AvailableIngredientsFocus": "general_pantry",
    "CuisinePreference": "avoid_specific: spicy",
    "SkillLevelEffort": "intermediate_moderate_effort",
    "TimeAvailability": "moderate_30_to_60_mins",
    "QueryStyleAndDetail": "short_keywords_minimal_detail"
}}

4. Student with limited ingredients and quick time:
{{
    "DietaryNeedsOrRestrictions": "vegetarian",
    "AvailableIngredientsFocus": "must_use_specific: pasta, canned tomatoes, cheese",
    "CuisinePreference": "any_cuisine",
    "SkillLevelEffort": "beginner_easy_low_effort",
    "TimeAvailability": "quick_under_30_mins",
    "QueryStyleAndDetail": "natural_question_moderate_detail"
}}

5. Food enthusiast with specific cuisine preference:
{{
    "DietaryNeedsOrRestrictions": "no restrictions",
    "AvailableIngredientsFocus": "no_specific_ingredients",
    "CuisinePreference": "specific_cuisine: thai",
    "SkillLevelEffort": "intermediate_moderate_effort",
    "TimeAvailability": "moderate_30_to_60_mins",
    "QueryStyleAndDetail": "detailed_request_high_detail"
}}

Generate {NUM_TUPLES_TO_GENERATE} unique dimension tuples following these patterns. Remember to maintain balanced diversity across all dimensions."""

    messages = [{"role": "user", "content": prompt}]

    try:
        print("Generating dimension tuples in parallel...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit five generation tasks using a loop
            futures = []
            for _ in range(5):
                futures.append(executor.submit(call_llm, messages, DimensionTuplesList))

            # Wait for all to complete and collect results
            responses = []
            for future in futures:
                responses.append(future.result())

        # Combine tuples and remove duplicates
        all_tuples = []
        for response in responses:
            all_tuples.extend(response.tuples)
        unique_tuples = []
        seen = set()

        for tup in all_tuples:
            # Convert tuple to a comparable string representation
            tuple_str = tup.model_dump_json()
            if tuple_str not in seen:
                seen.add(tuple_str)
                unique_tuples.append(tup)

        print(f"Generated {len(all_tuples)} total tuples, {len(unique_tuples)} unique")
        return unique_tuples
    except Exception as e:
        print(f"Error generating dimension tuples: {e}")
        return []
```

Hàm `generate_dimension_tuples()` là một **hàm sinh dữ liệu đầu vào đa dạng cho chatbot nấu ăn**, sử dụng GPT để tạo ra các "dimension tuples" (tổ hợp nhiều biến liên quan đến nhu cầu người dùng).

## ✅ Mục đích

Sinh ra nhiều tình huống người dùng khác nhau, mỗi tình huống là một "dimension tuple" gồm các thuộc tính như:

- `DietaryNeedsOrRestrictions` (hạn chế dinh dưỡng)
- `AvailableIngredientsFocus` (nguyên liệu có sẵn)
- `CuisinePreference` (ưu tiên ẩm thực)
- `SkillLevelEffort` (trình độ nấu ăn)
- `TimeAvailability` (thời gian rảnh)
- `QueryStyleAndDetail` (cách hỏi)

## 🧠 Giải thích chi tiết

### 1. Prompt yêu cầu GPT sinh dữ liệu:

```python
prompt = f"""Generate {NUM_TUPLES_TO_GENERATE} diverse combinations of dimension values ...
```

- GPT được hướng dẫn:

  - Sinh ra các tổ hợp khác nhau giữa các dimension
  - Tránh thiên lệch (ví dụ sinh quá nhiều món “nhanh”, hay “vegan”)
  - Đưa ví dụ cụ thể để hướng GPT đi đúng hướng
  - Các value như `"must_use_specific: ..."`, `"specific_cuisine: ..."`, `"avoid_specific: ..."` đều là **label + giá trị** dạng key\:value

### 2. Tạo messages cho GPT:

```python
messages = [{"role": "user", "content": prompt}]
```

- Đưa prompt vào định dạng ChatGPT (kiểu list message).

### 3. Gọi GPT song song bằng ThreadPool:

```python
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for _ in range(5):
        futures.append(executor.submit(call_llm, messages, DimensionTuplesList))
```

- Gọi GPT **5 lần song song** để tăng khả năng đa dạng hóa kết quả.
- Mỗi lần trả về là một `DimensionTuplesList` – chứa nhiều `DimensionTuple`.

### 4. Gom kết quả và lọc trùng:

```python
for response in responses:
    all_tuples.extend(response.tuples)

seen = set()
for tup in all_tuples:
    tuple_str = tup.model_dump_json()
    if tuple_str not in seen:
        seen.add(tuple_str)
        unique_tuples.append(tup)
```

- Gom tất cả các tuple lại
- Dùng JSON string để so sánh và lọc trùng (vì object không hashable trực tiếp)
- Kết quả là list `unique_tuples`

### 5. Kết quả:

```python
print(f"Generated {len(all_tuples)} total tuples, {len(unique_tuples)} unique")
return unique_tuples
```

## 🧩 Các thành phần phụ thuộc:

| Tên                      | Giải thích                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------- |
| `call_llm()`             | Hàm đã phân tích trước: gọi GPT và parse kết quả                                        |
| `DimensionTuplesList`    | Một lớp `Pydantic`, kiểu `BaseModel`, gồm field `tuples: List[DimensionTuple]`          |
| `DimensionTuple`         | Một cấu trúc chứa các field như `DietaryNeedsOrRestrictions`, `CuisinePreference`, v.v. |
| `NUM_TUPLES_TO_GENERATE` | Số lượng tuple mong muốn GPT tạo trong một lần gọi                                      |

## 💡 Tóm lại

Hàm này:

- **Gọi GPT nhiều lần song song** để sinh dữ liệu đầu vào mẫu cho bot
- **Tránh trùng lặp**, đảm bảo **đa dạng và cân bằng**
- **Trả về danh sách các tình huống người dùng cụ thể**, dùng cho:

  - Kiểm thử bot
  - Sinh câu hỏi
  - Phân tích lỗi

---

---

## VI. Hàm generate_queries_for_tuple() dùng để sinh các câu hỏi tự nhiên mà người dùng có thể hỏi chatbot dựa trên một tổ hợp điều kiện (dimension tuple).

```python
def generate_queries_for_tuple(dimension_tuple: DimensionTuple) -> List[str]:
    """Generate natural language queries for a given dimension tuple."""
    prompt = f"""Generate {NUM_QUERIES_PER_TUPLE} different natural language queries for a recipe chatbot based on these characteristics:
{dimension_tuple.model_dump_json(indent=2)}

The queries should:
1. Sound like real users asking for recipe help
2. Naturally incorporate all the dimension values
3. Vary in style and detail level
4. Be realistic and practical
5. Include natural variations in typing style, such as:
   - Some queries in all lowercase
   - Some with random capitalization
   - Some with common typos
   - Some with missing punctuation
   - Some with extra spaces or missing spaces
   - Some with emojis or text speak

Here are examples of realistic query variations for a beginner, vegan, quick recipe:

Proper formatting:
- "Need a simple vegan dinner that's ready in 20 minutes"
- "What's an easy plant-based recipe I can make quickly?"

All lowercase:
- "need a quick vegan recipe for dinner"
- "looking for easy plant based meals"

Random caps:
- "NEED a Quick Vegan DINNER recipe"
- "what's an EASY plant based recipe i can make"

Common typos:
- "need a quik vegan recip for dinner"
- "wat's an easy plant based recipe i can make"

Missing punctuation:
- "need vegan dinner ideas quick"
- "easy plant based recipe 20 mins"

With emojis/text speak:
- "need vegan dinner ideas asap! 🥗"
- "pls help with quick plant based recipe thx"

Generate {NUM_QUERIES_PER_TUPLE} unique queries that match the given dimensions, varying the text style naturally."""

    messages = [{"role": "user", "content": prompt}]

    try:
        response = call_llm(messages, QueriesList)
        return response.queries
    except Exception as e:
        print(f"Error generating queries for tuple: {e}")
        return []

```

## 🎯 Mục đích:

Từ một tổ hợp các đặc điểm người dùng (ví dụ: “vegan”, “beginner”, “quick meal”), hàm này sẽ:

- Gọi GPT để sinh ra `NUM_QUERIES_PER_TUPLE` câu hỏi **giống người thật hỏi**.
- Các câu hỏi sẽ đa dạng về:

  - Kiểu viết
  - Mức độ chi tiết
  - Phong cách gõ (sai chính tả, viết thường, có emoji…)

## 📌 Phân tích từng phần:

### 1. Nhận đầu vào:

```python
def generate_queries_for_tuple(dimension_tuple: DimensionTuple) -> List[str]:
```

- `dimension_tuple`: là một tổ hợp đặc điểm người dùng (ví dụ: ăn chay, ít thời gian, thích món Ý…)
- Kiểu dữ liệu: `DimensionTuple` – một `Pydantic model`

### 2. Tạo Prompt cho GPT:

```python
prompt = f"""Generate {NUM_QUERIES_PER_TUPLE} different natural language queries ..."""
```

#### 👉 Nội dung prompt có:

- **Mô tả mục tiêu**: sinh các câu hỏi giống người thật sẽ hỏi chatbot
- **Dữ liệu đầu vào**: `dimension_tuple` được dump ra JSON (dễ đọc)

  ```python
  {dimension_tuple.model_dump_json(indent=2)}
  ```

- **Yêu cầu GPT** sinh query với:

  - Nội dung phù hợp với dimension tuple
  - Kiểu viết đa dạng:

    - Viết thường
    - In hoa ngẫu nhiên
    - Lỗi chính tả
    - Không dấu câu
    - Có emoji

- **Ví dụ cụ thể** để GPT học cách sinh phong phú.

### 3. Gọi GPT để sinh query:

```python
messages = [{"role": "user", "content": prompt}]
response = call_llm(messages, QueriesList)
```

- `call_llm`: hàm gọi GPT đã giải thích trước
- `QueriesList`: class Pydantic định nghĩa kiểu dữ liệu `queries: List[str]`

### 4. Xử lý kết quả:

```python
return response.queries
```

- Trả về list các query GPT sinh ra (dưới dạng chuỗi)
- Nếu lỗi, in lỗi và trả về list rỗng

```python
except Exception as e:
    print(f"Error generating queries for tuple: {e}")
    return []
```

## 🧩 Các phần phụ thuộc:

| Tên                     | Vai trò                                          |
| ----------------------- | ------------------------------------------------ |
| `DimensionTuple`        | Class chứa các dimension: diet, cuisine, effort… |
| `QueriesList`           | Pydantic model chứa field `queries: List[str]`   |
| `NUM_QUERIES_PER_TUPLE` | Số lượng câu hỏi cần sinh ra                     |
| `call_llm`              | Gọi GPT và parse kết quả về kiểu mong muốn       |

## 💡 Tổng kết:

Hàm này là bước thứ hai sau `generate_dimension_tuples()`:

| Bước                           | Mục đích                                                           |
| ------------------------------ | ------------------------------------------------------------------ |
| `generate_dimension_tuples()`  | Sinh ra các tình huống người dùng đa dạng                          |
| `generate_queries_for_tuple()` | Chuyển từng tình huống thành câu hỏi cụ thể như người dùng hỏi bot |

---

---

## VII. Hàm generate_queries_parallel() dùng để generate hàng loạt câu hỏi (queries) từ nhiều tổ hợp dimension_tuple, chạy song song (multi-threading) để tăng tốc độ.

```python
def generate_queries_parallel(dimension_tuples: List[DimensionTuple]) -> List[QueryWithDimensions]:
    """Generate queries in parallel for all dimension tuples."""
    all_queries = []
    query_id = 1

    print(f"Generating {NUM_QUERIES_PER_TUPLE} queries each for {len(dimension_tuples)} dimension tuples...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all query generation tasks
        future_to_tuple = {
            executor.submit(generate_queries_for_tuple, dim_tuple): i
            for i, dim_tuple in enumerate(dimension_tuples)
        }

        # Process completed generations as they finish
        with tqdm(total=len(dimension_tuples), desc="Generating Queries") as pbar:
            for future in as_completed(future_to_tuple):
                tuple_idx = future_to_tuple[future]
                try:
                    queries = future.result()
                    if queries:
                        for query in queries:
                            all_queries.append(QueryWithDimensions(
                                id=f"SYN{query_id:03d}",
                                query=query,
                                dimension_tuple=dimension_tuples[tuple_idx]
                            ))
                            query_id += 1
                    pbar.update(1)
                except Exception as e:
                    print(f"Tuple {tuple_idx + 1} generated an exception: {e}")
                    pbar.update(1)

    return all_queries
```

## ✅ Mục tiêu:

- Cho một danh sách `dimension_tuples` (tức là các tổ hợp điều kiện người dùng)
- Với mỗi tuple → sinh ra `NUM_QUERIES_PER_TUPLE` câu hỏi tự nhiên
- Chạy **song song nhiều thread** để tối ưu thời gian
- Trả về danh sách các đối tượng `QueryWithDimensions`, mỗi item gồm:

  - ID
  - Câu hỏi
  - Thông tin dimension tương ứng

## 📌 Giải thích chi tiết:

### Hàm nhận vào:

```python
def generate_queries_parallel(dimension_tuples: List[DimensionTuple]) -> List[QueryWithDimensions]:
```

- `dimension_tuples`: danh sách các `DimensionTuple` bạn đã generate trước đó
- Trả về: danh sách `QueryWithDimensions` – object chứa query và metadata liên quan

### 1. Khởi tạo:

```python
all_queries = []
query_id = 1
```

- `all_queries`: nơi lưu toàn bộ kết quả cuối cùng
- `query_id`: dùng để tạo ID dạng `SYN001`, `SYN002`,...

### 2. Khởi tạo thread pool:

```python
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
```

- Tạo một thread pool với số luồng tối đa là `MAX_WORKERS` (giá trị khai báo ở nơi khác)

### 3. Submit task song song:

```python
future_to_tuple = {
    executor.submit(generate_queries_for_tuple, dim_tuple): i
    for i, dim_tuple in enumerate(dimension_tuples)
}
```

- Mỗi `generate_queries_for_tuple()` (tức gọi GPT để tạo câu hỏi từ 1 tuple) là một task
- `future_to_tuple`: ánh xạ từng thread future về index ban đầu trong list

### 4. Thu kết quả và hiển thị tiến độ:

```python
with tqdm(total=len(dimension_tuples), desc="Generating Queries") as pbar:
    for future in as_completed(future_to_tuple):
```

- Dùng `tqdm` để hiển thị progress bar
- `as_completed()` giúp xử lý theo thứ tự hoàn thành (bất kể thứ tự ban đầu)

### 5. Xử lý kết quả từng future:

```python
queries = future.result()
```

- Nếu thành công:

  - Mỗi câu query sẽ được đóng gói vào `QueryWithDimensions` với ID, câu hỏi, và dimension
  - Append vào `all_queries`

```python
all_queries.append(QueryWithDimensions(
    id=f"SYN{query_id:03d}",
    query=query,
    dimension_tuple=dimension_tuples[tuple_idx]
))
query_id += 1
```

- Nếu lỗi: in ra exception (không crash toàn bộ)

```python
except Exception as e:
    print(f"Tuple {tuple_idx + 1} generated an exception: {e}")
```

### 6. Trả kết quả:

```python
return all_queries
```

## 🧱 Các class phụ thuộc:

| Class                        | Mục đích                                             |
| ---------------------------- | ---------------------------------------------------- |
| `DimensionTuple`             | Một tổ hợp điều kiện (diet, time, cuisine, v.v.)     |
| `QueryWithDimensions`        | Pydantic model chứa `id`, `query`, `dimension_tuple` |
| `generate_queries_for_tuple` | Hàm gọi GPT sinh queries cho 1 tuple                 |
| `MAX_WORKERS`                | Số lượng thread song song (thường 4–8)               |

## ✅ Tóm tắt:

| Ý chính  | Chi tiết                                          |
| -------- | ------------------------------------------------- |
| Mục tiêu | Tạo nhiều câu hỏi cho chatbot test                |
| Input    | List các tình huống người dùng (dimension tuples) |
| Output   | List các query kèm theo metadata                  |
| Tối ưu   | Chạy đa luồng để sinh nhanh hơn                   |
| Tiện ích | Có `tqdm` để theo dõi tiến độ                     |

---

---

## VIII. Hàm save_queries_to_csv() dùng để lưu toàn bộ danh sách query đã sinh ra vào file CSV.

```python
def save_queries_to_csv(queries: List[QueryWithDimensions]):
    """Save generated queries to CSV using pandas."""
    if not queries:
        print("No queries to save.")
        return

    # Convert to DataFrame
    df = pd.DataFrame([
        {
            'id': q.id,
            'query': q.query,
            'dimension_tuple_json': q.dimension_tuple.model_dump_json(),
            'is_realistic_and_kept': q.is_realistic_and_kept,
            'notes_for_filtering': q.notes_for_filtering
        }
        for q in queries
    ])

    # Save to CSV
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Saved {len(queries)} queries to {OUTPUT_CSV_PATH}")

```

## ✅ Mục đích:

Lưu kết quả từ bước generate (một danh sách `QueryWithDimensions`) thành một file CSV dễ xử lý sau này (lọc, đánh giá, fine-tune, phân tích...).

## 📌 Giải thích chi tiết từng phần:

### Khởi đầu:

```python
if not queries:
    print("No queries to save.")
    return
```

- Nếu list `queries` rỗng thì dừng lại, không làm gì tiếp.

### Chuyển list → Pandas DataFrame:

```python
df = pd.DataFrame([
    {
        'id': q.id,
        'query': q.query,
        'dimension_tuple_json': q.dimension_tuple.model_dump_json(),
        'is_realistic_and_kept': q.is_realistic_and_kept,
        'notes_for_filtering': q.notes_for_filtering
    }
    for q in queries
])
```

- Duyệt qua từng item `q` trong list `queries`, tạo dict gồm:

  - `id`: ví dụ `SYN001`
  - `query`: câu hỏi sinh ra
  - `dimension_tuple_json`: toàn bộ thông tin về người dùng (dimension) → serialize thành JSON string
  - `is_realistic_and_kept`: bool đánh dấu câu này có được giữ lại không (dành cho bước lọc thủ công)
  - `notes_for_filtering`: ghi chú nếu câu bị loại bỏ (ví dụ: quá khó hiểu, lỗi chính tả quá nặng, bot bị ngáo,...)

➡️ Tạo thành một bảng (DataFrame) để xuất ra dễ dàng.

### Ghi file CSV:

```python
df.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"Saved {len(queries)} queries to {OUTPUT_CSV_PATH}")
```

- Ghi file ra đường dẫn `OUTPUT_CSV_PATH` (khai báo ở đầu file)
- `index=False`: không ghi cột chỉ mục

## 🧱 Phụ thuộc:

| Biến                  | Ý nghĩa                                               |
| --------------------- | ----------------------------------------------------- |
| `QueryWithDimensions` | Class chứa `query`, `id`, `dimension_tuple`, v.v.     |
| `OUTPUT_CSV_PATH`     | Đường dẫn file CSV để ghi ra                          |
| `model_dump_json()`   | Hàm của Pydantic model để chuyển object → JSON string |
| `pd.DataFrame()`      | Tạo bảng từ list các dict                             |

## ✅ Tóm lại:

| Mục      | Ý nghĩa                                                        |
| -------- | -------------------------------------------------------------- |
| 🎯       | Ghi list query đã sinh ra vào CSV                              |
| ✅ Check | Nếu không có query thì thoát                                   |
| 🏗️       | Mỗi dòng CSV chứa: id, query, dimension, flag giữ/lọc, ghi chú |
| 🧰 Dùng  | cho bước lọc, phân tích, training,...                          |

---

---

## IX. Hàm main() là điểm bắt đầu toàn bộ pipeline sinh dữ liệu cho chatbot, gồm 2 bước chính:

```python
def main():
    """Main function to generate and save queries."""
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    start_time = time.time()

    # Step 1: Generate dimension tuples
    print("Step 1: Generating dimension tuples...")
    dimension_tuples = generate_dimension_tuples()
    if not dimension_tuples:
        print("Failed to generate dimension tuples. Exiting.")
        return
    print(f"Generated {len(dimension_tuples)} dimension tuples.")

    # Step 2: Generate queries for each tuple
    print("\nStep 2: Generating natural language queries...")
    queries = generate_queries_parallel(dimension_tuples)

    if queries:
        save_queries_to_csv(queries)
        elapsed_time = time.time() - start_time
        print(f"\nQuery generation completed successfully in {elapsed_time:.2f} seconds.")
        print(f"Generated {len(queries)} queries from {len(dimension_tuples)} dimension tuples.")
    else:
        print("Failed to generate any queries.")
```

## ✅ Mục tiêu tổng thể:

Sinh ra dữ liệu huấn luyện (các câu hỏi người dùng giả lập) theo cấu trúc và tiêu chí định sẵn → ghi vào CSV.

## 📌 Giải thích từng phần:

### 🔐 Check API key:

```python
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    return
```

- Nếu chưa cấu hình `OPENAI_API_KEY` trong `.env` hoặc môi trường → thoát ngay.
- Vì code cần gọi API (`completion()` từ `litellm`), key là bắt buộc.

### 🕒 Bắt đầu tính thời gian:

```python
start_time = time.time()
```

### 🧩 Bước 1: Sinh các “dimension tuples”

```python
print("Step 1: Generating dimension tuples...")
dimension_tuples = generate_dimension_tuples()
```

- Gọi hàm `generate_dimension_tuples()` → sinh ra N tổ hợp đặc điểm người dùng (dietary, skill, cuisine, ...).
- Mỗi tổ hợp là 1 profile user để dùng sinh query.

```python
if not dimension_tuples:
    print("Failed to generate dimension tuples. Exiting.")
    return
print(f"Generated {len(dimension_tuples)} dimension tuples.")
```

### 💬 Bước 2: Sinh câu hỏi theo từng profile

```python
print("\nStep 2: Generating natural language queries...")
queries = generate_queries_parallel(dimension_tuples)
```

- Gọi `generate_queries_parallel()` để sinh ra danh sách câu hỏi tự nhiên tương ứng với từng dimension tuple.
- Mỗi dimension tuple sinh ra `NUM_QUERIES_PER_TUPLE` câu.

### 💾 Lưu CSV nếu thành công:

```python
if queries:
    save_queries_to_csv(queries)
    elapsed_time = time.time() - start_time
    print(f"\nQuery generation completed successfully in {elapsed_time:.2f} seconds.")
    print(f"Generated {len(queries)} queries from {len(dimension_tuples)} dimension tuples.")
```

- Gọi `save_queries_to_csv()` để ghi kết quả ra file.
- In thời gian chạy và tổng số query sinh được.

### ❌ Nếu không có query:

```python
else:
    print("Failed to generate any queries.")
```

## 🔁 Dòng chảy tổng quát:

```text
Check key → Sinh profile user → Sinh query từ profile → Ghi file CSV
```

## 📌 Hàm `main()` thường được gọi ở cuối file như sau:

```python
if __name__ == "__main__":
    main()
```

## ✅ Tóm gọn 1 câu:

> Hàm `main()` orchestrate toàn bộ pipeline từ gọi API, sinh dữ liệu người dùng → sinh câu hỏi → ghi file CSV để làm dataset huấn luyện/fine-tune cho chatbot.
