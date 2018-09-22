---
layout: post
lang: en
ref: iot_calendar_synology
title: "IoT (Internet of things) events calendar on Kindle"
comments: true
tags: [amazon dash button, python, docker, synology]
---

![](/images/dashboard.png)

If you want to see some calendar data (for example from
[Your DIY smart wifi button](/posts/en/amazon_dash_button_hack.html)
you can create image of it with help of my application described below.

I use old Amazon Kindle on wall to show the image.

Of cause you can use just PC or tablet PC. For example Amazon Fire HD 7 
is only $49 ($39 on sale), or simple Chinese table PC for the same money.
But with tablet PC you have to solve problem how to keep it charged and do not degrade battery.
Kindle works for weeks on one charge.

## Set up

Set up `settings.json` and `buttons.json`, as described in 
[Smart wifi button install](/posts/en/amazon_dash_button_hack_install.html).

In `dashboards` describe your dashboard. This is image `empty_image` for days without event (i.e.
mooch days). Also you can have absenties in your calendar (events described in
`absents`).
For example if you have in `absent` element with `summary` as `Sick`, and in your calendar
exists event with such name, during this event instead of `empty_image` will be image from
this element.

To see weather data on the calendar (if you already have Kindle on wall, why not show weather as well),
you should get your latitude and longitude from [Google maps](https://support.google.com/maps/answer/18539?co=GENIE.Platform%3DDesktop&hl=en).
And place them into `latitude` and `longitude` parameters in `settings.json`.

Also you need
[openweathermap API key](https://home.openweathermap.org/users/sign_up) and place it into
`openweathermap_key.json` with other setting files (you can change path to the file, if you want, 
in `openweathermap_key_file_name` parameter of `settings.json`).

## Synology set up

Add Docker image from URL `https://hub.docker.com/r/masterandrey/docker-iot-calendar/`:

![](/images/dash_synology_docker_image.png)
![](/images/dash_synology_docker_url.png)

After downloading the image you can create Docker container from it.

Instead of the instructions below you can just import 
[my container settings](https://github.com/masterandrey/docker-amazon-dash-button-hack/tree/master/synology).
The only specific thing that they assume - that you place [secrets and settings](https://github.com/masterandrey/docker-amazon-dash-button-hack/tree/master/amazon-dash-private)
in folder `docker/amazon-dash-private`.
![](/images/synology_import_settings.png)

Or you can do all that by youself - see instructions below.

Double click the image to start container create wizard.

In `Advanced settings` -> `Volume` add folder `/amazon-dash-private` with secrets and settings.
Download [examples](https://github.com/masterandrey/docker-amazon-dash-button-hack/tree/master/amazon-dash-private) 
of this files and place them in any place on Synology. 

In my case this is folder `docker/amazon-dash-private` on Synology volume:

![](/images/dash_synology_docker_volume.png)

In `Port Settings` connect port application `4444` to host.

![](/images/calendar_synology_docker_port.png)

And in Synology `Package Center` switch off auto-update for Docker.
Because it will stop all running containers after auto-update and your Docker applications suddenly stop to work.
So better to update Docker package manually and start the container after that.

![](/images/dash_synology_docker_autoupdate.png)

## Not Synology

Place `amazon-dash-hack.json` and other files in folder 
`amazon-dash-private` and add to your docker command line:

    -v $PWD/amazon-dash-private:/amazon-dash-private:ro
    
$PWD instructs Docker to search `amazon-dash-private` folder in the same folder 
where you start Docker.
If you place folder somewhere else you should change that path.

## IoT (Internet of things) events calendar

Open in browser `<your server>:4444` and you will see all dashboard that configured in `settings.json`
(`dashboards`).

`<your server>:4444?b=<dashboard>` - black and white version rotated version (for Kindle),
`<your server>:4444?b=<dashboard>&style=seaborn-talk&rotate=0` - colour unrotated version. 

The page auto-updates image.

The image is at `<ваш сервер>:4444/dashboard.png?b=<dashboard>`.
 
You can use 
[matplotlib styles](https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html).
For example, `<your server>:4444/dashboard.png?b=<dashboard>&style=seaborn-talk`.

Also you can switch off handwritten sub-stype with `xkcd=0` (this style is used in combination
with main style and change a number of visualization parameters).

If you do not like icons that I ship with the application, you can get another for example from 
[Noun Project](https://thenounproject.com).