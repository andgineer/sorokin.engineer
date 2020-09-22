---
layout: post
lang: ru
ref: 2020-03-03-macos_cannon_lbp_1120_driver
title: "Драйвер MacOS для принтера Cannon LaserJet LBP-1120"
comments: true
tags: [macos, printer, ghostscript]
---
![](/images/ghostscript.png){:style="float: left;margin-right: 7px;margin-top: 7px;"}

## Как печатать на принтере, для которого нет драйвера под MacOS?

По случаю я дешево купил лазерный принтер Cannon LaserJet LBP-1120. 

Для него нет драйверов под последние версии MacOS. Но есть драйвера под Windows XP.

Решение напрашивается. 
Установим принтер в виртуальной машине Windows, используя имеющиеся Windows-драйвера. 
Также установим в Windows  виртуальный принтер, который умеет документ PostScript отправить на 
настоящий принтер.
А в MacOS установим Generic PostScript Printer, который отправляет на принтер PostScript. И направим
его на виртуальный принтер в виртуальной Windows.

Такая вот двойная виртуализация. Но давно известно, что для автоматизации работы на пару часов,
любой программист не задумываясь потратит пару дней. Потому что так он избежит двухчасовой работы и 
получит два дня на развлечения 8-)

Итого, наш план:

1. Ставим виртуальный Windows на MacOS (уверен, в будущем вы найдете ему и иные применения)
2. Настраиваем в Windows физический принтер с настоящим драйвером от Cannon
3. Настраиваем в Windows виртуальный принтер, который PostScript документ отправит на физический
принтер
4. Настраиваем в MacOS удаленный принтер с драйвером Generic PostScript Printer, 
направленным на виртуальный принтер Windows

### Виртуальный Windows на MacOS

Нам нужна виртуальная машина и дистрибутив Windows.

#### Виртуальная машина

Я использую [Oracle Virtual Box](https://www.virtualbox.org/wiki/Downloads). Нам нужен дистрибутив
`OS X hosts`.

Ставится легко и не требует специальной настройки.

#### Установка Windows XP

Microsoft все еще хочет денег за Windows XP, но регистрировать ее не обязательно - она 
всего лишь будет вам напоминать о необходимости это сделать.

Так что я советую не ковыряться в заполненных вирусами пиратских развалах, а одеть белые штаны
и скачать дистрибутив с сайта microsoft. Я использовал 
[эту ссылку](https://www.microsoft.com/en-us/download/details.aspx?id=8002) но Microsoft 
славится тем, что ссылки на ее сайте работают недолго. Если ссылка не работает - не паникуйте, 
поищите `Windows XP Mode` в Microsoft Download Center.

Чтобы не тратить время на инсталляцию Windows, я советую вам использовать следующий трюк.


1. Установите в MacOS [The Unarchiver](https://theunarchiver.com/).
2. С его помощью распаковать скачанный вами архив `Windows XP Mode`. 
3. Затем **долнительно** распаковать файл `xpm` в распакованном каталоге `sources/xpminstl64`. 
У него нет расширения, так что явно выберите для него `Open With..` -> `other...` 
-> `The Unarchiver.app`. 
4. В распакованном каталоге надо сделать еще одно магическое действие. Файл `VirtualXPVHD` 
переименуйте в `VirtualXP.VHD`. Подтвердив MacOS, что вы осознаете все возможные ужасные 
последствия столь смелого действия. 

В результате этого трюка мы получаем готовый диск для Oracle Virtual Box с уже установленной Windows 
XP.

Теперь мы создаем новую виртуальную машину в Oracle Virtual Box - нажимаем на синюю иконку new:

![](/images/vmcreate.png)

Выбираем тип Windows XP 32bit. Билл Гейтс обещал, что всем хватит 640Кб, но я все же рекомендую 
выбрать примерно в восемьсот раз больше - 512Мб. 

Выберите `Use an existing virtual hard disk file`. Нажмите на пиктограмку справа с папочкой и 
зеленой стрелкой. 

![](/images/vmcreateproperties.png)

В открывшемся далее окне нажмите на иконку `Add` с зеленым плюсиком и выберите
с таким трудом извлеченный `VirtualXP.VHD`.

![](/images/adddiskimage.png)

Настройте Video Memory 128MB для этой машины.

При ее старте там уже будет установленная Windows XP.

### Физический принтер Windows

Его ставите самым стандартным для Windows образом - кнопка в левом нижнем углу `Start` -> 
`Printers and Faxes` -> в вертикальном меню слева `Add a printer`. Драйвер используем для вашего
принтера. 

Тестовую страницу советую распечатать, чтобы точно знать, что у нас все правильно
установилось.

**Внимание** - имя у принтера не должно включать пробелов и других спец-символов.
Это существенно упростит настройку виртуального принтера. 

Свой я назвал `cannon`.

### Виртуальный принтер Windows

#### GhostScript

Чтобы разобрать PostScript файлы, которые нам будет присылать MacOS, мы будем использовать
бесплатный пакет GhostScript.

Последняя версия у меня не заработала в Windows XP, поэтому я скачивал версию
[9.50](https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/tag/gs950) - файл 
`ghostpcl-9.50-win32.zip`.
Распакуйте его и запустите инсталлятор в Windows.

**Внимание** для упрощения настройки укажите каталог для установки `C:\gs`.

#### Параметры командной строки GhostScript

Чтобы далее при настройке виртуального принтера не писать длиннющую командную строку,
давайте положим все в файлик.

В каталоге `C:\gs` создайте файлик с именем попроще и расширением `rsp` - в моем случае 
`cannon.rsp`. Например, с помощью `Notepad`.
 
В файлике должно быть:

    -IC:\gs\lib;C:\gs\Resource\Font
    -sDEVICE=mswinpr2
    -dNOPAUSE
    -dSAFER
    -sPAPERSIZE=a4
    -sOutputFile="%printer%cannon"

В последней строке после `%printer%` должно быть имя вашего физического принтера.

#### RedMon

Чтобы перехватывать отправляемые на печать файлы PostScript мы будем использовать
[RedMon](http://www.ghostgum.com.au/software/redmon.htm). Я устанавливал версию `1.9`.
Распакуйте архив и запустите инсталлятор в Windows.

#### Настройка виртуального принтера

Нам надо настроить обеспечиваемое RedMon перенаправление так, чтобы расшифрованный PostScript 
отправлялся на настоящий принтер.

Создаем виртуальный принтер. `Start` -> `Printers and Faxes` -> `Add a printer`. 

В мастере настройки выбираем локальный принтер, отключаем 
`Automatically detect..` чтобы зря не ждать, пока оно ничего не найдет. 

На следующем шаге мастера переключаемся на `Create a new port` и выбираем тип `Redirected port`. 

![](/images/redirectprinter.png)

В качестве драйвера я выбрал `Apple LaserWriter`.

![](/images/redirectdriver.png)

Не забудьте расшарить этот принтер (Printer Sharing):

![](/images/printersharing.png)

Завершаем создание,
не надо делать его принтером по умолчанию и не надо печатать тестовую страницу.

Теперь открываем `Properties` свежесозданного принтера, и для выбранного `Redirected port` 
настраиваем командную строку `C:\gs\bin\gswin32c.exe`. Обратите внимание на `c` в имени.

Аргументы должны указывать на созданный нами выше файлик: `@C:\gs\cannon.rsp -`. Обратите 
внимание, что в конце пробел и тире. 

В `Output` выбираем `Copy temporary file to printer`. В `printer` выбираем наш физический принтер. 

Сохраняем кнопкой `Ok`.

![](/images/redirectport.png)

Я назвал принтер `cannonrd`.

Вот теперь стоит напечатать на этом виртуальном принтере тестовую страницу, чтобы убедится,
что у нас все корректно работает - клик правой кнопкой мыши на принтере `Properties` -> `General`
-> `Print Test Page`.

### Удаленный Windows принтер в MacOS
Стандатным образом устанавливаем принтер. `System preferences` -> `Printers & Sacnners`
Нажимаем плюсик внизу списка принтеров.

Выбираем вверху `Windows`, в появившемся списке сеток Windows выбираете нужную сеть, в ней наш 
виртуальный компьютер с Windows, и там должел появиться список принтеров. Выбираете виртуальный
принтер (тот что мы выше назвали `cannonrd`). Драйвер должен выбраться по умолчанию, 
`Generic PostScript Printer`.
 
![](/images/macos_remote_printer.png)

Все - мы можем из MacOS печатать на нашем принтере. Надо только не забывать запускать виртуальную
машину с Windows. Благо она стартует за полсекунды. И можно автоматизировать ее запуск с помощью
Alfred, указав командную строку

    VirtualBoxVM --startvm "<your virtual machine name>"
    