Welcome to my repository for education and outreach code.  Below are details about code for tephigram plotting and cglobal warming experiments

# Tephigram Plotting
The tephi_plt code allows users to plot the following isopleths as presented in tephigrams: temperature, potential temperature, wet bulb potential temperature, pressure and water mixing ratio.  To ensure dependecies are installed, the pip setup is recommended:

i) at the command line create a virtual environment in a suitable location (the environment will also contain the tephigram plotting package) using at least python 3: python3 -m venv tephi_env

ii) activate this virtual environment: source tephi_env/bin/activate

iii) ensure pip up to date in this environment: pip install --upgrade pip

# Global Warming Experiment
files for outreach activities

Raspberry Pi stuff:

Installing operating system:
https://www.raspberrypi.org/help/noobs-setup/2/

waterproof temperature sensor: https://www.mouser.es/ProductDetail/Adafruit/381?qs=sGAEpiMZZMu%252bmKbOcEVhFQfi8wYXkauJXVMDuFwOiLnzgYnqoe4nyQ%3d%3d

Raspberry pi stuff: https://cdn-learn.adafruit.com/downloads/pdf/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing.pdf

Get pi connected to wifi via tethering to phone:
https://www.youtube.com/watch?v=x_yhJ_QBfaU

to set up the screen, connect to the internet using above and then follow instructions saved in GWworkshop as RPi_screen_instructions.pdf

http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/

continuous servo motor: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-8-using-a-servo-motor/parts

How to shut down raspebrry pi:
From the command line or a terminal window you can enter the following to do a clean shutdown:
sudo shutdown -h now
Or from the LXDE GUI:
Click the shutdown button (red power button) in the menu bar at the bottom right corner of the screen. Then click shutdown (or logout on newer version, then issue the shutdown command listed above),
Once it says "system halted" you can remove the power cord if needed.

light sensor: https://www.raspberrypi-spy.co.uk/2015/03/bh1750fvi-i2c-digital-light-intensity-sensor/

setting up a new pi with thermometer.py

tether phone with wifi on (https://www.youtube.com/watch?v=x_yhJ_QBfaU):

plug phone into usb port and turn on tether option and wifi

then in terminal: 
sudo dhclient usb0 

sudo apt-get update

set up the mod probe:
sudo nano /boot/config.txt 
at bottom:
# Enable thermometer
dtoverlay=w1-gpio
 
then restart pi:
sudo reboot

reconnect to smartphone:
select tether on phone, then in terminal:
sudo dhclient usb0

Create virtual environment: (http://raspberrypi-aa.github.io/session4/venv.html)

sudo pip3 install virtualenv
virtualenv GWwork --system-site-packages

cd GWwork
source bin/activate


sudo apt-get install tcl-dev tk-dev python-tk python3-tk fbi

python3 -m pip install numpy matplotlib

# check that matplotlib works:
python3 
import matplotlib.pyplot as plt

this tells us if it works.
To make it work, go to the matplotlib backend directory.  To find this do the following: 
sudo apt-get install locate
sudo updatedb
locate matplotlib
which indicates the location of the matplotlib directory,
then cd into the backend directory and open the __init__.py file, inisde here set the backend to ‘TkAgg’, in the latest attempt this was done by setting the name variable

save thermometer.py in GWwork
save a plot by adding (https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/)
plt.savefig(‘TEMP_timeseries.png')
to thermometer.py

view figure with (https://www.cpdforteachers.com/resources/view-images-on-your-raspberry-pi):
gpicview TEMP_timeseries.png

deactivate environment:
deactivate

pins: yellow - 4
red - 3v3
blue - GND

need good connection between ribbon and header
 having gold end of resistor on the 3v3 end works
