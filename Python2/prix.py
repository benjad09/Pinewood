import typing
from race import Race
import typing
import os



class Prix:
    def __init__(self,lanes: int):
        self.lanes = lanes
        self.rounds :list[list[Race]]= [[]]
        self.type = "Uknown"



    def save(self,path: str):
        columns = 2 + len(self.rounds) * self.lanes
        roundLen = [len(round) for round in self.rounds]

        with open(path,"w+") as file:
            file.write(f"Version,2")
            file.write(","*(columns-2) + "\n")

            file.write(f"type,{self.type}")
            file.write(","*(columns-2) + "\n")

            file.write(f"lanes,{self.lanes}")
            file.write(","*(columns-2) + "\n")

            file.write(f"rounds,{len(self.rounds)}")
            file.write(","*(columns-2) + "\n")


            file.write(",,")
            for roundN in range(len(self.rounds)):
                file.write(f"Round {roundN+1}")
                file.write(","*self.lanes)

            file.seek(file.tell()-1,0) 
            file.truncate()
            file.write("\n")

            file.write(",lane,")
            for roundN in range(len(self.rounds)):
                for lane in range(self.lanes):
                 file.write(f"{lane+1},")

            file.seek(file.tell()-1,0) 
            file.truncate()
            file.write("\n")

            maxRoundLen = max(roundLen)
            for heat in range(maxRoundLen):
                file.write(f"Heat,{heat+1},")
                for roundN in range(len(self.rounds)):
                    if(heat < len(self.rounds[roundN])):
                        for racer in self.rounds[roundN][heat].getDrivers():
                            file.write(f"{racer+1},")
                    else:
                        file.write("N/A,"*self.lanes)
                file.seek(file.tell()-1,0) 
                file.truncate()
                file.write(f"\n")
                file.write(f",,")
                for roundN in range(len(self.rounds)):
                    if(heat < len(self.rounds[roundN])):
                        if self.rounds[roundN][heat].hasResults():
                            for place in self.rounds[roundN][heat].getResults():
                                file.write(f"{place},")
                        else:
                            file.write("*,"*self.lanes)
                    else:
                        file.write("N/A,"*self.lanes)
                file.seek(file.tell()-1,0)
                file.truncate()
                file.write("\n")

    def load(self,path: str):
        with open(path,"r") as file:
            line0=file.readline()[:-1]
            if("Version,2," in line0):
                line=file.readline()[:-1].split(',')
                self.type = line[1]
                line=file.readline()
                line=file.readline()
            elif("Version,1," not in line0):
                raise Exception("Not a valid prix file")
            line1=file.readline()[:-1].split(',')
            roundsN=(len(line1)-2)//self.lanes #-2 for first 2 lines
            file.readline()#clear Lane Markers

            self.rounds :list[list[Race]]= [[] for _ in range(roundsN)]
            while 1:
                driverRead=file.readline()[:-1]
                if(',' in driverRead):
                    resultRead=file.readline()[:-1].split(",")
                    driverRead=driverRead.split(",")
                    for round in range(roundsN):
                        roundDrivers = driverRead[(2+round*self.lanes):(2+(round+1)*self.lanes)]
                        roundResults = resultRead[(2+round*self.lanes):(2+(round+1)*self.lanes)]
                        if(roundDrivers[0].isnumeric()):
                            self.rounds[round].append(Race([int(driver)-1 for driver in roundDrivers]))
                            if(roundResults[0].isnumeric()):
                                self.rounds[round][-1].updateResults([int(result) for result in roundResults])

                else:
                    break

    def validRound(self,roundN: int) -> bool:
        return(roundN < self.getRoundN())

    def getRoundN(self) -> int:
        return len(self.rounds)
    
    def __requireValidRound(func):
        def wrapper(self,roundN: int,*args,**kwargs):
            if self.validRound(roundN):
                return func(self,roundN,*args,**kwargs)
            raise Exception("invalidRound")
        return wrapper

    @__requireValidRound
    def getHeatsInRound(self,roundN: int) -> int:
        return len(self.rounds[roundN])
    
    @__requireValidRound
    def validHeat(self,roundN: int, heatN: int) -> bool:
        return (heatN < self.getHeatsInRound(roundN))
    
    def __requireValidRace(func):
        def wrapper(self,roundN:int,heatN:int,*args,**kwargs):
            if self.validRound(roundN) and self.validHeat(roundN,heatN):
                return func(self,roundN,heatN,*args,**kwargs)
            raise Exception("invalidRace")
        return wrapper
    
    @__requireValidRace
    def getRace(self,roundN: int, heatN: int) -> Race:
        return self.rounds[roundN][heatN]
    
    @__requireValidRound
    def appendHeat(self,roundN:int, race: Race):
        self.rounds[roundN].append(race)
    
    def getTotalRaces(self) -> int:
        ret = 0
        for heat in self.rounds:
            ret = ret + len(heat)
        return ret
    
    def getRoundAndHeat(self,raceN :int) -> tuple[int,int]:
        roundN = 0
        while(roundN < self.getRoundN()):
            if raceN >= self.getHeatsInRound(roundN):
                raceN = raceN - self.getHeatsInRound(roundN)
                roundN = roundN + 1
            else:
                return (roundN,raceN)
        raise Exception("invalid race")

    
    def getRaceByN(self,raceN: int) -> Race:
        raceIndex = self.getRoundAndHeat(raceN)
        return self.getRace(raceIndex[0],raceIndex[1])
    
    def getRaceList(self) -> list[tuple[int,int]]:
        retlist = []
        for round in range(len(self.rounds)):
            for heat in range(len(self.rounds[round])):
                retlist.append((round,heat))
                #this could be done smaller but screw it
        return retlist

    def getAllRaces(self) -> list[Race]:
        return [self.getRace(event[0],event[1]) for event in self.getRaceList()]

    
    def getDriversRaceList(self,driverN: int) -> list[tuple[int,int]]:
        retlist = []
        for round in range(len(self.rounds)):
            for heat in range(len(self.rounds[round])):
                if(driverN in self.getRace(round,heat).getDrivers()):
                    retlist.append((round,heat))
        return retlist
    
    def getDriversRaces(self,driverN: int) -> list[Race]:
        return [self.getRace(event[0],event[1]) for event in self.getDriversRaceList(driverN)]
    
    def getDriverList(self) -> list[int]:
        ret = []
        for race in self.getAllRaces():
            for driver in race.getDrivers():
                if driver not in ret:
                    ret.append(driver)
        return ret

    def getDriverScore(self,driverN: int) -> float:
        score = 0.0
        racesComplete = 0.0
        for race in self.getDriversRaces(driverN):
            if race.getDriverResults(driverN):
                score = score + race.getDriverResults(driverN)
                racesComplete = racesComplete + 1.0
        return (score/racesComplete) if racesComplete>0 else 4.0

    


            


            

def main():
    pathname=f"{os.path.dirname(os.path.abspath(__file__))}"
    testPrix = Prix(3)
    testPrix.load(f"{pathname}\\prix\\club2024.csv")
    for event in testPrix.getAllRaces():
        print(f"{event.getResults()},")







    

if __name__ == "__main__":
    main()