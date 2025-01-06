from Simulateur.SimuConfig import SimuConfig
from Motor.MotorDC import MotorDC
from Motor.MotorUi import MotorUi
import control as ct
import numpy as np

class MotorConfig(SimuConfig):
    def __init__(self):
        super().__init__()

    def preCalcSimu(self, T = None, run = False):
        #setup system
        if T is None :
            T = np.linspace(0,5,num = 500)

        U = T*0 + 10
        self.response = ct.input_output_response(
            sys = self.motor.getSys(),
            X0 = self.motor.getState(), T =  T, U = U,
            return_x=True)
        
        self.pltUi.setCourbe(self.response.t,
                    self.response.y[0])

    def simuRt(self, dt : float, isRt : bool):
        stop = False
        T = [0,dt]
        if isRt :
            U = [10,10]

            ct.input_output_response(
                        sys = self.motor.getSys(),
                        X0 = self.motor.getState(), T =  T, U = U)
        
        if not isRt:
            if (not self.response is None ) and self.step < len(self.response.t) :
                self.motor.setState(self.getStateAt(self.response.x,
                                                    self.step))
                self.step += 1
            else:
                stop = True
                
        if not stop:
            self.pltUi.update2(dt = [T[1]],
                    value = [self.motor.getInfo("thetaDot")])
        
    def resetSimu(self):
        self.pltUi.clear()
        self.motor.setInitState()
        self.step = 0

    def setSimu(self,maFenetre, simu):
        self.motor = MotorDC()
        self.motorUi = MotorUi( module = self.motor,
                                frame = maFenetre.frame1,
                                root = maFenetre.root,
                                imagePath = "Ressources/Roue.png",
                                ratio=0.25)
        self.motorUi.move(100,100)
        self.motor.attach(self.motorUi)
        maFenetre.addUi(self.motorUi)

        super().setSimu(maFenetre, simu)

        self.pltUi.setYLabel("Vitesse [rad/s]")
"""
    def simuCalc(self, T, response, speed):
        self.pltUi.clear()
        dt = T[1] - T[0]
        for i in range(len(T)):
            self.pltUi.update2(dt = [dt],
                        value = [response.y[0][i]]) 
            time.sleep(dt/speed)

 """   
    
