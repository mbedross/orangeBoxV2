#!/usr/bin/env python2
#encoding: UTF-8

"""

This function generates the GUI for the DHM control from the HOST computer

"""

import Tkinter

def center(toplevel):
    # This module is called to center the window on the screen
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

class confirmIP(Tkinter.Tk):
    
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    
    def initialize(self):
        self.grid()
        
        # Text field to enter IP address
        self.IPVariable = Tkinter.StringVar()
        self.IP = Tkinter.Entry(self,textvariable=self.IPVariable)
        self.IP.grid(column=0,row=0,sticky='EW')
        self.IP.bind("<Return>", self.OnPressEnter)
        self.IPVariable.set(u"192.168.1.14")
        
        # Text field to enter UDP Port number
        self.PortVariable = Tkinter.StringVar()
        self.Port = Tkinter.Entry(self,textvariable=self.PortVariable)
        self.Port.grid(column=0,row=1,sticky='EW')
        self.Port.bind("<Return>", self.OnPressEnter)
        self.PortVariable.set(u"5005")
        
        button = Tkinter.Button(self, text=u"OK", command=self.OnButtonClick)
        button.grid(column=1,row=0)
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self, textvariable=self.labelVariable, anchor="w",fg="black",bg="white")
        label.grid(column=0,row=2,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Enter Host IP and Port Number. Press OK or ENTER when ready")
        
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False) #(Horizontal,Vertical) resizing constraints
        self.update()
        self.geometry(self.geometry())
        self.IP.focus_set()
        self.IP.selection_range(0, Tkinter.END)
        
#    def quit(self):
#        self.root.destroy()
        
    def OnButtonClick(self):
        ip = raw_input(self.IPVariable.get())  # Store input as IP
        port = raw_input(self.PortVariable.get())
        self.IP.focus_set()
        self.IP.selection_range(0, Tkinter.END)
        print("IP and Port are: %s, %s" % (ip, port))
        self.root.destroy()
        return ip, port

    def OnPressEnter(self,event):
        ip = raw_input(self.IPVariable.get())  # Store input as IP
        port = raw_input(self.PortVariable.get())
        self.IP.focus_set()
        self.IP.selection_range(0, Tkinter.END)
        print("IP and Port are: %s, %s" % (ip, port))
        self.root.destroy()
        return ip, port

if __name__ == "__main__":
    app = confirmIP(None)
    app.title('SHAMU')
    center(app)
    app.mainloop()
    app.lift()
    