from cup import Cup
from prix import Race
from prix import Prix
import tkinter as tk
from scrollingView import ScrollingView
from tkinter import messagebox
from ordinal import getOrdinal

RACE_VIEW_WIDTH = 100
RACE_VIEW_ELEMENT_HEIGHT = 15
RACE_VIEW_SPACING = 5
RACE_SAVE_HEIGHT = 200

FONT_SIZE = 12 

class MarshalRaceVeiwer(tk.Frame):
    def __init__(self,master,race: Race,raceUpdatedCB,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.bind("<Configure>", self.configSize)
        self.race = race
        self.lanes = self.race.getLaneN()
        self.raceUpdatedCB = raceUpdatedCB

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
            self.driverEntry.append(tk.Entry(self,textvariable = driverVar,state=tk.DISABLED,font=("Arial", FONT_SIZE)))
            

        self.resultEntry: list[tk.Entry] = []
        for resVar in self.resultVar:
            self.resultEntry.append(tk.Entry(self,textvariable= resVar,font=("Arial", FONT_SIZE)))
            self.resultEntry[-1].bind("<Return>",lambda _:self.manualUpdate(_))

        self.updateRace()
        
    def resOrNone(self) -> list[int]:
        ret = self.race.getResults()
        if not ret:
            ret = [None for _ in range(self.lanes)]
        return ret
    
    def manualUpdate(self,_):
        self.updateResult()
        self.raceUpdatedCB()
    
    def updateResult(self):
        results = []
        for res in self.resultVar:
            results.append(int(res.get()) if res.get().isnumeric() else None)
        if None not in results:
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


class MarshalBoard(tk.LabelFrame):
    def __init__(self,master,cup: Cup,raceUpdatedCB,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.cup = cup
        self.raceUpdatedCB = raceUpdatedCB
        self.raceViewer = ScrollingView(self)
        self.raceViewer.place(relx=0.0,rely=0.0,relwidth=1.0,relheight=1.0)
        self.raceVeiwes : list[MarshalRaceVeiwer] = []

        self.roundLabels : list[tk.Label] = []
        self.laneLabels : list[tk.Label] = []
        self.heatLabels : list[tk.Label] = []

    def updatePrix(self):
        for raceView in self.raceVeiwes:
            raceView.updateResult()

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
        lanes = prix.getNumLanes()
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
                self.raceVeiwes.append(MarshalRaceVeiwer(self.raceViewer.interiorFrame,prix.getRace(round,heat),self.raceUpdatedCB))
                self.raceVeiwes[-1].place(x=(RACE_VIEW_SPACING+RACE_VIEW_WIDTH)*(round+1),y=(RACE_VIEW_SPACING + RACE_VIEW_ELEMENT_HEIGHT*2)*(heat+1),width=RACE_VIEW_WIDTH,height=(RACE_VIEW_ELEMENT_HEIGHT*2))

class racePusher(tk.LabelFrame):
    def __init__(self,master,cup: Cup,prixUpdateCb,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.laneLabels: list[tk.Label] = []
        self.resultLabel: tk.Label = tk.Label(self,text="results")
        self.laneText: tk.Label = tk.Label(self,text="lane")
        self.resultVars: list[tk.StringVar] = []
        self.resultEntry: list[tk.Entry] = []
        self.pushButton = tk.Button(self,text="push",command=self.pushResults)
        self.havePrix = False
        self.cup = cup
        self.prixUpdateCb = prixUpdateCb


        self.bind("<Configure>",lambda _: self.configSize())

    
    def drawPrix(self):
        for resEntery in self.resultEntry:
            resEntery.place_forget()

        for laneL in self.laneLabels:
            laneL.place_forget()

        self.laneText.place_forget()
        self.resultLabel.place_forget()
        self.pushButton.place_forget()
        self.havePrix = False
        if(not self.cup.haveCurrentPrix()):
            return
        self.havePrix = True
        
        self.resultVars: list[tk.StringVar] = []
        self.resultEntry: list[tk.Entry] = []
        self.laneLabels: list[tk.Label] = []

        prix = self.cup.getCurrentPrix()
        lanes = prix.getNumLanes()
        for lane in range(lanes):
            self.laneLabels.append(tk.Label(self,text=f"{lane+1}"))
            self.resultVars.append(tk.StringVar())
            self.resultVars[lane].set("")
            self.resultEntry.append(tk.Entry(self,textvariable=self.resultVars[lane]))
        self.configSize()



    def configSize(self):
        h = self.winfo_height()-20 #this will come back to byte me
        w = self.winfo_width()-20
        wSpacing = w//3
        hSpacing = h//3
        if(self.havePrix):
            prix = self.cup.getCurrentPrix()
            lanes = prix.getNumLanes()
            self.laneText.place(x = 0,y = 0,height=hSpacing,width=wSpacing)
            self.resultLabel.place(x = 0,y = hSpacing,height=hSpacing,width=wSpacing)
            self.pushButton.place(x = 0,y=hSpacing*2,height=hSpacing,width=w)
            laneSpaceing = ((wSpacing*2))//lanes
            print(laneSpaceing)
            for index in range(lanes):
                self.laneLabels[index].place(x=wSpacing+index*laneSpaceing,y=0,height=hSpacing,width=laneSpaceing)
                self.resultEntry[index].place(x=wSpacing+index*laneSpaceing,y=hSpacing,height=hSpacing,width=laneSpaceing)
            for index in range(lanes-1):
                self.resultEntry[index].bind("<Return>",self.resultEntry[index+1].focus_set)
            self.resultEntry[-1].bind("<Return>",lambda _:self.pushResults())


            

    def pushResults(self):
        
        if not self.cup.racesLeft():
            messagebox.showwarning("Race Done","Prix Is Done")
            return
        results = [resVar.get() for resVar in self.resultVars]
        intRes = []
        for result in results:
            if not result.isnumeric():
                messagebox.showwarning("Format Error",f"{result} is not nummaric")
                return
            intRes.append(int(result))
        self.cup.pushRaceResults(intRes)
        self.prixUpdateCb()
        for resVar in self.resultVars:
            resVar.set("")
        self.resultEntry[0].focus_set()


     
RESULTPUSHERHEIGHT = 100
SCOREFRAMEWIDTH = 200
SCORELABELHEIGHT = 30

class ScoreVeiwer(tk.LabelFrame):
    def __init__(self,master,cup: Cup,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.scoresFrame = ScrollingView(self)
        self.scoreLabels: list[tk.Label] = []
        self.cup = cup
        self.scoresFrame.place(relx=0,rely=0,relwidth=1,relheight=1)



    def drawPrix(self):
        
        for scoreLabels in self.scoreLabels:
            scoreLabels.place_forget()
        if(not self.cup.haveCurrentPrix()):
            return
        
        self.scoreLabels: list[tk.Label] = []

        prix = self.cup.getCurrentPrix()
        drivers = prix.getDriverList()
        
        self.scoresFrame.setInteriorSize(SCOREFRAMEWIDTH-20,SCORELABELHEIGHT*len(drivers))
        for index,driver in enumerate(drivers):
            #print("Drawing Frame")
            self.scoreLabels.append(tk.Label(self.scoresFrame.interiorFrame,anchor='w',font=("Arial", FONT_SIZE), text = "NONE"))
            self.scoreLabels[-1].place(x=0,y=index*SCORELABELHEIGHT,width=SCOREFRAMEWIDTH-20,height=SCORELABELHEIGHT)
        self.updatePrix()

        
    def updatePrix(self):
        if(self.cup.haveCurrentPrix()):
            scoreList = self.cup.getCurrentPrix().getOrderedScoreList()
            for index,score in enumerate(scoreList):
                self.scoreLabels[index].config(text=f"{index+1}{getOrdinal(index+1)} #{score[0]+1}: {score[1]:.2f} {self.cup.getRoster().getDriverByNum(score[0]).getDriverName()}")
    
    
    

class LaneStats(tk.LabelFrame):
    def __init__(self,master,cup: Cup,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.laneLabels: list[tk.Label] = []
        self.laneStats: list[tk.Label] = []
        self.cup = cup
        self.lanes = 0

        #self.bind("<Configure>",lambda _: self.configSize())

    def drawPrix(self):
        for label in self.laneLabels:
            label.place_forget()
        for label in self.laneStats:
            label.place_forget()
        if(not self.cup.haveCurrentPrix()):
            return
        self.laneLabels: list[tk.Label] = []
        self.laneStats: list[tk.Label] = []
        prix = self.cup.getCurrentPrix()
        lanes = prix.getNumLanes()
        relW = 1.0/float(lanes)
        
        for lane in range(lanes):
            self.laneLabels.append(tk.Label(self,text = f"{lane+1}",anchor='center'))
            self.laneLabels[-1].place(relx=lane*relW,rely=0,relwidth=relW,relheight=.5)
            self.laneStats.append(tk.Label(self,text = "0.0"))
            self.laneStats[-1].place(relx=lane*relW,rely=0.5,relwidth=relW,relheight=.5)
        self.updatePrix()
        
    def updatePrix(self):
        prix = self.cup.getCurrentPrix()
        lanes = prix.getNumLanes()
        results = prix.getLaneResults()
        for lane in range(lanes):
            self.laneStats[lane].config(text=f"{results[lane]:.2f}")

        #{score[1]:.2f}
    # def configSize(self):
    #     h = self.winfo_height()
    #     w = self.winfo_width()




class MarshalVeiwer(tk.LabelFrame):
    def __init__(self,master,cup: Cup,prixUpdateCb,**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.cup = cup
        self.raceTable = MarshalBoard(self,cup,self.prixUpdate,text="Races")
        self.resultPusher = racePusher(self,cup,self.prixUpdate,text="Results")
        self.scoreFrame = ScoreVeiwer(self,cup,text="Score")
        self.laneStats = LaneStats(self,cup,text="lanes")
        self.prixUpdateCb = prixUpdateCb

        
        self.bind("<Configure>",lambda _: self.configSize())


    def drawPrix(self):
        self.raceTable.drawPrix()
        self.resultPusher.drawPrix()
        self.scoreFrame.drawPrix()
        self.laneStats.drawPrix()

    def prixUpdate(self):
        self.raceTable.updatePrix()
        self.scoreFrame.updatePrix()
        self.laneStats.updatePrix()
        self.prixUpdateCb()

        

    def configSize(self):
        h = self.winfo_height()
        w = self.winfo_width()
        self.raceTable.place(x=10,y=10,height=h-RESULTPUSHERHEIGHT-40,width=w-SCOREFRAMEWIDTH-40)
        self.resultPusher.place(x=10,y=h-30-RESULTPUSHERHEIGHT,height=RESULTPUSHERHEIGHT,width=200)
        self.scoreFrame.place(x=w-SCOREFRAMEWIDTH-20,y=10,height=h-RESULTPUSHERHEIGHT-40,width=SCOREFRAMEWIDTH)
        self.laneStats.place(x=w-SCOREFRAMEWIDTH-20,y=h-30-RESULTPUSHERHEIGHT,height=RESULTPUSHERHEIGHT,width=SCOREFRAMEWIDTH)




# RACE_VIEW_WIDTH = 100
# RACE_VIEW_HEIGHT = 40


