# -*- coding: utf-8 -*-
"""
Created on Wed May 08 15:19:59 2019

@author: ROBERTO MARIO
"""
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
import Tkinter
import tkFileDialog

def displayLap(someLap):
  plt.figure(figsize=(5,5))
  plt.polar(map(math.radians,someLap[:,1]),someLap[:,2], 'bo')
  plt.show()

if plt.get_fignums():
  plt.close("all")

#Close little square for dialogue to show up
tk=Tkinter.Tk()
filename = tkFileDialog.askopenfilename()

try:
  data = pickle.load( open( filename, "rb" ) )

  #The first lap is always cut short, just ignore it
  for i, lap in enumerate(data):
    if i!=0:
      displayLap(lap)
except Exception as e:
  print(str(e))
finally:
  tk.destroy()