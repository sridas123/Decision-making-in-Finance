# -*- coding: utf-8 -*-
#from collections import deque
#from __future__ import division
import random
import numpy as np
import math
"""
Created on Tue Nov 22 16:57:01 2016

@author: Srijita Das

This module creates random transactions in a stock market and then executes 
transactions so that an actual limit order book is simulated.
Original author of the code= Ash Booth
"""
'''
Created on Apr 11, 2013

@author: Ash Booth

For a full walkthrough of PyLOB functionality and usage,
see the wiki @ https://github.com/ab24v07/PyLOB/wiki

'''

"""This module randomly generates some transactions for the  buy and sell side"""
def generate_random_trans(count,maxask,maxbid):
    someOrders=[]
    tid=maxask
    #mean = [80,160]
    #cov = [[1, 0], [0, 1]] 
    #x, y = np.random.multivariate_normal(mean, cov, count).T

    for i in range(0,count):
        
        limit_dict={}
        limit_dict['type']='limit'
        if (i<=count/2-1):
           limit_dict['side']='ask'
           limit_dict['price']=random.randint(181,300)
        else:
           limit_dict['side']='bid' 
           limit_dict['price']=random.randint(101,200)
           
        if (i==count/2): 
            maxask=tid
            tid=maxbid
        
        limit_dict['qty']= random.randint(6,100)
        #limit_dict['price']=random.randint(100,300)
        limit_dict['tid']= tid
        tid=tid+1
        someOrders.append(limit_dict)
    maxbid=tid    
    return someOrders,maxask,maxbid   
    
def generate_random_trans_with_average(count,maxask,maxbid,mean_ask_price,mean_bid_price,mean_ask_vol,mean_bid_vol):
    print count/2
    ask_trans = np.random.poisson(mean_ask_price, count/2)
    bid_trans=  np.random.poisson(mean_bid_price, count/2)
    ask_vol=np.random.poisson(mean_ask_vol, count/2)
    bid_vol=np.random.poisson(mean_bid_vol, count/2)
    someOrders=[]
    tid=maxask
    
    print np.max(ask_trans)
    print np.min(ask_trans)
    print np.max(bid_trans)
    print np.min(bid_trans)
    j=0
    for i in range(0,count):
        
        limit_dict={}
        limit_dict['type']='limit'
        if (i<=count/2-1):
           
           limit_dict['side']='ask'
           limit_dict['price']=ask_trans[j]
           limit_dict['qty']= ask_vol[j]
           j=j+1
           #limit_dict['price']=random.randint(181,300)
        else:
           limit_dict['side']='bid' 
           limit_dict['price']=bid_trans[j]
           limit_dict['qty']= bid_vol[j]
           
        if (i==count/2): 
            maxask=tid
            tid=maxbid
            
        if (i==count/2-1):
            j=0
            
        #limit_dict['qty']= random.randint(6,100)
        #limit_dict['price']=random.randint(100,300)
        limit_dict['tid']= tid
        tid=tid+1
        someOrders.append(limit_dict)
    maxbid=tid    
    return someOrders,maxask,maxbid 
    
def calculate_best_price():
    
    All_trans_bid=[]
    All_trans_ask=[]
    """This part of the code calculate the return by selling the remaining volume at the current market price"""
        
    for key,value in lob.bids.orderMap.iteritems():
        stock_data=(value.qty,value.price,value.timestamp)
        All_trans_bid.append(stock_data)
        
    All_trans_bid=sorted(All_trans_bid, key=lambda x: (-x[1], x[2]))
    
    for key,value in lob.asks.orderMap.iteritems():
        stock_data=(value.qty,value.price,value.timestamp)
        All_trans_ask.append(stock_data)
        
    All_trans_ask=sorted(All_trans_ask, key=lambda x: (x[1], x[2]))
    
    return All_trans_bid[0][1],All_trans_ask[0][1]
        

if __name__ == '__main__':
    
    from PyLOB import OrderBook
    
    """ Create a LOB object"""
    lob = OrderBook()
    
    
    """########### Limit Orders #############"""
    trancount=5000
    maxask=1
    maxbid=1
    i=0
    while(True):
      if (i==1):
         break 
     
      someOrders,maxask,maxbid=generate_random_trans_with_average(trancount,maxask,maxbid,240,140,50,50)
    
      """ Add orders to LOB"""
      for order in someOrders:
          trades, idNum = lob.processOrder(order, False, False)
      i=i+1
      
      
    All_trans_list=[]
        
        
    for key,value in lob.bids.orderMap.iteritems():
            
        stock_data=(value.qty,value.price,value.timestamp)
        All_trans_list.append(stock_data)
            
      
    sum1=0
    for i in range (0,len(All_trans_list)):
        sum1=sum1+All_trans_list[i][1]
    print "The bid side average is",sum1/len(All_trans_list)  
        
    All_trans_list=[]
        
    for key,value in lob.asks.orderMap.iteritems():
            
        stock_data=(value.qty,value.price,value.timestamp)
        All_trans_list.append(stock_data)
            
    sum2=0
      
    for i in range (0,len(All_trans_list)):
        sum2=sum2+All_trans_list[i][1]      
       
    print "The ask side average is",sum2/len(All_trans_list)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    #bestbid,bestask=calculate_best_price()
    #print 'The best bid and the best ask is',bestbid,bestask    
      #print lob
      #print("*********************************")
     
    #someOrders=    [{'timestamp': 1, 'price': 186.4367, 'idNum': 1, 'qty': 14, 'tid': 1, 'type': 'limit', 'side': 'bid'}, {'timestamp': 2, 'price': 122.8578, 'idNum': 2, 'qty': 46, 'tid': 2, 'type': 'limit', 'side': 'bid'}, {'timestamp': 3, 'price': 109.7046, 'idNum': 3, 'qty': 48, 'tid': 3, 'type': 'limit', 'side': 'bid'}, {'timestamp': 4, 'price': 139.4787, 'idNum': 4, 'qty': 33, 'tid': 4, 'type': 'limit', 'side': 'bid'}, {'timestamp': 5, 'price': 186.4367, 'idNum': 5, 'qty': 27, 'tid': 5, 'type': 'limit', 'side': 'bid'}, {'timestamp': 6, 'price': 139.4787, 'qty': 47, 'tid': 1, 'type': 'limit', 'side': 'bid'}, {'timestamp': 7, 'price': 199.6157, 'qty': 48, 'tid': 2, 'type': 'limit', 'side': 'bid'}, {'timestamp': 8, 'price': 109.6851, 'idNum': 8, 'qty': 31, 'tid': 3, 'type': 'limit', 'side': 'bid'}, {'timestamp': 9, 'price': 181.0681, 'qty': 49, 'tid': 4, 'type': 'limit', 'side': 'bid'}]
    #someOrders=    [{'timestamp': 1, 'price': 186.4367, 'idNum': 1, 'qty': 14, 'tid': 1, 'type': 'limit', 'side': 'ask'}, {'timestamp': 2, 'price': 122.8578, 'idNum': 2, 'qty': 46, 'tid': 2, 'type': 'limit', 'side': 'ask'}, {'timestamp': 3, 'price': 109.7046, 'idNum': 3, 'qty': 48, 'tid': 3, 'type': 'limit', 'side': 'ask'}, {'timestamp': 4, 'price': 110.7735, 'idNum': 4, 'qty': 33, 'tid': 4, 'type': 'limit', 'side': 'ask'}, {'timestamp': 5, 'price': 147.0808, 'idNum': 5, 'qty': 27, 'tid': 5, 'type': 'limit', 'side': 'ask'}, {'timestamp': 6, 'price': 139.4787, 'qty': 47, 'tid': 1, 'type': 'limit', 'side': 'bid'}, {'timestamp': 7, 'price': 199.6157, 'qty': 48, 'tid': 2, 'type': 'limit', 'side': 'bid'}, {'timestamp': 8, 'price': 109.6851, 'idNum': 8, 'qty': 31, 'tid': 3, 'type': 'limit', 'side': 'bid'}, {'timestamp': 9, 'price': 181.0681, 'qty': 49, 'tid': 4, 'type': 'limit', 'side': 'bid'}]
#==============================================================================
#==============================================================================
#     """ Add orders to LOB"""
#     for order in someOrders:
#         trades, idNum = lob.processOrder(order, False, False)
#==============================================================================
    
    """ The current limit order book may be viewed using a print"""
    #print lob
    
    """The loops print the qty and price in the current LOB"""
#   for key,value in lob.asks.orderMap.iteritems():
#        print value.qty,value.price,value.timestamp
#  
    """This loop prints out the LOB price in sorted order""" 
#   All_trans_list=[]
#   for key,value in lob.bids.orderMap.iteritems(): 
#       Node=()
#       Node=(value.qty,value.price,value.timestamp)
#       All_trans_list.append(Node)  
#   print All_trans_list  
#   print sorted(All_trans_list, key=lambda x: (-x[1], x[2]))
    
    """These are the operations on LOB and are currently not required"""
    # Submitting a limit order that crosses the opposing best price will 
    # result in a trade.
#    crossingLimitOrder = {'type' : 'limit', 
#                          'side' : 'bid', 
#                          'qty' : 11, 
#                          'price' : 150,
#                          'tid' : 109}
#    trades, orderInBook = lob.processOrder(crossingLimitOrder, False, False)
    #print "Trade occurs as incoming bid limit crosses best ask.."
    #print trades
#    print lob
#    
#    # If a limit order crosses but is only partially matched, the remaining 
#    # volume will be placed in the book as an outstanding order
#    bigCrossingLimitOrder = {'type' : 'limit', 
#                             'side' : 'bid', 
#                             'qty' : 50, 
#                             'price' : 102,
#                             'tid' : 110}
#    trades, orderInBook = lob.processOrder(bigCrossingLimitOrder, False, False)
#    print "Large incoming bid limit crosses best ask.\
#           Remaining volume is placed in the book.."
#    print lob
#    
#    ############# Market Orders ##############
#    
#    # Market orders only require that the user specifies a side (bid
#    # or ask), a quantity and their unique tid.
#    marketOrder = {'type' : 'market', 
#                   'side' : 'ask', 
#                   'qty' : 40, 
#                   'tid' : 111}
#    trades, idNum = lob.processOrder(marketOrder, False, False)
#    print "A limit order takes the specified volume from the\
#            inside of the book, regardless of price" 
#    print "A market ask for 40 results in.."
#    print lob
#    
#    ############ Cancelling Orders #############
#    
#    # Order can be cancelled simply by submitting an order idNum and a side
#    print "cancelling bid for 5 @ 97.."
#    lob.cancelOrder('bid', 8)
#    print lob
#    
#    ########### Modifying Orders #############
#    
#    # Orders can be modified by submitting a new order with an old idNum
#    lob.modifyOrder(5, {'side' : 'bid', 
#                    'qty' : 14, 
#                    'price' : 99,
#                    'tid' : 100})
#    print "book after modify..."
#    print lob
    

