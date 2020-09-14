---
layout: post
lang: ru
ref: sqlalchemy_postgres_copy_from
title: "Как использовать COPY FROM в SQLAlchemy чтобы быстро добавить большое число записей"
comments: true
tags: [python, postgres, sqlalchemy]
---
![](/images/elephant_copy.jpg){:.post-title}

SQLAlchemy предоставляем вам удобный способ абстрагироваться от таблиц и работать в уютной
идеологии прикладных объектов.

Но что если вам надо добавить большое число записей, выполнить массовое добавление? 

Делать это через SQLAlchemy будет неэффективно.

Разработчики Postgres рекомендуют испольовать для этого специальную SQL команду 
[COPY FROM](https://www.postgresql.org/docs/current/populate.html). Она принимает на входе файл 
со всеми инсертами, и быстро выполняет их все разом. Файл может быть как в файловой системе 
сервера БД, так и может быть передан по сети.

С помощью Postgres `COPY FROM` вы за считанные миллисекунды вставите в таблицу Postgres тысячи 
записей. Если бы вы делали это с помощью отдельных `insert`, да еще и через SQLAlchemy абстракции, 
это  заняло бы у вас в сотни раз дольше.

Если необходимо добавить миллионы записей, то `COPY FROM` отработает за секунды, а отдельные
`insert` за часы.

Этой команды нет в SQLAlchemy по очевидным причинам - это уже вотчина 
[ETL](https://ru.wikipedia.org/wiki/ETL), а вовсе не [ORM](https://ru.wikipedia.org/wiki/ORM).

Эта команда реализована в драйвере [psycopg](https://www.psycopg.org/docs/index.html), 
обычно используемом для работы с Postgres из SQLAlchemy -
[copy_expert](https://www.psycopg.org/docs/cursor.html#cursor.copy_expert).

Как же добраться до команды `COPY FROM` из SQLAlchemy?

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

При работе с SQLAlchemy обычно у вас есть сессия. Для простоты в примере выше я ее создаю, но 
вы можете использовать ту же, что и для работы с объектами SQLAlchemy.

Из сессии вы берете курсор (`cursor`).

И вызываете функцию [copy_expert](https://www.psycopg.org/docs/cursor.html#cursor.copy_expert).

В переменной `my_csv_string` должен быть файл с записями для массового добавления - его 
параметры описываются в параметрах команды Postgres 
[COPY FROM](https://www.postgresql.org/docs/current/populate.html).
В данном случае я указал, что это CSV с заголовочной строкой. Разделитель по умолчанию
запятая но это можно изменить - смотрите описание команды `COPY`.

В переменной `my_columns_comma_separated` нужно через запятую перечислить колонки в том порядке, 
как они следуют в CSV. Я обычно использую для этого заголовок, с помощью которого я формировал
csv. 

Для формирования CSV можно использовать встроенный в Python 
[csv](https://docs.python.org/3/library/csv.html).
Но если уж вы формируете столь большое число строк для вставки, скорее всего вам нужно провести 
какие-то манипуляции с ними. И тут вряд ли можно посоветовать что-то лучше 
[pandas](https://pandas.pydata.org/), которая в том числе и CSV вам сформирует.

До и после `COPY FROM` вы используете эту сессию SQLAlchemy как обычно.

В моем примере я сразу делаю `commit()`, но это вам решать, когда закрывать транзакцию.
Возможно, что вы захотите что-то еще в ней сделать перед закрытием.

