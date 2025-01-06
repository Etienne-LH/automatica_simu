from Utilitaires.Observer import Subject
from control.matlab import *  # MATLAB-like functions
import control as ct
import logging

class Module(Subject):
    def __init__(self, params : dict = dict()):
        super().__init__()
        self.logger = logging.getLogger('__name__')
        self.initState = None
        self.setSysNames()

        self.params : dict = params
        self.setParams()
        self.sys = ct.nlsys(updfcn  =   self.updfcn,
                            outfcn  =   self.outfcn,
                            states  =   self.statesStr,
                            inputs  =   self.inputsStr,
                            outputs =   self.outputsStr,
                            params  =   self.params )

    
    def setCommande(self, u):
        self.u = u

    def getSys(self):
        return self.sys
        
    def setSysNames(self):
        pass

    def setParams(self):
        pass
     
    def updfcn(self,t, x, u, params):
        pass

    def outfcn(self, t,x,u,params):
        pass

    def setState(self, state):
        self.notify("state")
        self.state = state
        
    def getState(self,):
        return self.state
        
    def getInfo(self, name):    
        for i in range(len(self.statesStr)):
            if self.statesStr[i] == name :
               return self.state[i]
           
        for i in range(len(self.inputsStr)):
            if self.inputsStr[i] == name :
               return self.u[i]

        return None
    
    def setInitState(self) -> None:
        """
        Set l'état du module dans son état initial
        """
        self.state = self.initState
    