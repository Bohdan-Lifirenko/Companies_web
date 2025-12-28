**Інтерфейси в Python** — це спосіб описати *контракт*: які методи клас **зобов’язаний** реалізувати.
На відміну від Java чи C#, у Python немає окремого ключового слова `interface`, але є кілька стандартних підходів.

---

## 1️⃣ ABC (Abstract Base Classes) — правильний аналог інтерфейсів

Найближчий і рекомендований спосіб.

```python
from abc import ABC, abstractmethod

class Repository(ABC):

    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def save(self, data) -> None:
        pass
```

### Реалізація інтерфейсу

```python
class UserRepository(Repository):

    def get(self, id: int):
        return {"id": id}

    def save(self, data) -> None:
        print("Saved", data)
```

❌ Якщо не реалізувати всі методи — клас **не можна створити**:

```python
repo = UserRepository()  # OK
```

---

## 2️⃣ Кілька інтерфейсів (множинне наслідування)

Python **дозволяє** реалізовувати кілька інтерфейсів одночасно.

```python
class Readable(ABC):
    @abstractmethod
    def read(self):
        pass


class Writable(ABC):
    @abstractmethod
    def write(self, data):
        pass


class FileStorage(Readable, Writable):

    def read(self):
        return "data"

    def write(self, data):
        print(data)
```

✅ Це нормальна та поширена практика.

---

## 3️⃣ Як позначити, що повертає метод (type hints)

```python
def get_user(self, user_id: int) -> dict:
    return {"id": user_id}
```

Для складніших типів:

```python
from typing import Optional, List

def find(self, id: int) -> Optional[dict]:
    ...

def all(self) -> List[dict]:
    ...
```

---

## 4️⃣ Protocol (структурна типізація, “duck typing+”)

Якщо важлива **поведінка**, а не наслідування:

```python
from typing import Protocol

class Storage(Protocol):
    def save(self, data) -> None: ...
```

Будь-який клас з методом `save()` автоматично підходить:

```python
class DBStorage:
    def save(self, data) -> None:
        print("Saved")
```

✔ Використовується з `mypy`, `pyright`, IDE.

---

## 5️⃣ Коли що використовувати

| Ситуація                             | Рішення      |
| ------------------------------------ | ------------ |
| Контракт для сервісів / репозиторіїв | `ABC`        |
| Кілька ролей для класу               | кілька `ABC` |
| Перевірка типів без наслідування     | `Protocol`   |
| Малий проєкт / простий код           | duck typing  |

---

## Короткий висновок

✔ Python **має інтерфейси**, але реалізує їх через:

* `abc.ABC`
* `@abstractmethod`
* `Protocol`
  ✔ Один клас може реалізовувати **кілька інтерфейсів**
  ✔ Типи повернення позначаються через **type hints**

Якщо хочеш, я можу показати приклад **реального web-app (Service → Repository → Controller)** з інтерфейсами.
