from prix import Prix
from race import Race
import os

class RunoffPrix(Prix):
    def __init__(self):
        super().__init__()
        self.type = "runoff"

    def generatePrix(self,driverList: list[int]):
        self.lanes = len(driverList)
        self.rounds = [[Race(driverList)]]


class ChampPrix(Prix):
    def __init__(self):
        super().__init__()
        self.type = "championchip"

    def generatePrix(self,driverList: list[int]):
        self.lanes = len(driverList)
        driverN = len(driverList)
        driverList.reverse()
        if(driverN != self.lanes):
            raise Exception("expected champ and lanes to be the same")
        self.rounds = [[]] #one round winner takes all
        for i in range(driverN):
            driversInHeat = [driverList[((ii+i)%driverN)] for ii in range(driverN)]
            driversInHeat.reverse()
            self.rounds[0].append(Race(driversInHeat))


        
def main():
    pathname=f"{os.path.dirname(os.path.abspath(__file__))}"
    testPrix = ChampPrix(3)
    testPrix.newPrix([0,2,3])
    testPrix.save(f"{pathname}/champ.csv")

if __name__ == "__main__":
    main()