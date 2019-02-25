# Raspberry Pi & Arduino - Serial connection
**Erasmus+ SmartHouse Project**

This repository was created for Eramsmus+ project. It will let you create Raspberry Pi FLask web server from which through USB (serial) you can control/recieve and send data to the Arduino and display them on the web page in real-time. This is main functional part of the project and there are several possiblities how to expand it.

# Annotation
This code was created by Czech group as part for Erasmus+ project. The goal of the project was constructing a functional model of Smart house, which can be built in every country in Europe. Therefore, we had to have in mind every weather condition which can appear. We collaborated with 5 other countries -  Poland, France, Spain and Germany. Each country which participated had assigned work in the project. I have chosen this project because it is one of the most interesting projects which I have participated on in our school and as a Erasmus+ project it will have an impact on an actual situation and answer real problems. 
We, as Czech IT group, developed “smart” part of the project, which controls a whole house, for example controlling and stabilizing temperature and humidity, light control and garden watering system. My part in this project was to create and configure core computer and connect sensors to it, therefore it can gather actual information and display them on the webpage (which was made by my co-worker Adam) in real time. Additionally, I added access point (Wi-Fi), which can be connect to a user and control the house without a cable. Patrick, who is my co-worker, is programming sensors and their automation. 
My contribution to the project can be divided into four parts, which are completely documented on GitHub repository, which I created for this purpose. The majority of work in the first part of the project was about gathering information and choosing the best possible solution for the task. There were multiple possibilities for approaching the right solution. After many attempts to get the best result and researching multiple frameworks, for example Blynk and Home Assistant, I decided to fully develop my own application in python with help of Flash framework and Jijja2 templating system. 
In a second part, I connected the core computer to the Arduino and created demo website, with two buttons for led diode control (lights demo) and value, which is generated for demo purpose on Arduino as temperature value, from the Arduino computer. I also chose and ordered computers for the project.
In third part I extended website with input for numbers, which let the user set their favourite temperature. After the form is submitted, the request is sent to the Arduino and Arduino will sent it back and it as actual user set temperature value. This was created to demonstrate serial transfer. I also added database and JSON API for storing and accessing data, so Adam can use them in a graph.
In the fourth part, I spent the majority of time consulting and discussing Adam’s and Patrick’s parts, but I also fully installed my software on all 5 computers and wrote the documentation and installation guide.
In conclusion I sincerely believe that my part of the project is well accomplished. Everything is documented on GitHub as I mentioned before, and my work can be easily demonstrated there. The Erasmus+ project was created under European. I hope that some relevant answers will come out of our solution and If not, it can be helpful just for regular users of GitHub who can use it as Home management system.

# Installation
## Raspberry Pi
### Downloading on SD card
1. Download [Etcher](https://www.balena.io/etcher/) and install it on your computer.
2. Download [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) from the official Raspberry Pi.
3. Plug your SD card into computer.
3. Open Etcher and select from your hard drive the Raspberry Pi .img or .zip file you wish to write to the SD card.
4. Select the SD card you wish to write your image to.
5. Review your selections and click 'Flash!' to begin writing data to the SD card.
6. Plug your SD card into Raspberry Pi connect HDMI, keyboard and power cable.

### First boot
1. Login with these credentials - Login is "pi" and password is "raspberry". (Password cannot be seen)
2. Configure raspberry with command `sudo raspi-config`.
3. Go to `Advanced options` and `Expand filesystem` and 
4. Go to `Change user password` for changing default password and confirm with OK. Write your password 2 times and confirm with OK.
4. Go to `Network settings` and `Hostname` for changing hostname. Acknowledge the conventions and confirm by pressing OK. Write your hostname and confirm again.
5. Setup Wi-Fi or connect Ethernet cable. (I haven't programmed that path yet)
6. Click on `Finish` on the bottom.
7. Update Raspberry Pi with command `sudo apt-get update && upgrade`. Type `Y`If needed.
8. Reboot Raspberry Pi using command `sudo reboot -t 0`

### Installation of packages
1. Install necessary packages with command `sudo apt install apache2 libapache2-mod-wsgi python-setuptools python-serial python-flask`. Type `Y` If needed.

#### SSH
1. Enable SSH with command `sudo systemctl enable ssh` and `sudo systemctl start ssh`.
You should be able to connect through console from your computer connected to the same network. You can connect on iOS through console with `SSH` command and on Windows through PuTTy. You can find your IP in your router settings.
#### Samba
1. Install necessary packages with command `sudo apt-get install samba samba-common-bin`. Type `Y` If needed.
2. Configure samba by opening `sudo nano /etc/samba/smb.conf` and set up properties. (optional).
3. Add samba user and setup password for it - `sudo smbpasswd -a pi`. (pi is the password)
4. Restart the Samba utility - `sudo service smbd restart`.

# URLs
Raspberry Pi Official Image - https://www.raspberrypi.org/downloads/raspbian/
Raspbian Stretch Lite
