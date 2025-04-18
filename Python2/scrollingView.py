import tkinter as tk
from tkinter import Misc, ttk

class ScrollingView:

    def __init__(self, base_frame):
        self.container = ttk.Frame(base_frame)
        self.container.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.canvas = tk.Canvas(self.container)
        self.scroll_bar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)

        #self.frame.bind("<configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)

    def added_frame(self,width,height):
        default = self.canvas.bbox("all")
        expanded = (0,0,width,default[3]+height)
        self.canvas.configure(scrollregion=expanded)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")

    def clear_frame(self,width):
        self.canvas.configure(scrollregion=(0,0,width,0))
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")