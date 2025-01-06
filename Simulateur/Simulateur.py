import threading
import time
import logging
from Simulateur.SimuConfig import SimuConfig

import psutil
import os

class Simulateur:
    def __init__(self):
        self.logger = logging.getLogger('__name__')
        self.setupThread()
        

    def setupThread(self) -> None:
        """
        Initialise les attributs nécessaires pour gérer le thread et l'état de la simulation.
        """
        self.thread = None
        self.pause_event = threading.Event()
        self.stop_event = threading.Event()

    def simulationRt(self, step, speed,isRt):
        """
        Fonction de simulation.
        Cette fonction sera exécutée dans un thread séparé.
        Elle peut être mise en pause et reprise en utilisant les événements de pause et d'arrêt.
        """
        # Attribuer des cœurs spécifiques au thread de simulation
        #p = psutil.Process(os.getpid())
        #p.cpu_affinity([0, 1])  # Attribuer les cœurs 0 et 1 au thread de simulation
        start = time.perf_counter()
        cnt = 0
        dtTh = step/speed

        while not self.stop_event.is_set():
            dt =  cnt*dtTh -( time.perf_counter() - start)
            if dt < 0:
                if not self.pause_event.is_set():
                    self.pause_event.wait()  # Attendre que l'événement de pause soit réinitialisé
                self.config.simuRt(step, isRt)
                cnt += 1
            else:
                time.sleep(dt)  # Simuler une tâche avec un délai
            
                
    
    def startSimulation(self, step, speed, isRt) -> None:
        """
        Démarre la simulation dans un thread séparé.
        """
        
        self.stop_event.clear()
        self.config.resetSimu()
        if self.thread is None or not self.thread.is_alive():
            self.stop_event.clear()
            self.pause_event.set()  # Assurez-vous que la simulation commence en pause
            self.thread = threading.Thread(target=self.simulationRt, args=(step,speed,isRt, ))
            self.thread.start()


    def pause(self):
        """
        Met en pause la simulation.
        """
        self.logger.info("mise en pause")
        self.pause_event.clear()


    def resume(self):
        """
        Reprend la simulation si elle est en pause.
        """
        self.logger.info("Reprise simulation")
        self.pause_event.set()

        

    def stop(self):
        """
        Arrête la simulation.
        """
        self.stop_event.set()
        self.pause_event.set()  # Assurez-vous que la simulation peut se terminer proprement
        if self.thread is not None:
            self.thread.join()
        self.config.resetSimu()

    def calculSimulation(self, T) -> bool:
        """
        @brief Lance le calcul de la simulation
        @return Renvoie un boolean à la fin du calcul
        """
        self.config.resetSimu()
        self.config.preCalcSimu(T)
        return True


    def setConfig(self, config : SimuConfig):
        """
        @brief 
        """
        self.config = config

    
        



