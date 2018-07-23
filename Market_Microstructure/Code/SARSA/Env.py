# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 22:05:37 2016

@author: maydas
"""
from PyLOB import OrderBook
from copy import deepcopy
import numpy as np
import random as rand
import simulate_limit_order_book as order_book
import math
lob=OrderBook()

class EnvCls:
    def __init__(self,numTran,frunflag,volume,time):
        self.trancnt=numTran
        self.episodeOver = False
        self.lastAction = {}
        self.lastObs = {}
        #self.lob = OrderBook()
        self.someOrders=[]
        self.maxask=1
        self.maxbid=1
        #self.bid_orders=self.simulate_current_order_book()
        self.fepisode_flag=False
        self.bestprice=0
        self.trans_sorted=[]
        
        self.lob = OrderBook()
        if frunflag==False:
           self.bid_orders=self.simulate_current_order_book()
        self.lob=deepcopy(lob) 
        self.calculate_optimal_return(volume,time)
        #self.initbook=OrderBook()
        #self.initbook=deepcopy(self.lob)
        
    def env_start(self,volume,time,ep_flag):
        
        bbid,bbid_vol,bask,bask_vol=self.get_best_prices()
        self.lastObs = {"volume":volume,"time":time,"bbid":bbid,"bbid_vol":bbid_vol,"bask":bask,"bask_vol":bask_vol}
        self.episodeOver = False
        self.fepisode_flag=ep_flag
        return self.lastObs
        
    def simulate_current_order_book(self):
    
     self.someOrders,self.maxask,self.maxbid=order_book.generate_random_trans(self.trancnt,self.maxask,self.maxbid)
    
     """ Add orders to LOB"""
     for order in self.someOrders:
         trades, idNum = lob.processOrder(order, False, False)
    
     return lob.bids.orderMap
     
    def calculate_optimal_return(self,volume,time):
        All_trans_list=[]
        """This part of the code calculate the return by selling the remaining volume at the market price"""
        
        for key,value in self.lob.bids.orderMap.iteritems():
            
            stock_data=(value.qty,value.price,value.timestamp)
            All_trans_list.append(stock_data)
            
        All_trans_sorted=sorted(All_trans_list, key=lambda x: (-x[1], x[2]))
        
        return_val=0
        volume_to_be_sold=volume
        for i in range(0,len(All_trans_sorted)):
            qty=All_trans_sorted[i][0]
            price=All_trans_sorted[i][1]
            if (qty<=volume_to_be_sold):
               return_val=return_val + (qty*price)
               volume_to_be_sold=(volume_to_be_sold - qty)
               if (volume_to_be_sold ==0):
                   break
            else:
               return_val=return_val+(volume_to_be_sold*price)
               break
        print ("The optimal return from this environment is",return_val)   
     
    def get_return_from_last_action(self):
        
        All_trans_list=[]
        """This part of the code calculate the return by selling the remaining volume at the market price"""
        
        for key,value in self.lob.bids.orderMap.iteritems():
            
            stock_data=(value.qty,value.price,value.timestamp)
            All_trans_list.append(stock_data)
            
        All_trans_sorted=sorted(All_trans_list, key=lambda x: (-x[1], x[2]))
        volume_to_be_sold=self.lastObs['volume']
        reward=0
        
        for i in range(0,len(All_trans_sorted)):
            qty=All_trans_sorted[i][0]
            price=All_trans_sorted[i][1]
            if (qty<=volume_to_be_sold):
               reward=reward + (qty*price)
               volume_to_be_sold=(volume_to_be_sold - qty)
               if (volume_to_be_sold ==0):
                   break
            else:
               reward=reward+(volume_to_be_sold*price)
               break
          
        return reward,All_trans_sorted[0][1]    
        
    def get_return_from_last_action1(self):
        
        """I am selling at the current market price"""
        volume_to_be_sold=self.lastAction['vol']
        reward=0
        
        #print "The last transaction array is",self.trans_sorted 
        for i in range(0,len(self.trans_sorted)):
            
            qty=self.trans_sorted[i][0]
            price=self.trans_sorted[i][1]
            #print "The quantity and price to be sold is",qty,price
            if (qty<=volume_to_be_sold):
               reward=reward + (qty*price)
               volume_to_be_sold=(volume_to_be_sold - qty)
               if (volume_to_be_sold ==0):
                   break
            else:
               reward=reward+(volume_to_be_sold*price)
               break
           
           
        #print "The reward out of the last action is",reward            
        return reward,volume_to_be_sold   

    def sell_current_market_price(self):
        
        self.trans_sorted=[]
        """This part of the code calculate the return by selling the remaining volume at the market price"""
        
        for key,value in self.lob.bids.orderMap.iteritems():
            
            stock_data=(value.qty,value.price,value.timestamp)
            self.trans_sorted.append(stock_data)
            
        self.trans_sorted=sorted(self.trans_sorted, key=lambda x: (-x[1], x[2]))
        #print "The length of sorted transaction is", len(self.trans_sorted),self.lastAction,self.lastObs
        
        return self.trans_sorted[0][1] 
    
    """This function is for encoding extra features in the state encoding"""    
    def get_best_prices(self): 
        All_trans_list_bid=[]
        All_trans_list_ask=[]        
        for key,value in self.lob.bids.orderMap.iteritems():
            
            stock_data=(value.qty,value.price,value.timestamp)
            All_trans_list_bid.append(stock_data)
            
        All_trans_sorted_bid=sorted(All_trans_list_bid, key=lambda x: (-x[1], x[2]))    
        bbid=All_trans_sorted_bid[0][1]
        bbid_vol=All_trans_sorted_bid[0][0]
        
        for key,value in self.lob.asks.orderMap.iteritems():
            
            stock_data=(value.qty,value.price,value.timestamp)
            All_trans_list_ask.append(stock_data)
            
        All_trans_sorted_ask=sorted(All_trans_list_ask, key=lambda x: (-x[1], x[2]))    
        bask=All_trans_sorted_ask[len(All_trans_sorted_ask)-1][1]
        bask_vol=All_trans_sorted_ask[len(All_trans_sorted_ask)-1][0]
        
        return bbid,bbid_vol,bask,bask_vol
        
    def get_return_from_each_action(self):
        
        All_trans_list=[]

        """This part of the code calculate the return by selling the volume specified in the action at the price specified in the action"""
        
        for key,value in self.lob.bids.orderMap.iteritems():
            
            stock_data=(value.qty,value.price,value.timestamp)
            All_trans_list.append(stock_data)
            
        All_trans_sorted=sorted(All_trans_list, key=lambda x: (-x[1], x[2]))
        volume_to_be_sold=self.lastAction['vol']
        price_to_be_sold=self.lastAction['price']
        
        #print "The limit order book array is"        
        #print All_trans_sorted
        """Initialialization of reward"""
        #print "volume and price in which to be sold",volume_to_be_sold,price_to_be_sold
        reward=0
        
        for i in range(0,len(All_trans_sorted)):
            price=All_trans_sorted[i][1]
            qty=All_trans_sorted[i][0]

            if price< price_to_be_sold:
               break 
            else: 
               if qty<=volume_to_be_sold:
                  reward=reward + (qty*price)
                  volume_to_be_sold=(volume_to_be_sold - qty)
                  if (volume_to_be_sold ==0):
                     break
               else:
                  reward=reward+(volume_to_be_sold * price)
                  break 
        #print reward    
        return reward,volume_to_be_sold
        
    def env_step(self,thisAction,ep_flag):
         
         
         reward=0
 
         if self.lastObs['time']==0:
            thisAction['vol']= self.lastObs['volume']
            thisAction['price']=0 

         self.lastAction=thisAction
         
         """creates the new state s'"""
         thisObs={'volume':self.lastObs['volume']-thisAction['vol'],'time':self.lastObs['time']-1}
         #print 'thisObs is',thisObs
         if (thisObs['volume']==0 and thisObs['time']==-1):
             self.episodeOver=True
             reward,price=self.get_return_from_last_action()
             self.lastAction['vol']=self.lastObs['volume']
             self.lastAction['price']=price 
             
         elif  (thisObs['volume']==0 and thisObs['time'] > 0):  
               self.episodeOver=True 
               #print 'I am setting the episode over flag to False'
               reward=self.get_return_from_each_action()
         else:
              reward=self.get_return_from_each_action()
               
         self.lastObs=thisObs
         if self.fepisode_flag==False:
            self.bid_orders=self.simulate_current_order_book()
            
         return thisObs,reward,self.episodeOver
         
    def execute_action_on_current_limitbook(self):
        
        LimitOrder =    { 'type'  : 'limit', 
                          'side' : 'ask', 
                          'qty'  :  self.lastAction['vol'], 
                          'price':  self.lastAction['price'] ,
                          'tid' :   self.maxask  }
        self.maxask=self.maxask+1
        trades, orderInBook = self.lob.processOrder(LimitOrder, False, False)
                                   
    def env_end(self,reward):
        print "This is the environment end step"
    
    """The new environment step written by sdas"""    
    def env_step1(self,thisAction,ep_flag):
        
        reward=0
        #print "Action in the environment is",thisAction
        self.lastAction=thisAction
        
        if self.lastObs['time']==1:
           reward,vol_unexec=self.get_return_from_last_action1()
        else:   
           reward,vol_unexec=self.get_return_from_each_action()
           
        #thisObs={'volume':self.lastObs['volume']-thisAction['vol'],'time':self.lastObs['time']-1}
        
        #self.lastObs=thisObs
        
        #print"The new state returned by environemnt is",self.lastObs
        
        self.execute_action_on_current_limitbook()
        bbid,bbid_vol,bask,bask_vol=self.get_best_prices()
        thisObs={'volume':vol_unexec,'time':self.lastObs['time']-1,"bbid":bbid,"bbid_vol":bbid_vol,"bask":bask,"bask_vol":bask_vol}
        self.lastObs=thisObs
        
#        """**********************************************************"""
#        """This portion is just used for Testing purpose"""
#        All_trans_bid=[]
#        All_trans_ask=[]
#        for key,value in self.lob.bids.orderMap.iteritems():
#            
#            stock_data=(value.qty,value.price,value.timestamp)
#            All_trans_bid.append(stock_data)
#            
#        All_trans_bid_sorted=sorted(All_trans_bid, key=lambda x: (-x[1], x[2]))
#        
#        for key,value in self.lob.asks.orderMap.iteritems():
#            
#            stock_data=(value.qty,value.price,value.timestamp)
#            All_trans_ask.append(stock_data)
#            
#        All_trans_ask_sorted=sorted(All_trans_ask, key=lambda x: (-x[1], x[2]))    
#        
#        print "The current bid side lob is",   All_trans_bid_sorted
#        print "The current ask side lob is",   All_trans_ask_sorted
#        """**********************************************************"""
        if (thisObs['time']==1):
           self.bestprice=self.sell_current_market_price()
           
        if (thisObs['volume']==0 or thisObs['time']==0):   
           self.episodeOver=True
        
        """This change was done so that transactions are only inserted at every time step of the first episode, beyond that it remains constant"""

        #if self.fepisode_flag==False: 
        #self.bid_orders=self.simulate_current_order_book() 
        
        """This change was done for just one stable environment accross all episodes"""
        if self.episodeOver==True:
            
           #self.lob=deepcopy(self.initbook)
            self.lob=deepcopy(lob)
            #print self.lob
           #print "The length of the order book when episode ends is",len(self.lob.bids.orderMap)  
           
        return thisObs,reward,self.bestprice,self.episodeOver  
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        