# Home-Automation
A Raspberry Pi home automation project to control Nexa remote switch.

## Hardware
- Raspberry Pi
- RF Transmitter and Receiver 433 MHz ([Like this one](http://www.kjell.com/se/sortiment/el/elektronik/fjarrstyrning/sandar-och-mottagarmodul-433-mhz-p88905))

## Wiring
Here's a wiring example for a Raspberry Pi 2

![Wiring](http://www.crundberg.se/wp-content/uploads/2015/12/Breadboard.png)

## Install
### Install required packages
```
sudo apt-get update
sudo apt-get install mysql-server
sudo apt-get install python-mysqldb
sudo apt-get install apache2
sudo apt-get install php5 php5-curl libapache2-mod-php5
sudo apt-get install python-dev libboost-python-dev python-pip
sudo pip install Flask

cd /home/pi/Documents
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build

sudo pip install pi_switch

cd /home/pi/Documents
git clone https://github.com/lexruee/pi-switch-python.git
cd pi-switch-python
sudo python setup.py install
```

### Configure webserver
Open configuration file for Apache
`sudo nano /etc/apache2/sites-available/000-default.conf`

Find the row `DocumentRoot /var/www` and replace it with `DocumentRoot /home/pi/Documents/home-automation-webgui`.
Also add the following code.

```
<Directory /home/pi/Documents/home-automation-webgui/ >
  Options Indexes FollowSymLinks
  AllowOverride None
  Require all granted
</Directory>
```

Restart Apache with `sudo /etc/init.d/apache2 restart`

### Install Home-Automation
```
cd /home/pi/Documents
git clone https://github.com/crundberg/home-automation
git clone https://github.com/crundberg/home-automation-webgui

# Import MySQL database
mysql -u root -p mysql < /home/pi/Documents/home-automation/homeautomation.sql
```

## Start program
Start the program with `sudo python /home/pi/Documents/home-automation/main.py` and start the API with `sudo python /home/pi/Documents/home-automation/API.py`

Go to `http://your-raspberry-ip/`. Log in with username `admin` and password `admin123`.