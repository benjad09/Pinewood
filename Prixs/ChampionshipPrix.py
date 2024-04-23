from Prix import Prix,Race

class ChampPrix(Prix):
    def __init__(self):
        super().__init__()
        self.rounds = 1

    def calculateRacerScore(self,racer):
        if racer not in self.racersbyindex:
            return 4.0
        places = self.getRacerResults(racer)
        if len(places) == 0:
            return 0
        else:
            return float(sum(places))/float(len(places))

    def generatePrix(self, racers: "list[int]"):
        if len(racers) != 3:
            raise Exception("Championship expect 3 races")
        self.heatsPerRound = 3
        self.totalRaces = 3
        self.Nracers = 3
        self.racersbyindex = racers
        heats = []
        for i in range(3): 
            heats.append(Race([racers[(ii+i)%3] for ii in range(0,3)],[None for _ in range(0,3)],1,i,i))
        self.races.append(heats)
