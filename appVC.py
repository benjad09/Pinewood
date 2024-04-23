

from typing import Any
from Prix import Prix,Race
from Roster import Driver,Roster



class appViewFunctions:
    def __init__(self):
        self.updateQueFnc = None
        self.updateResultsFnc = None
        self.updateRaceResultsFnc = None
        self.updateRosterFnc = None
        self.updateFilePathFnc = None
        self.updateLeaderBoardFnc = None

    def registerCb(self,updateQue = None ,updateResults = None,updateRaceResults = None,updateRoster = None,updateFilePath = None,updateLeaderBoard = None):
        self.updateQueFnc = updateQue if updateQue is not None else self.updateQueFnc
        self.updateResultsFnc = updateResults if updateResults is not None else self.updateResultsFnc
        self.updateRaceResultsFnc = updateRaceResults if updateRaceResults is not None else self.updateRaceResultsFnc
        self.updateRosterFnc = updateRoster if updateRoster is not None else self.updateRosterFnc
        self.updateFilePathFnc = updateFilePath if updateFilePath is not None else self.updateFilePathFnc
        self.updateLeaderBoardFnc = updateLeaderBoard if updateLeaderBoard is not None else self.updateLeaderBoardFnc

    def updateQue(self,raceList : "list[Race]",lenOfQue : int):
        if self.updateQueFnc != None:
            return self.updateQueFnc(raceList,lenOfQue)
        
    def updateResults(self,races : "list[Race]",raceTotal):
        if self.updateResultsFnc != None:
            return self.updateResultsFnc(races,raceTotal)

    def updateRaceResults(self,posByLane : "list[int]"):
        if self.updateRaceResultsFnc != None:
            return self.updateRaceResultsFnc(posByLane)
        
    def updateRoster(self,roster :Roster):
        if self.updateRosterFnc != None:
            return self.updateRosterFnc(roster)
        
    def updateFilePath(self,mainFolder,pathtoprix,pathtoroster):
        if self.updateFilePathFnc != None:
            return self.updateFilePathFnc(mainFolder,pathtoprix,pathtoroster)
        
    def updateLeaderBoard(self,drivers: "list[Driver]",len):
        if self.updateLeaderBoardFnc != None:
            return self.updateLeaderBoardFnc(drivers,len)



class appControlFunctions:
    def __init__(self):
        self.upateMainFolderFnc = None

        self.updateRosterFileFnc = None
        self.saveRosterFnc = None
        self.loadRosterFnc = None
        self.addRacerFnc = None


        self.updatePrixFileFnc = None
        self.savePrixFnc = None
        self.loadPrixFnc = None

        self.generateMagicPrixFnc = None
        self.generateChampPrixFnc = None
        self.generateLeaderPrixFnc = None
        
        self.pushRaceResultFnc = None
        self.getRaceNFnc = None
        self.pushRaceNResultFnc = None

        self.getTotalRacesFnc = None

    def registerCB(self, upateMainFolder = None,
                   updateRosterFile = None,saveRoster = None,loadRoster = None,addRacer = None,
                   updatePrixFile = None,savePrix = None,loadPrix = None,
                   generateMagicPrix = None,generateChampPrix = None,generateLeaderPrix = None,
                   pushRaceResult = None,getRaceN = None,pushRaceNResult = None,getTotalRaces = None):
        
        self.updateMainFolderFnc = self.updateMainFolderFnc if upateMainFolder is None else upateMainFolder
        

        self.updateRosterFileFnc = self.updateRosterFileFnc if updateRosterFile is None else updateRosterFile
        self.saveRosterFnc = self.saveRosterFnc if saveRoster is None else saveRoster
        self.loadRosterFnc = self.loadRosterFnc if loadRoster is None else loadRoster
        self.addRacerFnc = self.addRacerFnc if addRacer is None else addRacer


        self.updatePrixFileFnc = self.updatePrixFileFnc if updatePrixFile is None else updatePrixFile
        self.savePrixFnc = self.savePrixFnc if savePrix is None else savePrix
        self.loadPrixFnc = self.loadPrixFnc if loadPrix is None else loadPrix

        self.generateMagicPrixFnc = self.generateMagicPrixFnc if generateMagicPrix is None else generateMagicPrix
        self.generateChampPrixFnc = self.generateChampPrixFnc if generateChampPrix is None else generateChampPrix
        self.generateLeaderPrixFnc = self.generateLeaderPrixFnc if generateLeaderPrix is None else generateLeaderPrix
        
        self.pushRaceResultFnc = self.pushRaceResultFnc if pushRaceResult is None else pushRaceResult
        self.getRaceNFnc = self.getRaceNFnc if getRaceN is None else getRaceN
        self.pushRaceNResultFnc = self.pushRaceNResultFnc if pushRaceNResult is None else pushRaceNResult

        self.getTotalRacesFnc = self.getTotalRacesFnc if getTotalRaces is None else getTotalRaces

    def upatedMainFolder(self,path):
        return None if self.updateMainFolderFnc is None else self.updateMainFolderFnc(path)

    def updateRosterFile(self,path):
        return None if self.updateRosterFileFnc is None else self.updateRosterFileFnc(path)
         
    def saveRoster(self):
        return None if self.saveRosterFnc is None else self.saveRosterFnc()
         
    def loadRoster(self):
        return None if self.loadRosterFnc is None else self.loadRosterFnc()
    
    def addRacer(self,name,carName = None):
        return None if self.addRacerFnc is None else self.addRacerFnc(name,carName)
                   
    def updatePrixFile(self,path):
        return None if self.updatePrixFileFnc is None else self.updatePrixFileFnc(path)
                   
    def savePrix(self):
        return None if self.savePrixFnc is None else self.savePrixFnc()
                   
    def loadPrix(self):
        return None if self.loadPrixFnc is None else self.loadPrixFnc()
                   
    def generateMagicPrix(self):
        return None if self.generateMagicPrixFnc is None else self.generateMagicPrixFnc()
                   
    def generateChampPrix(self,champs):
        return None if self.generateChampPrixFnc is None else self.generateChampPrixFnc(champs)
                   
    def generateLeaderPrix(self):
        return None if self.generateLeaderPrixFnc is None else self.generateLeaderPrixFnc()
                   
    def pushRaceResult(self,Results):
        return None if self.pushRaceResultFnc is None else self.pushRaceResultFnc(Results)
                   
    def getRaceN(self):
        return None if self.getRaceNFnc is None else self.getRaceNFnc()
                   
    def pushRaceNResult(self,N,Results):
        return None if self.pushRaceNResultFnc is None else self.pushRaceNResultFnc(N,Results)
    
    def getTotalRaces(self):
        return None if self.getTotalRacesFnc is None else self.getTotalRacesFnc
                   