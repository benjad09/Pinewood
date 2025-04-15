import typing

class racer:
    def __init__(self,racerNum: int,driverName: str,carName : typing.Optional[str]=None):
        self.racerNum = racerNum
        self.driverName = driverName
        self.carName = carName
    
    def getRacerNum(self) -> int:
        return self.racerNum

    def getDriverName(self) -> str:
        return self.driverName
    
    def getCarName(self) -> str:
        return self.carName
    

    

class roster:
    def __init__(self):
        self.clearRoster()

    def clearRoster(self):
        self.racerN = 0
        self.racers : list[racer]= []

    def save(self,filepath :str):
        with open(filepath,"w+") as file:
            file.write("Version,1,,\n")
            file.write("Num,name,car name\n")
            for racer in self.racers:
                file.write(f"{racer.getRacerNum()},{racer.getDriverName},{" " if racer.getCarName() is None else racer.getCarName()}\n")

    def newRacer(self,driverName: str,carName : typing.Optional[str]=None):
        self.racers.append(self.racerN+1,driverName,carName)
        self.racerN = self.racerN + 1

    def getRacerByNum(self,N: int) -> racer:
        for racer in self.racers:
            if racer.getRacerNum() == 
    


        