import typing
from race import Race
import typing
import os



class Prix:
    def __init__(self,lanes: int):
        self.lanes = lanes
        self.rounds :list[list[Race]]= [[]]




    def save(self,path: str):
        columns = 2 + len(self.rounds) * self.lanes
        roundLen = [len(round) for round in self.rounds]

        with open(path,"w+") as file:
            file.write(f"Version,1,")
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
            print(line0)
            if("Version,1," not in line0):
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
    
    def getRaceByN(self,raceN: int) -> Race:
        roundN = 0
        while(roundN < self.getRoundN()):
            if raceN >= self.getHeatsInRound(roundN):
                raceN = raceN - self.getHeatsInRound(roundN)
                roundN = roundN + 1
            else:
                return self.getRace(roundN,raceN)
        raise Exception("invalid race")

    


    


            


            

def main():
    pathname=f"{os.path.dirname(os.path.abspath(__file__))}"

    testPrix = Prix(3)
    rounds = [[[6,5,3],[4,2,1]],
             [[2,4,1],[3,6,5]]]
    
    testPrixRaces = []

    for round in rounds:
        heats = [Race(drivers) for drivers in round]
        testPrixRaces.append(heats)

    testPrix.rounds = testPrixRaces
    #testPrix.save(f"{pathname}/testPrix.csv")
    testPrix.load(f"{pathname}/club2024.csv")
    print(f"loaded prix with {testPrix.getRoundN()} rounds")

    testPrix.save(f"{pathname}/testSave.csv")




    

if __name__ == "__main__":
    main()