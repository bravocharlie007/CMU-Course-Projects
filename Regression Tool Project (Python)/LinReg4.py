from math import *
from random import *
from numpy import *
####################################
# General Helper Functions
####################################
def colAccess(a, col): 
    colList = [ a[i][col] for i in range(len(a)) ]
    return(colList)

####################################
# Main Function Helper Functions (First 4 were harvested from or inspired by stackoverflow.com/questions/36830737/writing-a-standard-deviation-function)
####################################
def mean(data):
    return float(sum(data) / len(data))

def variance(x):
    mu = [mean(x) for i in range(len(x))]
    n = len(x) -1
    return sum([(((x[i] - mu[i]) ** 2) / n) for i in range(n+1)])

def variance2(x):
    mu = mean(x)
    return sum([((X - mu) ** 2) / (len(x) - 1) for X in x])
    
def stddev(data):
    return sqrt(variance(data))
    
def covariance(x, y):
    return sum([(((x[i] - mean(x)) * (y[i] - mean(y))) / (len(x) - 1)) for i in range(len(x))])

def getTrainAndTestSets(dataframe):
    n = len(dataframe)
    indicesList = list(range(n))
    n //= 2                            # We only want to sample half of all elements 
    indices = sample(indicesList, n)
    trainSet, testSet = [], []
    for index in indicesList:
        if index in indices:
            trainSet += [dataframe[index]]
        elif index not in indices:
            testSet += [dataframe[index]]                
    return trainSet, testSet
    
def meanSquaredError(dataframe, beta0, beta1):
    n2 = len(dataframe)
    residuals = []
    residuals = returnResiduals(dataframe, beta0, beta1)
    n = len(residuals)
    SE = sum([(residuals[i][0])**2 for i in range(n)])
    MSE = round((SE / (n - 1)), 4)
    return MSE
    
def yPreds(x, beta0, beta1):
    if isinstance(x, int) == True or isinstance(x, float) == True:
        return beta0 + beta1 * x
    return [(beta0 + beta1 * X) for X in x]
    
def returnResiduals(dataframe, beta0, beta1):
    residualsList = []
    for row in dataframe:
        x = row[1]
        obsY = row[0]
        predY = yPreds(x, beta0, beta1)
        residual = obsY - predY
        residualsList.append([residual, x])     # Note that we inverted the order of y and x in our lists!!!!!
    return residualsList
    
####################################
# Main Function
####################################
def LinReg(dataframe):
    if dataframe == None:
        return None
    n = len(dataframe)
    trainSet = getTrainAndTestSets(dataframe)[0]
    testSet = getTrainAndTestSets(dataframe)[1]
    
    xTrain, yTrain = colAccess(trainSet, 1), colAccess(trainSet, 0)
    if len(xTrain) != len(yTrain):
        return False
    xTest, yTest = colAccess(testSet, 1), colAccess(testSet, 0)
    if len(xTest) != len(yTest):
        return False
        
    xBar, yBar = mean(xTrain), mean(yTrain)
    xSigma, ySigma = stddev(xTrain), stddev(yTrain) 
    xyCov = covariance(xTrain, yTrain)
    ro = xyCov/(xSigma * ySigma)
    beta1 = round(ro * ySigma/xSigma, 3)
    beta0 = round(yBar - beta1 * xBar, 3)
    residuals = returnResiduals(dataframe, beta0, beta1)
    residualsX, residualsY = residuals[1], residuals[0]
    MSE = meanSquaredError(dataframe, beta0, beta1)
    trainMSE = meanSquaredError(dataframe, beta0, beta1)
    return [beta0, beta1, trainMSE, MSE, "red", residuals, residualsX, residualsY]   # 8
 
# def getTrainAndTestSets(dataframe, n, train = True):
#     indicesList = list(range(n))
#     n //= 2                            # We only want to sample half of all elements 
#     indices = sample(indicesList, n)
#     if train == True:
#         trainSet = []
#         for index in indicesList:
#             if index in indices:
#                 trainSet += [dataframe[index]]
#                 return trainSet
#     elif train == False:
#         testSet = []
#         for index in indicesList:
#             if index not in indices:
#                 testSet += [dataframe[index]]
#                 return testSet
# 
# 
