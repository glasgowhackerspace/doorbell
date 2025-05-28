import discord
import dotenv
import os
import RPi.GPIO as gpio
from time import sleep

SERVO_PIN = 11
pwm = None

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return


    keyholder_mentioned = any([role.name == "keyholder" for role in message.role_mentions])
    if keyholder_mentioned:
        if (name := message.author.nick) is None:
            name = message.author.name
        print('\007', end="") # terminal bell sound
        print(f"detected message mentioning keyholder from: {message.author.name} ({name})")
        print(f"    [{message.content}]")

        wiggle()
        await message.channel.send(f"keyholder was mentioned in this message from {name}: [{message.content}]")


def setAngle(angle):
    duty = angle / 18 + 2.5
    pwm.ChangeDutyCycle(duty)
    sleep(0.3)

def main():
    global pwm
    gpio.setmode(gpio.BOARD)
    gpio.setup(SERVO_PIN, gpio.OUT)
    pwm = gpio.PWM(SERVO_PIN, 50)
    pwm.start(0)

    client.run(os.getenv("DISCORD_BOT_TOKEN"))

def wiggle():
    setAngle(0)
    setAngle(179)


if __name__ == "__main__":
    try:
        main()
    finally:
        print("\nRunning cleanup\n")
        if pwm:
            pwm.stop()
        gpio.cleanup()


