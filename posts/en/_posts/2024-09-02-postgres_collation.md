---
layout: post
lang: en
ref: postgres_collation
title: "The Great PostgreSQL Collation Conundrum: A Tale of Alphabetical Anarchy"
comments: true
tags: [aws postgres collation]
---

![](/images/postgres-collation.png){:.post-title}

I recently faced a puzzling issue with PostgreSQL that left me scratching my head. 
What should have been a quick half-point story turned into a full story point task..

## The Unexpected Sorting Surprise

After pushing a new sorting feature to production, I noticed something odd. 
This was a Django application, and at first, the behavior was really mysterious.

But after some time I found that the problem was in how `ORDER BY` worked
locally and on server.

On my local machine, when I ran:

```sql
SELECT * FROM users ORDER BY name;
```

The result was:

```
a
A
b
B
```

But on the server, I saw this instead:

```
A
B
a
b
```

Same query, different results. What was going on?

## The Culprit: Collation Differences

At this point, it was easy to guess the root cause: [collation](https://www.postgresql.org/docs/12/collation.html) settings. 
My local machine was using a case-insensitive collation that followed dictionary order, 
while the production server was using the default "C" locale, which sorts by ASCII codes.

## Attempted Fix: Specifying Collation

My first thought was to specify the collation for the column:

```sql
ALTER TABLE users ALTER COLUMN name TYPE VARCHAR COLLATE "en_US.utf8";
```

This approach should ensure consistent sorting for the column across all queries. 
However, I hit a snag...

## The Server Complication

It turned out our production PostgreSQL server didn't support the "en_US.utf8" 
collation I was trying to use. 

This was unexpected and threw a wrench in my initial plan.

## The Solution: LOWER to the Rescue

Ok different approach. I used `LOWER` in the `ORDER BY` clause:

```sql
SELECT * FROM users ORDER BY LOWER(name);
```

This method achieves case-insensitive sorting.
It's non-deterministic, but it works for my use case.

An additional benefit is that we don't have to alter the table structure.

To make this solution more efficient, I created an index:

```sql
CREATE INDEX ON users (LOWER(name));
```

This index significantly improves query performance when using `LOWER` in the `ORDER BY` clause.
