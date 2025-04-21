from race import Race
from clintsPrix import ClintsPrix
from defaultPrixs import ChampPrix
from roster import Roster
from roster import Driver
from cup import Cup
import os






results = [[3, 2, 1],
[2, 1, 3],
[3, 1, 2],
[3, 1, 2],
[2, 3, 1],
[3, 1, 2],
[1, 2, 3],
[2, 3, 1],
[2, 3, 1],
[3, 1, 2],
[3, 2, 1],
[2, 3, 1],
[2, 3, 1],
[3, 1, 2],
[2, 3, 1],
[2, 1, 3],
[1, 3, 2],
[1, 2, 3],
[3, 1, 2],
[3, 2, 1],
[3, 1, 2],
[3, 1, 2],
[1, 2, 3],
[1, 2, 3],
[1, 2, 3],
[2, 1, 3],
[1, 3, 2],
[1, 2, 3],
[2, 1, 3],
[1, 2, 3],
[1, 3, 2],
[3, 2, 1],
[1, 3, 2],
[1, 2, 3],
[1, 3, 2],
[3, 2, 1],
[3, 1, 2],
[2, 1, 3],
[2, 3, 1],
[1, 2, 3],
[1, 2, 3],
[2, 1, 3],]


def printRace(name: str,drivers: list[str],driverN: list[int]):
    print(name)
    string = ""
    for index in range(3):
        string = string+f"Lane {index+1}: {drivers[index]} (#{driverN[index]+1})      "
    print(string)

def main():
    pathname=f"{os.path.dirname(os.path.abspath(__file__))}"
    roster = Roster()
    roster.load(f"{pathname}\\joyclub2024.csv")
    prix = ClintsPrix()
    prix.generatePrix(range(roster.getRosterSize()))
    girlsCup = Cup()
    #girlsCup.load(f"{pathname}\\testCup")
    girlsCup._addPrixs("standard",prix)
    girlsCup.setPrix("standard")
    girlsCup.setRoster(roster)
    futureNames = ["Previous","Current","On Deck","Hole"]
    while(girlsCup.racesLeft()>12):
        for raceN in reversed(range(4)):
            race = girlsCup.getRelitive(raceN-1)
            if(race):
                printRace(futureNames[raceN],[driver.getDriverName() for driver in girlsCup.getRaceDrivers(race)],race.getDrivers())
                res = race.getResults()
                if res:
                    print(f"{res[0]}     {res[1]}       {res[2]}")
        girlsCup.pushRaceResults(results[girlsCup.getOnRace()])
        girlsCup.save(f"{pathname}\\testCup")
        print("\n\n")



if __name__ == "__main__":
    
    main()