---
layout: post
lang: en
ref: sqlalchemy_postgres_copy_from
title: "Bulk insert with Postgres COPY FROM in SQLAlchemy"
comments: true
tags: [python, postgres, sqlalchemy]
---
![](/images/elephant_copy.jpg){:.post-title}

SQLAlchemy is nice and comfortable way to work with DB using application abstractions instead of
ancient SQL.

But what if you need bulk insert for huge amount of records? 

It would be insane to insert each record separately with SQLAlchemy. That will take ages.

Postgres has some recommendation how to do that with
[COPY FROM](https://www.postgresql.org/docs/current/populate.html). This command takes file
and bulk insert records from it very fast.

It will take milliseconds to insert thousands of records. With plain vanilla inserts it would take 
hundred times more. If you insert millions of records, the difference could be seconds in `COPY FROM`
and hours in plain inserts!

The file could be in DB server file system or you can send it by network.

There is no such command in SQLAlchemy.
Because usually you need it in 
[ETL](https://en.wikipedia.org/wiki/ETL). But SQLAlchemy is [ORM](https://en.wikipedia.org/wiki/ORM).

This command could be found in [psycopg](https://www.psycopg.org/docs/index.html), 
usually you use this driver to work with Postgres from SQLAlchemy.

But how to use Postgres `COPY FROM` in SQLAlchemy?

{% highlight python %}
    engine = create_engine('postgresql://my_user:my_password@my.host.com/my_db')
    session = sessionmaker(bind=engine)()
    
    cursor = session.connection().connection.cursor()
    cursor.copy_expert( 
        f'COPY my_table ({my_columns_comma_separated}) FROM STDIN WITH (FORMAT CSV, HEADER)',
        io.StringIO(my_csv_string),
    )
    session.commit()
{% endhighlight %}

In SQLAlchemy you use sessions to work. In my example I created the session but in real application
 you would use the one you already have.

As you see, we are getting `cursor` from SQLAlchemy session.

In cursor you can call [copy_expert](https://www.psycopg.org/docs/cursor.html#cursor.copy_expert).

In `my_csv_string` you place file with records to insert - and describe parameters of your file in 
[COPY FROM command](https://www.postgresql.org/docs/current/populate.html).
In the example above I described it as CSV with header line. Default separator is "`,`" and of cause
you can change that.

In `my_columns_comma_separated` list you columns, separating them with "`,`", in exactly the same 
order as in the CSV file. Usually you just use the same descriptor you used to create the CSV. 

To create CSV you can use embedded Python 
[csv](https://docs.python.org/3/library/csv.html).
But usually before bulk insert you somehow pre-process you data.
And the best tool for that would be [pandas](https://pandas.pydata.org/).
And of cause `pandas` can create CSV.

After and before `COPY FROM` you use this SQLAlchemy session as usual.

You can `commit()` just after `COPY FROM` as in my example above.
Or you can do some more operations in this session with SQLAlchemy.

