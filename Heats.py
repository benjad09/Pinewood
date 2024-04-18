import numpy as np
import random

MAXRACERS = 39
NHEATS = 6

mrPetersonsMagicTable = [[0.857300337,0.308079215,0.728823235,0.352716281,0.303289638,0.253851582,0.598914348,0.015510995,0.889337449,0.874595994,0.684592527,0.754271013,0.249146269,0.757156713,0.29642595,0.485857276,0.362674398,0.856750454,0.203156418,0.924489651,0.499572911,0.912983241,0.144660844,0.072240074,0.324517789,0.497194224,0.936202324,0.388129328,0.105220366,0.753078018,0.6564249,0.936206893,0.217735927,0.028284173,0.878567586,0.122313569,0.78632484,0.369999545,0.389808043],
                         [0.237275565,0.428275812,0.069088433,0.390707809,0.856439463,0.776809136,0.863393502,0.940413826,0.440146422,0.963309568,0.975407114,0.395432537,0.992672622,0.773296592,0.53590114,0.722663123,0.572665854,0.416011142,0.932694413,0.32682142,0.048191452,0.118389335,0.652167125,0.200372764,0.563294287,0.006647578,0.953031756,0.842803869,0.03155421,0.507233658,0.440224529,0.659171661,0.854394299,0.037961201,0.457658817,0.0047766,0.000262193,0.916419781,0.125463647],
                         [0.078100596,0.41311648,0.014953443,0.605353771,0.799169648,0.796514152,0.596237864,0.804880265,0.081685044,0.150570409,0.607347936,0.333895133,0.931247464,0.746111595,0.616161753,0.912688253,0.631133422,0.100621595,0.745516889,0.937085378,0.874843383,0.847562067,0.62157019,0.542815298,0.352036653,0.228570952,0.272145576,0.211448068,0.050893008,0.965206792,0.092172783,0.048920461,0.565486515,0.229999657,0.716449072,0.03184945,0.537601969,0.327635179,0.172784252],
                         [0.834422846,0.234110762,0.32601605,0.615048776,0.542672624,0.221320149,0.45803736,0.874920431,0.852853106,0.673448655,0.982221365,0.944620972,0.140384881,0.024899174,0.990775362,0.656827346,0.844457775,0.228275053,0.357655452,0.484138658,0.460102181,0.880830489,0.580023444,0.183110833,0.320042838,0.912027008,0.452811406,0.098462491,0.00446386,0.0713526,0.893175934,0.788192403,0.647118843,0.909990701,0.878271573,0.140496948,0.53796215,0.061105418,0.461252567],
                         [0.120621433,0.17299896,0.840455625,0.279747859,0.881817671,0.898789328,0.758807322,0.749482089,0.281910348,0.142496907,0.286607361,0.778712279,0.020051834,0.577315301,0.574868084,0.580536147,0.613240315,0.771919046,0.340509758,0.531032768,0.664519782,0.307470675,0.218141604,0.743098644,0.299573232,0.583616811,0.510461408,0.74757022,0.493818668,0.027783324,0.290874845,0.186292319,0.891501455,0.522319383,0.031123811,0.334480111,0.974068489,0.977074613,0.904515826],
                         [0.804491324,0.984315413,0.237921711,0.818864517,0.287717187,0.149138322,0.54480679,0.394413823,0.618579634,0.594535299,0.906941786,0.076832032,0.247409503,0.41058609,0.815636243,0.036591916,0.35754016,0.410504082,0.624185845,0.516884198,0.619738641,0.925475628,0.681092232,0.300532713,0.155797602,0.654350096,0.029457197,0.580545387,0.190538895,0.960270487,0.699224066,0.595863452,0.990192463,0.623593421,0.452888687,0.707577961,0.976862106,0.516115034,0.398807982]
                        ]



class Prix:
    def __init__(self,):
        
        self.heats = []
        self.results = []
        self.Nracers = 0
        self.extraRacers = 0
        self.roundsPerHeat = 0

    def _requireValidRace(func):
        def wrapper(self,heat,round,*args,**kwargs):
            if heat >=NHEATS:
                raise Exception("Invalid Heat")
            if round>=self.roundsPerHeat:
                raise Exception("Invalid Round")
            return func(self,heat,round,*args,**kwargs)
        return wrapper
        
    def _requireHeat(func):
        def wrapper(self,*args,**kwargs):
            if(len(self.heats)==0):
                raise Exception("Generate Heats Required")
            else:
                return func(self,*args,**kwargs)
        return wrapper
    
    @_requireHeat
    def getRoundsPerHeat(self):
        return self.roundsPerHeat
    
    @_requireValidRace
    def getRace(self,heat,round):
        return self.heats[heat][round]["racers"]
    
    @_requireValidRace
    def getResults(self,heat,round):
        return self.heats[heat][round]["results"]
    
    @_requireValidRace
    def pushResults(self,heat,round,lane1,lane2,lane3):
        #require arguemnts to force correct format
        results = [lane1,lane2,lane3]
        if(1 not in results or 2 not in results or 3 not in results):
            raise Exception("Bad Results")
        self.heats[heat][round]["results"] = [lane1,lane2,lane3]
        

        
    def generateHeats(self, racers:int):
        if racers>MAXRACERS:
            raise Exception("Too Many Racers")

        self.Nracers = racers
        self.extraRacers = self.Nracers%3
        self.roundsPerHeat = int(self.Nracers/3) + (1 if self.extraRacers != 0 else 0)
        
        print(f"creating {NHEATS} heats with {self.roundsPerHeat} races per heat")
        for heatn in range(0,NHEATS):
            ranking = [rank for rank in np.argsort(np.argsort(mrPetersonsMagicTable[heatn][:racers]))]
            races = []
            extraHeat = []
            for i in range(0,self.roundsPerHeat-1):
                races.append({"racers":[ranking[i*3],ranking[i*3+1],ranking[i*3+2]],"results":[0,0,0]})
            if self.extraRacers == 0:
                extraHeat = [ranking[-3],ranking[-2],ranking[-1]]
            elif self.extraRacers == 2:
                extraHeat [ranking[-2],ranking[-1],ranking[0]]
            elif self.extraRacers == 1:
                extraHeat = [ranking[-1],ranking[2],ranking[0]]
            races.append({"racers":extraHeat,"results":[0,0,0]})
            self.heats.append(races)
        
 

def main():
    prix = Prix()
    finiteResults = [[1,2,3],[3,1,2],[2,1,3],[3,2,1],[1,3,2],[2,1,3]]
    res = [1,2,3]
    prix.generateHeats(15)
    for i in range(0,6):
        for ii in range(0,prix.getRoundsPerHeat()):
            res = finiteResults[(int(random.random()*6))]
            prix.pushResults(i,ii,res[0],res[1],res[2])

    
    print(prix.heats)
    
    

if __name__ == '__main__':
    main()