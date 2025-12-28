У Python **клас — це шаблон для створення об’єктів**, який містить атрибути (дані) і методи (функції). Ось детальний розбір структури класу та приклади.

---

## 1️⃣ Основна структура класу

```python
class ClassName:
    """Документація класу (docstring)"""

    # Атрибути класу (спільні для всіх об'єктів)
    class_attribute = 0

    # Конструктор (ініціалізація об'єкта)
    def __init__(self, param1, param2):
        self.param1 = param1   # Атрибут об'єкта
        self.param2 = param2

    # Методи об'єкта
    def method(self):
        print(self.param1, self.param2)

    # Метод класу (отримує клас як перший аргумент)
    @classmethod
    def class_method(cls):
        print(cls.class_attribute)

    # Статичний метод (не має доступу до класу чи об'єкта)
    @staticmethod
    def static_method():
        print("Це статичний метод")
```

---

## 2️⃣ Приклад використання

```python
# Створення об'єкта
obj = ClassName("Hello", "World")

# Виклик методу об'єкта
obj.method()  # Hello World

# Виклик класового методу
ClassName.class_method()  # 0

# Виклик статичного методу
ClassName.static_method()  # Це статичний метод
```

---

## 3️⃣ Атрибути

* **Атрибут об’єкта:** `self.param` → унікальний для кожного екземпляру
* **Атрибут класу:** `ClassName.class_attribute` → спільний для всіх екземплярів

```python
obj1 = ClassName("A", "B")
obj2 = ClassName("C", "D")

obj1.class_attribute = 5  # змінює тільки obj1.class_attribute
ClassName.class_attribute = 10  # змінює для всіх об'єктів
```

---

## 4️⃣ Інкапсуляція

* **Публічні атрибути:** `self.attr`
* **Приватні:** `_attr` (згідно з конвенцією)
* **Дуже приватні:** `__attr` (ім’я змінюється, name mangling)

```python
class Test:
    def __init__(self):
        self.public = 1
        self._protected = 2
        self.__private = 3
```

---

## 5️⃣ Наслідування

```python
class Base:
    def greet(self):
        print("Hello from Base")

class Child(Base):
    def greet(self):
        print("Hello from Child")
        super().greet()

c = Child()
c.greet()
```

**Вивід:**

```
Hello from Child
Hello from Base
```

---

## 6️⃣ Корисні поради

1. Використовуй **snake_case** для методів та атрибутів.
2. Використовуй **PascalCase** для назв класів.
3. Конструктор `__init__` завжди отримує `self` як перший аргумент.
4. Використовуй **docstring** для пояснення призначення класу.
5. Для абстрактних класів та інтерфейсів застосовуй `ABC` + `@abstractmethod`.

---

Якщо хочеш, я можу намалювати **графічну схему структури класу Python з методами, атрибутами та типами методів**, щоб усе було наочно.
