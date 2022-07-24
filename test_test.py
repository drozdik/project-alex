import time
import tkinter
from tkinter import *

root = Tk()


def increase_button_font():
    button.config(font=("Helvetica 48"))

def decrease_button_font():
    button.config(font=("Helvetica 24"))

flag = [False]
commands = [increase_button_font, decrease_button_font]

def button_command():
    # commands.pop(0)()
    # increase_button_font()
    # time.sleep(1)
    # decrease_button_font()
    flag[0] = True

button = Button(text="Press me", command=button_command, font="Helvetica 24")
button.pack(pady=100)
# root.mainloop()


# press button, font increased twice for 3 seconds, then back to normal, main thread should not be blocked for that time
# import the threading module
import threading
 
class thread(threading.Thread):
    def __init__(self, tk_root, tk_button, flag):
        threading.Thread.__init__(self)
        self.tk_root = tk_root
        self.tk_button = tk_button
        self.flag = flag
 
    def run(self):
        while True:
            time.sleep(0.05)
            if self.flag[0] is True:
                increase_button_font()
                print("sleep for 2 sec")
                time.sleep(2)
                decrease_button_font()
                self.flag[0] = False
 

thread1 = thread(root, button, flag)
thread1.start()
root.mainloop()
print("Exit")