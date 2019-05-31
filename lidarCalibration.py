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

def filterOutliers(someX, someY):
  xindexes=np.argsort(someX)
  xs=np.take(someX, xindexes)
  ys=np.take(someY, xindexes)
  xs=xs[4:-4]
  ys=ys[4:-4]
  yindexes=np.argsort(ys)
  xs=np.take(xs, yindexes)
  ys=np.take(ys, yindexes)
  xs=xs[4:-4]
  ys=ys[4:-4]
  return xs, ys

def improveCornerEstimates(someCartesianLap, guessedCornersIndexes, makePlot=False):
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
    filteredSegmentX, filteredSegmentY = filterOutliers(segmentX, segmentY)
    segmentedX.append(segmentX)
    segmentedY.append(segmentY)
    A = np.vstack([filteredSegmentX, np.ones(len(filteredSegmentX))]).T
    m, c = np.linalg.lstsq(A, filteredSegmentY, rcond=-1)[0]
    slopes.append(m)
    offsets.append(c)
  if(makePlot):
    plt.figure(figsize=(5,5))
    plt.plot(xs, ys, 'bo', segmentedX[0], slopes[0]*segmentedX[0]+offsets[0], 'r--', segmentedX[1], slopes[1]*segmentedX[1]+offsets[1], 'r--', segmentedX[2], slopes[2]*segmentedX[2]+offsets[2], 'r--', segmentedX[3], slopes[3]*segmentedX[3]+offsets[3], 'r--')
    plt.show()
  improvedCorners=(np.roll(offsets, 1)-offsets)/(slopes-np.roll(slopes, 1))
  improvedCorners=np.stack((improvedCorners,slopes*improvedCorners+offsets)).T
  return improvedCorners, slopes, offsets

def getPositionFromClosestCorner(someLap):
  cartesianValues=convertMultiplePolarToCartesian(someLap)
  candidateCornersIndexes=[cartesianValues[:,0].argmin(),cartesianValues[:,0].argmax(),cartesianValues[:,1].argmin(),cartesianValues[:,1].argmax()]
  candidateCorners=np.array(map(lambda x: [cartesianValues[x,0],cartesianValues[x,1]], candidateCornersIndexes))
  actualCorners, wallsSlopes, wallsOffsets=improveCornerEstimates(cartesianValues, candidateCornersIndexes)
  plt.figure(figsize=(5,5))
  plt.plot(cartesianValues[:,0], cartesianValues[:,1], 'bo', actualCorners[:,0], actualCorners[:,1], 'ro', 0, 0, 'yo')
  plt.show()
  distanceToCorners=np.array(map(lambda x:x[0]**2+x[1]**2, candidateCorners))
  minIndex=distanceToCorners.argmin()
  closestCorner=candidateCorners[minIndex]
  return closestCorner

def getPositionProbability(someLap):
  pass
  
data = pickle.load( open( "lidarReadings/save1.p", "rb" ) )
x=data[1]
#z=np.vstack((x[:50,:],x[100:,:]))
#print(z)
y=getPositionFromClosestCorner(x)
print(y)