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
numRuns = 30
ret = [0.0]*numEpisodes
numSteps=100
#path="C://Users//Srijita//Dropbox//Research1//Market_Microstructure//SARSA//Graphs//"
path = "C://Users//sridas//Dropbox//Research1//Market_Microstructure//SARSA//Graphs//"
numTran=10000
"""*************************************************************"""
"""This is the volume and time that the trader wants to sell off"""
"""These orders will be looked in the bids queue for the best price"""
"""Try adding extra state information"""
"""*************************************************************"""
volume=1000
time=10

ret_array=[0]*numEpisodes
ret_array1=[0]*numEpisodes
ret_array2=[0]*numEpisodes

"""Main experiment"""
def runExp():
    sys.setrecursionlimit(10000)
    frunflag=False
    print "Starting Greedy Algorithm"
    for r in range(0,numRuns):
        
        if (r > 0):
           frunflag=True 
           
        rl = rlg.rlglueD(numTran,numSteps,volume,time,frunflag,"greedy")
        
        i=0
        for ep in range(0,numEpisodes):
            """*************************************************************"""
            """This is the volume and time that the trader wants to sell off"""
            """These orders will be looked in the bids queue for the best price"""
            """Try adding extra state information"""
            """*************************************************************"""
            """This runs an entire episode"""            
            rl.rl_episode(volume,time,"greedy")
            print "I have processed episode",ep
            ret_array[i]=ret_array[i]+rl.getTotReward()
            i=i+1
     
    for i  in range(0,numEpisodes):
        ret_array[i]=ret_array[i]/numRuns 
        
"""Experiment for random baseline"""
        
frunflag=True 
       
def runExp1():
    sys.setrecursionlimit(10000)
    frunflag=True
    print "Starting Random Algorithm"""
    for r in range(0,numRuns):
           
        rl = rlg.rlglueD(numTran,numSteps,volume,time,frunflag,"random")
        
        i=0
        for ep in range(0,numEpisodes):
            """*************************************************************"""
            """This is the volume and time that the trader wants to sell off"""
            """These orders will be looked in the bids queue for the best price"""
            """Try adding extra state information"""
            """*************************************************************"""
            """This runs an entire episode"""            
            rl.rl_episode(volume,time,"random")
            print "I have processed episode",ep
            ret_array1[i]=ret_array1[i]+rl.getTotReward()
            i=i+1
     
    for i  in range(0,numEpisodes):
        ret_array1[i]=ret_array1[i]/numRuns

"""Experiment baseline for the strategy mentioned in nevmyvaka's ICML paper"""        
def runExp2():
    sys.setrecursionlimit(10000)
    frunflag=True
    print "Starting baseline Algorithm"""
    for r in range(0,numRuns):
           
        rl = rlg.rlglueD(numTran,numSteps,volume,time,frunflag,"baseline")
        
        i=0
        for ep in range(0,numEpisodes):
            """*************************************************************"""
            """This is the volume and time that the trader wants to sell off"""
            """These orders will be looked in the bids queue for the best price"""
            """Try adding extra state information"""
            """*************************************************************"""
            """This runs an entire episode"""            
            rl.rl_episode(volume,time,"baseline")
            print "I have processed episode",ep
            ret_array2[i]=ret_array2[i]+rl.getTotReward()
            i=i+1
     
    for i  in range(0,numEpisodes):
        ret_array2[i]=ret_array2[i]/numRuns

"""Runs all the experiments for the current modifications made"""            
runExp()
runExp1()
runExp2()
"""Ends all the experiments for all the strategies"""

episodes = range(0,numEpisodes)
"""Red color is for Greedy strategy"""
plt.plot(episodes,ret_array,color='r')
"""Blue color is for Random Strategy"""
plt.plot(episodes,ret_array1,color='b')
"""Magenta color is for Baseline Strategy in nevmywaka's paper"""
plt.plot(episodes,ret_array2,color='m')
plt.xlabel('Episodes')
plt.ylabel('Return')
plt.savefig(path+'Totreward_Episodes.png', bbox_inches='tight')



