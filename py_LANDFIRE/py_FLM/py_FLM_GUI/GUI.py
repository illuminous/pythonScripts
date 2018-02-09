from Tkinter import *
import random
fontsize = 25
colors = ['red', 'green', 'blue', 'yellow', 'orange', 'white', 'cyan', 'purple']

def reply(text):
    print text
    popup = Toplevel()
    color = random.choice(colors)
    Label(popup, text='Popup', bg='black', fg='color').pack()
    L.config(fg=color)

def timer():
    L.config(fg=random.choice(colors))
    win.after(250, timer)

def grow():
    global fontsize
    fontsize += 5
    L.config(font=('arial', fontsize, 'italic'))
    win.after(100, grow)
    win = Tk()
    L = Label(win, text='Spam',
              font=('arial', fontsize, 'italic'), fg='yellow', bg='navy',
    relief=RAISED)
    L.pack(side=TOP, expand=YES, fill=BOTH)
    Button(win, text='press', command=(lambda: reply('red'))).pack(side=BOTTOM, fill=X)
    Button(win, text='timer', command=timer).pack(side=BOTTOM, fill=X)
    Button(win, text='grow', command=grow).pack(side=BOTTOM, fill=X)
    win.mainloop()
