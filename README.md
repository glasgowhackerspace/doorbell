# Glasgow Hackerspace Doorbell Bot

A Discord bot to ring a bell in the Glasgow Hackerspace when `@doorbell` is mentioned.
The code is written in Python and designed to run on a Raspberry Pi Zero 2W.

## Hardware setup
 - A [Waveshare 2.13" e-paper display](https://www.waveshare.com/2.13inch-e-paper-hat.htm) is attached directly to the GPIO header on the pi, or as described in their [documentation](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi).
 - An [SG90 servo motor](http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf) is wired to 5v, GND, and [pin 7 (GPIO 4)](https://pinout.xyz/pinout/pin7_gpio4/) on the Pi. If the e-paper display is attached to the front of the GPIO header, then these connections must be made on the rear.
 - A push-button is wired between [pin 5 (GPIO 3)](https://pinout.xyz/pinout/pin5_gpio3/) and GND.

`.stl` files for a frame to mount the bell, and a stand to mount the servo are included under the [3d_files](./3d_files) directory. Everything was mounted into an [IKEA VÄSTANHED](https://www.ikea.com/gb/en/p/vaestanhed-frame-black-00479218/) photo frame.

## Software Setup
Deploying this project to a pi has been automated with Ansible. See [deploy.md](./ansible/deploy.md).

The bot requires a token to access the Discord API.
You need a Discord dev account to generate this token: https://discord.com/developers/
Once generated, these details should be entered into a `.env` file following the format of the [.env.template](.env.template) file in this repo.

If you don't want to use Ansible the following steps should achieve the same thing.

### Manual setup
```
# create a new user, add it to the required groups
useradd -m ding
usermod -a -G gpio,spi ding
# clone the code into the ding users home directory
su ding
cd /home/ding
git clone --recurse-submodules https://github.com/glasgowhackerspace/doorbell.git
# set up the python environemnt and dependencies
cd doorbell
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
# configure the services
su <your normal username>
pigpiod
ln -s /home/ding/doorbell/doorbell_bot.service /etc/systemd/system/doorbell_bot.service
systemctl enable doorbell_bot
systemctl start doorbell_bot
# if you want the shutdown button to work
echo "dtoverlay=gpio-shutdown" | sudo tee -a /boot/firmware/config.txt
reboot
```
