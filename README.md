# Glasgow Hackerspace Doorbell Bot

A Discord bot to ring a bell in the Glasgow Hackerspace when the `@keyholder` role is mentioned.
The code is written in Python and designed to run on a Raspberry Pi.

## Hardware setup
An [SG90 servo motor](http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf) is wired to 5v, GND, and pin 11 (GPIO 17) on the Raspberry Pi.
![Raspberry Pi GPIO Pinout](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png?hash=df7d7847c57a1ca6d5b2617695de6d46)


## Software Setup
```
$ git clone https://github.com/glasgowhackerspace/doorbell.git
$ cd doorbell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip3 install -r requirements.txt
```
1. Clone the repo to a Raspberry Pi.
2. Set up a Python virtual environment.
3. Activate the virtual environment.
4. Install the dependencies.

The bot requires a token to access the Discord API.
You need a Discord dev account to generate this token: https://discord.com/developers/

Once generated, these details should be entered into a `.env` file following the format of the [.env.template](.env.template) file in this repo.

Finally run the bot:
```
$ python3 main.py
```
