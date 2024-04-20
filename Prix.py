
import random

MAXRACERS = 39


def resToStr(value):
    return("*" if value is None else str(value))

def strToRes(value):
    return(None if value == "*" else int(value))

def remove0index(value):
    if type(value) == str:
        return "*" if value == "*" else str(int(value)+1)
    else:
        return value + 1
    
def add0index(value):
    if value is None:
        return None
    if type(value) == str:
        return str(int(value)-1)
    else:
        return value-1

class Prix:
    def __init__(self):

        #TODO make Prixs support Varible ammount of track lanes
        
        self.races = []
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
    
    @_requireHeat
    def getHeatsPerRound(self):
        return self.heatsPerRound
    

    def getNRounds(self):
        return self.rounds
    
    @_requireValidRace
    def getRace(self,round,heat):
        return self.races[round][heat]
    
    @_requireHeat
    def getRHfromN(self,N):
        return int(N/self.heatsPerRound),int(N%self.heatsPerRound)

    @_requireValidN
    def getRaceByN(self,N):
        return(self.getRace(*self.getRHfromN(N)))

    @_requireValidRace
    def getResults(self,round,heat):
        return self.races[round][heat]["results"]
    
    @_requireValidN
    def getResultsByN(self,N):
        return self.getResults(*self.getRHfromN(N))
    

    @_requireValidRace
    def pushResults(self,round,heat,results):
        #require arguemnts to force correct format
        if(1 not in results or 2 not in results or 3 not in results):
            raise Exception("Bad Results")
        self.races[round][heat]["results"] = results
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
        text =  f"Version,1,{self.appendCommas(columns-1)}"
        text += f"Racers,{self.Nracers},{self.appendCommas(columns-2)}\n"
        text += f"Rounds,{self.Nracers},{self.appendCommas(columns-2)}\n"
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
                temp = self.getRace(round,heat)["racers"]
                for i in range(0,3):
                    text += f'{remove0index(resToStr(temp[i]))},'
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
        DATASTART = 7

        with open(filepath,'r') as f:
            rawtext = f.read()
        lines = rawtext.split('\n')
        rawdata = []
        for line in lines:
            rawdata.append(line.split(','))
        if (rawdata[0][1] != 1):
            raise Exception("cannot read files that arenot version 1")
        if(rawdata[1][0]!="Racers" or rawdata[2][0] != "Rounds" or rawdata[3][0]!="Heats" or rawdata[4][0]!= "Total Races"):
            raise Exception("bad File")
        
        self.Nracers = int(rawdata[0][1])
        self.Nracers = int(rawdata[1][1])
        self.heatsPerRound = int(rawdata[2][1])
        self.totalRaces = int(rawdata[3][1])

        print(f"loading Prix with {self.Nracers} racers and {self.heatsPerRound} heats")

        for round in range(0,self.rounds):
            heats = []
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
                heats.append({"racers":racers,"results":results,"round":round,"heat":heat,"racen":round*self.heatsPerRound+heat})
            self.races.append(heats)
    
    def generatePrix(self,*args,**kwargs):
        raise Exception("Base Prix Cannot Generate Prix")

        

        
 

def main():
    prix = Prix()
    prix.loadPrix("results.csv")
    print(prix.getRaceByN(5))
    
    
    

if __name__ == '__main__':
    main()