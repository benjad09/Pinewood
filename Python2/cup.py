from prix import Prix
from prix import Race
from clintsPrix import ClintsPrix
from campPrix import ChampPrix
from roster import Roster
from roster import Driver

import os
from pathlib import Path


class Cup:
    def __init__(self):
        self.onRace = 0
        self.roster : Roster = Roster()

        self.prixs : dict[str,Prix] = {}

        self.prix : Prix = None


    def save(self,folderLoc: str):
        if(self.haveRoster()):
            self.roster.save(f"{folderLoc}\\roster.roster")
            self.roster.save(f"{folderLoc}\\roster.csv")
        for prixName in self.prixs.keys():
            self.prixs[prixName].save(f"{folderLoc}\\{prixName}.prix")
            self.prixs[prixName].save(f"{folderLoc}\\{prixName}.csv")
            

    def load(self,folderLoc: str):

        self.clearPrix()
        self.prixs = {}

        tempfiles = os.listdir(folderLoc)
        for file in tempfiles:
            if Path(file).name.split('.')[1] == "roster":
                self.roster.load(f"{folderLoc}\\{file}")
            if Path(file).name.split('.')[1] == "prix":
                prixName = Path(file).name.split('.')[0]
                newPrix = Prix(3)
                newPrix.load(f"{folderLoc}\\{file}")
                self.addPrixs(prixName,newPrix)


    def haveRoster(self) -> bool:
        return self.roster is not None
    
    def havePrix(self) -> bool:
        return self.prix is not None
    
    def setRoster(self,roster: Roster):
        self.roster = roster

    def getRoster(self) -> Roster:
        return self.roster
    
    
    def addPrixs(self,name,prix :Prix):
        if(name in self.prixs.keys()):
            print("already exists")
        self.prixs[name] = prix



    def getPrixsNames(self) -> list[str]:
        return [name for name in self.prixs.keys()]
    

    def setPrix(self,prixName: str):
        if(prixName not in self.prixs.keys()):
            raise Exception("Unkown Prix")
        self.prix = self.prixs[prixName]
        self.onRace = 0
        while self.onRace < self.prix.getTotalRaces():
            if(self.prix.getRaceByN(self.onRace).getResults()):
                self.onRace = self.onRace + 1
            else:
                break


    def clearPrix(self):
        self.prix = None
        self.onRace = 0


    def __returnNoneOnNoRoster(func):
        def wrapper(self,*args,**kwargs):
            if self.roster:
                return func(self,*args,**kwargs)
            else:
                return None
        return wrapper
    
    def __returnNoneOnNoPrix(func):
        def wrapper(self,*args,**kwargs):
            if self.prix:
                return func(self,*args,**kwargs)
            else:
                return None
        return wrapper
    
    def __requirePrix(func):
        def wrapper(self,*args,**kwargs):
            if self.prix:
                return func(self,*args,**kwargs)
            else:
                return None
        return wrapper
    
    def haveCurrentPrix(self) -> bool:
        return self.prix
    
    @__requirePrix
    def getCurrentPrix(self) -> Prix:
        return self.prix


    @__returnNoneOnNoPrix
    def getRelitive(self,racesOut:int) -> Race:
        return self.getRace(self.onRace+racesOut)
        
    @__returnNoneOnNoPrix    
    def getRace(self,raceN: int):
        if(raceN < 0):
            return None
        if(raceN >= self.prix.getTotalRaces()):
            return None
        return(self.prix.getRaceByN(raceN))
    

    def getDriver(self,driverN):
        noneDriver = Driver(-1,"missingNo")
        if self.roster and driverN<self.roster.getRosterSize():
            return self.roster.getDriverByNum(driverN)
        return noneDriver
    
    def getRaceDrivers(self,race: Race) -> list[Driver]:
        return [self.getDriver(driver) for driver in race.getDrivers()]
    
    @__requirePrix
    def pushRaceResults(self,results: list[int]):
        if(self.onRace < self.prix.getTotalRaces()):
            self.prix.getRaceByN(self.onRace).updateResults(results)
            self.onRace = self.onRace + 1

    @__requirePrix
    def getOnRace(self) -> int:
        return self.onRace
    
    @__requirePrix
    def racesLeft(self):
        return self.prix.getTotalRaces() - self.onRace
    



