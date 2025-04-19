import os

import tkinter as tk
from clintsPrix import ClintsPrix
from campPrix import ChampPrix
from rosterUI import RosterViewer
from roster import Roster
from roster import Driver
from cup import Cup
from tkinter import filedialog
from tkinter import ttk

FREMENMAJORVERSION = 0
FREMENMINORVERSION = 7

WINDOW_NAME = f"RACE CONTROL"

FONT_SIZE = 10
GUIXSIZE = 1200
GUIYSIZE = 820

GUIMINXSIZE = 1200
GUIMINYSIZE = 550

GUIXSIZE = GUIMINXSIZE
GUIYSIZE = GUIMINYSIZE



ROSTER_VIEWER_WIDTH = 350
FRAME_MARGIN = 10

CUP_VIEWER_WIDTH = 500
CUP_VEIWER_HEIGHT = 200
#3
FONT_SIZE = 10

        
        

class CupControl(tk.LabelFrame):
    def __init__(self,master,cup: Cup,loadCupCB,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.loadButton = tk.Button(self,text = "load",command=self.loadCmd,font=("Arial", FONT_SIZE))
        self.saveButton = tk.Button(self,text = "save",command=self.saveCmd,font=("Arial", FONT_SIZE))
        self.saveAsButton = tk.Button(self,text= "save as",command=self.saveAsCmd,font=("Arial", FONT_SIZE))
        self.savePath :str = None

        self.prixSelectionVar = tk.StringVar()
        self.prixLabel = tk.Label(self,text="Prixs: ")
        self.prixSelection = ttk.Combobox(self, textvariable = self.prixSelectionVar,postcommand = self.loadPrixs, state="readonly")

        
        #postcommand = self._refreshXAxisOptionMenu
        #self.prixSelection.bind("<<ComboboxSelected>>", lambda _: self._drawGraph())
        
        self.prixoption = tk.StringVar()
        self.prixSelection.grid(row=0,column=1)

        self.cup = cup
        self.loadCupCB = loadCupCB

        self.prixSelectionVar = tk.StringVar()
        self.prixLabel.grid(row=0,column=0)
        self.prixSelection.grid(row=0,column=1)
        self.loadButton.grid(row=2,column=0)
        self.saveButton.grid(row=2,column=1)
        self.saveAsButton.grid(row=2,column=2)

        #self.bind("<Configure>",self.configSize)

    def loadPrix(self):
        self.prixSelection['values'] = self.cup.getPrixsNames()
        #print(self.cup.getPrixsNames())

 
    def loadCmd(self):
        newpath = filedialog.askdirectory(title = "SelectFolder")
        if newpath:
            self.savePath = newpath
            self.cup.load(self.savePath)
            self.loadCupCB()
        pass
    def saveCmd(self):
        if(self.savePath):
            self.cup.save(self.savePath)
        else:
            self.saveAsCmd()


    def saveAsCmd(self):
        newpath = filedialog.askdirectory(title = "SelectFolder")
        if newpath:
            self.savePath = newpath
            self.cup.save(newpath)

        

class RaceControlGUI:
    """Setups up and controls the core of the GUI"""

    def __init__(self, root: tk.Tk,controller :"RaceControl"):
        self.root = root
        self.control = controller
        self.root.wm_title(WINDOW_NAME)
        self.screen_w = int(self.root.winfo_screenwidth())
        self.screen_h = int(self.root.winfo_screenheight())
        self.default_geometry = str(GUIXSIZE)+"x"+str(GUIYSIZE)+"+"+str(int(self.screen_w/4))+"+"+str(int(self.screen_h/4))
        self.root.geometry(self.default_geometry)
        self.root.minsize(width=GUIMINXSIZE,height=GUIMINYSIZE)
        self.root.protocol('WM_DELETE_WINDOW', self.control.exit)
        self.rosterViewer = RosterViewer(self.control.roster,master = self.root,text='Race Roster')

        self.cupViewer = CupControl(self.root,self.control.cup,self.newCupUpdate,text = "Cup Control")

        self.root.bind("<Configure>",self.configSize)

        #self.root.after(200,self.newCupUpdate)

    def newCupUpdate(self):
        self.rosterViewer.createFramesFromRoster()
        self.cupViewer.loadPrixs()


    def configSize(self,_):
        newWidth = self.root.winfo_width()
        newHeight = self.root.winfo_height() #assinging to varibles because of amount of useses
        self.updateWindowSize(newWidth,newHeight)


    def updateWindowSize(self,newW,newH):
        self.rosterViewer.place(x=newW-ROSTER_VIEWER_WIDTH-(FRAME_MARGIN*2),y=FRAME_MARGIN,height=newH-(FRAME_MARGIN*2),width=ROSTER_VIEWER_WIDTH)
        self.cupViewer.place(x=FRAME_MARGIN,y=(newH)-FRAME_MARGIN-CUP_VEIWER_HEIGHT,width=CUP_VIEWER_WIDTH,height=CUP_VEIWER_HEIGHT)




class RaceControl:
    def __init__(self):
        pathname=f"{os.path.dirname(os.path.abspath(__file__))}"

        self.cup = Cup()
        self.roster :Roster = self.cup.roster
        #self.cup.load(f"{pathname}\\testCup")

        self.root = tk.Tk()
        self.gui = RaceControlGUI(self.root,self)
        
        self.root.mainloop()

    def getSupportedPrixs() -> list[str]:
        return ["peterson","champ"]

    def createPrix(self,prixName: str,type: str,drivers: list[Driver]):
        driverN = [driver.getdriverNum() for driver in drivers]
        if type == "peterson":
            newPrix = ClintsPrix(3)
        elif type == "champ":
            newPrix = ChampPrix(3)
        else:
            Exception("Unreconized Prix Type")

        newPrix.newPrix(driverN)
        self.cup.addPrixs(prixName,newPrix)

        
        


    def exit(self):
        self.root.destroy()

    


def main():
    RaceControl()

if __name__ == "__main__":
    main()