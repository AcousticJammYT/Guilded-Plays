Credits:
AcousticJamm: Entire Guilded Plays framework
YumYummity: Coding help


How to use:
1) Just basic setup stuff. Make a channel (NOTE: doesn't work for streaming channels currently) and
   a bot. Give the bot a bot token; we'll use that for the next step. You'll want your bot to have
   basic permissions, such as seeing the channel and reading messages from it. I would also recommend
   having an input library installed on your computer (I use pynput).

2) Inside bot_info.json, you'll see the template for the bot information. Edit that to suit whatever
   you need, but keep in mind the "controls"; we'll use that later. Everything should be obvious.

3) This step is the tricky step; go into function.py and write the callCommand(command) function. What
   this function is meant for is to take the string command (as it is in bot_info.json)and convert it
   into pressing controls in the game. Be creative! You can use this to hold down a button or
   activate a macro of any kind; just be sure to test your code. For my original use, I originally
   hosted a "Guilded Plays Pokémon Red", which required just pressing the button.

4) Now that everything is made, you can run your main.py to start up the bot. If you set everything up
   correctly, inputting your commands will run the actions in game.

5) When you're ready to end the game, simply send "end event" and the bot will shut down.


Modes:
- "Normal": Your regular Guilded Plays. Everyone holds the same controls and does the same thing with
  these controls.
- "Crews": As seen on the Dougdoug YouTube channel, the chat splits up between two teams. By default,
  these teams are A Crew, which is those with usernames starting with A-M, and Z Crew, which is N-Z.
- "Democracy Multi": Users can send as many votes as they want. By the end of the voting period, the
  items with the most votes get played.
