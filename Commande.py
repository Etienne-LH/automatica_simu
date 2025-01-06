import numpy as np
import control as ct
import matplotlib.pyplot as plt

class Commande:
    def __init__(self, sys = None):
        self.sys = sys
        self.T = None
        self.Yout = None
        self.obj = None
        
        #PID
        self.kp : float = 0
        self.kd : float = 0
        self.ki : float = 0
  
        self.error = None
        self.cmd = None

        
    def setSys(self,sys):
        self.sys = sys
        
    def setTime(self, start : float = 0, end : float = 1,
                dt : float = 0, nb : int = 0 ):
        if start > end:
            start,end = end,start
         
        if dt == 0 and nb == 0:
            dt = 0.1
        
        if start == end:
            end = start + dt
        
        if nb == 0 :
            nb = 1 + (end - start) / dt 

        self.T = np.linspace(start,end,int(nb))
        
    def forced_response(self, initState):
        T, self.yout, xState = ct.forced_response(self.sys, T = self.T, U = self.U, X0 = initState, return_x = True)
        
    def step(self, initialState = None, uValue : float = 1):
        UCmd = np.ones(len(self.T)) * uValue
        if initialState is None:
            T, self.yout,xState = ct.forced_response(self.sys, T = self.T,
                                              U = UCmd, return_x = True)
        else:
            #T, self.yout = ct.step_response(self.sys, T = self.T, X0 = initialState)
            T, self.yout,xState = ct.forced_response(self.sys, T = self.T,
                                              U = UCmd, X0 = initialState
                                             ,return_x = True)
        
    def plot(self):
        nb = 111
        if not self.error is None:
            nb = 311
        if (not self.T is None) and (not self.yout is None):
            fig, (ax1,ax2,ax3) = plt.subplots(3,1)
            ax1.plot(self.T, self.yout.T)
            ax1.set(xlabel='Time (s)', ylabel='Sortie',
            title='Sorte en fonction du temps')
            ax1.grid()
            
            if not self.error is None:
                ax2.plot(self.T, self.error)
                ax2.set(xlabel='Time (s)', ylabel='erreur',
                title='Erreur')
                ax2.grid()
                
                ax3.plot(self.T, self.cmd)
                ax3.set(xlabel='Time (s)', ylabel='Commande',
                title='Commande')
                ax3.grid()
                
            

            
            #plt.plot(self.T, self.yout.T, xlabel= "Time [s]", ylabel = "Out")
            
    def setObj(self, obj = 0):
        self.obj = obj
        
    def setPID(self, kp : float = 0,kd : float =0 ,ki : float = 0):
        self.kp = kp;
        self.kd = kd;
        self.ki = ki;

    def getActualState(self, xState):
        state = np.array([])
        for i in xState:
            state = np.append(state,i[1])
        return state

    def sum(self, v):
        res = 0
        for i in v:
            res += v

    def run(self, initialState = None):
        error = np.zeros(len(self.T))
        cmd = np.ones(len(self.T))
        self.yout = np.zeros(len(self.T))

        for i in range(len(self.T) - 1):
            if i == 0:
                state = initialState
                
            else:
                state = self.getActualState(xState)
            
            error[i] = self.obj - self.yout[i]
            
            cmd[i] = cmd[i-1] + self.kp*error[i]
            if i > 1 :
                cmd[i] = cmd[i] + self.kd*(error[i] -error[i-1])
                cmd[i] = cmd[i] + self.ki*(np.sum(error[0:i]))
            

            
            T, y, xState = ct.forced_response(self.sys, T = [self.T[i],self.T[i+1]], U = [cmd[i],cmd[i+1]], X0 = state, return_x = True)
            self.yout[i+1] = y[1]
        
        error[len(error)-1] = error[len(error)-2]
        self.error = error
        cmd[len(cmd)-1] = cmd[len(cmd)-2]
        self.cmd = cmd

    def oneStep(self, dt,cmd,state):

        T, y, xState = ct.forced_response(self.sys, T = [0,dt], U = [cmd[0],cmd[1]], X0 = state, return_x = True)
        return y, xState
        
        

            
            
