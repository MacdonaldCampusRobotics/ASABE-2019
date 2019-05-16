# -*- coding: utf-8 -*-
"""
Created on Wed May 08 15:19:59 2019

@author: ROBERTO MARIO
"""
#120cm x 256.5cm for actual half board
#121.92cm x 483.87cm for ideal full board
import math
import pickle

import numpy as np
import matplotlib.pyplot as plt

def convertPolarToCartesian(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return(x, y)

def convertMultiplePolarToCartesian(someLap):
  return np.array(map(lambda x:convertPolarToCartesian(x[2],math.radians(x[1])),someLap))

def improveCornerEstimatesRegression(someCartesianLap, guessedCornersIndexes):
  xs=someCartesianLap[:,0]
  ys=someCartesianLap[:,1]
  orderedIndexes=np.sort(guessedCornersIndexes)
  segmentedX=[]
  segmentedY=[]
  slopes=[]
  offsets=[]
  for i in range(4):
    if i==3:
      segmentX=np.concatenate((xs[orderedIndexes[3]:], xs[:orderedIndexes[0]+1]))
      segmentY=np.concatenate((ys[orderedIndexes[3]:], ys[:orderedIndexes[0]+1]))
    else:
      segmentX=xs[orderedIndexes[i]:orderedIndexes[i+1]+1]
      segmentY=ys[orderedIndexes[i]:orderedIndexes[i+1]+1]
    segmentedX.append(segmentX)
    segmentedY.append(segmentY)
    A = np.vstack([segmentX, np.ones(len(segmentX))]).T
    m, c = np.linalg.lstsq(A, segmentY, rcond=-1)[0]
    slopes.append(m)
    offsets.append(c)
  plt.figure(figsize=(5,5))
  plt.plot(xs, ys, 'bo', segmentedX[0], slopes[0]*segmentedX[0]+offsets[0], 'r--', segmentedX[1], slopes[1]*segmentedX[1]+offsets[1], 'r--', segmentedX[2], slopes[2]*segmentedX[2]+offsets[2], 'r--', segmentedX[3], slopes[3]*segmentedX[3]+offsets[3], 'r--')
  plt.show()

def improveCornerEstimatesDerivative(someCartesianLap, guessedCornersIndexes):
  pass

def getPositionFromClosestCorner(someLap):
  cartesianValues=convertMultiplePolarToCartesian(someLap)
  candidateCornersIndexes=[cartesianValues[:,0].argmin(),cartesianValues[:,0].argmax(),cartesianValues[:,1].argmin(),cartesianValues[:,1].argmax()]
  candidateCorners=np.array(map(lambda x: [cartesianValues[x,0],cartesianValues[x,1]], candidateCornersIndexes))
  #actualCorners=improveCornerEstimates(cartesianValues, candidateCornersIndexes, candidateCorners)
  improveCornerEstimatesRegression(cartesianValues, candidateCornersIndexes)
  plt.figure(figsize=(5,5))
  plt.plot(cartesianValues[:,0], cartesianValues[:,1], 'bo', candidateCorners[:,0], candidateCorners[:,1], 'ro', 0, 0, 'yo')
  plt.show()
  distanceToCorners=np.array(map(lambda x:x[0]**2+x[1]**2, candidateCorners))
  closestCorner=candidateCorners[distanceToCorners.argmin()]
  return closestCorner

def getPositionProbability(someLap):
  pass
  
data = pickle.load( open( "lidarReadings/save1.p", "rb" ) )

y=getPositionFromClosestCorner(data[1])
print(y)
print(type(y))