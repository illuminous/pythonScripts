from Tkinter import *                 
from tkMessageBox import showinfo

#def reply(name):
#    showinfo(title='FLM Value', message='Value  %s!' % name)


top = Tk()
top.title('FLM Calculator')
top.iconbitmap('py-blue-trans-out.ico')

Label(top, text="Enter your CWD:").pack(side=TOP)
ent = Entry(top)
ent.pack(side=TOP)




Label(top, text="Enter your FWD:").pack(side=TOP)
ent = Entry(top)
ent.pack(side=TOP)




Label(top, text="Enter your Duff:").pack(side=TOP)
ent = Entry(top)
ent.pack(side=TOP)




Label(top, text="Enter your LITTER:").pack(side=TOP)
ent = Entry(top)
ent.pack(side=TOP)
btn = Button(top, text="Submit", command=(lambda: reply(ent.get())))
btn.pack(side=LEFT)
top.mainloop()




           

