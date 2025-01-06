import numpy as np
import control as ct
from Utilitaires.Observer import Subject

import logging
from Utilitaires.Module import Module

class MotorDC(Module):
    def __init__(self, params : dict = dict()):
        super().__init__()
        self.setMatrixState()
    
    def setParams(self):
        self.params.setdefault("RotorInteria",0.1)
        self.params.setdefault("DampingCoefficient",0.5)
        self.params.setdefault("TorqueConstant",1.0)
        self.params.setdefault("Resistor",1.0)
        self.params.setdefault("Impedance",1.0)
        self.params.setdefault("ElectromagneticConstant",5.0)

        self.J  : float = self.params.get("RotorInteria")
        self.b  : float = self.params.get("DampingCoefficient")
        self.Kt : float = self.params.get("TorqueConstant")
        self.L  : float = self.params.get("Resistor")
        self.R  : float = self.params.get("Impedance")
        self.Ke : float = self.params.get("ElectromagneticConstant")

    def setMatrixState(self):
        # define the system matrices
        self.A  =   [[0, 1, 0],
                    [ 0, -self.b/self.J, self.Kt/self.J],
                    [ 0, -self.Ke/self.L, -self.R/self.L]]

        self.B  =   [[0],
                    [0],
                    [ 1/self.L]]

        self.W  =   [[0],
                    [-1/self.J],
                    [0]]

        self.C  =   [0, 1, 0]

        self.D  =   0

        self.state = [[0],
                      [0],
                      [0]]
        
        self.initState = self.state

    def updfcn(self,t, x, u, params):
        return np.dot(self.A, x) + np.dot(self.B,u)

    def outfcn(self, t,x,u,params):
        self.setState(x)
        return np.dot(self.C, x) + np.dot(self.D,u)
    
    def setSysNames(self):
        self.statesStr  = ["theta","thetaDot","i"]
        self.inputsStr  = ["u"]
        self.outputsStr = ["thetaDot"]