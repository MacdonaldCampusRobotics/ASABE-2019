# -*- coding: utf-8 -*-
"""
Created on Wed May 08 15:19:59 2019

@author: ROBERTO MARIO
"""
import math
import pickle

import numpy as np
import matplotlib.pyplot as plt

def displayLap(someLap):
  plt.figure(figsize=(5,5))
  plt.polar(map(math.radians,someLap[:,1]),someLap[:,2], 'bo')
  plt.show()
  
data = pickle.load( open( "save3.p", "rb" ) )

if plt.get_fignums():
  plt.close("all")

#The first lap is always cut short, just ignore it
for i, lap in enumerate(data):
  if i!=0:
    displayLap(lap)