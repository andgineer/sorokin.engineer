---
layout: post
lang: en
ref: entrez_gene_streaming
title: "Fast Gene Information extraction from NCBI Entrez"
comments: true
tags: [Python, NCBI, Entrez, PubMed, bioinformatics, API, caching]
---

![](/images/dna-helix-streaming.png){:.post-title}

Working with biological data often means dealing with NCBI's Entrez API, a powerful but slow gateway to vast databases like PubMed. 

The challenge? 

Entrez responses can be massive (several megabytes), while you often need just a few fields from the beginning 
of the XML response.

I previously wrote about [streaming XML parsing for HTTP responses](https://sorokin.engineer/posts/en/xml_streaming_chunks_load.html), showing how to extract data without waiting for complete 
downloads. 

Today, let's dive deeper into a real-world application: building a smart gene information API using the 
[http-stream-xml](https://pypi.org/project/http-stream-xml/) library.

## The Entrez Challenge

When you request gene information from NCBI Entrez, you get detailed XML responses that can easily exceed 2MB. 

But here's the key insight: the essential gene information (summary, description, synonyms, and locus) appears within 
the first 5-10KB of the response.

Traditional approaches force you to:
- Wait for the entire multi-megabyte response
- Parse the complete XML document
- Extract just the fields you need

This is wasteful and slow, especially when dealing with unreliable government servers.

## Smart Streaming Solution

The `http-stream-xml` library includes a specialized `Genes` class that demonstrates how to build an intelligent API wrapper:

```python
from http_stream_xml.entrez import genes, GeneFields

# Simple case-insensitive gene lookup with caching
gene_info = genes['PPARA']
print(gene_info[GeneFields.description])
```

Behind this simple interface lies sophisticated streaming logic:

### 1. Early Termination Strategy

```python
extractor = XmlStreamExtractor(self.fields)
for line in request.iter_lines(chunk_size=1024):
    if line:
        extractor.feed(line)
        if extractor.extraction_completed:
            break  # Stop as soon as we have all required fields
```

The parser stops immediately when all required XML tags are found, typically after downloading just 5-10KB instead of the full 2MB response.

### 2. Intelligent Caching Layer

```python
def __getitem__(self, gene_name: str) -> dict[str, Any]:
    gene_name = self.canonical_gene_name(gene_name)  # Case-insensitive
    if gene_name in self.db and len(self.db[gene_name]) >= len(self.fields):
        return self.db[gene_name]  # Return cached result

    gene = self.get_gene_details(gene_name)
    if gene:
        self.db[gene_name] = gene  # Cache for future requests
    return gene
```

The caching system is smart about partial results—if a previous request didn't find all fields, it will retry the request.

### 3. Robust Error Handling

Government APIs can be unreliable. The implementation includes:

```python
@lru_cache(maxsize=100)
def requests_retry_session(
    retries: int = 3,
    backoff_factor: float = 1.0,
    status_forcelist: Collection[int] = (500, 502, 504),
):
    """Retry policy for unreliable government servers."""
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    # Configure adapters for both HTTP and HTTPS
```

### 4. Multiple Gene ID Handling

Real-world gene searches often return multiple IDs. The system intelligently handles this:

```python
def get_gene_id(self, gene_name: str) -> Optional[str]:
    # ... search logic ...
    if len(ids) > 1:
        # Try each ID until we find exact locus match
        for gene_id in ids:
            gene = self.get_gene_details_by_id(gene_id)
            if self.canonical_gene_name(gene[GeneFields.locus]) == gene_name:
                return gene_id
```

This ensures you get the exact gene you're looking for, even when multiple matches exist.

## Performance Benefits

The streaming approach delivers significant performance improvements:

- **Speed**: Extract data in ~1-2 seconds instead of 10-30 seconds
- **Bandwidth**: Download 5-10KB instead of 2MB+ per request
- **Reliability**: Early termination reduces exposure to network timeouts
- **Scalability**: Built-in caching eliminates redundant API calls

## Practical Usage Patterns

### Basic Gene Lookup
```python
from http_stream_xml.entrez import genes, GeneFields

# Get gene description
description = genes['SLC9A3'][GeneFields.description]
print(f"Gene function: {description}")
```

### Batch Processing
```python
gene_names = ['PPARA', 'SLC9A3', 'MYO5B', 'PDZK1']
for name in gene_names:
    if gene_data := genes[name]:
        print(f"{name}: {gene_data[GeneFields.summary]}")
```

### Custom Fields
```python
from http_stream_xml.entrez import Genes, GeneFields

# Create specialized instance for specific fields
custom_genes = Genes(fields=[GeneFields.summary, GeneFields.synonyms])
```

## Configuration Options

The `Genes` class offers flexible configuration:

```python
genes = Genes(
    timeout=30,                    # Request timeout
    max_bytes_to_fetch=10*1024,    # Safety limit
    api_key="your_entrez_key",     # For higher rate limits
    fields=[GeneFields.summary]    # Customize extracted fields
)
```

## Conclusion

The `http-stream-xml` library's Entrez integration demonstrates how streaming XML parsing can transform API interactions with large, slow data sources. By combining early termination, intelligent caching, and robust error handling, you can build APIs that are both fast and reliable.

This approach isn't limited to biological data—any scenario involving large XML responses with front-loaded important data can benefit from similar streaming strategies.

The next time you're faced with slow, large API responses, consider whether the data you need appears early in the response. If so, streaming parsing might be your performance salvation.

## Source Code

- [http-stream-xml](https://github.com/andgineer/http-stream-xml)
- [Entrez integration](https://github.com/andgineer/http-stream-xml/blob/master/src/http_stream_xml/entrez.py)
- [Usage examples](https://github.com/andgineer/http-stream-xml/tree/master/src/http_stream_xml/examples)