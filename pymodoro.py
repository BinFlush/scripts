#!/usr/bin/env python3
from tkinter import *
import sys
import time
import subprocess

class Pomodoro():
    def pauseplay(self, event=None):
        if self.count == True:
            #print("true. setting to false")
            self.count = False
        else:
            #print("flase. setting to true")
            self.count = True
            self.now_unix = round(time.time())
            self.starting_unix_timestamp = self.now_unix - self.progress


        self.timer()


    def reset(self):
        self.count = False
        self.lb.configure(bg='white')
        self.periods = 0
        self.progress = 0
        self.sum = self.work
        self.update()
#        self.cycle_t.set("0")

    def backward(self, event=None):
        if self.count:
            self.starting_unix_timestamp += self.changesteps
        else:
            self.progress -= self.changesteps
            self.sum += self.changesteps
        self.update()

    def forward(self, event=None):
        if self.count:
            self.starting_unix_timestamp -= self.changesteps
        else:
            self.progress += self.changesteps
            self.sum -= self.changesteps
        self.update()


    def timer(self):
        #print(str(self.count))
        if self.count == True:
            self.now_unix = round(time.time())
            self.progress = self.now_unix - self.starting_unix_timestamp
            self.sum = self.activity - self.progress
            if self.sum < 0 or self.periods == 0:
                self.iterate()
            self.update()
   #         if self.progress > 0 or self.has_done_first_start == False:
            #print("sum=", self.sum, "periods=", self.periods, "progress=", self.progress, "activity=", self.activity)
   #         self.has_done_first_start == True
            self.root.after(250,self.timer)

    def update(self):
        txt = time.strftime("%M:%S", time.gmtime(self.sum))
        self.t.set(txt)
        
    def action(self, message):
   
        sound_command = ["ffplay", "-nodisp", "-autoexit", self.notification_file] 
        subprocess.Popen(sound_command, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL)

        notify_command = ['notify-send', f'{self.message}']
        subprocess.Popen(notify_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def iterate(self):
        self.periods += 1
        self.full_cycle = -(-self.periods//2)
        self.cycle_t.set(str(self.full_cycle))
        self.sum = 0
        self.now_unix = round(time.time())
        if self.periods % 2 == 1:
            # odd number means work
            self.activity = self.work
            self.lb.configure(bg='red')
            self.message = "STARTING WORKING SESSION"
        else:
            # break
            self.lb.configure(bg='green')
            if self.periods % 8 == 0:
                # longbrake
                self.activity = self.long
                self.message = "STARTING LONG BRAKE"
            else:
                # shortbrake
                self.message = "STARTING BRAKE"
                self.activity = self.short
        self.action(self.message)
        self.starting_unix_timestamp = round(time.time())
        self.sum = self.activity
        if not self.count:
            self.update()



    def __init__(self):
        self.long_break_length_minutes = 15
        self.short_break_length_minutes = 5
        self.work_length_minutes = 25
        self.long = self.long_break_length_minutes * 60
        self.short = self.short_break_length_minutes * 60
        self.work = self.work_length_minutes * 60
        self.activity = self.work
        self.periods = 0
        self.progress = 0
        self.sum = self.work
        self.count = False
        self.has_done_first_start = False
        self.notification_file = '/home/jakupl/git/binflush/scripts/bell-sound.mp3' 
        self.changesteps = 60
        self.starting_unix_timestamp = round(time.time())
        self.full_cycle = 0

        self.root = Tk()
        self.root.title("Pymodoro")
#        self.root.geometry("170x140")
        self.t = StringVar()
        self.cycle_t = StringVar()
        self.cycle_t.set(str(self.full_cycle))
#        self.t.set("00:00:00")
        self.update()
        self.lb = Label(self.root, textvariable=self.t, font=("Times 25 bold"), bg="white")
        self.periods_label = Label(self.root, textvariable=self.cycle_t, font=("Times 18 bold"), bg="gray")
        self.bt1 = Button(self.root, text="On/Off", command=self.pauseplay, font=("Times 12 bold"), bg=("gray"))
        self.bt3 = Button(self.root, text="Reset", command=self.reset, font=("Times 12 bold"), bg=("gray"))
        self.bt4 = Button(self.root, text="->", command=self.forward, font=("Times 12 bold"), bg=("gray"))
        self.bt5 = Button(self.root, text="<-", command=self.backward, font=("Times 12 bold"), bg=("gray"))
        self.bt6 = Button(self.root, text="->>", command=self.iterate, font=("Times 12 bold"), bg=("gray"))
        self.root.bind("k",self.pauseplay)

        self.lb.grid(row=0,columnspan=3, sticky='ew')# counter
        self.periods_label.grid(row=2,column=0, sticky='ew')# counter
        self.bt5.grid(row=1,column=0, sticky='ew')# back
        self.bt1.grid(row=1,column=1, sticky='ew')# on/off
        self.bt4.grid(row=1,column=2, sticky='ew')# forward
        self.bt3.grid(row=2,column=1, sticky='ew')# reset
        self.bt6.grid(row=2,column=2, sticky='ew')# ->>
#       self.label = Label(self.root,text="",font=("Times 40 bold"))
        self.root.configure(bg='#191919')
        self.root.bind('<space>', self.pauseplay)
        self.root.bind('<Right>', self.forward)
        self.root.bind('<Left>', self.backward)
        self.root.mainloop()
a = Pomodoro() 
