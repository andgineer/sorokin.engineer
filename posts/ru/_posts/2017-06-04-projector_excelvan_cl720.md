---
layout: post
lang: ru
ref: projector_excelvan_cl720
title: "Бюджетный проектор на дачу Excelvan CL720"
comments: true
tags: [projector]
redirect_from: "/posts/ru/projector_excelvan_cl720/"
---

![](/images/excelvan_cl720_00001.png)

## Комплектующие

Проектор Excelvan CL720 куплен на Aliexpress за $140 (минус [7% кэшбэк](http://epngo.bz/cashback_index/tsvom5)) 
получается $130 или 7.5т.р.
Я взял вариант без TV-тюнера, потому что он уже есть у меня на даче как отдельное устройство.

Экран куплен там же за $11, 60 дюймов, пластик, а не тряпка. Можно было бы побольше, но в помещении, 
где планировал разместить проектор, экран большего размера уже неудобно вешать, к тому же стоимость 
фантастическая, учитывая что у нас цены начинаются с 3 тысяч за самый простенький.

Итого $130 + $11 + $3.69 = примерно 8 тысяч.

Т.е. цена как у маленького телевизора, а диагональ 60 дюймов.

## Доработка 

Проектор шумноват, поэтому я его немного модифицировал - добавил регулятр оборотов на турбину,
охлаждающую матрицу (она шумит больше всего). Использовал валявшийся у меня регулятор Zalman и
поставил напряжение 7 вольт. Регулятор вывел на верхнюю панель, чтобы больше внутрь не лазить.

Также поменял вентилятор, выдувающий воздух из корпуса сбоку, через радиатор светодиода - поставил менее
оборотистый Arctic F7 (Габариты вентилятора 92*25, причем нужно ровно такие, вентилятор не привинчен, 
а прижат кожухом, подразумевающим эти размеры).
Arctic создает не очень громкий высокочастотный шум, и дует довольно слабо, так что рекомендую подобрать 
что-то другое при возможности. Хотя шумность у него, конечно, заметно ниже, чем у штатного вентилятора.

Бесшумным агрегат не стал но исчез напргающий гул взлетающего бомбардировщика, присутствовавший
у не модифицированного проектора.

Температура на радиаторе при этих модификациях повысилась на 3 градуса. Температуру на матрице не проверял,
но пока работает без признаков перегрева.

Также я демонтировал бесполезные динамики и закрыл их отверстия отрезками фильтрующей ткани.

И встроил в корпус [термореле](/en/projector_thermostat.html) - просто потому что за 
[$3.69](https://www.aliexpress.com/item/Min-Microcomputer-Thermostat-Regulator-DC-12V-20A-Digital-Adjustable-Temperature-Controller-50-110C/32782920781.html)
не было разницы - ставить термометр или термореле.
Изначально хотел разрывать им питание светодиода, когда он сильно нагревается, но потом не стал заморачиваться.

## Источник сигнала

[Схема подключения](https://www.draw.io/#Hmasterandrey%2Fschemas%2Fmaster%2Fprojector.xml) 
у меня получилась причудливая, но все эти коробочки вместе с соединительными проводами и пятиметровым 
HDMI-кабелем к проектору в сумме обошлись мне порядка $20.
Не считая, конечно, mica player, стерео усилитель, жесткий диск и телевизор с DVD-плеером ;)

Зато в итоге 
* есть вывод звука на стерео усилитель (купленный на aliexpress за $20) и довольно 
приличную по звуку самодельную акустику
* upscale со старого DVD-проигрывателя, для которого на даче лежат горы CD-дисков
* возможность вывести картинку также на телевизор
* можно переключить вход проектора на TV-тюнер
* все переключения кнопками, не надо объяснять домашним, какой проводочек откуда вынуть и куда воткнуть

[Mica player](https://www.amazon.com/Micca-Full-HD-Portable-Digital-Player/dp/B008NO9RRM/ref=sr_1_1?ie=UTF8&qid=1496475226&sr=8-1&keywords=Mica+player), 
кстати, совершенно замечательное устройство, купленное на amazon и исправно воспроизводящее все мою медиатеку 
при крошечных размерах.