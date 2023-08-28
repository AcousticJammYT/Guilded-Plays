# !!! DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOU'RE DOING !!!

import guilded
from guilded.ext import commands
import random
import asyncio
import re
import io
import aiohttp
import time
import json
import warnings
from collections import Counter

refreshing = False
paused = False
removed = {}
start_time = round(time.time())
total_paused_time = 0
temp_pause_time = 0
pinned_messages = []
to_pin = []

while True:

    import functions as comm

    with open('bot_info.json') as f:
        data = json.load(f)

    #print(data)        # Test code to make sure the info gets passed along.

    async def get_prefix(bot, message):
        return data["prefix"]

    bot = commands.Bot(command_prefix=get_prefix, help_command=None)

    controls = data["controls"]

    if len(data["admins"]) < 1:
        raise ValueError("No admins were defined in bot_info.json")

    modes = ["Normal", "Crews", "Democracy Multi"]
    if not data["mode"].title() in modes:
        warnings.warn("Current mode not in list of supported modes.")
        
    init_message = None

    permissions = {
        "remove": 3,
        "allow": 3,
        "refresh": 3,
        "end": 4,
        "pause": 4,
        "resume": 4
    }

    votes = []
    voted = []

    trivia_list = [
        "Guilded Plays is based on a Twitch event known as Twitch Plays Pokemon, where a Twitch chat would attempt to complete various Pokemon games.",
        "Guilded Plays was made by AcousticJamm and the project was started on May 6th, 2023.",
        "The first ever Guilded Plays event was hosted on the official Guilded Plays server on May 20th, 2023. On that day, a few people got together in an attempt to beat Brock in Pokemon Red.",
        "Guilded Plays is inspired by Dougdoug, who frequently lets his Twitch chat play games on his Twitch channel.",
        "Did you know there is an official Guilded Plays Guilded server? Look it up in the Discover tab if you're interested in getting to know how this code works!",
        "This version of the Guilded Plays bot is written in the Guilded.py library posted by shay.",
        "Guilded Plays wouldn't have happened if it weren't for Guilded's bot API. Guilded's staff really is amazing!",
        "Guilded does what Discan't.",
        "The creator of Guilded Plays, AcousticJamm, intends on updating the code. He isn't all done yet!",
        "There are currently three different modes that are built into the base code: Normal, Crews, and Democracy Multi.",
        "The base Guilded Plays code comes with the functions necessary for controling the game. You are encouraged to edit these functions to suit the game your Guilded chat is playing.",
        "The bot's current version is 1.0.0.",
        "With proper coding skills, a single application of Guilded Plays does not have to be limited to one computer; you could potentially control real world things with it!",
        "The default for Crews mode is two crews, being A Crew and Z Crew, but realistically, you could have as many as you want.",
        "Guilded was released to the public on March 17, 2017, a few days over Discord's release date.",
    ]

    @bot.event
    async def on_ready():
        global refreshing, pinned_messages, to_pin
        if not refreshing:
            print("Guilded is ready to play!")
            channel = bot.get_partial_messageable(data["channel"])
            cont_string = controls[0]
            for i in range(1, len(controls)):
                cont_string += ", " + controls[i]
            init_message = await channel.send("Guilded Plays " + data["game"] + " is live! The controls are as follows: " + cont_string + ". Current mode: " + data["mode"].title() + ".")
            init_private_message = await channel.send(embed=guilded.Embed(title="Admin Controls", description=f"<@{'> <@'.join(data['admins'])}>\n**Here are the admin only commands:**\n`{data['prefix']}refresh` - Refresh the bot and configs.\n`{data['prefix']}end` - Ends the event.\n`{data['prefix']}pause` - Pauses the event.\n`{data['prefix']}resume` - Resumes the event.\n`{data['prefix']}remove {{users}}` - Removes user(s) from the event. Good for troublemakers.\n`{data['prefix']}allow {{users}}` - Allows user(s) to participate in the event. Use after someone who was previously removed needs to be let back in."), private=True)
            init_commands_message = await channel.send(embed=guilded.Embed(title="Commands", description=f"`{data['prefix']}time` - The ongoing time of the event."))
            if data["pin_messages"]:
                await init_message.pin()
                await init_commands_message.pin()
                pinned_messages = [init_message, init_commands_message]
                await channel.send("Check the pins for more info!")
            if data["voice"]:
                await channel.send("The host of this event has indicated that you may join the voice chat. Feel free to join in to listen to some strategy!")
            if data["trivia"]:
                await channel.send("Fun fact: " + random.choice(trivia_list))
        else:
            print("Guilded is ready to play after a refresh!")
            channel = bot.get_partial_messageable(data["channel"])
            cont_string = controls[0]
            for i in range(1, len(controls)):
                cont_string += ", " + controls[i]
            init_message = await channel.send("Guilded Plays " + data["game"] + " has been refreshed! The controls are as follows: " + cont_string + ". Current mode: " + data["mode"].title() + ".")
            init_commands_message = await channel.send(embed=guilded.Embed(title="Commands", description=f"`{data['prefix']}time` - The ongoing time of the event."))
            if data["pin_messages"]:
                await init_message.pin()
                await init_commands_message.pin()
                pinned_messages = [init_message, init_commands_message]
                await channel.send("Check the pins for more info!")
        if data["mode"].title() == "Democracy Single" or data["mode"].title() == "Democracy Multi":
            await doDemocracy()
        refreshing = False

    @bot.event
    async def on_message(message):
        if paused or (not message.author) or message.author.bot or removed.get(message.author.id):
            await bot.process_commands(message)
            return
        for i in controls:
            if message.content.lower() == i and message.channel.id == data["channel"]:
                if data["xp"]:
                    await message.author.award_xp(1)
                match data["mode"].title():
                    case "Normal":
                        comm.callCommand(i)
                    case "Crews":
                        comm.callCommandCrew(i, message.author.name)
        await bot.process_commands(message)

    def checkPermissions(userid, level):
        if int(data["admins"][userid]) >= level:
            return True
        return False

    def getMostCommonItems(lst):
        if not lst:
            return []
        
        counter = Counter(lst)
        most_common = counter.most_common()
        if most_common:
            max_count = most_common[0][1]
            return [item for item, count in most_common if count == max_count]
        else:
            return []

    def gettime(secs:float|int) -> str:
        secs = int(secs)
        days = secs//86400
        hours = (secs - days*86400)//3600
        minutes = (secs - days*86400 - hours*3600)//60
        seconds = secs - days*86400 - hours*3600 - minutes*60
        result = ("{0} day{1}, ".format(days, "s" if days!=1 else "") if days else "") + \
        ("{0} hour{1}, ".format(hours, "s" if hours!=1 else "") if hours else "") + \
        ("{0} minute{1}, ".format(minutes, "s" if minutes!=1 else "") if minutes else "") + \
        ("{0} second{1}, ".format(seconds, "s" if seconds!=1 else "") if seconds else "")
        result = result.strip()
        result = result.strip(',')
        if result == '':
            return '0 seconds'
        return result

    async def doDemocracy():
        while True:
            global votes
            global voted
            # Wait for the allowed time
            await asyncio.sleep(data["democracy_timer"])
            
            # Your update logic goes here
            print("Doing votes...")
            
            most_common_items = getMostCommonItems(votes)
            channel = bot.get_partial_messageable(data["channel"])
            
            if most_common_items:
                most_common_items_str = ', '.join(map(str, most_common_items))
                await channel.send("Winning items: " + most_common_items_str)
            else:
                await channel.send("No items")
            
            for i in most_common_items:
                comm.callCommand(i)
            
            votes = []
            voted = []

    @bot.command(name="print")
    async def printPermissions(ctx:commands.Context):
        await ctx.reply(data["admins"][ctx.author.id])

    @bot.command(name="time")
    async def event_time(ctx:commands.Context):
        pt = (int( time.time() - temp_pause_time ) if paused else 0)
        tt = (int(time.time()) - start_time)
        await ctx.send(
            (
                "Guilded Plays " + data["game"] + \
                f" has been ongoing for **{gettime(tt - pt - total_paused_time)}**" \
                + (f"\nCurrently on pause for: **{gettime(round( time.time() - temp_pause_time ))}**" if paused else f"\nPaused for: **{gettime(total_paused_time)}**") + \
                f"\nTotal time: **{gettime(tt)}**"
            )
        )

    @bot.command(name="refresh", aliases=["reload"])
    async def refresh_bot(ctx:commands.Context):
        global temp_pause_time, total_paused_time, refreshing
        if checkPermissions(ctx.author.id, permissions[ctx.command.name]):
            if paused:
                total_paused_time += time.time() - temp_pause_time
                temp_pause_time = 0
            refreshing = True
            for message in pinned_messages:
                await message.unpin()
            await bot.close()

    @bot.command(name="end")
    async def end_event(ctx:commands.Context):
        global temp_pause_time, total_paused_time
        if checkPermissions(ctx.author.id, permissions[ctx.command.name]):
            if paused:
                total_paused_time += time.time() - temp_pause_time
                temp_pause_time = 0
            channel = bot.get_partial_messageable(data["channel"])
            event_time = (round(time.time())-start_time)
            await channel.send("Guilded Plays " + data["game"] + " has ended. Your messages are no longer being read by the bot. Thank you for participating!" + f"\nTotal event time: **{gettime(event_time-total_paused_time)}**\nTotal paused time: **{gettime(total_paused_time)}**\nTotal time: **{gettime(event_time)}**")
            for message in pinned_messages:
                await message.unpin()
            await bot.close()
            exit()

    @bot.command(name="pause")
    async def pause_event(ctx:commands.Context):
        global paused, temp_pause_time
        if checkPermissions(ctx.author.id, permissions[ctx.command.name]):
            if paused:
                return await ctx.reply("This game is already paused!", private=ctx.message.private)
            paused = True
            temp_pause_time = time.time()
            channel = bot.get_partial_messageable(data["channel"])
            await channel.send("Guilded Plays " + data["game"] + " has been paused. Your messages are no longer being read by the bot.")

    @bot.command(name="resume")
    async def pause_event(ctx:commands.Context):
        global paused, temp_pause_time, total_paused_time
        if checkPermissions(ctx.author.id, permissions[ctx.command.name]):
            if not paused:
                return await ctx.reply("This game isn't paused!", private=ctx.message.private)
            paused = False
            total_paused_time += time.time() - temp_pause_time
            temp_pause_time = 0
            channel = bot.get_partial_messageable(data["channel"])
            await channel.send("Guilded Plays " + data["game"] + " has been resumed. Your messages are now being read by the bot.")

    @bot.command(name="remove")
    async def remove_user(ctx:commands.Context, *, _:str=None):
        global removed
        users = []
        if checkPermissions(ctx.author.id, permissions[ctx.command.name]):
            if _:
                if len(ctx.message.user_mentions) != 0:
                    for user in ctx.message.user_mentions:
                        users.append(user)
                for possible_user_id in _.split(' '):
                    try:
                        user = await bot.getch_user(possible_user_id)
                    except:
                        user = None
                    if user:
                        users.append(user)
                users = list(set(users))
                if len(users) < 1:
                    return await ctx.reply("No user(s) selected.", private=ctx.message.private)
                msg = []
                for user in users:
                    if removed.get(user.id):
                        msg.append(f"{user.name} - Already removed from the event.")
                        continue
                    removed[user.id] = True
                    msg.append(f"{user.name} - Removed from the event successfully.")
                enter = "\n";await ctx.reply(f"**Success!**\n{enter.join(msg)}", private=ctx.message.private)
            else:
                return await ctx.reply("No user(s) selected.", private=ctx.message.private)

    @bot.command(name="allow")
    async def allow_user(ctx:commands.Context, *, _:str=None):
        global removed
        users = []
        if checkPermissions(ctx.author.id, permissions[ctx.command.name]):
            if _:
                if len(ctx.message.user_mentions) != 0:
                    for user in ctx.message.user_mentions:
                        users.append(user)
                for possible_user_id in _.split(' '):
                    try:
                        user = await bot.getch_user(possible_user_id)
                    except:
                        user = None
                    if user:
                        users.append(user)
                users = list(set(users))
                if len(users) < 1:
                    return await ctx.reply("No user(s) selected.", private=ctx.message.private)
                msg = []
                for user in users:
                    if not removed.get(user.id):
                        msg.append(f"{user.name} - Already allowed in the event.")
                        continue
                    del removed[user.id]
                    msg.append(f"{user.name} - Allowed into the event successfully.")
                enter = "\n";await ctx.reply(f"**Success!**\n{enter.join(msg)}", private=ctx.message.private)
            else:
                return await ctx.reply("No user(s) selected.", private=ctx.message.private)

    bot.run(data["token"])

# !!! DO NOT EDIT THIS UNLESS YOU KNOW WHAT YOU'RE DOING !!!
# Guilded Plays by AcousticJamm
# Helped by YumYummity
