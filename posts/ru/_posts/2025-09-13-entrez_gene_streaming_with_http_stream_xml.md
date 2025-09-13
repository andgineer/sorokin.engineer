---
layout: post
lang: ru
ref: entrez_gene_streaming
title: "Создание умного API для генетической информации с потоковой обработкой NCBI Entrez"
comments: true
tags: [Python, NCBI, Entrez, PubMed, биоинформатика, API, кэширование]
---

![](/images/dna-helix-streaming.png){:.post-title}

Работа с биологическими данными часто означает взаимодействие с API NCBI Entrez — мощным, но медленным шлюзом к огромным базам данных, 
таким как PubMed. 

Проблема в том, что ответы Entrez могут быть огромными (несколько мегабайт), в то время как часто нужны лишь несколько полей 
из начала XML-ответа.

Ранее я писал о [потоковом парсинге XML для HTTP-ответов](https://sorokin.engineer/posts/ru/xml_streaming_chunks_load.html), показывая, как извлекать данные без ожидания полной загрузки. 

Сегодня давайте углубимся в реальное применение: создание умного API для генетической информации с использованием библиотеки 
[http-stream-xml](https://pypi.org/project/http-stream-xml/).

## Проблемы Entrez

Когда вы запрашиваете информацию о гене из NCBI Entrez, вы получаете детализированные XML-ответы, которые легко могут превышать 2MB. 

Но основная информация о гене — краткое описание, полное описание, синонимы и локус — появляется в первых 5-10КБ ответа.

Традиционные подходы заставляют вас:
- Ждать получения всего многомегабайтного ответа
- Парсить полный XML-документ
- Извлекать только нужные поля

Это расточительно и медленно, особенно при работе с ненадежными государственными серверами.

## Умное потоковое решение

Библиотека `http-stream-xml` включает специализированный класс `Genes`, который демонстрирует, как создать интеллектуальную обертку API:

```python
from http_stream_xml.entrez import genes, GeneFields

# Простой поиск генов без учета регистра с кэшированием
gene_info = genes['PPARA']
print(gene_info[GeneFields.description])
```

За этим простым интерфейсом скрывается сложная потоковая логика:

### 1. Стратегия раннего завершения

```python
extractor = XmlStreamExtractor(self.fields)
for line in request.iter_lines(chunk_size=1024):
    if line:
        extractor.feed(line)
        if extractor.extraction_completed:
            break  # Останавливаемся, как только получили все нужные поля
```

Парсер останавливается сразу же, как только найдены все необходимые XML-теги, обычно после загрузки всего 5-10КБ вместо полных 
2МБ ответа.

### 2. Интеллектуальный слой кэширования

```python
def __getitem__(self, gene_name: str) -> dict[str, Any]:
    gene_name = self.canonical_gene_name(gene_name)  # Без учета регистра
    if gene_name in self.db and len(self.db[gene_name]) >= len(self.fields):
        return self.db[gene_name]  # Возвращаем кэшированный результат

    gene = self.get_gene_details(gene_name)
    if gene:
        self.db[gene_name] = gene  # Кэшируем для будущих запросов
    return gene
```

Система кэширования умно обрабатывает частичные результаты — если предыдущий запрос не нашел все поля, она повторит запрос.

### 3. Надежная обработка ошибок

Сервисы могут быть ненадежными. Реализация включает:

```python
@lru_cache(maxsize=100)
def requests_retry_session(
    retries: int = 3,
    backoff_factor: float = 1.0,
    status_forcelist: Collection[int] = (500, 502, 504),
):
    """Политика повторов для ненадежных государственных серверов."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    # Настройка адаптеров для HTTP и HTTPS
```

### 4. Обработка множественных ID генов

Реальные поиски генов часто возвращают множественные ID. Система интеллектуально обрабатывает это:

```python
def get_gene_id(self, gene_name: str) -> Optional[str]:
    # ... логика поиска ...
    if len(ids) > 1:
        # Пробуем каждый ID, пока не найдем точное совпадение локуса
        for gene_id in ids:
            gene = self.get_gene_details_by_id(gene_id)
            if self.canonical_gene_name(gene[GeneFields.locus]) == gene_name:
                return gene_id
```

Это гарантирует, что вы получите именно тот ген, который ищете, даже если существует несколько совпадений.

## Преимущества производительности

Потоковый подход обеспечивает значительные улучшения производительности:

- **Скорость**: Извлечение данных за ~1-2 секунды вместо 10-30 секунд
- **Трафик**: Загрузка 5-10КБ вместо 2МБ+ на запрос
- **Надежность**: Раннее завершение снижает воздействие сетевых таймаутов
- **Масштабируемость**: Встроенное кэширование исключает избыточные API-вызовы

## Практические паттерны использования

### Базовый поиск гена
```python
from http_stream_xml.entrez import genes, GeneFields

# Получить описание гена
description = genes['SLC9A3'][GeneFields.description]
print(f"Функция гена: {description}")
```

### Пакетная обработка
```python
gene_names = ['PPARA', 'SLC9A3', 'MYO5B', 'PDZK1']
for name in gene_names:
    if gene_data := genes[name]:
        print(f"{name}: {gene_data[GeneFields.summary]}")
```

### Пользовательские поля
```python
from http_stream_xml.entrez import Genes, GeneFields

# Создать специализированный экземпляр для конкретных полей
custom_genes = Genes(fields=[GeneFields.summary, GeneFields.synonyms])
```

## Параметры конфигурации

Класс `Genes` предлагает гибкую конфигурацию:

```python
genes = Genes(
    timeout=30,                    # Таймаут запроса
    max_bytes_to_fetch=10*1024,    # Лимит безопасности
    api_key="your_entrez_key",     # Для повышенных лимитов скорости
    fields=[GeneFields.summary]    # Настройка извлекаемых полей
)
```

## Ключевые принципы дизайна

1. **Быстрый отказ**: Прекращайте обработку, как только получили то, что нужно
2. **Умное кэширование**: Сохраняйте результаты, но проверяйте полноту
3. **Обработка отказов**: Сервисы по природе ненадежны
4. **Гибкость**: Поддерживайте как простые, так и продвинутые случаи использования

## Заключение

Интеграция Entrez в библиотеке `http-stream-xml` демонстрирует, как потоковый парсинг XML может трансформировать взаимодействие 
с API больших, медленных источников данных. 
Сочетая раннее завершение, интеллектуальное кэширование и надежную обработку ошибок, вы можете создавать API, 
которые одновременно быстры и надежны.

Этот подход не ограничивается биологическими данными — любой сценарий, включающий большие XML-ответы с важными данными в начале, 
может извлечь выгоду из подобных потоковых стратегий.

В следующий раз, когда вы столкнетесь с медленными, большими API-ответами, подумайте, появляются ли нужные вам данные в начале ответа. 
Если да, потоковый парсинг может стать вашим спасением производительности.

## Исходный код

- [http-stream-xml](https://github.com/andgineer/http-stream-xml)
- [Интеграция Entrez](https://github.com/andgineer/http-stream-xml/blob/master/src/http_stream_xml/entrez.py)
- [Примеры использования](https://github.com/andgineer/http-stream-xml/tree/master/src/http_stream_xml/examples)