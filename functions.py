# This file is where you write the code for your Guilded Plays.

from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

def callCommand(command):
    print(command)
    match command:
        case "left":
            keyboard.press(Key.left)
            time.sleep(0.1)
            keyboard.release(Key.left)
        case "right":
            keyboard.press(Key.right)
            time.sleep(0.1)
            keyboard.release(Key.right)
        case "up":
            keyboard.press(Key.up)
            time.sleep(0.1)
            keyboard.release(Key.up)
        case "down":
            keyboard.press(Key.down)
            time.sleep(0.1)
            keyboard.release(Key.down)
        case "a":
            keyboard.press('s')
            time.sleep(0.1)
            keyboard.release('s')
        case "b":
            keyboard.press('a')
            time.sleep(0.1)
            keyboard.release('a')
        case "start":
            keyboard.press(Key.enter)
            time.sleep(0.1)
            keyboard.release(Key.enter)
        case "select":
            keyboard.press(Key.shift_l)
            time.sleep(0.1)
            keyboard.release(Key.shift_l)

def callCommandCrew(command, name):
    print(command, name)
    if (name[0].lower() >= 'a' and name[0].lower() <= 'm') or (name[0] >= 0 and name[0] <= 4):
        print(name + " is in A Crew.")
        # Do controls for A Crew.
    elif (name[0].lower() >= 'n' and name[0].lower() <= 'z') or (name[0] >= 5 and name[0] <= 9):
        print(name + " is in Z Crew.")
        # Do controls for Z Crew.