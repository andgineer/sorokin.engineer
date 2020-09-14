---
layout: post
lang: en
ref: apache_airflow_sqlalchemy_operator
title: "How to use SQLAlchemy in Apache Airflow DAG"
comments: true
tags: [python, sqlalchemy, airflow]
---
![](/images/airflow.png){:.post-title}

With Apache Airflow you can design your [ETL](https://en.wikipedia.org/wiki/ETL) 
as elegant Python code you would love to maintain and debug.

Usually we use Apache Airflow for bulk DB updates. So this is highly optimized SQL queries and so on. 


But from time to time you would like to use [SQLAlchemy](https://www.sqlalchemy.org/) models
inside your [DAG](https://airflow.apache.org/docs/stable/concepts.html) for some not so massive
but complex operations with DB.

And Apache Airflow even based on SQLAlchemy!

For example this is how to get Apache Airflow Connections which id's started with `my_prefix_`:
{% highlight python %}
from airflow import settings
from airflow.models import Connection

session = settings.Session()
try:
    conns: Iterable[Connection] = (
        session.query(Connection.conn_id)
        .filter(Connection.conn_id.ilike('my_prefix_%'))
        .all()
    )
    conn_ids = [conn.conn_id for conn in conns]
finally:
    session.commit()
{% endhighlight %}

In common DAG you would not use SQLAlchemy - for bulk operations that would be just too slow.

If you do need SQLAlchemy model inside DAG you can get SQLAlchemy session for example from
 [PostgresHook](https://airflow.readthedocs.io/en/stable/_modules/airflow/hooks/postgres_hook.html)
 
{% highlight python %}
hook = PostgresHook(postgres_conn_id=my_conn_id)
engine = hook.get_sqlalchemy_engine()
session = sessionmaker(bind=engine)()
{% endhighlight %}

But if you are going to do that in many Apache Airflow tasks this code will unnecessary complicate
you business logic code. Moreover you should close the DB connection to prevent connection leakage.
So this is additional `try-finally` around your code and it will became even more obscure.

Luckily you can easily create SQLAlchemy Operator for Apache Airflow and encapsulate all this code in it.

For example this is SQLAlchemy Operator for Postgres.
{% highlight python %}
from airflow.operators.python_operator import PythonOperator
from airflow.utils.decorators import apply_defaults
from sqlalchemy.orm import sessionmaker, Session
from airflow.hooks.postgres_hook import PostgresHook


def get_session(conn_id: str) -> Session:
    hook = PostgresHook(postgres_conn_id=conn_id)
    engine = hook.get_sqlalchemy_engine()
    return sessionmaker(bind=engine)()


class SQLAlchemyOperator(PythonOperator):
    """
    PythonOperator with SQLAlchemy session management - creates session for the Python callable
    and commit/rollback it afterwards.

    Set `conn_id` with you DB connection.

    Pass `session` parameter to the python callable.
    """
    @apply_defaults
    def __init__(
            self,
            conn_id: str,
            *args, **kwargs):
        self.conn_id = conn_id
        super().__init__(*args, **kwargs)

    def execute_callable(self):
        session = get_session(self.conn_id)
        try:
            result = self.python_callable(*self.op_args, session=session, **self.op_kwargs)
        except Exception:
            session.rollback()
            raise
        session.commit()
        return result
{% endhighlight %}

This is how to use it:
{% highlight python %}
dag = DAG(
    dag_id='SQAlchemyDAG',
    schedule_interval='0 2 1 * *',  # monthly at 2:00 AM, 1st day of a month
    start_date=datetime(2020, 8, 1),  
)


def sqlalchemy_task(session: Session, **kwargs):
    session.query(YourSQLAlchemyModel)


request_count = SQLAlchemyOperator(
    dag=dag,
    task_id='sqlalchemy',
    conn_id='my_db',
    python_callable=sqlalchemy_task,
    provide_context=True,
)
{% endhighlight %}