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
import epaper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)
discord.VoiceClient.warn_nacl = False

EP = epaper.epaper("epd2in13_V4")
# GPIO 4, header pin 7
SERVO_PIN = 4
pwm = None
epd = None

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

FONT_FILE = "AtkinsonHyperlegibleMonoVF-Variable.ttf"
FONT15 = ImageFont.truetype(FONT_FILE, size=15, encoding="unic")
FONT15.set_variation_by_name("ExtraBold")
FONT24 = ImageFont.truetype(FONT_FILE, size=24, encoding="unic")
FONT24.set_variation_by_name("ExtraBold")


def main():
    global pwm
    global epd
    pwm = pigpio.pi()
    pwm.set_mode(SERVO_PIN, pigpio.OUTPUT)
    pwm.set_PWM_frequency(SERVO_PIN, 50)

    epd = EP.EPD()
    epd.init()
    display_message("d[•_•]b", "Listening for @doorbell mentions on Discord")

    client.run(os.getenv("DISCORD_BOT_TOKEN"))


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    logger.debug(f"detected message: [{message}] role_mentions: [{message.role_mentions}] mentions: [{message.mentions}] content: [{message.clean_content}]")

    if user_mentioned("doorbell", message) or role_mentioned("doorbell", message):
        logger.info(f"{message.author.name} mentioned @doorbel [{message.clean_content}]")

        with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(ring_bell())
            t2 = tg.create_task(display_message(message.author.nick or message.author.global_name or message.author.name, message.clean_content))
            t3 = tg.create_task(message.add_reaction("🔔"))


def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = [""]
    for word in text.split():
        line = f"{lines[-1]} {word}".strip()
        if font.getlength(line) <= line_length:
            lines[-1] = line
        else:
            lines.append(word)
    return "\n".join(lines)


def role_mentioned(role: str, message: discord.Message) -> bool:
    return any([r.name == role for r in message.role_mentions])


def user_mentioned(username: str, message: discord.Message) -> bool:
    return any([username == u.name for u in message.mentions])


async def display_message(heading: str, body: str):
    epd.init() # wake the display from sleep
    image = Image.new("1", (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), heading, font=FONT24, fill=0)
    time = dt.strftime(dt.now(), "%H:%M")
    line = get_wrapped_text(f"[{time}] {body}", FONT15, epd.height)
    draw.text((0, 35), line, font=FONT15, fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()


async def ring_bell():
    pwm.set_servo_pulsewidth(SERVO_PIN, 500)
    asyncio.sleep(0.3)
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
            EP.epdconfig.module_exit(cleanup=True)
