import typing
import os

class Driver:
    def __init__(self,driverNum: int,driverName: str,carName : typing.Optional[str]=None):
        self.driverNum = driverNum
        self.driverName = driverName
        self.carName = carName
    
    def getdriverNum(self) -> int:
        return self.driverNum

    def getDriverName(self) -> str:
        return self.driverName
    
    def getCarName(self) -> str:
        return self.carName
    

    

class Roster:
    def __init__(self):
        self.clearRoster()

    def clearRoster(self):
        self.driverN = 0
        self.drivers : list[Driver]= []

    def save(self,filepath :str):
        with open(filepath,"w+") as file:
            file.write("Version,1,,\n")
            file.write("Num,name,car name\n")
            for driver in self.drivers:
                file.write(f"{driver.getdriverNum()+1},{driver.getDriverName()},")
                file.write("" if driver.getCarName() is None else driver.getCarName())
                file.write("\n")

    def load(self,filepath :str):
        with open(filepath,"r") as f:
            linein = f.readline()
            if(linein != "Version,1,\n"):
                raise Exception("Unreconized file type")
            if(f.readline() != "Num,name,car name\n"):
                raise Exception("Unreconized file type")
            while 1:
                driverList = f.readline()[:-1] ##remove newline
                if(driverList):
                    driverList = driverList.split(",")
                    self.newdriver(driverList[1],None if len(driverList)<3 else driverList[2])
                else:
                    break
            
        
        

    def newdriver(self,driverName: str,carName : typing.Optional[str]=None):
        self.drivers.append(Driver(self.driverN,driverName,carName))
        self.driverN = self.driverN + 1

    def getdriverByNum(self,N: int) -> Driver:
        for driver in self.drivers:
            if driver.getdriverNum() == N:
                return driver
        raise Exception("driver Not Found")
    

def main():
    pathname=f"{os.path.dirname(os.path.abspath(__file__))}"
    testRoster = Roster()
    # testRoster.newdriver("Ben","bens car")
    # testRoster.newdriver("Cullen")
    # testRoster.newdriver("Brandyon","fast car")
    # testRoster.newdriver("Testdriver")
    # testRoster.newdriver("driver 4")
    # testRoster.save(f"{pathname}/testroster.csv")
    testRoster.load(f"{pathname}/testroster.csv")
    testRoster.save(f"{pathname}/testroster3.csv")
    

if __name__ == "__main__":
    main()



        