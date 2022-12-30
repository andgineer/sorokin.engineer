---
layout: post
lang: ru
ref: python_annotated
title: "Использование Annotated для хранения метаданных"
comments: true
tags: [Python, mypy]
---

Зачастую нам необходимо сохранить некие метаданные, описывающие атрибуты объекта.

Например, мы хотим описать размерности полей объекта, чтобы можно
было показать значения вместе с размерностями:

```python
MEASURES = {
    "n1": "Hz",
}

class PrettyNumbers:
    n1: Annotated[int, "Hz"] = 10000.1
        
    def measure(self, attr_name: str) -> str:
        return MEASURES[attr_name]
        
    def __repr__(self) -> str:
        return f"{self.n1} {self.measure('n1')}"
    
print(PrettyNumbers())
```

В результате будет напечатано `10000 Hz`.

Проблема в примере выше в том, что у нас в разных местах описаны атрибуты 
и их метаданные. Это и неудобно и чревато ошибками

Начиная с Python 3.9 появилось `Annotated`.
В первую очередь это предназначено для библиотек типа Pydantic но
никто не запрещает нам использовать это и в наших приложениях.
 
Например, вот так можно переписать пример выше, используя `Annotated`:

```python
from typing import Annotated, get_type_hints

class PrettyNumbers:
    n1: Annotated[int, "Hz"] = 10000.1
        
    def measure(self, attr_name: str) -> str:
        return get_type_hints(PrettyNumbers, include_extras=True)[attr_name].__metadata__[0]
        
    def __repr__(self) -> str:
        return f"{self.n1} {self.measure('n1')}"
    
print(PrettyNumbers())
```
