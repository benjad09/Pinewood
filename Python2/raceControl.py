
import tkinter as tk
from scrollingView import ScrollingView


from race import Race
from prix import Prix
from clintsPrix import ClintsPrix
from campPrix import ChampPrix
from roster import Roster
from roster import Driver
from weekend import Weekend


FREMENMAJORVERSION = 0
FREMENMINORVERSION = 7

WINDOW_NAME = f"RACE CONTROL"

FONT_SIZE = 10
GUIXSIZE = 1200
GUIYSIZE = 820

GUIMINXSIZE = 950
GUIMINYSIZE = 550

GUIXSIZE = GUIMINXSIZE
GUIYSIZE = GUIMINYSIZE


class DriverInfo(tk.Frame):
    def __init__(self,root,driver: Driver,**frameKwargs):
        super().__init__(root,**frameKwargs)
        self.driver = driver
        self.driverNameStr = tk.StringVar()
        self.nameLabel = tk.Entry(self,textvariable = self.driverNameStr)
        self.nameLabel.bind("<Return>",self.updateDriver)

        self.driverNStr = tk.StringVar()
        self.numberLabel = tk.Entry(self,textvariable = self.driverNStr,state='disabled')

        self.carName = tk.StringVar()
        self.carNameLabel = tk.Entry(self,textvariable = self.carName)
        self.carNameLabel.bind("<Return>",self.updateDriver)

        self.bind("<Configure>", self.configSize )

        self.updateDriverLabels()

    def updateDriverLabels(self):
        self.driverNameStr.set(self.driver.getDriverName())
        self.driverNStr.set(str(self.driver.getdriverNum()))
        self.carName.set(self.driver.getCarName() if self.driver.getCarName() else 'NULL')

    def updateDriver(self):
        self.driver.setDriverName(self.driverNameStr.get())
        carName = self.carName.get()
        if carName != 'NULL':
            self.driver.setCarName(carName)

    def configSize(self,_):
        w = self.winfo_width()
        h = self.winfo_height()
        xSpace = 4
        ySpace = 2
        numWidth = 35
        nameWidth = 120
        self.numberLabel.place(x=xSpace,y=ySpace,height=h-(ySpace*2),width=numWidth)
        self.nameLabel.place(x=(xSpace*2)+numWidth,y=ySpace,height = h-(ySpace*2),width = nameWidth)
        self.carNameLabel.place(x=(xSpace*3)+numWidth+nameWidth,y = ySpace,height = h-(ySpace*2),width = w-((xSpace*6)+numWidth+nameWidth))


        




class RosterViewer(tk.LabelFrame):

    def __init__(self,roster: Roster,**frameKwargs):
        
        super().__init__(**frameKwargs)
        self.roster = roster
        self.loadButton = tk.Button(self,text = "load")
        self.saveButton = tk.Button(self,text = "save")
        self.saveAsButton = tk.Button(self,text= "save as")

        self.driverEntryStr = tk.StringVar()
        self.driverEntry = tk.Entry(self,textvariable = self.driverEntryStr)
        self.driverEntry.bind("<Return>",self.toCarName)
        self.carNameStr = tk.StringVar()
        self.carNameEntry = tk.Entry(self,textvariable = self.carNameStr)
        self.carNameEntry.bind("<Return>",self.addBind)
        self.addDriverButton = tk.Button(self,text = "Add",command=self.addDriverEntry)

        self.savePath : str = None

        self.driverFrames: list[DriverInfo] = []

        self.rosterViewer = ScrollingView(self)

        self.ben = Driver(1,"ben","car2")
        self.brandyn = Driver(2,"brandyn")

        self.driverFrames.append(DriverInfo(self.rosterViewer.interiorFrame,self.ben))
        self.driverFrames.append(DriverInfo(self.rosterViewer.interiorFrame,self.brandyn))

        self.roster = Roster()

        self.bind("<Configure>", self.sizeconfig )

        for i in range(50):
            newDriver = self.roster.newdriver(f"Driver #{i}",None)
            self.driverFrames.append(DriverInfo(self.rosterViewer.interiorFrame,newDriver))


    
    def toCarName(self,_):
        self.carNameEntry.focus_set()
    
    def addBind(self,_):
        self.driverEntry.focus_set()
        self.addDriverEntry()

    def addDriverEntry(self):
        name = self.driverEntryStr.get()
        self.driverEntryStr.set("")
        carname = self.carNameStr.get()
        self.carNameStr.set("")
        if name != "":
            if(not self.roster):
                self.roster = Roster()
            newDriver = self.roster.newdriver(name,None if carname == "" else carname)
            self.driverFrames.append(DriverInfo(self.rosterViewer.frame,newDriver))

    def placeDrivers(self,w):
        
        self.rosterViewer.setInteriorSize(w-10,2+(25*len(self.driverFrames)))
        for index, driverFrame in enumerate(self.driverFrames):
            driverFrame.place(x = 10,y = 2 + 25*index,width=w-30,height=25)

    def sizeconfig(self,_):
        h = self.winfo_height()
        w = self.winfo_width()
        buttonH = 25
        buttonW = (w-40)//3
        W_5 = (w-40)//5
        self.placeDrivers(w)
        self.rosterViewer.place(x=10,y=10,height=h - ((buttonH*3)+60),width=w-20)
        

        self.driverEntry.place(x=10,y=h - buttonH*2 - 40,height = buttonH,width=(W_5*2))
        self.carNameEntry.place(x=20+(W_5*2),y=h - buttonH*2 - 40,height = buttonH,width=(W_5*2))
        self.addDriverButton.place(x=30+(W_5*4),y=h - buttonH*2 - 40,height = buttonH,width=W_5)

        self.loadButton.place(x=10,y=h - buttonH - 30,height = buttonH,width=buttonW)
        self.saveButton.place(x=20+buttonW,y=h-buttonH-30,height = buttonH,width=buttonW)
        self.saveAsButton.place(x=30+(buttonW*2),y=h-buttonH-30,height = buttonH,width=buttonW)


ROSTER_VIEWER_WIDTH = 300
FRAME_MARGIN = 10

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

        self.root.bind("<Configure>",self.configSize)


    def configSize(self,_):
        newWidth = self.root.winfo_width()
        newHeight = self.root.winfo_height() #assinging to varibles because of amount of useses
        self.updateWindowSize(newWidth,newHeight)


    def updateWindowSize(self,newW,newH):
        self.rosterViewer.place(x=newW-ROSTER_VIEWER_WIDTH-(FRAME_MARGIN*2),y=FRAME_MARGIN,height=newH-(FRAME_MARGIN*2),width=ROSTER_VIEWER_WIDTH)



class RaceControl:
    def __init__(self,):
        self.prix :Prix = None
        self.roster :Roster = None
        self.weekend : Weekend = None
        self.root = tk.Tk()
        self.gui = RaceControlGUI(self.root,self)
        self.root.mainloop()




    def exit(self):
        self.root.destroy()



def main():
    RaceControl()

if __name__ == "__main__":
    main()