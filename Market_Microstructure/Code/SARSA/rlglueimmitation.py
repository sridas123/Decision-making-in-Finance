import Agent2_baseline as Agent_base
import Env as Env

class rlglueD:
    def __init__(self,numTran,numStep,volume,time,frunflag):
        self.numSteps = numStep
        self.lastAction = None
        self.lastState = None
        self.env = Env.EnvCls(numTran,frunflag,volume,time)
        self.agent = Agent_base.Agentbase(volume,time)
        self.lastStep = 0
        self.totalRewards=0
        self.fepisode_over=False
        
    
    def rl_start(self,volume,time):
        
        self.lastStep =1
        self.totalRewards=0
        lastState = self.env.env_start(volume,time,self.fepisode_over)
        lastAction = self.agent.agent_start(lastState)
        return lastState,lastAction
        
        
    def rl_episode(self,volume,time):
         self.lastState,self.lastAction = self.rl_start(volume,time)
         #print 'The state and action is',self.lastState,self.lastAction
         
         """This while loop is a check on when an episode will terminate"""
         epOv=False 
        
         while self.lastStep<=self.numSteps:
             
           
           state,reward,price,epOv = self.env.env_step1(self.lastAction,self.fepisode_over)
           #print state
           self.lastState=state
           print 'The Reward is',reward
           self.totalRewards += reward
           self.lastStep += 1
           if epOv == True:
              
              #print 'I am trying to end the episode'
              self.fepisode_over=True
              self.agent.agent_end(state,reward) 
              return
              
           else:
              #print 'I am getting into the Agent step' 
              self.lastAction = self.agent.agent_step(reward,state,price) 
           print 'The state and action is',self.lastAction,epOv   
            
    def rl_get_steps(self):
        return self.lastStep
        
    def getTheta(self):
        return self.agent.retTheta()
        
    def getTotReward(self):
        return self.totalRewards
        
    
    