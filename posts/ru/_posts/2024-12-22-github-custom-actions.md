---
layout: post
lang: ru
ref: github_custom_actions
title: "Создайте Свой GitHub Action за 5 Минут на Python"
comments: true
tags: [github actions, Python]
---

![](/images/github-custom-actions.png){:.post-title}

# Простые GitHub Actions на Python

Создание собственных GitHub Actions может выглядеть сложным - нужно разбираться с переменными окружения, 
входными/выходными параметрами, обработкой ошибок и многим другим. Но это может быть намного проще.

Библиотека [github-custom-actions](https://andgineer.github.io/github-custom-actions/ru/) избавляет от всей рутины и предоставляет:
- Типизацию переменных GitHub с автодополнением в IDE
- Удобный доступ ко всему контексту GitHub (репозиторий, workflow, runner и т.д.)
- Встроенные Jinja шаблоны для красивых отчетов
- Автоматическую обработку и логирование ошибок
- Типизированные входные/выходные параметры

Вы просто пишете код на Python, а библиотека берет на себя всю интеграцию с GitHub Actions. 

Давайте посмотрим, как легко создать свой action.

## Пример: Валидатор Имени Ветки

Вот action, который проверяет соответствие имени ветки правилам вашей команды:

```python
from github_custom_actions.action_base import ActionBase
from github_custom_actions.inputs_outputs import ActionInputs, ActionOutputs
import re

class ValidatorInputs(ActionInputs):
   pattern: str = "^(feature|bugfix|hotfix)/[a-z0-9-]+$"
   """Шаблон имени ветки (регулярное выражение)"""

class ValidatorOutputs(ActionOutputs):
   valid: str
   """Соответствует ли имя ветки шаблону"""

class BranchValidator(ActionBase):
   inputs: ValidatorInputs
   outputs: ValidatorOutputs

   def main(self):
       # Получаем имя текущей ветки из переменных окружения GitHub
       branch = self.env.github_ref_name
       
       # Проверяем соответствие имени ветки шаблону
       is_valid = bool(re.match(self.inputs.pattern, branch))
       self.outputs.valid = str(is_valid)

       # Создаем отчет используя шаблон
       self.summary.text = self.render("""
## Проверка Имени Ветки
{% raw %}
Branch: `{{ branch }}`
Pattern: `{{ inputs.pattern }}`
Status: {{ "✅ Valid" if outputs.valid == "true" else "❌ Invalid" }}
{% endraw %}
""", branch=branch)

       if not is_valid:
           raise ValueError(f"Invalid branch name: {branch}")

if __name__ == "__main__":
   BranchValidator().run()
```

Используйте в вашем workflow:

```yaml
name: Validate Branch
on: [push, pull_request]

jobs:
 check:
   runs-on: ubuntu-latest
   steps:
     - uses: ./
       with:
         pattern: '^(feature|bugfix|hotfix)/[a-z0-9-]+$'
```

## Публикация в GitHub Marketplace

1. Создайте репозиторий для вашего action с такой структурой:
```python
my-action/
  ├── action.yml       # Метаданные action
  ├── Dockerfile      # Используем образ Python и устанавливаем ваш action
  ├── requirements.txt # Включаем github-custom-actions
  └── main.py         # Ваш код action
```

2. Добавьте в `action.yml`:
```yaml
name: 'Branch Name Validator'
description: 'Validates branch names against pattern'
inputs:
  pattern:
    description: 'Branch name pattern (regex)'
    required: true
    default: '^(feature|bugfix|hotfix)/[a-z0-9-]+$'
outputs:
  valid:
    description: 'Whether branch name is valid'
runs:
  using: 'docker'
  image: 'Dockerfile'
```

3. Создайте `Dockerfile`:
```dockerfile
FROM python:3-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "/main.py"]
```

4. [Опубликуйте в GitHub Marketplace](https://docs.github.com/en/actions/creating-actions/publishing-actions-in-github-marketplace)

После этого любой сможет использовать ваш action:

```yaml
- uses: your-github-name/your-action-repo@v1
  with:
    pattern: '^(feature|bugfix|hotfix)/[a-z0-9-]+$'
```