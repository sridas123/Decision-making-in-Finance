import Agent2 as Agent
import Agent2_rnd as Agent_rnd
import Agent2_baseline as Agent_baseline
import Env as Env

class rlglueD:
    def __init__(self,numTran,numStep,volume,time,frunflag,parm):
        self.numSteps = numStep
        self.lastAction = None
        self.lastState = None
        self.env = Env.EnvCls(numTran,frunflag,volume,time)
        
        """Calls separate Agent modules based on different strategies"""
        if parm=="greedy":
           self.agent = Agent.AgentCls(volume,time)
        elif parm=="random":
           self.agent=Agent_rnd.AgentRand(volume,time)
        else:
           self.agent=Agent_baseline.Agentbase(volume,time)
           
        self.lastStep = 0
        self.totalRewards=0
        
        if parm=="greedy" and frunflag==False:
           self.fepisode_over=False
        else: 
           self.fepisode_over= True
           
           
    def rl_start(self,volume,time):
        
        self.lastStep =1
        self.totalRewards=0
        lastState = self.env.env_start(volume,time,self.fepisode_over)
        lastAction = self.agent.agent_start(lastState)
        return lastState,lastAction
        
        
    def rl_episode(self,volume,time,parm):
         self.lastState,self.lastAction = self.rl_start(volume,time)
         #print 'The state and action is',self.lastState,self.lastAction
         
         """This while loop is a check on when an episode will terminate"""
         epOv=False 
        
         while self.lastStep<=self.numSteps:
             
           
           state,reward,price,epOv = self.env.env_step1(self.lastAction,self.fepisode_over,parm)
           #print state
           self.lastState=state
           #print 'The Reward is',reward
           self.totalRewards += reward
           self.lastStep += 1
           if epOv == True:
              
              #print 'I am trying to end the episode'
              self.fepisode_over=True
              if (parm=="greedy" or parm=="baseline"):
                 self.agent.agent_end(state,reward) 
              return
              
           else:
              #print 'I am getting into the Agent step' 
              self.lastAction = self.agent.agent_step(reward,state,price) 
           #print 'The state and action is',state,self.lastAction,epOv   
            
    def rl_get_steps(self):
        return self.lastStep
        
    def getTheta(self):
        return self.agent.retTheta()
        
    def getTotReward(self):
        return self.totalRewards
        
    
    