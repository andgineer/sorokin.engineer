---
layout: post
lang: en
ref: serious_training_endurance_athlets_rob_sleamaker_ray_browning_sheet
title: "Google sheet based on book Serious Training for Endurance Athletes, Rob Sleamaker"
comments: true
tags: [sport ski]
redirect_from: "/posts/en/2019-03-01-serious_training_endurance_athlets_rob_sleamaker_google_sheet/"
---
![](/images/2019-03-02_15-49-22.png){:.post-title}

In this article I describe how to use Google sheet based on book:
* [Роб Слимейкер, Рэй Браунинг Серьезные тренировки для спортсменов на выносливость](https://www.ozon.ru/context/detail/id/142772738/)
* [Rob Sleamaker, Ray Browning Serious Training for Endurance Athletes 2nd](https://www.amazon.com/Serious-Training-Endurance-Athletes-2nd/dp/0873226445) 

How to train using this plan I describe in
 [Serious Training..](/posts/en/serious_training_endurance_athlets_rob_sleamaker_ray_browning.html).

## How to adjust the plan for you
 
The Google documents sheet is public:
[Training plan google sheet](https://docs.google.com/spreadsheets/d/1GcrX_6qRqsKnWwP0Ya3QMR7ztyWaiKZsMRE6p0xxe0E)

To customize plan:
* Enter beginning date into cell `C4` 
* Enter to cell `A2` number of hours that you can use for trainings in one year. 
* If you want the plan to finish early remove some weeks from it. 
Do not remove first weeks of each cycle or if you do please adjust formula in cell `B6`.
When you remove columns google sheet will show warning about changing read-only
range. You can ignore this warning. 

Take into account that on intense phase there are more trainings in a week than on base phase.
So check that and decrease number of hours in year if you see that you do not have so much time
as intense phase will require. 

## Plan weeks details

* You can automate that. For example you can use formula that will place all strength
hours into days that you usually go into gym.
* Take into account you cannot change plan for Sunday.
It just use all hours that you did not plan for other days.
That keeps you from errors.
If you want to change total hours for some weeks - for example for pre-racing
weeks when you want days off. Do not change Sundays - just correct percents for
the week in row `6`.
There are percents for each column in row `6`, but initially they are the same color as
background to keep it more visually simple, because initially all weeks in the cycle are the same.
Just change ink color to black so you can see that digits and correct week that you
want to change.

## Other languages localization

I translated all texts into Russian and English by hand. And use Google Translate for other languages
so you can set any language and have the table in your native language. 

Set language you want in `File - Spreadsheet settings`. 

Unfortunately there are no way to change textx when you change sheet language.
 So I retranslate all textx on each sheet open. Technically for that I wrote random number into cell `B4`.
Ink and background in this cell have the same color so you do not see that but that cause all text to change.

## Changes

Do not treat that plan as something you cannot change.
It's better to adjust the plan as your life dictate than just do not follow it. If you miss the plan for
many days you will loose your motivation and just completely ignore it. Better adjust the plan to be on the 
plan and feel you are good.

And you have to understand that this is just example. Feel free to accomodate it for you personally.
For example for me I increase hours for strength training just because I like it.

## Log training

When you log your training int the plan it will show you how close are you to the plan.
For Saturday and Sunday there are gray digits that show how many hours for each type of training you did 
not log for the week.
Gray digits do not used to calculate week result. When you enter real digids the cells will change color
to black and the sheet will use them to calculate week results.