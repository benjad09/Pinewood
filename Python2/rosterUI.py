import tkinter as tk
from scrollingView import ScrollingView
from tkinter import filedialog

from roster import Roster
from roster import Driver


class DriverInfo(tk.Frame):
    def __init__(self,root,driver: Driver,removeDriverCb,**frameKwargs):
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

        self.removeDriverCb = removeDriverCb

        self.deleteButton = tk.Button(self,text="X",bg="red",command=lambda N=self.driver.getdriverNum():self.removeDriverCb(N))

        self.bind("<Configure>", self.configSize )

        self.updateDriverLabels()

    def disableDel(self):
        self.deleteButton.config(state="disable")
        
    def enableDel(self):
        self.deleteButton.config(state="active")

    def updateDriverLabels(self):
        self.driverNameStr.set(self.driver.getDriverName())
        self.driverNStr.set(str(self.driver.getdriverNum()))
        self.carName.set(self.driver.getCarName() if self.driver.getCarName() else 'NULL')

    def updateDriver(self,_):
        self.driver.setDriverName(self.driverNameStr.get())
        carName = self.carName.get()
        if carName != 'NULL':
            self.driver.setCarName(carName)

    def configSize(self,_):
        w = self.winfo_width()
        h = self.winfo_height()
        xSpace = 4
        ySpace = 2
        delSpace = 15
        numWidth = 35
        nameWidth = 120
        self.deleteButton.place(x=xSpace,y=ySpace,height=h-(ySpace*2),width=delSpace)
        self.numberLabel.place(x=xSpace*2+delSpace,y=ySpace,height=h-(ySpace*2),width=numWidth)
        self.nameLabel.place(x=(xSpace*3)+numWidth+delSpace,y=ySpace,height = h-(ySpace*2),width = nameWidth)
        self.carNameLabel.place(x=(xSpace*4)+numWidth+nameWidth+delSpace,y = ySpace,height = h-(ySpace*2),width = w-((xSpace*5)+numWidth+nameWidth))


        




class RosterViewer(tk.LabelFrame):

    def __init__(self,roster: Roster,**frameKwargs):
        
        super().__init__(**frameKwargs)
        self.roster = roster
        self.loadButton = tk.Button(self,text = "load",command=self.loadRosterButton)
        self.saveButton = tk.Button(self,text = "save",command=self.saveRoster)
        self.saveAsButton = tk.Button(self,text= "save as",command=self.saveAsRoster)

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

        self.roster = Roster()

        #self.roster = Roster()

        self.bind("<Configure>", self.configSize )


    def loadRosterButton(self):
        newpath = filedialog.askopenfilename(title="Select Roster",filetypes=[("csv", "*.csv")])
        if newpath != '':
            self.loadRoster(newpath)

    def loadRoster(self,path):
        self.savePath = path
        self.roster.clearRoster()
        self.roster.load(path)
        self.createFramesFromRoster()

    def enableEditing(self):
        self.carNameEntry.config(state='active')
        self.driverEntry.config(state='active')
        self.addDriverButton.config(state='active')
        for driverViewer in self.driverFrames:
            driverViewer.enableDel()
    
    def disableEditing(self):
        self.carNameEntry.config(state="disabled")
        self.driverEntry.config(state='disabled')
        self.addDriverButton.config(state='disabled')
        for driverViewer in self.driverFrames:
            driverViewer.disableDel()

            

    def saveRoster(self):
        if(self.savePath):
            for driverFrame in self.driverFrames:
                driverFrame.updateDriver()
            self.roster.save(self.savePath)
        else:
            self.saveAsRoster()

    def saveAsRoster(self):
        newpath = filedialog.asksaveasfilename(title="Save Roster As",defaultextension=".csv",filetypes=[("csv", "*.csv")])
        if newpath != '':
            self.savePath = newpath
            self.saveRoster()
    
    def toCarName(self,_):
        self.carNameEntry.focus_set()
    
    def addBind(self,_):
        self.driverEntry.focus_set()
        self.addDriverEntry()

    def createFramesFromRoster(self):
        self.driverFrames = []
        for driver in self.roster.getAllDrivers():
            self.driverFrames.append(DriverInfo(self.rosterViewer.interiorFrame,driver,self.removeDriver))
        self.placeDrivers()


    def addDriverEntry(self):
        name = self.driverEntryStr.get()
        self.driverEntryStr.set("")
        carname = self.carNameStr.get()
        self.carNameStr.set("")
        if name != "":
            newDriver = self.roster.newdriver(name,None if carname == "" else carname)
            self.driverFrames.append(DriverInfo(self.rosterViewer.interiorFrame,newDriver,self.removeDriver))
        self.placeDrivers()

    def removeDriver(self,N):
        self.roster.removeDriver(N)
        self.createFramesFromRoster()

    def placeDrivers(self):
        w = self.winfo_width()-20
        self.rosterViewer.setInteriorSize(w-10,2+(25*len(self.driverFrames)))
        for index, driverFrame in enumerate(self.driverFrames):
            driverFrame.place(x = 10,y = 2 + 25*index,width=w-30,height=25)

    def configSize(self,_):
        h = self.winfo_height()
        w = self.winfo_width()
        buttonH = 25
        buttonW = (w-40)//3
        W_5 = (w-40)//5
        self.placeDrivers()
        self.rosterViewer.place(x=10,y=10,height=h - ((buttonH*3)+60),width=w-20)
        

        self.driverEntry.place(x=10,y=h - buttonH*2 - 40,height = buttonH,width=(W_5*2))
        self.carNameEntry.place(x=20+(W_5*2),y=h - buttonH*2 - 40,height = buttonH,width=(W_5*2))
        self.addDriverButton.place(x=30+(W_5*4),y=h - buttonH*2 - 40,height = buttonH,width=W_5)

        self.loadButton.place(x=10,y=h - buttonH - 30,height = buttonH,width=buttonW)
        self.saveButton.place(x=20+buttonW,y=h-buttonH-30,height = buttonH,width=buttonW)
        self.saveAsButton.place(x=30+(buttonW*2),y=h-buttonH-30,height = buttonH,width=buttonW)
