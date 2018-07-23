# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 21:07:15 2016

@author: maydas
"""
from __future__ import division
from collections import namedtuple
from copy import deepcopy
import numpy as np
import random as rand
import operator
import math
epsilon = 0.1
gamma = 1.0
alpha=0.1
temp=0.5

class AgentCls:
    def __init__(self,volume,time):
        
        self.lastAction = {}
        self.lastObs = {}
        self.Qvalue= {}
        self.random_array=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        self.price_range=[181,300]
        self.price_bin=5
        self.vol_range=[1,volume]
        self.vol_bin=5
        
        """Initialization due to Boltzman exploration"""
        #self.prob_dist_action=[]
        #self.prob_dist_val=[]
        #self.highest_vol=0
        #self.probsum=0
        #self.initialize_Q_table(time)
        #self.calculate_prob_distribution()
        
    def agent_start(self,thisObs):
         
         """Action is the amount of volume of stock that is placed at a particular price"""         
         action={'vol':0,'price':0}
         
         """Changes for Boltzman Exploration"""
         #choice=self.pick_action_from_dist()
         #action_bin=self.prob_dist_action[choice]
         #action=self.unbin_action(action_bin,thisObs)
         
         """Changes for epsilon greedy method"""
         self.explore=rand.choice(self.random_array)
         if (self.explore >= epsilon):
            action=self.return_greedy_action(thisObs)
         else:
            action= self.return_random_action(thisObs)
            
         self.lastAction=action
         self.lastObs=thisObs
         return action                                                                            
         
    def agent_step(self,reward,thisObs,market_price):
         
         next_step_action={'vol':0,'price':0}

         if (thisObs['time']==1):
            next_step_action['vol']=thisObs['volume']
            next_step_action['price']=market_price
         else:
             
           self.explore=rand.choice(self.random_array)
           if (self.explore >= epsilon): 
              next_step_action=self.calcQ1(thisObs,next_step_action,reward)
           else: 
             next_step_action=self.return_random_action(thisObs)
            
         self.lastObs=thisObs
         self.lastAction=next_step_action
         
         return next_step_action
    
             
    def agent_end(self,thisObs,reward):
        
        """Converts the Obs and Action tuples to discretized tuples"""
        #thisObs1   =  self.convert_Obs_to_bin(thisObs)
        lastObs    =  self.convert_Obs_to_bin(self.lastObs)
        lastAction =  self.convert_Action_to_bin()
        
        lastAction_tup=(lastAction['vol'],lastAction['price'])
        lastObs_tup=   (lastObs['volume'],lastObs['time'],lastObs['bbid'],lastObs['bbid_vol'],lastObs['bask'],lastObs['bask_vol'])
        
        lastQvalue=0
        maxQvalue=0
        
        if (len(self.Qvalue)>0): 
           """Searches the Q-value dictionary"""
           for key,value in self.Qvalue.iteritems():
            
                if (key[0][0]== lastObs_tup[0]         and key[0][1]==lastObs_tup[1] 
                    and key[0][2] == lastObs_tup[2]    and key[0][3]== lastObs_tup[3]
                    and key[0][4] == lastObs_tup[4]    and key[0][5]== lastObs_tup[5]
                    and key[1][0]== lastAction_tup[0]  and key[1][1]==lastAction_tup[1]):
                   
                    lastQvalue=self.Qvalue[key]
                      
                    
        self.Qvalue[(lastObs_tup,lastAction_tup)]=lastQvalue+alpha*(reward+(gamma*maxQvalue)-lastQvalue) 
        
        """Changes due to Boltzman Exploration"""        
        #self.probsum=(lastQvalue-self.Qvalue[(lastObs_tup,lastAction_tup)])/temp
        #self.calculate_prob_distribution()
        
    def initialize_Q_table(self,time):
        
        vol_low=self.vol_range[0]
        vol_high=self.vol_range[1]
        bin_low=(int)((vol_low-1)/self.vol_bin)
        bin_high=(int)((vol_high-1)/self.vol_bin)
        state_tuple=[]
        state_vol_range=range(bin_low,bin_high+1)
        state_time_range=range(1,time+1)
        for i in state_vol_range:
            for j in state_time_range:
                state_tuple.append((i,j))
        action_tuple=[]
        price_low= self.price_range[0]
        price_high=self.price_range[1]
        pbin_low=(int)((price_low-1)/self.price_bin)       
        pbin_high=(int)((price_high-1)/self.price_bin)
        action_price_range=range(pbin_low,pbin_high+1)
        for i in state_vol_range:
            for j in action_price_range:
                action_tuple.append((i,j))
                
        for i in state_tuple:
            for j in action_tuple:
                self.Qvalue[(i,j)]=0
                            
        for key,value in self.Qvalue.iteritems():
            self.probsum=self.probsum+(value/temp)                    
                            
        print "The length of the Qtable is",len(self.Qvalue) 

    def calculate_prob_distribution(self):
        self.prob_dist_action=[]
        self.prob_dist_val=[]

        if(all(value == 0 for value in self.Qvalue.values())):
            for key,value in self.Qvalue.iteritems():
                action=key[1]
                val=0
                prob=(math.exp(val/temp)/math.exp(self.probsum))
                self.prob_dist_action.append(action)
                self.prob_dist_val.append(prob)
        else:
            for key,value in self.Qvalue.iteritems():
                action=key[1]
                val=value
                prob=(math.exp(val/temp)/math.exp(self.probsum))
                self.prob_dist_action.append(action)
                self.prob_dist_val.append(prob)
                       
    def pick_action_from_dist(self):
        
        print "The length of the distribution array is",len(self.prob_dist_action)
        action_index=range(0,len(self.prob_dist_action))
        choice=np.random.choice(action_index,p=self.prob_dist_action)
        return choice


                  
    def calcQ(self,thisObs,next_action,reward):
        
        """Converts dictionaries to tuples"""
        
        thisObs_tup=(thisObs['volume'],thisObs['time'])
        lastAction_tup=(self.lastAction['vol'],self.lastAction['price'])
        lastObs_tup=(self.lastObs['volume'],self.lastObs['time'])
        lastQvalue=0
        maxQvalue=0
        temp_action=()
        
        if (len(self.Qvalue)>0): 
           """Searches the Q-value dictionary"""
           for key,value in self.Qvalue.iteritems():
                  
                if (key[0][0]== thisObs_tup[0] and key[0][1]==thisObs_tup[1]):
                   if (value > maxQvalue):
                      maxQvalue=value
                      temp_action = key[1]
            
                if (key[0][0]== lastObs_tup[0]    and key[0][1]==lastObs_tup[1] and 
                    key[1][0]== lastAction_tup[0] and key[1][1]==lastAction_tup[1]):
                   
                    lastQvalue=self.Qvalue[key]
                    #print("This state was already encoutered and updated")
                        
        self.Qvalue[(lastObs_tup,lastAction_tup)]=lastQvalue+alpha*(reward+(gamma*maxQvalue)-lastQvalue) 
        #print 'The Qtable is',self.Qvalue
        if (len(temp_action)!=0):
           #print "I found a greedy action"   
           next_action['vol']  =  temp_action[0]
           next_action['price']=temp_action[1]
        else: 
           next_action=self.return_random_action(thisObs)
            
        return next_action
    
    def convert_Obs_to_bin(self,thisObs):
        
        thisObs1=deepcopy(thisObs)
        volume=thisObs1['volume']
        vbin=(int)((volume-1)/self.vol_bin)
        thisObs1['volume']=vbin
        
        """Discretizing the extra state encodings(bbid,bbid_vol,bask,bask_vol)"""
        bbid=thisObs1['bbid']
        bbid_bin=(int)((bbid-1)/self.price_bin)
        thisObs1['bbid']=bbid_bin
        
        bbid_vol=thisObs1['bbid_vol']
        bbid_vol_bin=(int)((bbid_vol-1)/self.vol_bin)
        thisObs1['bbid_vol']=bbid_vol_bin
        
        bask=thisObs1['bask']
        bask_bin=(int)((bask-1)/self.price_bin)
        thisObs1['bask']=bask_bin
        
        bask_vol=thisObs1['bask_vol']
        bask_vol_bin=(int)((bask_vol-1)/self.vol_bin)
        thisObs1['bask_vol']=bask_vol_bin
        return thisObs1
        
    def  convert_Action_to_bin(self): 
          #print "Before Discretization",self.lastAction
          Action={'vol':0,'price':0}  
          
          """Discretize the volume"""
          volume=self.lastAction['vol']
          vbin=(int)((volume-1)/self.vol_bin)
          Action['vol']=vbin
          
          """Discretize the price"""
          price=self.lastAction['price']
          pbin=(int)((price-1)/self.price_bin)
          Action['price']=pbin
          #print "After Discretization",Action
          return Action
          
    def unbin_action(self,temp_action,thisObs):
        #print "I am now unbinning the discretized values"
        next_step_action={'vol':0,'price':0}
        vbin=temp_action[0]
        pbin=temp_action[1]

        volume_start=(vbin*self.vol_bin +1)
        volume_end=volume_start+(self.vol_bin-1)
        #if vbin==0:
        #   volume_start=volume_start+1 
        price_start=(pbin*self.price_bin +1 )
        price_end=price_start+(self.price_bin-1)
        #if pbin==0:
        #   price_start=price_start+1 
        #print "vbin,volume_start,volume_end",vbin,volume_start,volume_end
        next_step_action['vol']=rand.randint(volume_start,thisObs['volume'])
        next_step_action['price']=rand.randint(price_start,price_end)
        return  next_step_action
        

    """The states and the action pairs aare stored in the Q table discretized"""    
    def calcQ1(self,thisObs,next_action,reward):
        
        """Converts the Obs and Action tuples to discretized tuples"""
        thisObs1   =   self.convert_Obs_to_bin(thisObs)
        lastObs1    =  self.convert_Obs_to_bin(self.lastObs)
        lastAction1 =  self.convert_Action_to_bin()
        
        """Converts dictionaries to tuples"""
        
        thisObs_tup=(thisObs1['volume'],thisObs1['time'],thisObs1['bbid'],thisObs1['bbid_vol'],thisObs1['bask'],thisObs1['bask_vol'])
        #print thisObs_tup        
        lastAction_tup=(lastAction1['vol'],lastAction1['price'])
        lastObs_tup=(lastObs1['volume'],lastObs1['time'],lastObs1['bbid'],lastObs1['bbid_vol'],lastObs1['bask'],lastObs1['bask_vol'])
        lastQvalue=0
        maxQvalue=0
        temp_action=()
        
        if (len(self.Qvalue)>0): 
           """Searches the Q-value dictionary"""
           for key,value in self.Qvalue.iteritems():
                  
                if (    key[0][0] == thisObs_tup[0]  and key[0][1]==thisObs_tup[1]
                    and key[0][2] == thisObs_tup[2]  and key[0][3]==thisObs_tup[3]
                    and key[0][4] == thisObs_tup[4]  and key[0][5]==thisObs_tup[5]):
                   if (value > maxQvalue):
                      maxQvalue=value
                      temp_action = key[1]
            
                if (    key[0][0] == lastObs_tup[0]    and key[0][1]==lastObs_tup[1] 
                    and key[0][2] == lastObs_tup[2]    and key[0][3]== lastObs_tup[3]
                    and key[0][4] == lastObs_tup[4]    and key[0][5]== lastObs_tup[5]
                    and key[1][0] == lastAction_tup[0] and key[1][1]==lastAction_tup[1]):
                   
                    lastQvalue=self.Qvalue[key]
        
        self.Qvalue[(lastObs_tup,lastAction_tup)]=lastQvalue+alpha*(reward+(gamma*maxQvalue)-lastQvalue) 
        
        """Changes to action selection due to Boltzmann exploration"""
        #self.probsum=(lastQvalue-self.Qvalue[(lastObs_tup,lastAction_tup)])/temp
        #self.calculate_prob_distribution()
        #choice=self.pick_action_from_dist()
        #action_bin=self.prob_dist_action[choice]
        #next_action=self.unbin_action(action_bin,thisObs)
        
        """Action chunk"""
        if (len(temp_action)!=0): 
           next_action=self.unbin_action(temp_action,thisObs) 
        else:  
           next_action=self.return_random_action(thisObs)
            
        return next_action    
             
    def return_random_action(self,thisObs): 
              
        next_action={}
        volume=rand.randint(1,thisObs['volume'])
        price=rand.randint(181,300)
        next_action['vol']=volume
        next_action['price']=price 
        
        return next_action   
        
    def return_greedy_action(self,thisObs): 
              
        next_action={}
        temp_action=()
        
        if (len(self.Qvalue)>0): 
           
           thisObs1   =  self.convert_Obs_to_bin(thisObs)
           thisObs_tup=(thisObs1['volume'],thisObs1['time'],thisObs1['bbid'],thisObs1['bbid_vol'],thisObs1['bask'],thisObs1['bask_vol'])
           maxQvalue=0
                   
           """Searches the Q-value dictionary"""
           for key,value in self.Qvalue.iteritems():
                  
               if (key[0][0]== thisObs_tup[0] and key[0][1]==thisObs_tup[1]
                   and key[0][2] == thisObs_tup[2]  and key[0][3]==thisObs_tup[3]
                   and key[0][4] == thisObs_tup[4]  and key[0][5]==thisObs_tup[5]):
                    
                   if (value > maxQvalue):
                      maxQvalue=value
                      temp_action = key[1]

        if (len(temp_action)!=0):
            
           next_action=self.unbin_action(temp_action,thisObs)  
        else: 
           next_action=self.return_random_action(thisObs)
        
        return next_action 
                   
        
        
          







        
            
           