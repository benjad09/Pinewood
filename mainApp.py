

from Prix import Prix,Race
from Roster import Driver,Roster
from MrPetersonsMagicPrix import ClintsPrix

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
                                   self.pushRaceNResult,self.getRaceN,self.pushRaceNResult)

    def updateQue(self):
        RacesLeft = self.prix.totalRaces - self.raceN
        if RacesLeft < self.QueN:
            self.QueN = RacesLeft
        self.raceList = []
        for i in range(0,self.QueN):
            self.raceList.append(self.prix.getRaceByN(self.raceN+i))

        for viewer in self.viewers:
            viewer.updateQue(self.raceList,self.QueN)
        
    def updateResults(self):
        for viewer in self.viewers:
            viewer.updateResults(self.prix,self.raceN)

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
            self.scores.append(self.prix.calculateRacerScore(racer))
        ranking = [int(rank) for rank in np.argsort(self.scores)]
        ranking.reverse()
        self.leaderBoard = racers[ranking]
        
        
    def updateLeaderBoard(self):
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
        self.prix = ClintsPrix()
        self.prix.generatePrix(self.roseter.getIntDriverList())
        self.QueN = 3

                   
    def generateChampPrix(self):
        self.QueN = 1
        print("Todo when rankings")
        
                   
    def generateLeaderPrix(self):
        print("Todo")
                   
    def pushRaceResult(self,Results):
        self.pushRaceNResult(self,self.raceN,Results)
        self.raceN = self.raceN + 1
        
                   
    def getRaceN(self):
        return self.raceN
                   
    def pushRaceNResult(self,N,Results):
        self.prix.pushResultsbyN(N,Results)
        self.savePrix()
        self.updateQue()
        self.updateLeaderBoard()
        self.updateRaceResults(Results)
        self.updateResults()


def main():
    controller = appControlFunctions()
    viewer = appViewFunctions()
    MainApp(controller,[viewer])

if __name__ == "__main__":
    main()
    