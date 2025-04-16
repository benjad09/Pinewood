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
            file.write(","*(columns-1) + "\n")


            file.write(",,")
            for roundN in range(len(self.rounds)):
                file.write(f"Round {roundN+1}")
                file.write(","*self.lanes)

            file.write("\n")

            file.write(",lane,")
            for roundN in range(len(self.rounds)):
                for lane in range(self.lanes):
                 file.write(f"{lane+1},")

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
                file.write("\n")

    def load(self,path: str):
        with open(path,"r") as file:
            line0=file.readline()[:-1]
            print(line0)
            if("Version,1," not in line0):
                raise Exception("Not a valid prix file")
            line1=file.readline()[:-1].split(',')
            print(line1)
            roundsN=(len(line1)-3)//self.lanes
            print(f"loading {roundsN} rounds")
            

            


            

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
    testPrix.save(f"{pathname}/testPrix.csv")
    testPrix.load(f"{pathname}/testPrix.csv")




    

if __name__ == "__main__":
    main()