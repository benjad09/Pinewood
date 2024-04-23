import tkinter as tk
from tkinter import Misc, ttk

from appVC import appViewFunctions,appControlFunctions
from mainApp import MainApp

from Roster import Driver,Roster
from Prix import Race

from commandLineVersion import CommandLineViewer


WINDOW_NAME = "Derby Racers"
FONT_SIZE = 10
GUIXSIZE = 1200
GUIYSIZE = 820

GUIMINXSIZE = 950
GUIMINYSIZE = 550

GUIXSIZE = GUIMINXSIZE
GUIYSIZE = GUIMINYSIZE



    # def checkWindowSize(self):
    #     newWidth = self.root.winfo_width()
    #     newHeight = self.root.winfo_height() #assinging to varibles because of amount of useses
    #     if(newWidth != self.windowWidth or newHeight != self.windowHeight):
    #         self.windowWidth = newWidth
    #         self.windowHeight = newHeight
    #         self.updateWindowSize(newWidth,newHeight)
    #     self.root.after(33,self.checkWindowSize) #Check window sizing at ~30Hz

    # def updateWindowSize(self,newW,newH):
    #     frameWidth = newW-460
    #     #frameWidth = 490
    #     frameHeight = newH-20
    #     #self.jobframe.place_forget()
    #     self.remotejobsframe.place(x=450,y=10,height=frameHeight,width=frameWidth)
    #     frameHeight = newH-290
    #     self.jobViewerFrame.place(x=10,y=280,height=frameHeight,width=430)





        # frame = tk.Label(self,text=driver.getDriverName())
        # frame.pack()


class RaceViewer(tk.LabelFrame):
    def __init__(self,master,race :Race,roster :Roster,**kwargs):
        super().__init__(master = master, width = 600, height = 250,**kwargs)
        bylane = race.getRacers()
        spaceing = [0,200,400]
        raceInfoLabel = tk.Label(self,text=f"Race #{race.getN()+1}, Round #{race.getRound()+1}, Heat #{race.getHeat()+1}")
        raceInfoLabel.place(x=0,y=0,width=500,height=25)
        for i in range(3):
            driverFrames = self.DriverViewer(self,roster.getDriver(bylane[i]),text = f"lane{i+1}")
            driverFrames.place(x=spaceing[i],y=25,width=190,height=100)

    class DriverViewer(tk.LabelFrame):
        def __init__(self,master,driver :Driver,**kwargs):
            DEFAULTWIDTH = 200
            super().__init__(master = master,width = DEFAULTWIDTH,height = 75,**kwargs)

            
            #self.DriverL = 
            self.DriverL = tk.Label(self,text="Driver: ",anchor='e')
            
            self.Driver =  tk.Label(self,text=driver.getDriverName(),anchor='w')
            
            #
            self.carName = driver.getCarName()
            if self.carName is not None:
                self.carL = tk.Label(self,text="Is Driving: ",anchor='e')
                
                self.car = tk.Label(self,text=self.carName,anchor='w')
                
            self.driverNL = tk.Label(self,text = f"Driver #: ",anchor='e')
            
            self.driverN = tk.Label(self,text = f"{driver.getDriverNumber()+1}",anchor='w')
            

        def place(self,**kwargs):
            width = kwargs["width"]-10
            labelWidth = 50
            self.DriverL.place(x = 5,y=0,height = 25,width=labelWidth)
            self.Driver.place(x = labelWidth,y=0,height = 25,width=width-labelWidth)


            if(self.carName is not None):
                self.carL.place(x = 5,y=25,height = 25,width=labelWidth)
                self.car.place(x = labelWidth,y=25,height = 25,width=width-labelWidth-5)

            self.driverNL.place(x = 5,y=50,height = 25,width=labelWidth)
            self.driverN.place(x = labelWidth,y=50,height = 25,width=width-labelWidth-5)
            
            super().place(**kwargs)


class RosterVeiwer(tk.LabelFrame):
    def __init__(self,master,roster:Roster,**kwargs):
        super().__init__(master = master,**kwargs)

        self.roster = roster

        self.scrollingViews = ScrollingView(self)

        self.haveLabel = False

    def addRacer(self,n):
        if(not self.haveLabel):
            self.haveLabel = True
            self.RacerLabeler(self.scrollingViews.frame).pack()
            self.scrollingViews.added_frame(175,25)
        racer = self.RacerViewer(self.scrollingViews.frame,self.roster.getDriver(n))
        racer.pack()
        self.scrollingViews.added_frame(175,25)

        
    
            

        # self.driverList = []
    class RacerLabeler(tk.Frame):
        def __init__(self,master,**kwargs):
            super().__init__(master = master,width=175,height=25,**kwargs)
            tk.Label(self,text = "#").place(x=0,y=0,width=25,height=25)
            tk.Label(self,text = "Name").place(x=25,y=0,width=75,height=25)
            tk.Label(self,text = "Car").place(x=100,y=0,width=75,height=25)
        


    class RacerViewer(tk.Frame):
        def __init__(self,master,driver :Driver,**kwargs):
            super().__init__(master = master,width=175,height=25,**kwargs)
            self.numlabel = tk.Label(self,text = f"#{driver.getDriverNumber()+1}")
            self.nameVar = tk.StringVar()
            self.nameVar.set(driver.getDriverName())
            self.nameEntry = tk.Entry(self,state='disabled',textvariable = self.nameVar)
            self.CarVar = tk.StringVar()
            self.CarVar.set("*" if driver.getCarName() is None else driver.getCarName())
            self.CarEntry = tk.Entry(self,state='disabled',textvariable = self.CarVar)

            self.numlabel.place(x=0,y=0,width=25,height=25)
            self.nameEntry.place(x=25,y=0,width=75,height=25)
            self.CarEntry.place(x=100,y=0,width=75,height=25)

            


        

class RaceResultViewer(tk.LabelFrame):
    def __init__(self,master,race:Race,controller: appControlFunctions,**kwargs):
        super().__init__(master = master,width=150,height=75,**kwargs)
        tk.Label(self,text = f"Race #{race.getN()+1}",anchor='e').place(x=0,y=12,width = 50,height=25)
        tk.Label(self,text = f"R{race.getRound()+1} H{race.getHeat()+1}",anchor='e').place(x=0,y=37,width = 50,height=25)



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






resultList = [[1,2,3],[1,3,2],[3,2,1],[1,2,3],[1,3,2],
              [1,3,2],[2,3,1],[1,2,3],[1,2,3],[1,3,2],
              [1,2,3],[3,1,2],[2,1,3],[2,1,3],[1,3,2],
              [2,1,3],[3,1,2],[3,2,1],[3,2,1],[2,3,1],
              [2,3,1],[3,1,2],[1,2,3],[3,1,2],[2,1,3],
              [2,1,3],[1,3,2],[3,2,1],[2,1,3],[2,1,3]]

class appGUI:
    def __init__(self, root: tk.Tk,viewer :appViewFunctions,controller: appControlFunctions):
        self.root = root
        self.root.wm_title(WINDOW_NAME)

        self.controller=controller
        self.resultN = 0

        viewer.registerCb(self.updateQue,self.updateResults,self.updateRaceResults,
                        self.updateRoster,self.updateFilePath,self.updateLeaderBoard)

        self.screen_w = int(self.root.winfo_screenwidth())
        self.screen_h = int(self.root.winfo_screenheight())
        #self.default_geometry = str(GUIXSIZE)+"x"+str(GUIYSIZE)+"+"+str(int(self.screen_w/4))+"+"+str(int(self.screen_h/4))
        #self.root.geometry(self.default_geometry)
        self.root.state("zoomed")
        self.root.minsize(width=GUIMINXSIZE,height=GUIMINYSIZE)

        self.RaceQUE : "list[RaceViewer]"= []

        self.racerQueframe = tk.LabelFrame(self.root,text = "Que")
        self.racerQueframe.place(x=0,y=0,width = 750,height=1000)

        self.rosterFrame = tk.LabelFrame(self.root,text = "Roster")
        self.rosterFrame.place(x=750,y=0,width = 300,height=1000)

        self.resultsFrame = tk.LabelFrame(self.root,text= "results")
        self.resultsFrame.place(x=950,y=0,width = 200,height=500)
        self.resultsviewerframe = ScrollingView(self.resultsFrame)

        self.leaderBoard : "list[Driver]" = []

        self.root.after(2000,self.pushNext)
        #self.root.protocol('WM_DELETE_WINDOW', self.controller.exit)


    def pushNext(self):
        if self.resultN < len(resultList):
            self.controller.pushRaceResult(resultList[self.resultN])
            self.resultN = self.resultN+1

        self.root.after(2000,self.pushNext)

    def checkWindowSize(self):
        newWidth = self.root.winfo_width()
        newHeight = self.root.winfo_height() #assinging to varibles because of amount of useses
        if(newWidth != self.windowWidth or newHeight != self.windowHeight):
            self.windowWidth = newWidth
            self.windowHeight = newHeight
            self.updateWindowSize(newWidth,newHeight)
        self.root.after(33,self.checkWindowSize) #Check window sizing at ~30Hz


    def updateWindowSize(self,newW,newH):
        pass
        self.resultsFrame.place(x=950,y=0,width = 200,height=500)


        
    def printResults(self):
        index = 1
        for i in self.leaderlist:
            racer = self.roster.getDriver(i)
            print(f"#{index}: {racer.getDriverName()} {racer.getDriverScore()}")
            index = index+1


    def updateQue(self,raceList : "list[Race]",lenOfQue : int):
        for item in self.RaceQUE:
            item.pack_forget()

        self.RaceQUE = []
        raceNames = ["Current","OnDeck","In the Hole"]

        for i in range(min(lenOfQue,3)):
            self.RaceQUE.append(RaceViewer(self.racerQueframe,raceList[i],self.roster,text=raceNames[i]))
            self.RaceQUE[-1].pack()


        
    def updateResults(self,races : "list[Race]",lastResult : int):
        # self.resultsFrame.place_forget()
        # self.resultsFrame = tk.LabelFrame(self.root,text="results")
        # self.resultsFrame.place(x=950,y=0,width = 200,height=1000)
        
        for race in races:
            RaceResultViewer(self.resultsviewerframe.frame,race,self.controller).pack()
            self.resultsviewerframe.added_frame(175,75)

        
        pass

    def updateRaceResults(self,posByLane : "list[int]"):
        print(f"lane 1:{posByLane[0]}, lane 2:{posByLane[1]}, lane 3:{posByLane[2]}")
        
    def updateRoster(self,roster :Roster):
        print("updating roster")
        self.roster = roster
        self.rosterFrame.place_forget()
        self.rosterFrame = RosterVeiwer(self.root,self.roster,text = "Roster")
        self.rosterFrame.place(x=750,y=0,width = 200,height=250)
        for racer in roster.getIntDriverList():
            self.rosterFrame.addRacer(racer)
        
    def updateFilePath(self,mainFolder,pathtoprix,pathtoroster):
        print(f"main folder:{mainFolder}")
        print(f"prix: {pathtoprix}")
        print(f"roster: {pathtoroster}")
        
    def updateLeaderBoard(self,drivers: "list[Driver]",len):
        self.leaderlist = drivers


def main():
    view = appViewFunctions()
    viewText = appViewFunctions()
    controller = appControlFunctions()
    #CommandLineViewer(viewText)
    MainApp(controller,[view,viewText])

    root = tk.Tk()

    appGUI(root,view,controller)
    
    #cmveiwer = CommandLineViewer(controller,view)
    controller.upatedMainFolder("./TestClub2024")

    controller.updateRosterFile("./TestClub2024/15DriverRoster.csv")
    controller.loadRoster()

    # controller.addRacer("Bob","Bobs car")
    # controller.addRacer("Dave")
    # controller.addRacer("Warren")
    # controller.saveRoster()

    controller.generateMagicPrix()


    

    root.mainloop()


if __name__ == "__main__":
    main()