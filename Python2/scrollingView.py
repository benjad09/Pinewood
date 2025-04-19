import tkinter as tk
from tkinter import ttk


class ScrollingView(tk.Frame):
    def __init__(self,root,**frameKwargs):
        super().__init__(root,**frameKwargs)
        self.canvas = tk.Canvas(self)
        self.verticalScroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.verticalScroll.set)
        self.interiorFrame = tk.Frame(self.canvas)

        self.bind("<Configure>",self.sizeConfig)
        self.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.bind('<Leave>', self.onLeave)  

    def setInteriorSize(self,w,h):
        self.interiorFrame.place(x=0,y=0,width=w,height=h)
        self.canvas.create_window((0, 0), window=self.interiorFrame, anchor="nw",width=w,height=h)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        

    def sizeConfig(self,_):
        w = self.winfo_width()
        h = self.winfo_height()
        self.canvas.place(x=0,y=0,width=w-10,height = h)
        self.verticalScroll.place(x=w-10,y=0,width=10,height = h)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    
    def onMouseWheel(self, event):                                                  #WINDOWS ONLY MOTHER HUBERDS
        self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")

    
    def onEnter(self, _):                                                       # bind wheel events when the cursor enters the control
        self.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, _):                                                       # unbind wheel events when the cursorl leaves the control
        self.unbind_all("<MouseWheel>")
