

from Prix import Prix,Race
from Roster import Driver,Roster
from Prixs.MrPetersonsMagicPrix import ClintsPrix
from Prixs.ChampionshipPrix import ChampPrix

from pathlib import Path

from appVC import appViewFunctions,appControlFunctions


import numpy as np



class MainApp:
    def __init__(self,controller: appControlFunctions,viewers :"list[appViewFunctions]"):
        self.controller = controller
        self.viewers = viewers

        self.mainFolder = Path(".").absolute()
        self.rosterPath = Path(str(self.mainFolder)+"\\roster.csv")
        self.prixPath = Path(str(self.mainFolder)+"\\magicPrix.csv")
        
        self.prix : Prix= None
        self.roseter : Roster= None

        self.raceN = 0

        self.QueN = 3
        self.raceList: list[Race]= []
        self.leaderBoard: list[Driver] = []

        self.controller.registerCB(self.upatedMainFolder,self.updateRosterFile,self.saveRoster,self.loadRoster,
                                   self.addRacer,self.updatePrixFile,self.savePrix,self.loadPrix,
                                   self.gengenerateMagicPrix,self.generateChampPrix,self.generateLeaderPrix,
                                   self.pushRaceResult,self.getRaceN,self.pushRaceNResult,self.getTotalRaces)

    def updateQue(self,offset=0):
        N = self.raceN+offset
        RacesLeft = self.prix.totalRaces - N
        if RacesLeft < self.QueN:
            self.QueN = RacesLeft
        self.raceList = []
        for i in range(0,self.QueN):
            self.raceList.append(self.prix.getRaceByN(N+i))

        for viewer in self.viewers:
            viewer.updateQue(self.raceList,self.QueN)
        
    def updateResults(self):
        races = []
        for i in range(0,self.raceN):
            races.append(self.prix.getRaceByN(i))
        for viewer in self.viewers:
            viewer.updateResults(races,self.raceN)

    def updateRaceResults(self,posByLane : "list[int]"):
        for viewer in self.viewers:
            viewer.updateRaceResults(posByLane)
        
    def updateRoster(self):
        for viewer in self.viewers:
            viewer.updateRoster(self.roseter)
        
    def updateFilePaths(self):
        for viewer in self.viewers:
            viewer.updateFilePath(str(self.mainFolder),str(self.prixPath),str(self.rosterPath))

    def generateLeaderBoard(self):
        racers = self.roseter.getIntDriverList()
        self.scores = []
        for racer in racers:
            score = self.prix.calculateRacerScore(racer)
            self.roseter.getDriver(racer).setDriverScore(score)
            self.scores.append(score)
        ranking = [int(rank) for rank in np.argsort(self.scores)]
        # ranking.reverse()
        self.leaderBoard = [racers[rank] for rank in ranking]
        
        
    def updateLeaderBoard(self):
        self.generateLeaderBoard()
        for viewer in self.viewers:
            viewer.updateLeaderBoard(self.leaderBoard,4)

    def upatedMainFolder(self,path):
        self.mainFolder = Path(path).absolute()
        self.rosterPath = Path(str(self.mainFolder)+"\\"+self.rosterPath.name)
        self.prixPath = Path(str(self.mainFolder)+"\\"+self.prixPath.name)
        self.updateFilePaths()

    def updateRosterFile(self,path):
        self.roseterFile = Path(path)
        self.updateFilePaths()
         
    def saveRoster(self):
        self.roseter.saveRoster(str(self.roseterFile))
         
    def loadRoster(self):
        self.roseter = Roster()
        self.roseter.loadRoster(str(self.roseterFile))
        self.updateRoster()
    
    def addRacer(self,name,carName = None):
        self.roseter.addRacer(name,carName)
                   
    def updatePrixFile(self,path):
        self.prixPath = Path(path)
        self.updateFilePaths()
                   
    def savePrix(self):
        self.prix.savePrix(str(self.prixPath))
                   
    def loadPrix(self):
        self.prix = Prix()
        self.prix.loadPrix(str(self.prixPath))
                   
    def gengenerateMagicPrix(self):
        self.raceN = 0
        self.prix = ClintsPrix()
        self.prix.generatePrix(self.roseter.getIntDriverList())
        self.updatePrixFile(str(self.mainFolder)+"\\"+"magicPrix.csv")
        self.updateQue()
        self.savePrix()
        self.QueN = 3

                   
    def generateChampPrix(self,champions):
        self.raceN = 0
        self.QueN = 1
        self.updatePrixFile(str(self.mainFolder)+"\\"+"championship.csv")
        self.prix = ChampPrix()
        self.prix.generatePrix(champions)
        self.updateQue()
        self.savePrix()

        print("Todo when rankings")
        
                   
    def generateLeaderPrix(self):
        print("Todo")
                   
    def pushRaceResult(self,Results):
        self.pushRaceNResult(self.raceN,Results)
        self.raceN = self.raceN + 1
        
                   
    def getRaceN(self):
        return self.raceN
                   
    def pushRaceNResult(self,N,Results):
        self.prix.pushResultsbyN(N,Results)
        self.savePrix()
        self.updateQue(1)
        self.updateRaceResults(Results)
        self.updateResults()
        self.updateLeaderBoard()

    def getTotalRaces(self):
        return self.prix.getNRounds() * self.prix.getHeatsPerRound()


def main():
    controller = appControlFunctions()
    viewer = appViewFunctions()
    MainApp(controller,[viewer])

if __name__ == "__main__":
    main()
    