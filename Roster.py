from saveUtils import remove0index, add0index


class Driver:
    def __init__(self,driverNumber: int,driverName: str,carName: str = None):
        self.driverNumber = driverNumber
        self.driverName = driverName
        self.carName = carName

    def getDriverName(self) -> str:
        return self.driverName
    
    def getCarName(self) -> str:
        return self.carName
    
    def getDriverNumber(self) -> int:
        return self.driverNumber


class Roster:
    def __init__(self):
        self.drivers : list[Driver] = []
        self.driverNumbers = []
        #its late so yes these need to be the same len


        self.rosterLocked = False
        self.drivern = 0


    def _notLocked(func):
        def wrapper(self,*args,**kwargs):
            if self.rosterLocked:
                raise Exception("Roster Is locked")
            return func(self,*args,**kwargs)
        return wrapper
    
    
    def lockRoster(self):
        self.rosterLocked = True

    @_notLocked
    def addRacer(self,driverName,carName = None):
        self.drivers.append(Driver(self.drivern,driverName,carName))
        self.driverNumbers.append(self.drivern)
        self.drivern = self.drivern+1

    def getDriver(self,N) -> Driver:
        for driver in self.drivers:
            if N == driver.getDriverNumber():
                return driver
        raise Exception("Driver Not Found")
    
    def getDriverByName(self,Name) -> Driver:
        for driver in self.drivers:
            if Name == driver.getDriverName():
                return driver
        raise Exception("Driver Not Found")
    
    def getIntDriverList(self):
        ret = []
        for driver in self.drivers:
            ret.append(driver.getDriverNumber())
        return ret
        


    def removeRacer(self,index):
        driverCopy = self.drivers
        self.drivers = []
        self.driverNumbers = []
        self.drivern = 0
        driverCopy.pop(index)
        self.addRoster(driverCopy)
        


    def saveRoster(self,filepath):
        text = "Version,1,\n"
        text += f"Drivers,{self.drivern},\n"
        text += f"Driver Name,Car Name\n"
        for driver in self.drivers:
            carName = "*" if driver.getCarName() is None else driver.getCarName
            text += f"{remove0index(driver.getDriverNumber())},{driver.getDriverName()},{carName}\n"
        with open(filepath,"w+") as f:
            f.write(text)


    @_notLocked
    def loadRoster(self,filepath):
        DATASTART = 3
        with open(filepath,"r") as f:
            rawText = f.read()
        rawData = [line.split(",") for line in rawText.split('\n')]
        if (rawData[0][0] != "Version" or int(rawData[0][1]) != 1):
            raise Exception("Bad Data")
        for i in range(DATASTART,len(rawData)):
            if(len(rawData[i])>=3):
                carName = None if rawData[i][2] == "*" else rawData[i][2]
                self.addRacer(rawData[i][1],carName)

    @_notLocked
    def addRoster(self,roster :"Roster"):
        for driver in roster.drivers:
            self.addRacer(driver.getDriverName(),driver.getCarName())



def main():
    ros = Roster()
    ros.loadRoster("newRos.csv")
    ros2 = Roster()
    ros2.addRacer("ben","blue meany")
    ros2.addRacer("jeff")
    ros.addRoster(ros2)
    driverlist = ros.getIntDriverList()
    print(driverlist)
    for i in driverlist:
        print(f"driver {i} is {ros.getDriver(i).getDriverName()}")


if __name__ == "__main__":
    main()