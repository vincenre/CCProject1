# CCProject1

## Web Service

This is an API to display weather data from a Custom API as well as from a Weather API

I have used Open Weather Map API

I have also used Bootstrap for UI and JQuery to make AJAX calls to my python Webservice

I have used CanvasJS to plot the graph

## Docker

I have made a DockerFile and a requirements for listing out the packages needed by my webservice

I have bundled the docker image in a tar file and stored it google drive

I have also uploaded in on the docker hub

You just need to use the following two commands to pull the image and start the webservice

docker pull roshanvin4u/dockerprj

docker run -id -p 8081:80 roshanvin4u/dockerprj 

To check the web service, point to your docker ip followed by the 8081 port

for example if my docker ip is 192.168.99.100 then to access my website, I need to go to http://192.168.99.100:8081
