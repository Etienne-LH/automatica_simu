import logging
from Simulateur.SimuUi import SimuUi
from PltUi import PltUi
import numpy as np

class SimuConfig:
    def __init__(self):
        #log
        self.logger = logging.getLogger('__name__')
        self.step = 0
        self.response = None

    def preCalcSimu(self, T = None, run = False):
        pass


    def simuRt(self, dt : float, isRt : bool):
        pass
        
    def resetSimu(self):
        pass

    def simuCalc(self,T, response, speed):
        pass

    def setSimu(self,maFenetre, simu):
        """
        Instancie les composant de la simulation
        Autant graphique que physique

        @param maFenetre : Fenetre d'affichage
        @param simu : Interface graphique de gestion de la simulation
        @return pltUI : interface 
        """
        self.pltUi = PltUi(frame=maFenetre.frame3, size=1)

        self.simuUi = SimuUi(frame=maFenetre.frame2, root=maFenetre.root, simu = simu)

        maFenetre.addUi(self.pltUi)
        maFenetre.addUi(self.simuUi)

    def getStateAt(self, states, tp):
        """
        @brief Retrun the array of state for a specifique time tp
        """
        state = np.array([])
        for iState in states:
            state = np.append(state, iState[tp])

        return state
        
