
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





class RosterViewer(tk. LabelFrame):
    class DriverInfo(tk.Frame):
        def __init__(self,driver: Driver,**frameKwargs):
            super().__init__(**frameKwargs)
            self.driver = driver
            self.driverNameStr = tk.StringVar()
            self.nameLabel = tk.Entry(self,textvariable = self.driverNameStr)
            self.nameLabel.bind("<Return>",self.updateDriver)

            self.driverNStr = tk.StringVar()
            self.numberLabel = tk.Entry(self,textvariable = self.driverNStr,state='disabled')

            self.carName = tk.StringVar()
            self.carNameLabel = tk.Entry(self,textvariable = self.carName)
            self.carNameLabel.bind("<Return>",self.updateDriver)

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

        def place(self,**placeArgs):
            super().place(placeArgs)
            xSpace = 4
            ySpace = 4
            numWidth = 35
            nameWidth = 120
            w = placeArgs["width"]
            h = placeArgs["height"]
            self.numberLabel.place(x=xSpace,y=ySpace,height=h-(ySpace*2),width=numWidth)
            self.nameLabel.place(x=(xSpace*2)+numWidth,y=ySpace,height = h-(ySpace*2),width = nameWidth)
            self.carNameLabel.place(x=(xSpace*3)+numWidth+nameWidth,y = ySpace,height = h-(ySpace*2),width = w-((xSpace*4)+numWidth+nameWidth))






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

        # self.ben = Driver(1,"ben","car2")
        # self.brandyn = Driver(2,"brandyn")
        # self.bensLabel = self.DriverInfo(self.ben,master = self)
        # self.brandynLabel = self.DriverInfo(self.brandyn,master = self)


    
    def toCarName(self,_):
        self.carNameEntry.focus_set()
    
    def addBind(self,_):
        self.carNameEntry.focus_set()
        self.addDriverEntry()

    def addDriverEntry(self):
        name = self.driverEntryStr.get()
        self.driverEntryStr.set("")
        carname = self.carNameStr.get()
        self.carNameStr.set("")
        if name != "":
            if(not self.roster):
                self.roster = Roster()
            self.roster.newdriver(name,None if carname == "" else carname)
        
    
    def place(self,**placeArgs):
        super().place(placeArgs)
        w = placeArgs["width"]
        h = placeArgs["height"]
        print(f"windowH2 {h}")
        buttonH = 25
        buttonW = (w-40)//3
        W_5 = (w-40)//5
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


        self.windowWidth = self.root.winfo_width()
        self.windowHeight = self.root.winfo_height()
        self.checkWindowSize() #this will exicute on startup because it turns out that we dont have a window size until we start


    def checkWindowSize(self):
        newWidth = self.root.winfo_width()
        newHeight = self.root.winfo_height() #assinging to varibles because of amount of useses
        if(newWidth != self.windowWidth or newHeight != self.windowHeight):
            self.windowWidth = newWidth
            self.windowHeight = newHeight
            self.updateWindowSize(newWidth,newHeight)
        self.root.after(33,self.checkWindowSize) #Check window sizing at ~30Hz

    def updateWindowSize(self,newW,newH):
        print(f"windowH {newH}")
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