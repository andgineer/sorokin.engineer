---
layout: post
lang: ru
ref: async_task_handling_rest
title: "Асинхронная Обработка Задач в REST API с FastAPI и Celery"
date: 2025-06-20
comments: true
tags: [fastapi, celery, http, status-codes, async]
---
![](/images/async_rest.png){:.post-title}

При создании API, которые обрабатывают долгоработающие задачи с Celery, RESTful интерфейс должен предоставлять 
асинхронный API для задач.

Вы не можете держать HTTP соединения открытыми бесконечно, ожидая результатов.

## Этапы долго работающих задач

1. **Создание задачи**: Принять запрос и немедленно вернуть идентификатор задачи
2. **Получение результата**: Позволить клиентам опрашивать результаты, используя идентификатор задачи

## Три ключевых кода состояния

Давайте рассмотрим, как эффективно использовать коды состояния 200, 202 и 303 при обслуживании результатов Celery задач из FastAPI.

### 303 See Other - Ответ при создании задачи

При создании новой задачи используйте **303 See Other**, чтобы указать, что задача была принята, 
и направить клиента туда, где можно проверить результаты:

```python
def create_task(
    task_name: str,
    task_args: List[str],
    request: Request,
    response: Response,
) -> None:
    """
    Создать задачу и вернуть task id в заголовке `Location` с кодом состояния 303.
    """
    task_id = tasks.send(task_name, args=task_args)
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers["Location"] = f"{request.url.path}/{task_id}"
```

**Почему 303?** Этот код состояния явно сообщает клиенту, что ресурс был создан в другом месте, 
и предоставляет местоположение, где можно получить результат.

Он семантически корректен для создания асинхронных задач.

### 202 Accepted - Задача все еще обрабатывается

Когда клиент опрашивает результаты, но задача еще не завершена, верните **202 Accepted**:

```python
def get_task(task_id: str, response: Response) -> Any:
    """
    Установить код состояния ответа 202, если задача в процессе, и 500, если она не удалась.
    Возвращает результаты задачи, если они есть, или None.
    """
    try:
        results = tasks.get(task_id)
        if isinstance(results, Exception):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return None
        if results is None:
            response.status_code = status.HTTP_202_ACCEPTED
        return results
    except Exception:
        response.status_code = status.HTTP_404_NOT_FOUND
    return None
```

**Почему 202?** Этот код состояния указывает, что запрос был принят для обработки, но еще не завершен.

Он идеально подходит для текущих задач.

### 200 OK - Задача завершена

Когда задача завершена и результаты доступны, верните **200 OK** с фактическими результатами:

```python
@router.get("/{words_id}")
def words_result(
    words_id: str = Path(..., description="words ID"),
    response: Response = None,
) -> Optional[api_models.Words]:
    """
    Возвращает результат `POST /words`.
    Когда результат еще не готов, возвращает ответ `202`.
    """
    results = get_task(words_id, response=response)
    return api_models.Words(count=results) if results is not None else response
```

**200** - это стандартный код успеха, когда ресурс доступен и возвращается в теле ответа.

## Реальный пример: API подсчета слов

Вот как этот паттерн работает на практике с сервисом подсчета слов:

### 1. Запрос подсчета слов
[Запуск задачи](https://github.com/andgineer/fastapi-celery/blob/master/backend/app/api/v1/words/create.py)

### 2. Получение результатов

[Получение результатов](https://github.com/andgineer/fastapi-celery/blob/master/backend/app/api/v1/words/get.py)

### 3. Удаление задачи
[Удаление задачи](https://github.com/andgineer/fastapi-celery/blob/master/backend/app/api/v1/words/delete.py)

## Пример взаимодействия

1. **Клиент создает задачу**:
   ```
   POST /words
   → 303 See Other
   Location: /words/abc-123-def
   ```

2. **Клиент опрашивает результаты**:
   ```
   GET /words/abc-123-def
   → 202 Accepted (задача все еще выполняется)
   ```

3. **Клиент опрашивает снова позже**:
   ```
   GET /words/abc-123-def
   → 200 OK
   {"count": 1547}
   ```

## Преимущества этого подхода

1. **Четкая семантика**: Каждый код состояния имеет конкретное значение, на которое могут полагаться клиенты
2. **RESTful дизайн**: Следует стандартам HTTP и принципам REST
3. **Масштабируемость**: Не привязывает серверные ресурсы к долгоработающим соединениям
4. **Дружественность к клиенту**: Предоставляет четкое руководство о том, что клиент должен делать дальше

Конечно, даже при первом запросе вы можете вернуть результат, если он уже доступен - в этом случае нет необходимости в GET запросе.