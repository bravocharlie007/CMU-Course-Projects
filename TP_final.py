from tkinter import *
from math import *
from random import *
from scatterplot2 import *
from LinReg4 import *    # Lin Reg returns [beta0, beta1, trainMSE, MSE, "red", residuals, residualsX, residualsY]
from tkinter.filedialog import askopenfilename

####################################
# General Helper Functions
####################################
def parseFile(s, data):
    result = []
    for line in s.split('\n'):
        storage = []
        for stringedValue in line.split(','):
            storage.append(float(stringedValue))
        result.append(storage)
    data.file = result

####################################
# customize these functions
####################################
class Box(object):
    def __init__(self, data):
        self.left = 4 * data.margin    # 100
        self.right =  data.width - 4 * data.margin   # 400   
        self.top = data.height - 4 * data.margin # 400
        self.bottom = data.height   # 500
        self.boundsX = set(range(self.left, self.right + 1))
        self.boundsY = set(range(self.top, self.bottom + 1))   # Up is down
        self.bounds = [self.left, self.top, self.right, self.bottom]
        self.xCenter = self.left + (self.right - self.left) // 2    # 250
        self.yCenter = self.top + (self.bottom - self.top) // 2     # 450  0
        
    def draw(self, data, canvas):
        canvas.create_rectangle(self.bounds)
        canvas.create_text(self.xCenter, self.yCenter, text = "Browse...", font = "Times 20 bold italic")
    
def init(data):
    data.margin = 20
    data.loadFile = Box(data)
    data.xSeperator = data.width // 2
    data.titleBorder = 3 * data.margin
    data.scatterplotHeight = data.loadFile.top - data.titleBorder
    data.scatterplotWidth = data.width - data.xSeperator
    # data.loadFileLower = data.width - 4 * data.margin
    # data.loadFileUpper = data.width - 8 * data.margin
    data.file = None
    data.titleX = data.width // 2
    data.titleY = data.titleBorder // 2
    pass


def mousePressed(event, data):
    # use event.x and event.y
    if  event.x in data.loadFile.boundsX and event.y in data.loadFile.boundsY:
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        print(filename)
        with open(filename, "rt") as f:
            datafile = f.read()
            print(datafile)
            parseFile(datafile, data)
            
    
####################################
# General Helper Functions
####################################

def drawTitle(data, canvas):
    canvas.create_text(data.titleX, data.titleY, 
    text = "Glorious Project for Righteous Cause of Statistical Analysis", font = "Times %d bold" % (data.height // data.width * 24), fill = "blue") 

def drawGloriousProject(canvas, data):
    drawTitle(data, canvas)
    data.loadFile.draw(data, canvas)
    if data.file == None:
        return None
    drawScatterplot(0, data.titleBorder, data.xSeperator, data.scatterplotHeight, canvas, 4, margin = data.margin, dataframe = LinReg(data.file)[5], isresiduals = True)  
    #0, 60, 250, 400
    drawScatterplot(data.xSeperator, data.titleBorder, data.scatterplotWidth, data.scatterplotHeight, canvas, 4, model = LinReg(data.file), margin = data.margin, dataframe = data.file) 
    # 250, 60, 500, 400
   
    # 
    
def redrawAll(canvas, data):
    drawGloriousProject(canvas, data)
    pass








####################################
# use the run function as-is
####################################

def run(width=500, height=500):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.file = []
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 500)