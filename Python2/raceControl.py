
import tkinter as tk

from rosterUI import RosterViewer
from roster import Roster


FREMENMAJORVERSION = 0
FREMENMINORVERSION = 7

WINDOW_NAME = f"RACE CONTROL"

FONT_SIZE = 10
GUIXSIZE = 1200
GUIYSIZE = 820

GUIMINXSIZE = 950
GUIMINYSIZE = 550

GUIXSIZE = GUIMINXSIZE
GUIYSIZE = GUIMINYSIZE



ROSTER_VIEWER_WIDTH = 350
FRAME_MARGIN = 10

class RaceControlGUI:
    """Setups up and controls the core of the GUI"""

    def __init__(self, root: tk.Tk,controller :"RaceControl"):
        self.root = root
        self.control = controller
        self.root.wm_title(WINDOW_NAME)
        self.screen_w = int(self.root.winfo_screenwidth())
        self.screen_h = int(self.root.winfo_screenheight())
        self.default_geometry = str(GUIXSIZE)+"x"+str(GUIYSIZE)+"+"+str(int(self.screen_w/4))+"+"+str(int(self.screen_h/4))
        self.root.geometry(self.default_geometry)
        self.root.minsize(width=GUIMINXSIZE,height=GUIMINYSIZE)
        self.root.protocol('WM_DELETE_WINDOW', self.control.exit)
        self.rosterViewer = RosterViewer(self.control.roster,master = self.root,text='Race Roster')

        self.root.bind("<Configure>",self.configSize)


    def configSize(self,_):
        newWidth = self.root.winfo_width()
        newHeight = self.root.winfo_height() #assinging to varibles because of amount of useses
        self.updateWindowSize(newWidth,newHeight)


    def updateWindowSize(self,newW,newH):
        self.rosterViewer.place(x=newW-ROSTER_VIEWER_WIDTH-(FRAME_MARGIN*2),y=FRAME_MARGIN,height=newH-(FRAME_MARGIN*2),width=ROSTER_VIEWER_WIDTH)



class RaceControl:
    def __init__(self,):
        self.roster :Roster = None
        self.root = tk.Tk()
        self.gui = RaceControlGUI(self.root,self)
        self.root.mainloop()




    def exit(self):
        self.root.destroy()



def main():
    RaceControl()

if __name__ == "__main__":
    main()