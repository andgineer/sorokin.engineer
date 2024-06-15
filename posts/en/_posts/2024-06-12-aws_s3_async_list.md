---
layout: post
lang: en
ref: aws_s3_async_list
title: "Efficiently Listing Large AWS S3 Buckets with Python"
comments: true
tags: [aws s3 bucket list_objects async aiobotocore python]
---

![](/images/s3-list-objects-async.png){:.post-title}

In AWS S3, there are no folders, just a flat namespace. 
For effective object distribution, it's recommended to use hashes as key prefixes. 
This ensures better performance and scalability.

One major issue arises when you need to list objects in a large bucket with dozens of thousands 
or even millions of objects. This process can take many minutes, 
because for AWS this is just single huge flat list, collected from many nodes.

To address this problem, I've created a Python class called 
[`S3BucketObjects`](https://andgineer.github.io/async-s3/) that 
efficiently lists large buckets.

## Async

`S3BucketObjects` uses `aiobotocore` for non-blocking IO operations. 
This allows the package to efficiently work in parallel.

### Intelligent Parallelism

Although S3 doesn't have actual folders, `S3BucketObjects` simulates recursive folder 
traversal by using the `Delimiter` parameter in the AWS S3 `list_objects` API call. 
This parameter treats the given delimiter (`/`) as a folder separator, 
causing `list_objects` to return not all the keys with the requested prefix, 
but two lists: objects ("files") and "common prefixes" - logical "subfolders".

`S3BucketObjects` starts by listing objects at the specified prefix (the root directory), 
utilizing the delimiter to retrieve the immediate objects and "subfolders" instead of listing 
all the objects at once. 

It then recursively calls `list_objects` for each "subfolder", treating it as a new root 
prefix.

To reduce the number of API calls needed, `S3BucketObjects` employs two key optimizations.

#### *Recursion Depth Limitation* 

You can specify a maximum recursion depth (`max_depth`) to limit how deep the package 
traverses into the directory structure. 

Under the specified depth, `S3BucketObjects` will list objects just as flat list,
without further recursion.

This can significantly reduce the number of API calls required, especially for buckets with 
deeply nested "subfolders".

#### *Prefix Grouping*

`S3BucketObjects` intelligently groups "folders" prefixes to minimize the number of API calls 
needed. 

Instead of listing objects for each individual "folder" (which would require a separate API 
call per "folder"), it groups "folders" by common prefixes and makes a single API 
call for each group prefix.

For example, with object keys like:

```
folder0001/
folder0002/
folder0003/
..
folder9999/
```

Instead of making thousands of API calls (one for each "folder"), `S3BucketObjects`
with `max_folders=10` parameter will group them into just ten prefix groups:

```
folder0
folder1
...
folder9
```

This significantly reduces the number of API calls required, resulting in faster listing 
times for "folders" with big number of "subfolders".

By combining asynchronous operations, recursive traversal utilizing the "Delimiter" parameter, 
depth control, and intelligent prefix grouping, `S3BucketObjects` can improve the
performance tenfold.

## Usage

See [documentation](https://andgineer.github.io/async-s3/).

## Command-Line Utility

The `async-s3` package also includes [a command-line utility](https://andgineer.github.io/async-s3/as3/) 
for convenient experiments with your S3 buckets.

```bash
as3 du s3://my-bucket/my-key -d 1 -f 20 -r 3
```

This command shows the size and number of objects in `s3://my-bucket/my-key`, limiting the 
recursion depth to `1`. 

If there are more than `20` folders at one level, it tries to group them by prefixes. 

The request is repeated `three` times, and the average time is calculated. 
