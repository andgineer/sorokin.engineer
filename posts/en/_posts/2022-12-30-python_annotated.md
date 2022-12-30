---
layout: post
lang: en
ref: python_annotated
title: "Using Annotated to store metadata"
comments: true
tags: [Python, mypy]
---

Often we need some metadata about class attributes.

For example, if we have class with some measures and we want to show all
attributes with appropriate measures:

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

Result will be `10000 Hz`.

The problem in the code above - attributes and metadata stored
separately. It's easy to forget add metadata and it's not easy to look
for measures in separate place.

Starting from Python 3.9 we have new way to add metadata - `Annotated`.
It extremely useful for libraries like Pydantic but we can use it in
our application.

here the example from above but using new `Annotated`:

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
