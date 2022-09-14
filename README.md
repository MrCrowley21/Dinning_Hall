## Dinning Hall
This repository, _Dinning Hall_, represents a part of a bigger project of a restaurant simulation,
performed as laboratory work during the _Network Programming_ course. The another component of
this project, _Kitchen_, can be found following this 
[link](https://github.com/MrCrowley21/Kitchen.git). \
!**Note** the fact that this version of README file is not final and will be modified  further.\
First, to run the project into a docker container, perform the following commands:
````
$ docker build -t dinning_hall_image . 
$ docker run --net restaurant_network -p 8000:8000 --name dinning_hall_container dinning_hall_image
````
The first line will create an image of our project, while the next one - run project inside 
the created container. \
**NOTE** that this container should be run after the network is created (explained in the
_Kitchen_) and the _Kitchen_ container is run.
The _Dinning Hall_ project consists of:
* a _README_ file with explanations;
* a _Dockerfile_ to assemble the image;
* a _requirements.txt_ file that contains all necessary libraries the program to run properly;
* a _server.py_ file that starts the server and program execution;
* a _config.py_ file that contains defined constants and global variables;
* a _dinning_hall_data_ map that contains json files with cooks and food items from menu;
* a _Components_logic_ map that contains classes that defines each project entity behaviour.

For this moment, for more explanation regarding the code itself, please take a look at the comments 
that appears there.
