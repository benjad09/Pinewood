from appVC import appViewFunctions,appControlFunctions
from mainApp import MainApp

from Roster import Driver,Roster
from Prix import Race

import time

class CommandLineViewer:
    def __init__(self,control :appControlFunctions,view :appViewFunctions):
        self.control = control
        self.view = view

        view.registerCb(self.updateQue,self.updateResults,self.updateRaceResults,
                        self.updateRoster,self.updateFilePath,self.updateLeaderBoard)

        self.roster :Roster = None
        self.leaderlist : list[Driver] = []

    def getRaceStringRace(self,race:Race):
        bylane = race.getRacers()
        byracrer = [self.roster.getDriver(N).getDriverName() for N in bylane]
        string = ""
        for i in range(0,3):
            string += f"Lane {i+1}: {byracrer[i]} #{bylane[i]+1} "
        return string
        
    def printResults(self):
        index = 1
        for i in self.leaderlist:
            racer = self.roster.getDriver(i)
            print(f"#{index}: {racer.getDriverName()} {racer.getDriverScore()}")
            index = index+1


    def updateQue(self,raceList : "list[Race]",lenOfQue : int):
        if lenOfQue >= 3:
            print(f"In the Hole: {self.getRaceStringRace(raceList[2])}")
        if lenOfQue >= 2:
            print(f"On Deck: {self.getRaceStringRace(raceList[1])}")
        if lenOfQue >= 1:
            print(f"Race {self.getRaceStringRace(raceList[0])}")
        pass
        
    def updateResults(self,races : "list[Race]",lastResult : int):
        
        pass

    def updateRaceResults(self,posByLane : "list[int]"):
        print(f"lane 1:{posByLane[0]}, lane 2:{posByLane[1]}, lane 3:{posByLane[2]}")
        
    def updateRoster(self,roster :Roster):
        print("updating roster")
        self.roster = roster
        
    def updateFilePath(self,mainFolder,pathtoprix,pathtoroster):
        print(f"main folder:{mainFolder}")
        print(f"prix: {pathtoprix}")
        print(f"roster: {pathtoroster}")
        
    def updateLeaderBoard(self,drivers: "list[Driver]",len):
        self.leaderlist = drivers


resultList = [[1,2,3],[1,3,2],[3,2,1],[1,2,3],[1,3,2],
              [1,3,2],[2,3,1],[1,2,3],[1,2,3],[1,3,2],
              [1,2,3],[3,1,2],[2,1,3],[2,1,3],[1,3,2],
              [2,1,3],[3,1,2],[3,2,1],[3,2,1],[2,3,1],
              [2,3,1],[3,1,2],[1,2,3],[3,1,2],[2,1,3],
              [2,1,3],[1,3,2],[3,2,1],[2,1,3],[2,1,3]]    

champRes = [[1,2,3],[2,1,3],[2,3,1]]

def main():
    view = appViewFunctions()
    controller = appControlFunctions()
    MainApp(controller,[view])
    cmveiwer = CommandLineViewer(controller,view)
    controller.updateRosterFile("newRos.csv")
    controller.upatedMainFolder("./JoyClub2024")
    controller.loadRoster()
    controller.generateMagicPrix()
    races = controller.getTotalRacesFnc()
    
    for i in range(0,races):
        results = [0,0,0]
        while 1 not in results or 2 not in results or 3 not in results:
            results = resultList[i]
            time.sleep(.1)
            
            # instr = input()
            # if instr == "lead":
            #     cmveiwer.printResults()
            # else:
            #     results = [int(s) for s in instr.split(',')]
        controller.pushRaceResult(results)
    cmveiwer.printResults()

    controller.generateChampPrix([12,13,14])
    races = controller.getTotalRacesFnc()
    #controller.generateChampPrix()
    
    for i in range(0,races):
        results = resultList[i]
        time.sleep(1)
            
            # instr = input()
            # if instr == "lead":
            #     cmveiwer.printResults()
            # else:
            #     results = [int(s) for s in instr.split(',')]
        controller.pushRaceResult(champRes[i])
    cmveiwer.printResults()



    pass


if __name__ == "__main__":
    main()