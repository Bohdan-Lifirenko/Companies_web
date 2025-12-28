Правильно сформульоване запитання: **«Як позначити, що повертає метод?»**
У Python це робиться за допомогою **type hints** (анотацій типів).

---

## ✅ Базовий синтаксис

```python
def get_user() -> dict:
    return {"id": 1, "name": "Ivan"}
```

👉 `-> dict` означає: метод **повинен повертати словник**.

---

## 🔹 Поширені типи повернення

### Нічого не повертає

```python
def save_user(user) -> None:
    print("Saved")
```

---

### Повертає число або рядок

```python
def count() -> int:
    return 5

def get_name() -> str:
    return "Ivan"
```

---

### Повертає список

```python
def get_ids() -> list[int]:
    return [1, 2, 3]
```

---

### Повертає словник з типами

```python
def get_user() -> dict[str, int | str]:
    return {"id": 1, "name": "Ivan"}
```

---

## 🔹 Optional (може повернути None)

```python
from typing import Optional

def find_user(id: int) -> Optional[dict]:
    if id == 0:
        return None
    return {"id": id}
```

(Починаючи з Python 3.10)

```python
def find_user(id: int) -> dict | None:
    ...
```

---

## 🔹 Класи та власні типи

```python
class User:
    ...

def get_user() -> User:
    return User()
```

---

## 🔹 Для інтерфейсів (ABC / Protocol)

### ABC

```python
from abc import ABC, abstractmethod

class Repository(ABC):

    @abstractmethod
    def get(self, id: int) -> dict:
        pass
```

---

### Protocol

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, id: int) -> dict: ...
```

---

## 🔹 Кортежі, генератори, ітератори

```python
def get_pair() -> tuple[int, str]:
    return 1, "a"

def numbers() -> list[int]:
    return [1, 2, 3]
```

---

## ⚠️ Важливо знати

* Python **не перевіряє типи під час виконання**
* Анотації потрібні для:

  * читабельності
  * IDE (PyCharm, VS Code)
  * `mypy`, `pyright`

---

## 🧠 Коротко

| Що повертає      | Як писати                     |    |
| ---------------- | ----------------------------- | -- |
| Нічого           | `-> None`                     |    |
| Один тип         | `-> int`                      |    |
| Кілька варіантів | `-> A                         | B` |
| Може бути None   | `-> Optional[T]`              |    |
| Колекція         | `-> list[T]`, `-> dict[K, V]` |    |

---

Якщо хочеш, можу показати:

* як правильно типізувати **pandas / SQLAlchemy**
* як описати **складні структури DTO**
* як ловити помилки через `mypy`
