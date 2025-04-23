import os

import tkinter as tk
from rosterUI import RosterViewer
from roster import Roster
from roster import Driver
from tkinter import messagebox
from cup import Cup
from tkinter import filedialog
from tkinter import ttk
from marshalVeiwer import MarshalVeiwer
from cupVeiwer import CupVeiwer

from tkinter import messagebox

FREMENMAJORVERSION = 0
FREMENMINORVERSION = 7

WINDOW_NAME = f"RACE CONTROL"

FONT_SIZE = 10


GUIMINXSIZE = 1440
GUIMINYSIZE = 900

GUIXSIZE = GUIMINXSIZE
GUIYSIZE = GUIMINYSIZE



ROSTER_VIEWER_WIDTH = 350
FRAME_MARGIN = 10

ANNOUNCER_VIEWER_WIDTH = 600

CUP_VEIWER_HEIGHT = 150
#3
FONT_SIZE = 10


class NewPrixWindow(tk.Toplevel):
    def __init__(self, master,cup: Cup):
        super().__init__(master)
        self.cup = cup
        self.title("Prix Selection")
        self.geometry("500x250")


        self.prixNameVar = tk.StringVar()
        self.prixName = tk.Entry(self,textvariable = self.prixNameVar)
        tk.Label(self,text="Name:").grid(row=0,column=0,pady=10)
        self.prixName.grid(row=0,column=1,pady=10)


        self.typeSelectionVar = tk.StringVar()
        self.typeSelection = ttk.Combobox(self, textvariable = self.typeSelectionVar, state="readonly",font=("Arial", FONT_SIZE))
        self.typeSelection['values'] = self.cup.getSupportedPrixs()
        tk.Label(self,text = "Type:",font=("Arial", FONT_SIZE)).grid(row=1,column=0,pady=10)
        self.typeSelection.grid(row=1,column=1,pady=10)

        self.racerListBox = tk.Listbox(self,selectmode = tk.EXTENDED)
        for name in [driver.getDriverName() for driver in cup.getRoster().getAllDrivers()]:
            self.racerListBox.insert(tk.END,name)

        self.racerListBox.grid(row=0,column=2,padx=5,rowspan=2)
        tk.Button(self,text="Select All",command =lambda :self.racerListBox.select_set(0, tk.END)).grid(row=3,column=2)
        tk.Button(self,text="cancel",command=lambda :self.destroy()).grid(row=3,column=1)
        tk.Button(self,text="generate",command = self.confirmAndGenerate).grid(row=3,column=0)



    def confirmAndGenerate(self):
        name = self.prixName.get()
        nameList = [name for name in [self.racerListBox.get(index) for index in self.racerListBox.curselection()]]
        prixType = self.typeSelectionVar.get()
        if name == '':
            messagebox.showwarning("yooooo","Need a name")
        elif(len(nameList)<1):
            messagebox.showwarning("yooooo","Need at least 1 racer")
        elif(prixType not in self.cup.getSupportedPrixs()):
            messagebox.showwarning("yooooo",f"no {prixType} type")
        else:
            label = f"Generate {prixType} prix with "
            if nameList == [driver.getDriverName() for driver in self.cup.getRoster().getAllDrivers()]:
                label = label + "all drivers"
            else:
                for nameIndex in range(min(len(nameList),3)):
                    label = label + nameList[nameIndex] + " "
                if(len(nameList)>3):
                    label = label + "and more"
            if(messagebox.askokcancel("You Good?",label)):
                self.cup.makeNewPrix(name,prixType,[self.cup.getRoster().getDriverByName(driver) for driver in [drivername for drivername in nameList]])
                self.destroy()


        #tk.Label(self, text="This is a new window").pack(pady=20)

class CupControl(tk.LabelFrame):
    def __init__(self,master,cup: Cup,newCupCb,loadCupCB,loadPrixCb,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.loadButton = tk.Button(self,text = "load",command=self.loadCmd,font=("Arial", FONT_SIZE))
        self.saveButton = tk.Button(self,text = "save",command=self.saveCmd,font=("Arial", FONT_SIZE))
        self.saveAsButton = tk.Button(self,text= "save as",command=self.saveAsCmd,font=("Arial", FONT_SIZE))
        self.newPrixButton = tk.Button(self,text= "newPrix",command=self.newPrix,font=("Arial", FONT_SIZE))
        self.newCupButton = tk.Button(self,text= "newCup",command=self.newCup,font=("Arial", FONT_SIZE))
        self.savePath :str = None


        self.prixSelectionVar = tk.StringVar()
        self.prixLabel = tk.Label(self,text="Prixs: ")
        self.prixSelection = ttk.Combobox(self, textvariable = self.prixSelectionVar,postcommand = self.loadPrixNames, state="readonly")
        self.prixSelection.bind("<<ComboboxSelected>>",lambda _:self.loadPrix())

        
        
        self.prixoption = tk.StringVar()
        self.prixSelection.grid(row=0,column=1)

        self.cup = cup
        self.loadCupCB = loadCupCB
        self.loadPrixCb = loadPrixCb
        self.newCupCb = newCupCb

        self.prixSelectionVar = tk.StringVar()
        self.prixLabel.grid(row=0,column=0)
        self.prixSelection.grid(row=0,column=1)
        self.loadButton.grid(row=2,column=0)
        self.saveButton.grid(row=2,column=1)
        self.saveAsButton.grid(row=2,column=2)
        self.newPrixButton.grid(row=3,column=0)
        self.newCupButton.grid(row=3,column=2)

        

        #self.bind("<Configure>",self.configSize)

    def newCup(self):
        self.newCupCb()


    def newPrix(self):
        NewPrixWindow(self,self.cup)
        self.loadPrixNames()

    def loadPrix(self):
        prixname = self.prixSelection.get()
        if(prixname != ""):
            self.cup.setPrix(prixname)
            self.loadPrixCb()


    def loadPrixNames(self):
        self.prixSelection.set("")
        self.prixSelection['values'] = self.cup.getPrixsNames()

 
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


class mainVeiwer(tk.Toplevel):
    def __init__(self, master,cup: Cup):
        super().__init__(master)
        self.cup = cup
        self.title("14st Derby Night")
        self.minsize(width=500,height=500)
        self.state('zoomed')
        self.raceViewer = CupVeiwer(self,self.cup,fontSize=32,raceFrameH=250,displayCarNames=True,displayDriverNumbers=False,displayResults=False,carLeadIn="In the ")
        self.raceViewer.config(bg = 'red')
        #self.raceViewer.raceHeight = 250
        self.raceViewer.place(relx=0.1,rely=0.05,relwidth=.8,relheight=.9)

    def drawPrix(self):
        self.raceViewer.drawPrix()

    def updatePrix(self):
        self.raceViewer.updatePrix()
    



    

class RaceControlGUI:
    """Setups up and controls the core of the GUI"""

    def __init__(self, root: tk.Tk,cup :Cup):
        self.root = root
        #self.cup = cup
        self.cup = Cup()
        self.root.wm_title(WINDOW_NAME)
        self.screen_w = int(self.root.winfo_screenwidth())
        self.screen_h = int(self.root.winfo_screenheight())
        self.default_geometry = str(GUIXSIZE)+"x"+str(GUIYSIZE)+"+"+str((self.screen_w-GUIXSIZE)//2)+"+"+str((self.screen_h-GUIYSIZE)//2)
        self.root.geometry(self.default_geometry)
        self.root.minsize(width=GUIMINXSIZE,height=GUIMINYSIZE)
        #self.root.protocol('WM_DELETE_WINDOW', self.cup.exit)
        self.rosterViewer = RosterViewer(self.cup.roster,master = self.root,text='Race Roster')

        self.cupCont = CupControl(self.root,self.cup,self.newCupCb,self.newCupUpdate,self.newPrixUpdate,text = "Cup Control")

        self.marshalViewer = MarshalVeiwer(self.root,self.cup,self.prixUpdateCb,text = "Marshal Veiwer")

        self.announcerViewer = tk.LabelFrame(self.root,text="Announcer")
        self.cupViewer = CupVeiwer(self.announcerViewer,self.cup,fontSize=20,raceFrameH=250,displayCarNames=True)
        self.cupViewer.place(relx=0,rely=0,relwidth=1.0,relheight=1.0)

        self.root.bind("<Configure>",self.configSize)


        self.bigVeiw = mainVeiwer(self.root,self.cup)
        #self.root.after(200,self.newCupUpdate)

    def newCupCb(self):
        self.cup.resetCup()
        self.newCupUpdate()
        


    def newCupUpdate(self):
        self.rosterViewer.createFramesFromRoster()
        self.cupCont.loadPrixNames()
        self.newPrixUpdate()

    def prixUpdateCb(self):
        self.cupCont.saveCmd()
        self.bigVeiw.updatePrix()
        self.cupViewer.updatePrix()
        
        
        

    def newPrixUpdate(self):
        self.marshalViewer.drawPrix()
        self.bigVeiw.drawPrix()
        self.cupViewer.drawPrix()
        

    def configSize(self,_):
        newWidth = self.root.winfo_width()
        newHeight = self.root.winfo_height() #assinging to varibles because of amount of useses
        self.updateWindowSize(newWidth,newHeight)


    def updateWindowSize(self,newW,newH):
        #ANNOUNCER_VIEWER_WIDTH

        self.rosterViewer.place(x=newW-ROSTER_VIEWER_WIDTH-(FRAME_MARGIN*2),y=FRAME_MARGIN,height=newH-(FRAME_MARGIN*3)-CUP_VEIWER_HEIGHT,width=ROSTER_VIEWER_WIDTH)
        self.cupCont.place(x=newW-ROSTER_VIEWER_WIDTH-(FRAME_MARGIN*2),y=(newH)-FRAME_MARGIN-CUP_VEIWER_HEIGHT,width=ROSTER_VIEWER_WIDTH,height=CUP_VEIWER_HEIGHT)
        self.marshalViewer.place(x=ANNOUNCER_VIEWER_WIDTH+(FRAME_MARGIN*2),y=FRAME_MARGIN,width=newW-(ROSTER_VIEWER_WIDTH+ANNOUNCER_VIEWER_WIDTH+(FRAME_MARGIN*5)),height=newH-(2*FRAME_MARGIN))
        self.announcerViewer.place(x=FRAME_MARGIN,y=FRAME_MARGIN,width=ANNOUNCER_VIEWER_WIDTH,height=newH-(2*FRAME_MARGIN))


class RaceControl:
    def __init__(self):
        self.cup = Cup()
        #pathname=f"{os.path.dirname(os.path.abspath(__file__))}"
        #self.cup.load(f"{pathname}\\test3")

        self.root = tk.Tk()
        self.gui = RaceControlGUI(self.root,self.cup)
        
        self.root.mainloop()

    


def main():
    RaceControl()

if __name__ == "__main__":
    main()