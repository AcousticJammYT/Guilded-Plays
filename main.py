# !!! DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOU'RE DOING !!!

import guilded
import random
import re
import io
import aiohttp
import json
import functions as comm

client = guilded.Client()

with open('bot_info.json') as f:
   data = json.load(f)

#print(data)        # Test code to make sure the info gets passed along.

controls = data["controls"]

modes = ["Normal", "Crews"]
if not data["mode"].title() in modes:
    raise ValueError("Current mode not in list of supported modes.")
    
init_message = None

@client.event
async def on_ready():
    print("Guilded is ready to play!")
    channel = client.get_partial_messageable(data["channel"])
    cont_string = controls[0]
    for i in range(1, len(controls)):
        cont_string += ", " + controls[i]
    init_message = await channel.send("Guilded Plays " + data["game"] + " is live! The controls are as follows: " + cont_string + ". Current mode: " + data["mode"].title() + ".")

@client.event
async def on_message(message):
    for i in controls:
        if message.content.lower() == i and message.channel.id == data["channel"]:
            if data["xp"]:
                await message.author.award_xp(1)
            match data["mode"].title():
                case "Normal":
                    comm.callCommand(i)
                case "Crews":
                    comm.callCommandCrew(i, message.author.name)
        elif message.content.lower() == "end event" and message.author.id in data["admins"]:
            channel = client.get_partial_messageable(data["channel"])
            await channel.send("Guilded Plays " + data["game"] + " has ended. Your messages are no longer being read by the bot. Thank you for participating!")
            await client.close()

client.run(data["token"])

# !!! DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOU'RE DOING !!!
# Guilded Plays by AcousticJamm
