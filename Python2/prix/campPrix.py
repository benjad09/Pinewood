from prix import Prix
from race import Race
import os

class ChampPrix(Prix):
    def newPrix(self,driverList: list[int]):
        driverN = len(driverList)
        driverList.reverse()
        print(driverList)
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