---
layout: post
lang: en
ref: gantt_excel_google_sheets
title: "Free Gantt chart template (like MS Project) for Google sheets or Excel"
comments: true
tags: [gantt, teamlead, google sheets]
---
![](/images/gantt-template.png){:.post-title}

## Project scheduling without MS Project

If you need just a simple Gantt chart but do not want to buy MS Project why
do use just Gogle Sheets or MS Excel?

All you need just a very simple 
[free template](https://docs.google.com/spreadsheets/d/1BYKeYAow1r19hAtiLpTRBtArD4UIKPFw0IRmMh1LJ9g/edit?usp=sharing).

There are no complex formulas and VBA scripts.

## How to setup the Gantt chart for you project

Copy the template from the link above to your Google Drive.

Set your start date in cell `H1`.

Fill your resources in the table `G11:G15`.

Fill you holidays in table `C11:C15`.

That's all!

## How use this free Gantt chart template for Google Sheets(Excel) in your project

Enter ID and name of you task in columns `A` and `B`.

Select Resource from drop-down list in column `G`.

Enter number of days for the task in column `D`.

List all predecessor tasks in column `C` (separate by `,`).

For the task without predecessors will be used the project start date you
 entered to cell`H1`.

For all other tasks the sheet will calculate start date as `max` of 
all predecessors' last dates.

Last dates are calculated using task length in column `D` taking into account 
weekends and holidays you already entered in table `C11:C15`.

## How to add line to Gantt chart

Just copy&past any existing line.

## How to add more resources

Add line in table `G11:G15` and create custom formatting rule for it (select cell 
`H3` and choose in menu `Format` -> `Conditional formatting`).
