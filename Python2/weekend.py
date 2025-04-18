from prix import Prix
from prix import Race
from clintsPrix import ClintsPrix
from campPrix import ChampPrix
from roster import Roster
from roster import Driver





class Weekend:
    def __init__(self):
        self.onRace = 0
        self.roster : Roster = None
        self.prix : Prix = None


    def haveRoster(self) -> bool:
        return self.roster is not None
    
    def havePrix(self) -> bool:
        return self.roster is not None
    
    def setRoster(self,roster: Roster):
        self.roster = roster

    def setPrix(self,prix: Prix):
        self.prix = prix
        self.onRace = 0
        while self.onRace < self.prix.getTotalRaces():
            if(self.prix.getRaceByN(self.onRace).getResults()):
                self.onRace = self.onRace + 1
            else:
                break

    def clearRoster(self):
        self.roster = None

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
        if self.roster and driverN<self.roster.getDriverN():
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
    



