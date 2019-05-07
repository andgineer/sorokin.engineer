---
layout: post
lang: en
ref: text_processing_from_birds_eye_view
comments: true
title: "Regular expressions: Text processing from bird's eye view"
tags: [pascal, regex, delphi]
redirect_from: "/posts/en/text_processing_from_birds_eye_view/"
---

This article was published on delphi3000.com, but now the site is dead.

![](/images/bookshelves.png){:.post-title}

Do you want to write Delphi/Pascal program for extracting weather forecast or 
currency rates or e-mails or whatsoever you want from HTML-pages, e-mails or o
ther unformatted source? Or do you need to import data into your database from 
old DB's ugly export format? Or you want just ensure that the e-mail user entered is 
syntaxically correct one?

There are two ways.

The traditional one - you must make full featured text parser. This is an awful peace 
of work!
For example, try to implement rules how to recognize e-mail address - simple code like

{% highlight pascal linenos %}
p := Pos ('@', email);
if (p > 1) and (p < length (email))
  then ...
{% endhighlight %}

don't filter many common errors, for example, users frequently forget enter domain-part
of e-mail, you'll need much more complex code (just read the big article
[Extended E-mail Address Verification and Correction](http://delphi-kb.blogspot.ru/2005/11/extended-e-mail-address-verification.html)).
Just think about writing and debugging this code.

The second way - look at the text from bird's eye view with help of regular expressions 
engine. You don't write the check processing routine, you just describe how regexp 
engine must do it for you. Your application will be implemented very fast and will 
be robust and easy to change!

Unfortunately, Delphi component palette contains no TRegularExpression component.

But there are some third-party implementations, for example my [TRegExpr](http://regexpstudio.com).

## Example 1 How to check e-mail address syntax.
Just write

{% highlight pascal linenos %}
if ExecRegExpr ('[\w\d\-\.]+@[\w\d\-]+(\.[\w\d\-]+)+', email)
    then ... gotcha! e-mail is valid ...
{% endhighlight %}

Do not forget to add TRegExpr into uses section of the unit.

## Example 2 How to extract phone numbers from unformatted text (web-pages, e-mails, etc).
For example, we need only St-Petersburg (Russia) phones (city code 812).

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

For the input text
{% highlight html %}
"Hi !
Please call me at work (812)123-4567 or at home +7 (812) 12-345-67
truly yours .."
{% endhighlight %}

this procedure returns
{% highlight html %}
APhones[0]='123-4567'
APhones[1]='12-345-67'
{% endhighlight %}

## Example 3 Extracting currency rate from Russian Bank web page.

Create new project and place at the main form TBitBtn, TLabel and TNMHTTP components.

Add following code as BitBtn1 OnClick event handler (don't mind Russian letter - they 
need for Russian web-page parsing):

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
       Label1.Caption := Format ('Russian rouble rate %s.%s.%s: %s',
         [Match [2], Match [1], Match [3], Match [4]]);
      end;
    finally Free;
   end;
end;
{% endhighlight %}

Now, then you click at the BitBtn1, programm connects to specified web-server and 
extract current rate.

Conclusion
"Free your mind" ((c) The Matrix ;)) and you'll find many other tasks there regular 
expressions can save 
you incredible amount of stupid coding work !

[Regular expressions syntax explained](https://regex.masterandrey.com/regex)

