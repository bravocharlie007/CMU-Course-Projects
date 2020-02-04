# Make sure to have packages installed!

from random import *
from tkinter import *
from math import *
from numpy import *
from LinReg4 import *

####################################
# General Helper Functions
####################################
def colAccess(a, col): 
    colList = [ a[i][col] for i in range(len(a)) ]
    return(colList)

####################################
# Main Function
####################################

def drawScatterplot(x0, y0, width, height, canvas, labelNumber, margin = 20, dataframe = None, model = None, isresiduals = False): # Draws Panel, Axis, Labels and Points
    if dataframe == None:
        return None
    elif len(dataframe) > 3:
        x0Margin, y0Margin = x0 + margin // 4, y0 + margin // 4            # Reminder: col 0 is Y, col 1 is X
        x1Margin, y1Margin = x0 + width - margin // 4, y0 + height - margin // 4
        
        x0Margin2, y0Margin2 = x0 + 2 * margin, y0 + 2 * margin   # pointsMargin2 takes off 2*margin on both sides
        x1Margin2, y1Margin2 = x0 + width - 2 * margin, y0 + height - 2 * margin
        
        points = [(x0, y0), (x0 + width, y0 + height)]              # Original Points
        pointsMargin = [(x0Margin, y0Margin), (x1Margin, y1Margin)] # Points for drawn Panel
        pointsMargin2 = [(x0Margin2, y0Margin2), (x1Margin2, y1Margin2)] # Points for drawn Axis
        
        panelWidth = width - 2 * margin          
        panelHeight = height - 2 * margin
        axisWidth = panelWidth - 2 * margin     
        axisHeight = panelHeight - 2 * margin
        
        unscaledY = returnRange(dataframe)[1][0]
        unscaledX = returnRange(dataframe)[1][1]
        
        maxY = max(unscaledY)
        maxX = max(unscaledX)
        minY = min(unscaledY)
        minX = min(unscaledX)
        rangeY = returnRange(dataframe)[0][0]
        rangeX = returnRange(dataframe)[0][1]
    
        drawPanel(pointsMargin, canvas)
        drawAxis(pointsMargin2, dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, canvas, margin, labelNumber)
        drawPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, canvas, margin, model)
        
        if model != None:
            drawModelPredictions(x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, canvas, margin, model)
            drawModelMSE(x0Margin, y0Margin, x1Margin, margin, model, canvas)
        
        if isresiduals == True:
            drawResidualsLine(pointsMargin2, dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, canvas, margin)
            drawResidualsTitle(x0Margin, y0Margin, x1Margin, margin, canvas)
    else:
        print("drawScatterplot requires a dataframe of at least 4 points due to our use of training and testing Sets")
        return False
####################################
# Helper Functions for Main Function
####################################
def returnRange(dataframe):                        # Extracts unscaled x and y values from list and returns their range
    for row in dataframe:
        if len(row) != 2:
            return False
    unscaledX, unscaledY = colAccess(dataframe, 1), colAccess(dataframe, 0)
    rangeX = abs(max(unscaledX) - min(unscaledX))
    rangeY = abs(max(unscaledY) - min(unscaledY))
    
    return (rangeY, rangeX), (unscaledY, unscaledX)

def returnCleanPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin):   
    flippedNotScaled = flipYXvalues(dataframe, maxY, minX)                                # we could have skipped going through flipY then scale and done it all in one function
    cleanPoints =  scaleValues(flippedNotScaled, axisHeight, axisWidth, rangeY, rangeX)   # Since y = axisHeight - abs(minY - Y) * axisHeight // rangeY
    for row in cleanPoints:                                                               # All depends on reference point. Either tkinter y = 0 or y = axisHeight
        row[1] += x0 + 2 * margin                                                         # Map scaled and flipped values to non tkinter origin                      
        row[0] += y0 + 2 * margin  
    scaledRangeY = max(colAccess(cleanPoints, 0)) - min(colAccess(cleanPoints, 0))
    scaledRangeX = max(colAccess(cleanPoints, 1)) - min(colAccess(cleanPoints, 1))  
    return cleanPoints, scaledRangeY, scaledRangeX                                              

def flipYXvalues(dataframe, maxY, minX):
    flippedDataframe = []
    for i in range(len(dataframe)):
        flippedDataframe += [[abs(maxY - dataframe[i][0]), dataframe[i][1] - minX]]       # We flip y by substracting the yvalue from the max.
    return flippedDataframe                                                               # Substracting the min from X
    
def scaleValues(dataframe, axisHeight, axisWidth, rangeY, rangeX):
    for i in range(len(dataframe)):
        dataframe[i][0] = int(dataframe[i][0] * (axisHeight / rangeY))
        dataframe[i][1] = int(dataframe[i][1] * (axisWidth / rangeX))
    return dataframe
    
def inverseCleanPointY(scaledY, y0, margin, rangeY, axisHeight, maxY): 
    step1 = scaledY - y0 - 2 * margin               # Unmap scaled value from non tkinter origin
    step2 = int(step1 * rangeY/axisHeight)          # Unscale
    step3 = maxY - step2
    return step3

def inverseCleanPointX(scaledX, x0, margin, rangeX, axisWidth, minX):
    step1 = scaledX - x0 - 2 * margin
    step2 = ceil(step1 * rangeX/axisWidth)
    step3 = step2 + minX
    return step3
    
def createModelDataframe(model, minX, maxX):
    beta0, beta1 = model[0], model[1]
    minX, maxX = int(minX), int(maxX) + 1    # Interize for range function
    modelDataframe = [[0 for i in range(2)] for j in range(maxX - minX)]    # Create Empty List
    
    for i in range(minX, maxX):
        modelDataframe[i][1] = i
        modelDataframe[i][0] = yPreds(i, beta0, beta1)
    return modelDataframe
####################################
# Drawing Helper Functions
####################################
def drawPanel(pointsMargin, canvas):          # We do not pass in x1 and y1 as in other 
    x0M, y0M = pointsMargin[0][0], pointsMargin[0][1]
    x1M, y1M = pointsMargin[1][0], pointsMargin[1][1]   
    points = [(x0M, y0M), (x1M, y1M)]
    canvas.create_rectangle(points)

def drawAxis(pointsMargin2, dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, canvas, margin, labelNumber):  
    xOrigin = pointsMargin2[0][0]                                 # Contains precalculated origin.
    yOrigin = pointsMargin2[1][1]                              
    yAxisEndX = xOrigin
    yAxisEndY = pointsMargin2[0][1] - margin//2                  # Alternatively y0 + 3/2 * data.margin or 
    xAxisEndX = pointsMargin2[1][0] + margin//2                  # pointsMargin2 = [(x0Margin2, y0Margin2), (x1Margin2, y1Margin2)]
    xAxisEndY = yOrigin
    
    xAxis = [(xOrigin, yOrigin), (xAxisEndX, xAxisEndY)]
    yAxis = [(xOrigin, yOrigin), (yAxisEndX, yAxisEndY)]
    canvas.create_line(xAxis), canvas.create_line(yAxis)
    drawLabels(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin, labelNumber, xAxis, yAxis, canvas)
    pass
    
def drawLabels(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin, labelNumber, xAxis, yAxis, canvas):
    scaledRangeY = returnCleanPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin)[1]
    scaledRangeX = returnCleanPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin)[2]
    maxX, minY = rangeX + minX, maxY - rangeY
    minScaledY = min(colAccess(returnCleanPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin)[0], 0))
    minScaledX = min(colAccess(returnCleanPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin)[0], 1))
   
    xOrigin,yOrigin = xAxis[0][0], xAxis[0][1]
    xAxisEndX, xAxisEndY = xAxis[1][0], xAxis[0][1]
    yAxisEndX, yAxisEndY = xOrigin, yAxis[1][0]

    labelLength = max(int(margin/2), 5)                     # We do not want labelLength to grow past a certain size
    
    # Actual Drawing (i is for x Axis, j is for y Axis)
    for i in range(xOrigin, xOrigin + scaledRangeX + 1, int(scaledRangeX / (labelNumber - 1))):    # +-1 in stop and step is to ensure even repartition
        canvas.create_line(i, yOrigin, i, yOrigin +  labelLength)                                  # x Axis label lines
        canvas.create_text(i, yOrigin + labelLength + 4, 
        text = str(round(inverseCleanPointX(i, x0, margin, rangeX, axisWidth, minX))), font = "Times 10 bold italic", anchor = N) # x text
     
       
    for j in range(yOrigin, yOrigin - scaledRangeY - 1, - int(scaledRangeY / (labelNumber - 1))):  
        canvas.create_line(xOrigin, j, xOrigin - labelLength, j)                                  # y Axis label lines. Don't forget up is Down
        canvas.create_text(xOrigin - labelLength - 4, j, 
        text = str(round(inverseCleanPointY(j, y0, margin, rangeY, axisHeight, maxY))), font = "Times 10 bold italic", anchor = E)
        
 
def drawPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, canvas, margin, model): 
    readyToPlot = returnCleanPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin)[0]
    for row in readyToPlot:              # Scatterplot Points
        cx, cy = row[1], row[0]
        radius = 2
        points = [(cx - radius, cy - radius), (cx + radius, cy + radius)]
        canvas.create_oval(points, fill = "black")

        
def drawModelPredictions(x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, canvas, margin, model):
    maxX = rangeX + minX  # calculate max to feed to following function
    
    modelDataframe = createModelDataframe(model, minX, maxX)
    cleanPredictions = returnCleanPoints(modelDataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin)[0]
    
    # if model == LinReg
    modelCleanY, modelCleanX = colAccess(cleanPredictions, 0), colAccess(cleanPredictions, 1)
    
    modelMinY, modelMaxY = min(modelCleanY), max(modelCleanY)      # Following is how to get corresponding x of the point where y = min(y)
    RowIndexMinY, RowIndexMaxY = modelCleanY.index(modelMinY), modelCleanY.index(modelMaxY) 
    xOfModelMinY, xOfModelMaxY = modelCleanX[RowIndexMinY], modelCleanX[RowIndexMaxY]     # Index is the same for modelY or cleanPreds so indexX = indexY
    
    startPoint, endPoint = [xOfModelMinY, modelMinY], [xOfModelMaxY, modelMaxY]
    
    modelColor = model[4]
    radius = 2
    canvas.create_line(startPoint, endPoint, fill = modelColor)
    
    # for i in range(len(cleanPredictions)):                            # This code would be valid for other models but, since we have lin
    #     cx, cy = cleanPredictions[i][1], cleanPredictions[i][0]
    #     radius = 2
    #     pointsOLS = [(cx - radius, cy - radius), (cx + radius, cy + radius)]
    #     canvas.create_oval(pointsOLS, fill = modelColor)

def drawModelMSE(x0Margin, y0Margin, x1Margin, margin, model, canvas):
    trainMSE = model[2]
    MSE = model[3]
    modelColor = model[4]
    canvas.create_text(x0Margin + 2, y0Margin, text = "Training Error = %d" % trainMSE, fill = modelColor, anchor = NW)  # Slight Adjustment
    canvas.create_text(x1Margin - 1, y0Margin, text = "Test Error/MSE = %d" % MSE, fill = modelColor, anchor = NE)           # Slight Adjustment
    pass       
    
def drawResidualsLine(pointsMargin2, dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, canvas, margin):
    xOrigin = pointsMargin2[0][0]                                 # Contains precalculated origin. 
    xAxisEndX = pointsMargin2[1][0] + margin//2                  # pointsMargin2 = [(x0Margin2, y0Margin2), (x1Margin2, y1Margin2)]
    scaledRangeX = returnCleanPoints(dataframe, x0, y0, axisHeight, axisWidth, rangeY, rangeX, maxY, minX, margin)[2]
    yRes0 = []
    for i in range(xOrigin, xOrigin + scaledRangeX + 1):        # Pixel Values
        j = inverseCleanPointY(i, y0, margin, rangeY, axisHeight, maxY)
        if j < 0.5 and j > -0.5:
            yRes0 = i
            break
    canvas.create_line(xOrigin, yRes0, xAxisEndX, yRes0, fill = "red")
    
def drawResidualsTitle(x0Margin, y0Margin, x1Margin, margin, canvas):
    title = "Residuals Plot"
    middleResidualsPlot = (x0Margin + x1Margin) // 2
    canvas.create_text(middleResidualsPlot, y0Margin, text = title, fill = "dark blue", font = "Times 15 bold", anchor = N)
