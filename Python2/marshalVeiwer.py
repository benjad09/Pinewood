from cup import Cup
from prix import Race
from prix import Prix
import tkinter as tk
from scrollingView import ScrollingView


RACE_VIEW_WIDTH = 100
RACE_VIEW_ELEMENT_HEIGHT = 15
RACE_VIEW_SPACING = 5

class MarshalRaceVeiwer(tk.Frame):
    def __init__(self,master,race: Race,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.bind("<Configure>", self.configSize)
        self.race = race
        self.lanes = self.race.getLaneN()

        self.driverNvar:  list[tk.StringVar] = []
        for driverN in self.race.getDrivers():
            nString = str(driverN+1)
            self.driverNvar.append(tk.StringVar())
            self.driverNvar[-1].set(nString)

        self.resultVar: list[tk.StringVar] = []
        for resN in self.resOrNone():
            resString = str(resN) if resN else ""
            self.resultVar.append(tk.StringVar())
            self.resultVar[-1].set(resString)

        self.driverEntry: list[tk.Entry] = []
        for driverVar in self.driverNvar:
            self.driverEntry.append(tk.Entry(self,textvariable = driverVar,state=tk.DISABLED))
            

        self.resultEntry: list[tk.Entry] = []
        for resVar in self.resultVar:
            self.resultEntry.append(tk.Entry(self,textvariable= resVar))
            self.resultEntry[-1].bind("<Return>",lambda _:self.updateResult())

        self.updateRace()
        
    def resOrNone(self) -> list[int]:
        ret = self.race.getResults()
        if not ret:
            ret = [None for _ in range(self.lanes)]
        return ret
    
    def updateResult(self):
        results = []
        for res in self.resultVar:
            results.append(int(res.get()) if res.get().isnumeric() else 4.0)
        self.race.updateResults(results)
        self.updateRace()

    def updateRace(self):
        raceDrivers = self.race.getDrivers()
        raceRes = self.resOrNone()
        for index in range(self.lanes):
            self.driverNvar[index].set(str(raceDrivers[index]+1))
            self.resultVar[index].set(str(raceRes[index]) if raceRes[index] else "")


    def configSize(self,_):
        w = self.winfo_width()
        h = self.winfo_height()
        wLane = w//self.lanes
        hElem = h//2
        for laneN in range(self.lanes):
            self.driverEntry[laneN].place(x = laneN*wLane,y=0,width=wLane,height=hElem)
            self.resultEntry[laneN].place(x = laneN*wLane,y=hElem,width=wLane,height=hElem)



RACE_SAVE_HEIGHT = 200

class MarshalBoard(tk.LabelFrame):
    def __init__(self,master,cup: Cup,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.cup = cup

        self.raceViewer = ScrollingView(self)
        self.raceViewer.place(relx=0.0,rely=0.0,relwidth=1.0,relheight=1.0)
        self.raceVeiwes : list[MarshalRaceVeiwer] = []

        self.roundLabels : list[tk.Label] = []
        self.laneLabels : list[tk.Label] = []
        self.heatLabels : list[tk.Label] = []

    def drawPrix(self):
        for raceVeiw in self.raceVeiwes:
            raceVeiw.place_forget()
        for roundL in self.roundLabels:
            roundL.place_forget()
        for heatL in self.heatLabels:
            heatL.place_forget()
        for laneL in self.laneLabels:
            laneL.place_forget()
        if(not self.cup.haveCurrentPrix()):
            return
        
        self.roundLabels : list[tk.Label] = []
        self.laneLabels : list[tk.Label] = []
        self.heatLabels : list[tk.Label] = []
        prix = self.cup.getCurrentPrix()
        prixRounds = prix.getRoundN()
        heatsPerRound = [prix.getHeatsInRound(round) for round in range(prixRounds)]
        maxHeats = max(heatsPerRound)
        self.raceViewer.setInteriorSize((prixRounds+1)*(RACE_VIEW_SPACING+RACE_VIEW_WIDTH),(maxHeats+1)*(RACE_VIEW_SPACING+RACE_VIEW_ELEMENT_HEIGHT*2))
        for roundN in range(prixRounds):
            self.roundLabels.append(tk.Label(self.raceViewer.interiorFrame,text=f"Round {roundN+1}"))
            self.roundLabels[-1].place(x=(roundN+1)*(RACE_VIEW_SPACING+RACE_VIEW_WIDTH),y = (RACE_VIEW_SPACING),width=RACE_VIEW_WIDTH,height=(RACE_VIEW_ELEMENT_HEIGHT))
        for heatN in range(maxHeats):
            self.heatLabels.append(tk.Label(self.raceViewer.interiorFrame,text=f"Heat {heatN+1}"))
            self.heatLabels[-1].place(x=RACE_VIEW_SPACING,y=(RACE_VIEW_SPACING + RACE_VIEW_ELEMENT_HEIGHT*2)*(heatN+1),width=RACE_VIEW_WIDTH,height=(RACE_VIEW_ELEMENT_HEIGHT))
        self.laneLabels.append(tk.Label(self.raceViewer.interiorFrame,text=f"lane"))
        self.laneLabels[-1].place(x=RACE_VIEW_SPACING,y=RACE_VIEW_ELEMENT_HEIGHT+RACE_VIEW_SPACING,width=RACE_VIEW_WIDTH,height=(RACE_VIEW_ELEMENT_HEIGHT))
        lanes = prix.lanes
        lane_spaceing = RACE_VIEW_WIDTH//lanes
        print(lane_spaceing)
        for roundN in range(prixRounds):
            for laneN in range(lanes):
                #print(f"lane {laneN+1}")
                self.laneLabels.append(tk.Label(self.raceViewer.interiorFrame,text=f"{laneN+1}"))
                self.laneLabels[-1].place(x=(RACE_VIEW_SPACING+RACE_VIEW_WIDTH)*(roundN+1)+(lane_spaceing*laneN),y=RACE_VIEW_ELEMENT_HEIGHT+RACE_VIEW_SPACING,width=lane_spaceing,height=(RACE_VIEW_ELEMENT_HEIGHT))
        


        for round,heats in enumerate(heatsPerRound):
            for heat in range(heats):
                #print(f"r {round}, h {heat}")
                self.raceVeiwes.append(MarshalRaceVeiwer(self.raceViewer.interiorFrame,prix.getRace(round,heat)))
                self.raceVeiwes[-1].place(x=(RACE_VIEW_SPACING+RACE_VIEW_WIDTH)*(round+1),y=(RACE_VIEW_SPACING + RACE_VIEW_ELEMENT_HEIGHT*2)*(heat+1),width=RACE_VIEW_WIDTH,height=(RACE_VIEW_ELEMENT_HEIGHT*2))



class MarshalVeiwer(tk.LabelFrame):
    def __init__(self,master,cup: Cup,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.cup = cup
        self.raceTable = MarshalBoard(self,cup,text="Races")
        

        
        self.bind("<Configure>",lambda _: self.configSize())


    def drawPrix(self):
        self.raceTable.drawPrix()
        

    def configSize(self):
        h = self.winfo_height()
        w = self.winfo_width()
        self.raceTable.place(x=10,y=10,height=h-40,width=w-40)



# RACE_VIEW_WIDTH = 100
# RACE_VIEW_HEIGHT = 40


