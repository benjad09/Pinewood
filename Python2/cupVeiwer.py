from cup import Cup
from roster import Driver
from prix import Prix
import tkinter as tk
from scrollingView import ScrollingView
from tkinter import messagebox
from ordinal import getOrdinal

RACEVEIWSPACEING = 5


class RaceVeiwer(tk.Frame):
    def __init__(self,master,cup: Cup,raceN: int,fontSize:int,displayDriverNumbers=True,displayCarNames=False,displayResults=True,carLeadIn="",**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.cup = cup
        self.master = master
        prix = self.cup.getCurrentPrix()
        self.race = prix.getRaceByN(raceN)
        round,heat = prix.getRoundAndHeat(raceN)
        self.drivers: list[Driver] = self.cup.getRaceDrivers(self.race)
        self.raceName = tk.Label(self,anchor='w',text = "",font=("Arial",fontSize))
        self.roundAndHeatLabel = tk.Label(self,anchor='e',text = f"Round: {round+1} Heat: {heat + 1}",font=("Arial",fontSize))
        self.lanes = self.race.getLaneN()
        self.laneLabels : list[tk.Label] = [tk.Label(self,anchor='w',text = f"Lane {laneN+1}",font=("Arial",fontSize)) for laneN in range(self.lanes)]
        driverNamesStr = [driver.getDriverName() for driver in self.drivers]
        driverNumStr = [str(driver.getdriverNum() + 1) for driver in self.drivers]
        carNameString = [driver.getCarName() for driver in self.drivers]
        self.displayCarName = displayCarNames
        self.displayResults = displayResults

        


        if(displayDriverNumbers):
            self.driverLabels : list[tk.Label] = [tk.Label(self,anchor='w',text=f"{driverNamesStr[laneN]} #{driverNumStr[laneN]}",font=("Arial",fontSize)) for laneN in range(self.lanes)]
        else:
            self.driverLabels : list[tk.Label] = [tk.Label(self,anchor='w',text=f"{driverNamesStr[laneN]}",font=("Arial",fontSize)) for laneN in range(self.lanes)]
        self.resultLabels : list[tk.Label] = [tk.Label(self,anchor='w',text=f"",font=("Arial",fontSize)) for laneN in range(self.lanes)]

        self.carLabels : list[tk.Label] = [tk.Label(self,anchor='w',text = f"{carLeadIn}{carname}" if carname else "",font=("Arial",fontSize)) for carname in carNameString]

        self.bind("<Configure>", self.configSize )

    def updatePrix(self):
        res = self.race.getResults()
        if res:
            for index,result in enumerate(res):
                self.resultLabels[index].config(text = f"Finished {result}{getOrdinal(result)}")
        pass

    def setRaceName(self,name):
        self.raceName.config(text = name)

    def setBgColor(self,bgcolor):
        self.config(bg = bgcolor)
        self.raceName.config(bg=bgcolor)
        self.roundAndHeatLabel.config(bg = bgcolor)
        for label in self.laneLabels:
            label.config(bg = bgcolor)
        for label in self.driverLabels:
            label.config(bg = bgcolor)
        for label in self.resultLabels:
            label.config(bg = bgcolor)
        for label in self.carLabels:
            label.config(bg = bgcolor)
        


    def configSize(self,_):
        h = self.winfo_height()
        w = self.winfo_width()
        nLabels = 3 + (1 if self.displayCarName else 0) + (1 if self.displayResults else 0)
        #print(nLabels)
        resultSpaceing = 4 if self.displayCarName else 3

        laneSpaceing = (w-((self.lanes+1)*RACEVEIWSPACEING))//self.lanes
        hSpaceing = (h-(RACEVEIWSPACEING*(nLabels+1)))//nLabels
        self.roundAndHeatLabel.place(x=w//2,y=RACEVEIWSPACEING,width=(w//2-RACEVEIWSPACEING),height=hSpaceing)
        self.raceName.place(x=RACEVEIWSPACEING,y=RACEVEIWSPACEING,width=(w//2-RACEVEIWSPACEING),height=hSpaceing)
        for laneN in range(self.lanes):
            self.laneLabels[laneN].place(x=(RACEVEIWSPACEING+(RACEVEIWSPACEING+laneSpaceing)*laneN),y=RACEVEIWSPACEING*2+hSpaceing,width=laneSpaceing,height=hSpaceing)
            self.driverLabels[laneN].place(x=(RACEVEIWSPACEING+(RACEVEIWSPACEING+laneSpaceing)*laneN),y=RACEVEIWSPACEING*3+hSpaceing*2,width=laneSpaceing,height=hSpaceing)
            if self.displayCarName:
                self.carLabels[laneN].place(x=(RACEVEIWSPACEING+(RACEVEIWSPACEING+laneSpaceing)*laneN),y=RACEVEIWSPACEING*4+hSpaceing*3,width=laneSpaceing,height=hSpaceing)
            if self.displayResults:
                self.resultLabels[laneN].place(x=(RACEVEIWSPACEING+(RACEVEIWSPACEING+laneSpaceing)*laneN),y=RACEVEIWSPACEING*(resultSpaceing+1)+hSpaceing*(resultSpaceing),width=laneSpaceing,height=hSpaceing)



SPACING = 5

class CupVeiwer(tk.Frame):
    def __init__(self,master,cup: Cup,fontSize: int = 16,displayDriverNumbers=True,displayCarNames=False,displayResults=True,raceFrameH=200,veiwLag = 1,carLeadIn="",**kwargsFrame):
        super().__init__(master,**kwargsFrame)
        self.cup = cup
        self.displayDriverNums = displayDriverNumbers
        self.veiwlag = veiwLag

        self.displayCarNames = displayCarNames
        self.displayResults = displayResults
        self.carLeadIn = carLeadIn

        self.fontSize = fontSize
        self.raceFrames : list[RaceVeiwer] = []
        self.frame = ScrollingView(self)
        self.frame.place(relx=0,rely=0,relwidth=1,relheight=1)
        self.raceHeight = raceFrameH
        
        self.spaceing = 5

        self.PCFcolors = ["gray","green","yellow"]
        
        self.bind("<Configure>", self.configSize )

    def drawPrix(self):
        for raceFrame in self.raceFrames:
            raceFrame.place_forget()
        if(not self.cup.haveCurrentPrix()):
            return
        self.raceFrames : list[RaceVeiwer] = []
        w = self.winfo_width()
        self.frame.setVeiw(0,0)
        totalRaces = self.cup.getCurrentPrix().getTotalRaces()
        self.frame.setInteriorSize(w-10,(totalRaces*(self.spaceing+self.raceHeight)+self.spaceing))
        for raceN in range(totalRaces):
            self.raceFrames.append(RaceVeiwer(self.frame.interiorFrame,self.cup,raceN,self.fontSize,displayDriverNumbers=self.displayDriverNums,displayCarNames=self.displayCarNames,displayResults=self.displayResults,carLeadIn=self.carLeadIn))
            self.raceFrames[-1].place(x=self.spaceing,y=(raceN)*(self.spaceing+self.raceHeight),width=w-(self.spaceing*2)-10,height=self.raceHeight)

        self.updatePrix()

    def getnameAndColorByPosition(self,index,onRace) -> tuple[str,str]:
        diff = onRace-index
        if(diff == 0):
            return ("Current",self.PCFcolors[1])
        if(diff == -1):
            return ("Next",self.PCFcolors[2])
        if(diff == 1):
            return ("Last",self.PCFcolors[0])
        if(diff < 0):
            return (f"Up in {diff*-1}",self.PCFcolors[2])
        else:
            return (f"Race {index+1}",self.PCFcolors[0])



    def updatePrix(self):
        if(self.cup.haveCurrentPrix()):
            

            onRace = self.cup.getOnRace()
            self.frame.setVeiw(0,(onRace-self.veiwlag)*(SPACING+self.raceHeight))
            for index,raceFrame in enumerate(self.raceFrames):
                raceFrame.updatePrix()
                info = self.getnameAndColorByPosition(index,onRace)
                raceFrame.setRaceName(info[0])
                raceFrame.setBgColor(info[1])
        


    def configSize(self,_):
        pass
    



    


    