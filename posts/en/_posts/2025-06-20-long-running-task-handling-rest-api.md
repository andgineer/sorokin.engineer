---
layout: post
lang: en
ref: async_task_handling_rest
title: "Long running Background Tasks Handling in REST APIs with FastAPI and Celery"
date: 2025-06-20
comments: true
tags: [fastapi, celery, http, status-codes, async]
---
![](/images/async_rest.png){:.post-title}

When building APIs that handle long-running background tasks with Celery, a RESTful interface should provide an async API for the tasks. 

You can't keep HTTP connections open indefinitely waiting for results. 

## The Stages of Long-Running Tasks

1. **Task Creation**: Accept the request and immediately return a task identifier
2. **Result Retrieval**: Allow clients to poll for results using the task identifier

## The Three Key Status Codes

Let's explore how to use status codes 200, 202, and 303 effectively when serving Celery task results from FastAPI.

### 303 See Other - Task Creation Response

When creating a new task, use **303 See Other** to indicate that the task has been accepted and direct the client where 
to check for results:

```python
def create_task(
    task_name: str,
    task_args: List[str],
    request: Request,
    response: Response,
) -> None:
    """
    Create task and return the task id in `Location` header with 303 status code.
    """
    task_id = tasks.send(task_name, args=task_args)
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers["Location"] = f"{request.url.path}/{task_id}"
```

**Why 303?** This status code explicitly tells the client that the resource has been created elsewhere 
and provides the location where they can retrieve the result. 

It's semantically correct for async task creation.

### 202 Accepted - Task Still Processing

When the client polls for results but the task isn't complete yet, return **202 Accepted**:

```python
def get_task(task_id: str, response: Response) -> Any:
    """
    Set response status code to 202 if task in process and 500 if it failed.
    Returns task results if there are any, or None.
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

**Why 202?** This status code indicates that the request has been accepted for processing but hasn't been completed yet. 

It's perfect for ongoing tasks.

### 200 OK - Task Complete

When the task is finished and results are available, return **200 OK** with the actual results:

```python
@router.get("/{words_id}")
def words_result(
    words_id: str = Path(..., description="words ID"),
    response: Response = None,
) -> Optional[api_models.Words]:
    """
    Returns result of `POST /words`.
    When the result is not yet ready returns `202` response.
    """
    results = get_task(words_id, response=response)
    return api_models.Words(count=results) if results is not None else response
```

**200** is the standard success code when the resource is available and returned in the response body.

## Real-World Example: Word Count API

Here's how this pattern works in practice with a word counting service:

### 1. Request Word Count Endpoint
[Start Task](https://github.com/andgineer/fastapi-celery/blob/master/backend/app/api/v1/words/create.py)

### 2. Get Results Endpoint

[Get Results](https://github.com/andgineer/fastapi-celery/blob/master/backend/app/api/v1/words/get.py)

### 3. Delete Task Endpoint
[Delete Task](https://github.com/andgineer/fastapi-celery/blob/master/backend/app/api/v1/words/delete.py)

## Client Flow Example

1. **Client creates task**:
   ```
   POST /words
   → 303 See Other
   Location: /words/abc-123-def
   ```

2. **Client polls for results**:
   ```
   GET /words/abc-123-def
   → 202 Accepted (task still running)
   ```

3. **Client polls again later**:
   ```
   GET /words/abc-123-def
   → 200 OK
   {"count": 1547}
   ```

## Benefits of This Approach

1. **Clear semantics**: Each status code has a specific meaning that clients can rely on
2. **RESTful design**: Follows HTTP standards and REST principles
3. **Scalable**: Doesn't tie up server resources with long-running connections
4. **Client-friendly**: Provides clear guidance on what the client should do next

Of course, even on the first request you can return the result if it's already available - no need for a GET request in this case.
