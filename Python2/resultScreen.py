
import tkinter as tk
from cupVeiwer import CupVeiwer
from cup import Cup
import json
from typing import Any
import os
from pathlib import Path
import random

MEMECYCLERATE_S = 30

class theMemeMahine(tk.Frame):
    def __init__(self,master,titlesSize=28,textSize=18,defaultbg='white',**frameKwargs):
        super().__init__(master,**frameKwargs)
        self.defaultbg = defaultbg
        self.config(bg=defaultbg)
        self.titlesSize = titlesSize
        self.textSize = textSize
        self.onIndex = 0
        self.indexList: list[int] = []
        self.assets: list[dict[str,Any]] = []
        try:
            self.loadAssets()
        except:
            print("Failed to load memes :(")
            self.config(bg=master['bg'])
            return
        self.displayAssets: list[tk.Label] = []
        self.newFact()
        self.bind("<Configure>",lambda _: self.drawMeme())
        
        


    def newFact(self):
        self.meme = self.getRandomMeme()
        self.drawMeme()
        cycleTime = MEMECYCLERATE_S

        self.after(cycleTime*1000,self.newFact)

    def setbgcolor(self,color):
        self.config(bg = color)
        for frame in self.displayAssets:
            frame.config(bg = color)


    def drawMeme(self):
        for frame in self.displayAssets:
            frame.place_forget()

        if(not self.meme):
            return



        memeProperties = {
            "title": "",
            "titleSize": self.titlesSize,
            "titleAnchor": 'w',
            "subTitle": None,
            "subTitleSize": self.titlesSize,
            "subTitleAnchor": 'w',
            "text": "",
            "textSize": self.textSize,
            "textAnchor": 'nw',
            "textJustify": 'left',
            "rightAsset": None,
            "leftAsset": None,
            "bg": self.defaultbg,
            
        }

        for key in memeProperties.keys():
            if key in self.meme.keys():
                memeProperties[key] = self.meme[key]
        
        self.wrap = int(self.winfo_width()*.9)
        #print(self.wrap)
        #if "title" in self.meme.keys():
        titleSize = .2

        self.displayAssets.append(tk.Label(self,text=memeProperties["title"],font=("Arial",memeProperties["titleSize"]),anchor=memeProperties["titleAnchor"]))
        self.displayAssets[-1].place(relx=0.05,rely=0.05,relwidth=.9,relheight=titleSize)

        if(memeProperties["subTitle"]):
            self.displayAssets.append(tk.Label(self,text=memeProperties["subTitle"],font=("Arial",memeProperties["subTitleSize"]),anchor=memeProperties["subTitleAnchor"]))
            self.displayAssets[-1].place(relx=0.05,rely=titleSize+0.1,relwidth=.9,relheight=titleSize)


        yPositontext = titleSize+.1 + (titleSize+.05 if memeProperties["subTitle"] else 0)
        #if "text" in self.meme.keys():
        self.displayAssets.append(tk.Label(self,text=memeProperties["text"],font=("Arial",memeProperties['textSize']),anchor=memeProperties['textAnchor'],justify=memeProperties['textJustify'],wraplength=self.wrap))
        self.displayAssets[-1].place(relx=0.05,rely=yPositontext,relwidth=.9,relheight=.95-yPositontext)
        self.setbgcolor(memeProperties["bg"])


        

    def getRandomMeme(self) -> dict[str,Any]:
        self.onIndex = self.onIndex + 1
        if(self.onIndex >= len(self.indexList)):
            self.onIndex = 0
            random.shuffle(self.indexList)
        return self.assets[self.indexList[self.onIndex]]
        #self.indexList: list[int] = []
        #return self.assets[randint(0,len(self.assets)-1)]


    def loadAssets(self):
        pathname=f"{os.path.dirname(os.path.abspath(__file__))}"
        assetFolder = f"{pathname}\\infoAssets"
        tempfiles = os.listdir(assetFolder)
        for file in tempfiles:
            if Path(file).name.split('.')[1] == "json":
                with open(f"{assetFolder}\\{file}","r") as f:
                    self.assets.append(json.loads(f.read()))
        self.indexList = [i for i in range(len(self.assets))]
        #print(assetFolder)


class mainVeiwer(tk.Toplevel):
    def __init__(self, master,cup: Cup):
        super().__init__(master)
        self.cup = cup
        self.title("14st Derby Night")
        self.minsize(width=500,height=500)
        self.state('zoomed')
        self.raceViewer = CupVeiwer(self,self.cup,fontSize=32,raceFrameH=210,displayCarNames=True,displayDriverNumbers=False,displayResults=False,veiwLag = 0,carLeadIn="In the ")
        self.raceViewer.config(bg = 'red')
        #self.memes = theMemeMahine(self,defaultbg='white')
        #self.raceViewer.raceHeight = 250
        self.raceViewer.place(relx=0.1,rely=0.05,relwidth=.8,relheight=.9)
        #self.memes.place(relx=0.2,rely=.8,relwidth=.6,relheight=.15)

    def drawPrix(self):
        self.raceViewer.drawPrix()

    def updatePrix(self):
        self.raceViewer.updatePrix()




def createSponsorSegment(LeadIn,Company,FlavorText):
    ret = {}
    ret["title"] = LeadIn
    ret["subTitle"] = Company
    ret["subTitleAnchor"] = 'center'
    ret["text"]=FlavorText
    return ret


def createFact(Title,Text,Fontsize):
    ret = {}
    ret["title"] = Title
    ret["text"]=Text
    return ret

def createSpecialThanks(Person,Reason):
    ret = {}
    ret["title"] = "Special Thanks To:"
    ret["subTitle"] = Person
    ret["text"]=Reason
    return ret


def main():
    pass
    # pathname=f"{os.path.dirname(os.path.abspath(__file__))}"
    # assetFolder = f"{pathname}\\infoAssets"

    # tempfiles = os.listdir(assetFolder)
    # for file in tempfiles:
    #     if input(f"Add color to {file}: ") == 'y':
    #         color = input("new Color: ")
    #         with open(f"{assetFolder}\\{file}","r") as f:
    #             dictThing = json.loads(f.read())
    #         dictThing['bg'] = color
    #         with open(f"{assetFolder}\\{file}","w") as f:
    #             f.write(json.dumps(dictThing))

        


    #text = createSponsorSegment("Now A word from our sponsors","Judas Iscariot Collectible Coins","Get one of these timeless 30 silver coins. Each one is deeply imbued with history as well as guilt over betraying the son of God. While supplies last.")
    
    #text = createFact("Pro Derby Tip","The secret to doing well in a pine wood derby is to go faster than your openents. This can be achived by reaching the end of track as soon as possible.",22)
    #
    # text = createSpecialThanks("The Joy Club Leaders","For everything you did to get this night ready and helping foster the minds of the next generation")
    # text = createSpecialThanks("The Cadet Leaders","For everything you did to get this night ready and helping foster the minds of the next generation")
    # text = createFact("Did You?","Create an entire derby scoreing application for that you could add a funny banner on the bottem? Yes, yes I did. It also lets you name the car as well so thats cool right? Was it worth 24 hours of work? YES! special thanks to Clint Peterson for letting me take his algorithm that did make this alot easier",18)

    # with open(f"{assetFolder}\\meta.json",'w+') as f:
        
    #     f.write(json.dumps(text))



if __name__ == "__main__":
    main()