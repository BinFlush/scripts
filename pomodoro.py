#!/usr/bin/env python3

import subprocess
import time
import datetime

NOTIFICATION_FILE = 'bell-sound.mp3' 

def main():
    long_break_length_minutes = 30
    short_break_length_minutes = 5
    work_length_minutes = 25
    periods = 0

    while True:
        periods += 1
        message = f"WORK PERIOD {periods} STARTED"
        action(message)
        timer(work_length_minutes * 60)

        if periods % 4 == 0:
            # Long break
            message = "LONG BREAK STARTED"
            breaklength = long_break_length_minutes
        else:
            message = "SHORT BREAK PERIOD STARTED"
            breaklength = short_break_length_minutes
        action(message)
        timer(breaklength * 60)



def action(message):
   
    sound_command = ["ffplay", "-nodisp", "-autoexit", NOTIFICATION_FILE] 
    subprocess.Popen(sound_command, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL)

    notify_command = ['notify-send', f'"{message}"']
    subprocess.Popen(notify_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    tm = datetime.datetime.now()
    print(message, "at", str(tm.hour) + ":" + str(tm.minute))

def timer(seconds):
    progress = 0
    adjustment = 0
    starting_unix_timestamp = round(time.time())
    breaklength: str = time.strftime("%H:%M:%S", time.gmtime(seconds))

    while progress < seconds:
        now_unix = round(time.time())
        progress = now_unix - starting_unix_timestamp
        current: str = time.strftime("%H:%M:%S", time.gmtime(progress))
        print(current, " of ", breaklength,"      ", end="\r")
        time.sleep(0.02)


if __name__ == "__main__":
    main()
