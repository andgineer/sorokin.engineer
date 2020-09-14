---
layout: post
lang: ru
ref: apache_airflow_sqlalchemy_operator
title: "Как использовать модели SQLAlchemy в Apache Airflow DAG"
comments: true
tags: [python, sqlalchemy, airflow]
---
![](/images/airflow.png){:.post-title}

Apache Airflow позволяет вам описывать задачи [ETL](https://ru.wikipedia.org/wiki/ETL) как код 
на Python. Как результат, скучные конвейры данных превращаются в элегантный код,
который приятно читать и отлаживать.

Основной режим использования Apache Airflow - массивные изменения баз данных. Для которых,
безусловно, более уместны вручную оптимизированные SQL-запросы. 

Но зачастую в ваших ETL [DAG](https://airflow.apache.org/docs/stable/concepts.html) было бы удобно
задействовать [SQLAlchemy ORM](https://www.sqlalchemy.org/) для каких-то вспомогательных операций.

Интересно, что внутри Apache Airflow основана на SQLAlchemy.

Например, вот так вы можете получить из нее список соединения (Apache Airflow Connections) 
начинающиеся с `my_prefix_`:
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

То, что SQLAlchemy обычно не используется для Apache Airflow DAG - понятно и обоснованно. 
Дополнительные уровни абстракции, с которыми так удобно работать в SQLAlchemy, в конвейерах по 
перемалыванию данных были бы только ненужным замедлителем работы.

Если же вам нужны модели SQLAlchemy их легко использовать, получив SQLAlchemy соединение,
например, из 
 [PostgresHook](https://airflow.readthedocs.io/en/stable/_modules/airflow/hooks/postgres_hook.html)
 
{% highlight python %}
hook = PostgresHook(postgres_conn_id=my_conn_id)
engine = hook.get_sqlalchemy_engine()
session = sessionmaker(bind=engine)()
{% endhighlight %}

Но во-1х неправильно захламлять код, делая это в каждой Apache Airflow Task. Во-2х, что бы у вас не 
было утечки соединений Postgres надо обязательно закрывать соединение после работы. Что означает
обрамление вашего прикладного кода в `try-finally` и еще большее его захламление.

К счастью, в Apache Airflow вы с легкостью можете создавать свои операторы, где можно спрятать все 
эти не относящиеся к прикладному коду детали.

Вот пример SQLAlchemy Operator для Postgres. При необходимости можно с легкомтью сделать его
универсальным - чтобы он работал с любым типом БД, а не только Postgres.
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

Вот пример его использования:
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