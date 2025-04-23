import tkinter as tk
from tkinter import ttk


class ScrollingView(tk.Frame):
    def __init__(self,root,**frameKwargs):
        super().__init__(root,**frameKwargs)
        self.canvas = tk.Canvas(self)
        self.verticalScroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.horizontalScroll = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.verticalScroll.set)
        self.canvas.configure(xscrollcommand=self.horizontalScroll.set)
        self.interiorFrame = tk.Frame(self.canvas)

        self.verScrollOn = False
        self.horzScrollOn = False
        
        self.visScroll = True

        self.inW = 0
        self.inH = 0

        self.bind("<Configure>",self.sizeConfig)
        self.bind('<Enter>', self.onEnter)                                 # bind wheel events when the cursor enters the control
        self.bind('<Leave>', self.onLeave)  

    def setInteriorSize(self,w,h):
        self.inW = w
        self.inH = h
        self.interiorFrame.place(x=0,y=0,width=w,height=h)
        self.canvas.create_window((0, 0), window=self.interiorFrame, anchor="nw",width=w,height=h)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.sizeConfig(None)

    def setVisibleScroll(self,visbileScroll):
        self.visScroll = visbileScroll
        self.sizeConfig(None)

    def setVeiw(self,x,y):
        if(self.inW and (self.inW > self.winfo_width())):
            self.canvas.xview_moveto(x/self.inW )
        if(self.inH and (self.inH > self.winfo_height())):
            self.canvas.yview_moveto(y/self.inH)
        if(self.inH and self.inW):
            print(f"x:{x} y:{y} w:{self.inW} h:{self.inH}")
        
        

    def sizeConfig(self,_):
        w = self.winfo_width()
        h = self.winfo_height()

        #print(f"In size {self.inW} x {self.inH} window size {w} x {h}")
        self.canvas.place(x=0,y=0,width=w-10,height = h-10)
        self.verScrollOn = True if (self.inH-10)>h else False
        self.horzScrollOn = True if (self.inW-10)>w else False

        if(self.verScrollOn and self.visScroll):
            self.verticalScroll.place(x=w-10,y=0,width=10,height = h-10)
        else:
            self.verticalScroll.place_forget()
        if(self.horzScrollOn and self.visScroll):
            self.horizontalScroll.place(x=0,y=h-10,width=w-10,height=10)
        else:
            self.horizontalScroll.place_forget()


        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    
    def onMouseWheel(self, event):                                                  #WINDOWS ONLY MOTHER HUBERDS
        self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")

    
    def onEnter(self, _): 
        if(self.verScrollOn):                                                      # bind wheel events when the cursor enters the control
            self.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, _):                                                       # unbind wheel events when the cursorl leaves the control
        self.unbind_all("<MouseWheel>")
