---
lang: ru
layout: post
comments: true
ref: text_processing_from_birds_eye_view
title: "Взгляд на текст с высоты птичьего полета"
tags: [pascal, regexp, delphi]
---

Эту статью я опубликовал на delphi3000.com, но сайт прожил недолго..

![](/images/bookshelves.png){:.post-title}

Вам необходимо извлечь данные о погоде со страницы, или курсы конвертации валют,
или email-ы, или еще что-то плохо формализуемое?
Или вам надо почистить кривые данные из старой БД?
Или вам необходимо проверить ввод пользователя с точки зрения корректности?

Вариатов сделать это немало.

Есть полноразмерные парсеры.
Можно написать специализированный.
Например, чтобы проверить формат email, надо что-то поизощреннее, чем

{% highlight pascal %}
p := Pos ('@', email);
if (p > 1) and (p < length (email))
  then ...
  {% endhighlight %}

Чтобы просто испугаться можно посмотреть например на это:
[Extended E-mail Address Verification and Correction](http://delphi-kb.blogspot.ru/2005/11/extended-e-mail-address-verification.html)).
Представьте, что вам надо это осознать и отладить.

Регулярные выражения (regular expression) позволяют нам посмотреть на текст как бы
с высоты птичьего полета.
Вы не пишете код, для проверки текста, вы описываете текст, как он с вашей точки зрения,
должен выглядеть.

К сожалению, в Delphi нет компонента TRegularExpression.

Поэтому мне и пришлось написать свой вариант - [TRegExpr](http://regexpstudio.com).

## Пример 1 Простая проверка e-mail

{% highlight pascal linenos %}
if ExecRegExpr ('[\w\d\-\.]+@[\w\d\-]+(\.[\w\d\-]+)+', email)
    then ... gotcha! e-mail is valid ...
{% endhighlight %}

И добавьте TRegExpr в оператор uses вашего модуля.

## Пример 2 Простой поиск текста, похожего на номера телефонов
Допустим, мы ищем номера только Санкт-Петербурга (код города 812).

{% highlight pascal linenos %}
procedure ExtractPhones (const AText : string; APhones : TStrings);
begin
  with TRegExpr.Create do try
     Expression := '(\+\d *)?(\((\d+)\) *)?(\d+(-\d*)*)';
     if Exec (AText) then
      REPEAT
        if Match [3] = '812'
         then APhones.Add (Match [4])
      UNTIL not ExecNext;
    finally Free;
   end;
end;
{% endhighlight %}

Тогда из текста
{% highlight html %}
"Привет !
Позвони мне на работу (812)123-4567 или домой +7 (812) 12-345-67
жду .."
{% endhighlight %}

Мы извлечем
{% highlight html %}
APhones[0]='123-4567'
APhones[1]='12-345-67'
{% endhighlight %}

## Пример 3 Извлечение курсов обмена со страницы Центробанка

Создайте в Delphi новый проект и поместите на форму компоненты TBitBtn, TLabel и TNMHTTP.

В обработчик сообщения BitBtn1 OnClick добавьте:

{% highlight pascal linenos %}
procedure TForm1.BitBtn1Click(Sender: TObject);
const
  Template = '(?i)Ioeoeaeuiue eo?n OA ii aieea?o'
   + '.*Aaoa\s*Eo?n\s*Eo?n iie.\s*Eo?n i?ia. [^<\d]*'
   + '(\d?\d)/(\d?\d)/(\d\d)\s*[\d.]+\s*([\d.]+)';
begin
  NMHTTP1.Get ('http://win.www.citycat.ru/finance/finmarket/_CBR/');
  with TRegExpr.Create do try
     Expression := Template;
     if Exec (NMHTTP1.Body) then begin
       Label1.Caption := Format ('Курс российского рубля %s.%s.%s: %s',
         [Match [2], Match [1], Match [3], Match [4]]);
      end;
    finally Free;
   end;
end;
{% endhighlight %}

Теперь при нажатии на BitBtn1, программа соединиться с сайтом Центробанка и покажет вам текущие курсы валют.

#### Заключение
"Освободи свой разум" ((c) Матрица ;)) текст не обязательно анализировать
процедурным кодом.
Лучше опишите его на языке регулярных выражений и тем самым избавьтесь от
нудной работы!

[Описание синтаксиса регулярных выражений TRegExpr](http://regexpstudio.com/regexp_syntax_ru/)
