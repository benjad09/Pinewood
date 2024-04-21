
from saveUtils import resToStr,strToRes,remove0index,add0index


class Race:
    def __init__(self,racers,results,round,heat,N):
        self.racers = racers
        self.results = results
        self.round = round
        self.heat = heat
        self.N = N
    
    def setResults(self,results):
        self.results = results

    def getResults(self) -> "list[int]":
        return self.results
    
    def getRacers(self) -> "list[int]":
        return self.racers
    
    def getRound(self) -> int:
        return self.round
    
    def getHeat(self) -> int:
        return self.heat
    
    def getN(self) -> int:
        return self.N

    def getAsDict(self):
        return {"racers":self.racers,"results":self.results,"round":self.round,"heat":self.heat,"N":self.N}



class Prix:
    def __init__(self):

        #TODO make Prixs support Varible ammount of track lanes
        
        self.races : list[Race] = [] 
        self.racersbyindex = []
        self.rounds = 6
        self.Nracers = 0
        self.heatsPerRound = 0
        self.totalRaces = 0
        self.onRace = 0 #actully stores the higest index

    def _requireValidRace(func):
        def wrapper(self,round,heat,*args,**kwargs):
            if round >=self.rounds:
                raise Exception("Invalid Heat")
            if heat>=self.heatsPerRound:
                raise Exception("Invalid Round")
            return func(self,round,heat,*args,**kwargs)
        return wrapper
    
    def _requireValidN(func):
        def wrapper(self,N,*args,**kwargs):
            if N >= self.totalRaces:
                raise Exception("Invalid N")
            return func(self,N,*args,**kwargs)
        return wrapper
        
    def _requireHeat(func):
        def wrapper(self,*args,**kwargs):
            if(len(self.races)==0):
                raise Exception("Generate Heats Required")
            else:
                return func(self,*args,**kwargs)
        return wrapper
    
    def _requireValidRacer(func):
        def wrapper(self,racer,*args,**kwargs):
            if racer not in self.racersbyindex:
                raise Exception("Racer N not in Pri")
            else:
                return func(self,racer,*args,**kwargs)
        return wrapper
    
    @_requireValidRacer
    def getRacerResultRace(self,racer, race: Race):
        if racer not in race:
            return None
        return race.getResults(race.getRacers().index(racer))
        

    @_requireValidRacer      
    def getRacerResults(self,racer):
        results = []
        for race in self.getRaces():
            if racer in race.getRacers() and None not in race.getResults():
                results.append(self.getRacerResultRace(racer,race))
        return results

    @_requireValidRace
    def calculateRacerScore(self,racer):
        places = self.getRacerResults(racer)
        if len(places) == 0:
            return 0
        else:
            return float(sum(places))/float(len(places))

    @_requireHeat
    def getLaneResults(self):
        laneResults = []
        for _ in range(0,3):
            laneResults.append([])
        for race in self.getRaces():
            res = race.getResults()
            if None not in race:
                for i in range(0,3):
                    laneResults[i].append(res[i])
        if len(laneResults[0]) == 0:
            return[0,0,0]
        ret = []
        for i in range(0,3):
            ret = (float(sum(laneResults[i]))/float(len(laneResults[i])))
        return ret


    def getRaceN(self):
        return self.totalRaces

    
    @_requireHeat
    def getHeatsPerRound(self):
        return self.heatsPerRound
    

    def getNRounds(self) -> int:
        return self.rounds
    
    @_requireValidRace
    def getRace(self,round,heat) -> Race:
        return self.races[round][heat]
    
    @_requireHeat
    def getRaces(self) -> "list[Race]":
        races = []
        for round in self.rounds:
            for heat in self.heatsPerRound:
                races.append(self.races[round][heat])
        return races
    
    @_requireHeat
    def getRHfromN(self,N):
        return int(N/self.heatsPerRound),int(N%self.heatsPerRound)

    @_requireValidN
    def getRaceByN(self,N):
        return(self.getRace(*self.getRHfromN(N)))

    @_requireValidRace
    def getResults(self,round,heat):
        return self.races[round][heat]
    
    @_requireValidN
    def getResultsByN(self,N):
        return self.getResults(*self.getRHfromN(N))
    

    @_requireValidRace
    def pushResults(self,round,heat,results):
        #require arguemnts to force correct format
        if(1 not in results or 2 not in results or 3 not in results):
            raise Exception("Bad Results")
        self.races[round][heat].results = results
        self.onRace = heat*round

    @_requireValidN
    def pushResultsbyN(self,N,results):
        return self.pushResults(self,*self.getRHfromN(N),results)
        
    def appendCommas(self,commas):
        text = ","
        for _ in range(0,commas-1):
            text+=","
        return text

    @_requireHeat
    def savePrix(self,filepath):
        columns = self.rounds*4+2
        text =  f"Version,1,{self.appendCommas(columns-1)}\n"
        text += f"Racers,{self.Nracers},{self.appendCommas(columns-2)}\n"
        text += f"Rounds,{self.rounds},{self.appendCommas(columns-2)}\n"
        text += f"Heats,{self.heatsPerRound},{self.appendCommas(columns-2)}\n"
        text += f"Total Races,{self.totalRaces},{self.appendCommas(columns-2)}\n"
        text += f"{self.appendCommas(columns)}\n"
        text += ",,"
        for rounds in range(0,self.rounds):
            text += f"Round {rounds},,,,"
        text +="\n"
        text +=',lanes,'
        for _ in range(0,self.rounds):
            for lane in range(0,3):
                text+=f"{lane},"
            text+=','
        text += '\n'
        for heat in range(0,self.heatsPerRound):
            text += f'heat #{heat},racers,'
            for round in range(0,self.rounds):
                temp = self.getRace(round,heat).racers
                for i in range(0,3):
                    text += f'{remove0index(resToStr(temp[i]))},'
                text += ','
            text += '\n'
            text += f',Results,'
            for round in range(0,self.rounds):
                temp = self.getResults(round,heat)
                for i in range(0,3):
                    text += resToStr(temp[i])#str(temp[i]) if temp[i] != None else "*"
                    text += ','
                text += ','
            text += '\n'
            text += f'{self.appendCommas(columns)}\n'


        with open(filepath,"w") as f:
            f.write(text)


    def loadPrix(self,filepath):
        DATASTART = 8

        with open(filepath,'r') as f:
            rawtext = f.read()
        lines = rawtext.split('\n')
        rawdata = []
        for line in lines:
            rawdata.append(line.split(','))
        if (int(rawdata[0][1]) != 1):
            raise Exception("cannot read files that arenot version 1")
        if(rawdata[1][0]!="Racers" or rawdata[2][0] != "Rounds" or rawdata[3][0]!="Heats" or rawdata[4][0]!= "Total Races"):
            raise Exception("bad File")
        
        self.Nracers = int(rawdata[1][1])
        self.Nracers = int(rawdata[2][1])
        self.heatsPerRound = int(rawdata[3][1])
        self.totalRaces = int(rawdata[4][1])

        print(f"loading Prix with {self.Nracers} racers and {self.heatsPerRound} heats")

        for round in range(0,self.rounds):
            heats :list[Race]= []
            for heat in range(self.heatsPerRound):
                racers = []
                results = []
                resStr = []
                for i in range(0,3):
                    resStr = rawdata[DATASTART+(heat*3)][2+(round*4)+i]
                    racers.append(add0index(strToRes(resStr)))
                    resStr = (rawdata[DATASTART+1+(heat*3)][2+(round*4)+i])
                    results.append(strToRes(resStr))
                    if(resStr != '*'):
                        self.onRace = heat*round
                heats.append(Race(racers,results,round,heat,round*self.heatsPerRound+heat))
            self.races.append(heats)
    
    def generatePrix(self,*args,**kwargs):
        raise Exception("Base Prix Cannot Generate Prix")

        

        
 

def main():
    prix = Prix()
    prix.loadPrix("clintsPrix.csv")
    print(prix.getRaceByN(5).getAsDict())
    
    
    

if __name__ == '__main__':
    main()