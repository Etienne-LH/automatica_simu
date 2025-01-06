from re import I
import numpy as np
import control as ct
from Utilitaires.Observer import Subject

import logging

class Robot(Subject):
    def __init__(self, x= 0, y = 0, th = 0, params : dict = dict()):
        super().__init__()
        self.logger = logging.getLogger('__name__')
        
        th = np.deg2rad(th)
        self.setState([x,y,th])
        self.setSysNames()
        self.params : dict = params
        self.setParams()
        self.sys = ct.nlsys(updfcn  =   self.updfcn,
                            outfcn  =   self.outfcn,
                            states  =   self.statesStr,
                            inputs  =   self.inputsStr,
                            outputs =   self.outputsStr,
                            params  =   self.params )
    
        
        self.u = np.array([None,None])

    def setSpeed(self, phiD = None, phiG = None):
        change = False
        if not phiD is None:
            if phiD !=self.u[0]:
                self.u[0] = phiD
                change = True
            
        if not phiG is None:
            if phiG !=self.u[1]:
                self.u[1] = phiG
                change = True  
        if change:
            self.notify("speed")   
    
            
    def getPhiD(self):
        return self.u[0]
    
    def getPhiG(self):
        return self.u[1]

    def getSys(self):
        return self.sys
        
    def setSysNames(self):
        self.statesStr  = ["x","y","th"]
        self.inputsStr  = ["phiD","phiG"]
        self.outputsStr = self.statesStr

    def setParams(self):
        self.params.setdefault("rayon",1.0)
        self.params.setdefault("distance",130.0)

        self.r : float = self.params.get("rayon")
        self.R : float = self.params.get("distance")

        self.rMat = [[self.r/2 , self.r/2],
                    [-self.r/(2*self.R) , self.r/(2*self.R)]]
        
        self.rMat = np.linalg.inv(self.rMat)
     
    def updfcn(self,t, x, u, params):
        self.logger.debug("Boucle d'entrée")
        if self.u[0] is None:
            self.setSpeed(phiD = u[0],phiG=u[1])
        else :
            u = self.u

        uMat = np.dot(self.rMat,u)
        uMat = u
        
        th      = x[2]
        thMat   =   [[np.cos(th) , 0],
                    [np.sin(th), 0],
                    [0,1]]
        return np.dot(thMat,uMat)

    def outfcn(self, t,x,u,params):
        self.logger.debug("Boucle de sortie")
        self.setState(x)
        return x

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
           
        

            
 
        

class RobotError():
    def __init__(self, robot):
        self.robot = robot
        self.setOP()
        
    def setOP(self):
        #OP = OP0 + l1*i1 +l2*j1   
        self.l1 = 0
        self.l2 = 0

    def calculError(self, xr, yr, u1, u2, xdr, ydr):
        theta = 0 #radiant
        self.error = [self.xp - xr, self.yp - yr]

        A = [[np.cos(theta), -self.l1 * np.sin(theta)],
            [np.sin(theta), self.l1 * np.cos(theta)]]
        B = [[1,-self.l2],
             [0,1]]
        C = [[u1],
             [u2]]
        
        D = [[xdr],
             [ydr]]
        

        self.errorDot = np.dot(np.dot(A,B),C) - D

    def other(self,u2):
        thd = u2

        
    