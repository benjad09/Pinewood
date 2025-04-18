from race import Race
from clintsPrix import ClintsPrix
from campPrix import ChampPrix
from roster import Roster
from roster import Driver
from weekend import Weekend
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
    prix = ClintsPrix(3)
    prix.newPrix(range(roster.getDriverN()))
    theWeekend = Weekend()
    theWeekend.setPrix(prix)
    theWeekend.setRoster(roster)
    futureNames = ["Previous","Current","On Deck","Hole"]
    while(theWeekend.racesLeft()):
        for raceN in reversed(range(4)):
            race = theWeekend.getRelitive(raceN-1)
            if(race):
                printRace(futureNames[raceN],[driver.getDriverName() for driver in theWeekend.getRaceDrivers(race)],race.getDrivers())
                res = race.getResults()
                if res:
                    print(f"{res[0]}     {res[1]}       {res[2]}")
        theWeekend.pushRaceResults(results[theWeekend.getOnRace()])
        prix.save(f"{pathname}\cleaner.csv")
        print("\n\n")



if __name__ == "__main__":
    
    main()