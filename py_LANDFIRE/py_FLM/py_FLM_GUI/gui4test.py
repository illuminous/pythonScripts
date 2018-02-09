# Example just for Carrol
import os,re,win32com.client
connection=win32com.client.Dispatch(r'ADODB.Connection')
result=win32com.client.Dispatch(r'ADODB.Recordset')
from Tkinter import *

class Gui:
    def __init__(self, root):
        """Implements the graphical surface."""
        self.root = root
        self.dir = []
        # Frame to contain the fields
        f = Frame(root) ; f.pack(side=TOP, fill=X)
        # Text field for entry:
        self.t1 = Text(f, width=20, height=1)
        self.t1.pack(side=TOP,expand=YES,fill=X)
        self.t2 = Text(f, width=20, height=1)
        self.t2.pack(side=TOP,expand=YES,fill=X)
        # Button
        self.button = Button(root, text = 'Calculate FLM', command = self.show_it )
        self.button.pack(side=TOP)
        return

    def show_it(self):
        # get whatever was entered and put it onto the screen
        print 't1:',self.t1.get('0.0',END)
        print 't2:',self.t2.get('0.0',END)
        self.root.destroy()
        self.root.quit()

        return


if __name__ == '__main__':
        # If run as stand alone ...
    root = Tk()
    Gui(root)
    mainloop()

