#!/usr/bin/env python
from datetime import datetime as dt
import logging
import os
import sys
import time
# for discord bot
import discord
import dotenv
# to control servo motor
import pigpio
# to write to e-paper display
from PIL import Image,ImageDraw,ImageFont
sys.path.append("e-Paper/RaspberryPi_JetsonNano/python/lib/")
from waveshare_epd import epd2in13_V4

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# GPIO 4, header pin 7
SERVO_PIN = 4
pwm = None
epd = None

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

FONT_FILE = 'AtkinsonHyperlegibleMonoVF-Variable.ttf'
FONT15 = ImageFont.truetype(FONT_FILE, size=15, encoding='unic')
FONT15.set_variation_by_name('ExtraBold')
FONT24 = ImageFont.truetype(FONT_FILE, size=24, encoding='unic')
FONT24.set_variation_by_name('ExtraBold')


def main():
    global pwm
    global epd
    pwm = pigpio.pi()
    pwm.set_mode(SERVO_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(SERVO_PIN, 50)

    epd = epd2in13_V4.EPD()
    epd.init()
    display_message("d[•_•]b", "Listening for @keyholder mentions on Discord")

    client.run(os.getenv("DISCORD_BOT_TOKEN"))


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    keyholder_mentioned = any([role.name == "keyholder" for role in message.role_mentions])
    if keyholder_mentioned:
        logger.info(f"{message.author.name} mentioned @keyholder [{message.clean_content}]")

        ring_bell()
        display_message(message.author.nick or message.author.name, message.clean_content)
        await message.add_reaction("🔔")


def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return '\n'.join(lines)


def display_message(heading: str, body: str):
    epd.init()
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), heading, font=FONT24, fill=0)
    time = dt.strftime(dt.now(), "%H:%M")
    line = get_wrapped_text(f"[{time}] {body}", FONT15, epd.height)
    draw.text((0, 35), line, font=FONT15, fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()


def ring_bell():
    pwm.set_servo_pulsewidth(SERVO_PIN, 500)
    time.sleep(0.3)
    pwm.set_servo_pulsewidth(SERVO_PIN, 2500)


if __name__ == "__main__":
    try:
        main()
    finally:
        logger.info("running cleanup")
        if pwm:
            pwm.set_PWM_dutycycle(SERVO_PIN, 0)
            pwm.set_PWM_frequency(SERVO_PIN, 0)
        if epd:
            display_message("(-.-) Zzz", "Sleeping")
            epd2in13_V4.epdconfig.module_exit(cleanup=True)
