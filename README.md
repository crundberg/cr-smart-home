# CR Smart Home
A Raspberry Pi home automation project to control Nexa remote switch.

## Hardware
- Raspberry Pi
- RF Transmitter and Receiver 433 MHz ([Like this one](http://www.kjell.com/se/sortiment/el/elektronik/fjarrstyrning/sandar-och-mottagarmodul-433-mhz-p88905))

## Wiring
Here's a wiring example for a Raspberry Pi 2

![Wiring](http://www.crundberg.se/wp-content/uploads/2015/12/Breadboard.png)

## Install

### Preparations
If you install CR Smart Home on your Raspberry Pi you'll need to extend the swap file from 100 to 300 during the installation. I recommend to change back when the installation is done.
```
sudo nano /etc/dphys-swapfile
CONF_SWAPSIZE=300
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
```

### Install required packages
Install the following packages. The packages pi_switch and pi-switch-python takes a while to install, please be patient.
```
sudo apt-get update
sudo apt-get install mysql-server
sudo apt-get install python-mysqldb
sudo apt-get install apache2
sudo apt-get install php5 php5-curl php5-mysql libapache2-mod-php5
sudo apt-get install python-dev libboost-python-dev python-pip
sudo apt-get install build-essential python-openssl
sudo apt-get install python-w1thermsensor
sudo pip install Flask
sudo pip install flask-httpauth
sudo pip install pi_switch

cd /home/pi/Documents
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build

cd /home/pi/Documents
git clone https://github.com/lexruee/pi-switch-python.git
cd pi-switch-python
sudo python setup.py install

cd /home/pi/Documents
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
```

### Configure webserver
Open configuration file for Apache
`sudo nano /etc/apache2/sites-available/000-default.conf`

Find the row `DocumentRoot /var/www` and replace it with `DocumentRoot /home/pi/Documents/cr-smart-home-webgui`.
Also add the following code.

```
<Directory /home/pi/Documents/cr-smart-home-webgui/ >
  Options Indexes FollowSymLinks
  AllowOverride None
  Require all granted
</Directory>
```

Restart Apache with `sudo /etc/init.d/apache2 restart`

### Install Home-Automation
```
cd /home/pi/Documents
git clone https://github.com/crundberg/cr-smart-home
git clone https://github.com/crundberg/cr-smart-home-webgui

# Import MySQL database
mysql -u root -p mysql < /home/pi/Documents/cr-smart-home/crsmarthome.sql
```

## Start program

### Start manually
Start the program with `sudo python /home/pi/Documents/cr-smart-home/main.py` and start the API with `sudo python /home/pi/Documents/cr-smart-home/API.py`

### Autostart
```
sudo cp /home/pi/Documents/cr-smart-home/autostart/crsmarthome /etc/init.d/
sudo chmod +x /etc/init.d/crsmarthome
sudo update-rc.d crsmarthome defaults
```

### Use it!
Go to `http://your-raspberry-ip/`. Log in with username `admin` and password `admin123`.