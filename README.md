# Raspberry Pi & Arduino - Serial connection
**Erasmus+ SmartHouse Project**

This repository was created for Eramsmus+ project. It will let you create Raspberry Pi Flask web server from which through USB (serial) you can control/recieve and send data to the Arduino and display them on the web page in real-time. This is main functional part of the project and there are several possibilities how to expand it.

## Annotation
This code was created by Czech group as part for Erasmus+ project. The goal of the project was constructing a functional model of Smart house, which can be built in every country in Europe. Therefore, we had to have in mind every weather condition which can appear. We collaborated with 5 other countries -  Poland, France, Spain and Germany. Each country which participated had assigned work in the project. I have chosen this project because it is one of the most interesting projects which I have participated on in our school and as a Erasmus+ project it will have an impact on an current situation and answer real problems. 
We the Czech IT group, developed “smart” part of the project, which controls the whole house, for example controlling and stabilizing temperature and humidity, light control and garden watering system. My part in this project was to create and configure core computer and connect sensors to it, therefore it could gather actual information and display them on the webpage (which was made by my co-worker Adam Skokan) in real time. Additionally, I added access point (Wi-Fi), which can be connected to a user and control the house without a cable. Patrick Tsidina, who is my co-worker, is programming sensors and their automation. 
My contribution to the project can be divided into four parts, which are completely documented on GitHub repository, which I created for this purpose. The majority of work in the first part of the project was about gathering information and choosing the best possible solution for the task. There were multiple possibilities for approaching the right solution. After many attempts to get the best result and researching multiple frameworks, for example Blynk and Home Assistant, I decided to fully develop my own application in python with help of Flash framework and Jijja2 templating system. 
In a second part, I connected the core computer to the Arduino and created demo website, with two buttons for led diode control (lights demo) and value, which is generated for demo purpose on Arduino as temperature value, from the Arduino computer. I also chose and ordered computers for the project.
In third part I extended website with input for numbers, which let the user set their favourite temperature. After the form is submitted, the request is sent to the Arduino and Arduino will sent it back and it as actual user set temperature value. This was created to demonstrate serial transfer. I also added database and JSON API for storing and accessing data, so Adam can use them in a graph.
In the fourth part, I spent the majority of time consulting and discussing Adam’s and Patrick’s parts, but I also fully installed my software on all 5 computers and wrote the documentation and installation guide.
In conclusion I sincerely believe that my part of the project is well accomplished. Everything is documented on GitHub as I mentioned before, and my work can be easily demonstrated there. The Erasmus+ project was created under the European Union. I hope that some relevant answers will come out of our solution and If not, it can be helpful just for regular users of GitHub who can use it as Home management system.

## Installation
### Raspberry Pi
#### Downloading on SD card
1.  Download [Etcher](https://www.balena.io/etcher/) and install it on your computer.
2.  Download [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) from the official Raspberry Pi.
3.  Plug your SD card into computer.
4.  Open Etcher and select from your hard drive the Raspberry Pi .img or .zip file you wish to write to the SD card.
5.  Select the SD card you wish to write your image to.
6.  Review your selections and click 'Flash!' to begin writing data to the SD card.
7.  Plug your SD card into Raspberry Pi connect HDMI, keyboard and power cable.

#### First boot
1.  Login with these credentials - Login is "pi" and password is "raspberry". (Password cannot be seen)
2.  Configure raspberry with command `sudo raspi-config`.
3.  Go to `Advanced options` and `Expand filesystem` and 
4.  Go to `Change user password` for changing default password and confirm with OK. Write your password 2 times and confirm with OK.
5.  Go to `Network settings` and `Hostname` for changing hostname. Acknowledge the conventions and confirm by pressing OK. Write your hostname and confirm again.
6.  Setup Wi-Fi or connect Ethernet cable. (I haven't programmed that path yet)
7.  Click on `Finish` on the bottom.
8.  Update Raspberry Pi with command `sudo apt-get update && upgrade`. Type `Y`If needed.
9.  Reboot Raspberry Pi using command `sudo reboot -t 0`

#### Installation of packages
1.  Install necessary packages with command `sudo apt install apache2 libapache2-mod-wsgi python-setuptools python-serial python-flask`. Type `Y` If needed.

##### SSH
1.  Enable SSH with command `sudo systemctl enable ssh` and `sudo systemctl start ssh`.
You should be able to connect through console from your computer connected to the same network. You can connect on iOS through console with `SSH` command and on Windows through PuTTy. You can find your IP in your router settings.

##### Samba
1.  Install necessary packages with command `sudo apt-get install samba samba-common-bin`. Type `Y` If needed.
2.  Configure samba by opening `sudo nano /etc/samba/smb.conf` and set up properties. (optional).
3.  Add samba user and setup password for it - `sudo smbpasswd -a pi`. (pi is the password)
4.  Restart the Samba utility - `sudo service smbd restart`.

#### Core files 
1.  Clone this repository `git clone https://github.com/TheLupp/EraRaspArd28.git`.

2.  Create web server folder `sudo mkdir /var/www/server`.

3.  Copy files from cloned repository into server folder - `sudo cp -a EraRaspArd28-master/. /var/www/server/`.

4.  Delete previous Apache config - `sudo a2dissite 000-default`.

5.  Configure Apache with new config bellow over here `sudo nano /etc/apache2/sites-available/`.

          <VirtualHost *>
            WSGIDaemonProcess server user=pi group=www-data threads=5
            WSGIScriptAlias / /var/www/server/server.wsgi

            <Directory /var/www/server>
              WSGIProcessGroup server
              WSGIApplicationGroup %{GLOBAL}
              Order allow,deny
              Allow from all
              #Require all granted
            </Directory>
           </VirtualHost>

6.  Enable mod_wsgi module - `sudo a2enmod wsgi`.

7.  Reload Apache - `sudo systemctl restart apache2`.

#### Access point 
1.  Install necessary packages with command `sudo apt-get -y install hostapd dnsmasq`. Type `Y` If needed.

2.  Edit the dhcpcd file - `sudo nano /etc/dhcpcd.conf` and add `denyinterfaces wlan0` at the bottom and save.

3.  Edit interfaces file - `sudo nano /etc/network/interfaces` and add at bottom this:

        auto lo
        iface lo inet loopback

        auto eth0
        iface eth0 inet dhcp

        allow-hotplug wlan0
        iface wlan0 inet static
            address 192.168.28.1
            netmask 255.255.255.0
            network 192.168.28.0
            broadcast 192.168.28.255        

4.  Configure hostpd `sudo nano /etc/hostapd/hostapd.conf`.

        interface=wlan0
        driver=nl80211
        ssid=SmartHouse28
        hw_mode=g
        channel=6
        ieee80211n=1
        wmm_enabled=1
        ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]
        macaddr_acl=0
        auth_algs=1
        ignore_broadcast_ssid=0
        wpa=2
        wpa_key_mgmt=WPA-PSK
        wpa_passphrase=erasmus28
        rsn_pairwise=CCMP

5.  Configure path to hostpd `sudo nano /etc/default/hostapd`. Find the line `#DAEMON_CONF=""` and replace it with: `DAEMON_CONF="/etc/hostapd/hostapd.conf"`.

6.  Configure Dnsmasq for automatically assigning IP addresses

     Backup current dnsmasq - `sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak` 
     Edit `sudo nano /etc/dnsmasq.conf` and add into blank file this:
     
        interface=wlan0 
        listen-address=192.168.28.1
        bind-interfaces 
        server=8.8.8.8
        domain-needed
        bogus-priv
        dhcp-range=192.168.28.100,192.168.28.200,24h
        
7.  Reboot the Raspberry PI - `sudo reboot`.

#### NAT
1.  Edit the sysctl file - `sudo nano /etc/sysctl.conf` and look for the line `#net.ipv4.ip_forward=1`, and uncomment it by deleting the `#`.

2.  Bunch of commands - blah blah blah

        sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE  
        sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
        sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
        sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

3.  Edit the rc.local file - `sudo nano /etc/rc.local` Just above the `exit 0` line (which ends the script), add the following: `iptables-restore < /etc/iptables.ipv4.nat` and `sudo reboot`.

### Arduino 
1.  Download [Arduino IDE](https://www.arduino.cc/en/Main/Software) and install it on your computer.
2.  Upload `arduino-ir.ino` to your board.
3.  Connect Arduino to Raspberry through Serial/USB cable.

**YOU ARE READY!**

## ERRORS
### Internal Server Error 

In order to successfully start Flask server on Raspberry Pi you need to connect with USB/Serial Arduino. 

*  Solution 1. - Delete `*.pyc` (with c!) -  `sudo rm *.pyc` & Delete database.jsou - `sudo rm database.json` and reboot.
*  Solution 2. - If you are not using original Arduino go to pyduino.py (`sudo nano pyduino.py`) and change connection from `/dev/ttyACM0` to `/dev/ttyAMA0` and save + reboot.

      

## URLs
* Raspberry Pi Official Image of Raspbian Stretch Lite - [](https://www.raspberrypi.org/downloads/raspbian/)
* Official Arduino software - [https://www.arduino.cc/en/Main/Software](https://www.arduino.cc/en/Main/Software)
