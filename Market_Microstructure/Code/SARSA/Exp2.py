# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 15:38:40 2016

@author: maydas
"""
from __future__ import division
import sys
import rlglueimmitation as rlg
import numpy as np
import matplotlib.pyplot as plt

numEpisodes = 100
numRuns = 1
ret = [0.0]*numEpisodes
numSteps=100
path = "D://Research//Market_Microstructure//Code//SARSA//Graphs//"
numTran=10000
"""*************************************************************"""
"""This is the volume and time that the trader wants to sell off"""
"""These orders will be looked in the bids queue for the best price"""
"""Try adding extra state information"""
"""*************************************************************"""
volume=1000
time=10
ret_array=[0]*numEpisodes
def runExp():
    sys.setrecursionlimit(10000)
    frunflag=False
    for r in range(0,numRuns):
        
        if (r > 0):
           frunflag=True 
           
        rl = rlg.rlglueD(numTran,numSteps,volume,time,frunflag)
        
        i=0
        for ep in range(0,numEpisodes):
            """*************************************************************"""
            """This is the volume and time that the trader wants to sell off"""
            """These orders will be looked in the bids queue for the best price"""
            """Try adding extra state information"""
            """*************************************************************"""
            """This runs an entire episode"""            
            rl.rl_episode(volume,time)
            print "I have processed episode",ep
            ret_array[i]=ret_array[i]+rl.getTotReward()
            i=i+1
     
    for i  in range(0,numEpisodes):
        ret_array[i]=ret_array[i]/numRuns    
            
runExp()
episodes = range(0,numEpisodes)
plt.plot(episodes,ret_array)
plt.xlabel('Episodes')
plt.ylabel('Return')
plt.savefig(path+'Totreward_Episodes.png', bbox_inches='tight')

