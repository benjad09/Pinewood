
import typing


class Race:
    """A race expects a list of races by lane so if races 17 7 13 the initilization is
    self.race([17,7,13])"""
    def __init__(self,driverBylane: list[int]):
        self.driverBylane = driverBylane
        self.results = None

    def getDrivers(self) -> list[int]:
        return self.driverBylane
    
    def getLaneN(self) -> int:
        return len(self.driverBylane)

    def updateResults(self,placeByLanes: list[int]):
        """Sets the results or updates the result in terms of 1 indexed results IE
        [1,2,3] [3,1,2] ect"""
        if len(self.driverBylane) != len(placeByLanes):
            raise Exception("expected results equal to lane")
        self.results = placeByLanes

    def hasResults(self) -> bool:
        return self.results != None
    
    def clearResults(self):
        self.results = None

    def driverInRace(self,driver: int) -> bool:
        return (driver in self.driverBylane)

    def __noneIfNoResults(func):
        def wrapper(self,*args,**kwargs):
            if self.hasResults():
                return func(self,*args,**kwargs)
            return None
        return wrapper
    
    @__noneIfNoResults
    def getResults(self) -> typing.Optional[list[int]]:
        return self.results


    @__noneIfNoResults
    def getLaneResult(self,laneN: int) -> typing.Optional[int]:
        if(laneN > len(self.results)):
            raise Exception("Lane does not exist")
        return self.results[laneN]
    
    @__noneIfNoResults
    def getDriverResults(self,driver: int)  -> typing.Optional[int]:
        if not self.driverInRace(driver):
            return None
        return self.getLaneResult(self.driverBylane.index(driver))