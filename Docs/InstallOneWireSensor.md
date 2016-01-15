# Install one wire temperature sensor

## Supported sensors
- DS18S20
- DS1822
- DS18B20
- MAX31850K

## Install

1. Connect to Raspberry
  See how to connect the sensor to your Raspberry Pi on [Adafruit](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/hardware).
  I have connected the data to pin 10 instead of pin 4.

2. Enable I2C
  In your terminal run the following command `sudo raspi-config`. Select Advanced Options and I2C. Enable I2C and select to load I2C kernel module by default.
  Reboot after the changes.

3. Edit config file
  Open the config file with `sudo nano /boot/config.txt`

  Paste the following line at the end of the file `dtoverlay=w1-gpio,gpiopin=10`.
  Reboot your Raspberry with `sudo shutdown -r now`.

4. Get the device serial number
  When you have listed the directory in devices you can see the sensors serial number, replace xxxx with it.
  For example `28-0000072f3122`.
  ```
  cd /sys/bus/w1/devices
  ls
  cd xxxx
  cat w1_slave
  ```
  
  If everything works properly, you will see YES on the first line and the temperature in 1/000 degrees °C on the second line.
  ```
  59 01 4b 46 7f ff 07 10 a2 : crc=a2 YES
  59 01 4b 46 7f ff 07 10 a2 t=21562
  ```

5. Add sensor in webgui
  Open webgui and click Add -> Sensors. Fill the form, write 0 on GPIO and enter the serial number from above. For example `0000072f3122`
