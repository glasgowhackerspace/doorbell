# Glasgow Hackerspace Doorbell Bot

A Discord bot to ring a bell in the Glasgow Hackerspace when the `@keyholder` role is mentioned.
The code is written in Python and designed to run on a Raspberry Pi Zero 2W.

## Hardware setup
An [SG90 servo motor](http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf) is wired to 5v, GND, and pin 7 (GPIO 4) on the Pi.
![Raspberry Pi GPIO Pinout](https://www.etechnophiles.com/wp-content/uploads/2021/11/Raspberry-Pi-Zero-2W-GPIO-Pinout.jpg)

A [Waveshare 2.13" e-paper display](https://www.waveshare.com/2.13inch-e-paper-hat.htm) is also attached as described in their [documentation](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi).

## Software Setup
```
$ git clone --recurse-submodules https://github.com/glasgowhackerspace/doorbell.git
$ cd doorbell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
$ sudo pigpiod
```
1. Clone the repo to a Raspberry Pi.
2. Set up a Python virtual environment.
3. Activate the virtual environment.
4. Install the dependencies.
5. Start the pigpio deamon.

The bot requires a token to access the Discord API.
You need a Discord dev account to generate this token: https://discord.com/developers/

Once generated, these details should be entered into a `.env` file following the format of the [.env.template](.env.template) file in this repo.

Finally run the bot:
```
$ python3 main.py
```
