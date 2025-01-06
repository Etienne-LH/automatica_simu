
#utilitaires
from Utilitaires import Log

#Robot
from Robot.Robot import Robot
from Robot.RobotControllerUi import RobotControllerUi
from Robot.RobotUi import RobotUi

#Motor
from Motor.MotorDC import MotorDC

#Courbe
from PltUi import PltUi

#Fenetre
from Windows.Fenetre import Fenetre


#Simulation
from Simulateur.Simulateur import Simulateur
from Simulateur.SimuUi import SimuUi
from Simulateur.SimuConfig import SimuConfig
from Simulateur.SimuConfigs import *
#from Commande import Commande

#Python
import threading
import os
import control as ct
import argparse
import time
import numpy as np

import importlib

def importSimu():
    # Chemin vers le dossier contenant les fichiers Python
    folderPath = os.path.join('Simulateur', 'SimuConfigs')

    # Dictionnaire pour stocker les modules des classes
    classModules = {}

    # Liste tous les fichiers dans le dossier
    for filename in os.listdir(folderPath):
        if filename.endswith('.py') and filename != '__init__.py':
            # Construit le nom du module
            moduleName = filename[:-3]  # Enlève l'extension .py
            modulePath = f"Simulateur.SimuConfigs.{moduleName}"

            # Importe le module
            module = importlib.import_module(modulePath)

            # Détermine le nom de la classe de façon automatique
            className = f"{moduleName}"
            classObj = getattr(module, className, None)

            if classObj:
                # Stocke le module dans le dictionnaire
                classModules[className] = module
                logger.info(f"Imported {className} from {modulePath}")
            else:
                logger.info(f"Class {className} not found in module {moduleName}")

    return classModules


def parsing():
    # Initialize the ArgumentParser object
    parser = argparse.ArgumentParser(description="Set the logging level via command line")

    # Add a command-line argument for the logging level
    parser.add_argument("-lc", '--logConsole', default='INFO',choices=['DEBUG', 'INFO', 'WARNING','ERROR','CRITICAL'], help='Set the logging console level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    parser.add_argument("-lf", '--logFile', default='DEBUG', choices=['DEBUG', 'INFO', 'WARNING','ERROR','CRITICAL'], help='Set the logging file level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')

    return parser

def doSomething(robot,pltUi):
    global running
    global logger
    logger.debug("Debut Thread")

    
    #setup system
    sys = robot.getSys()
    T = [0,0.1]
    phiD = 0.1
    phiG = 0.1
    U = [[phiD,phiD],
         [phiG,phiG]]
    
    # #Boucle infinie
    while running:
        logger.debug("Nouvelle boucle")

        response = ct.input_output_response(
            sys = sys,X0 = robot.getState(), T =  T, U = U)
        #time.sleep(0.1)
        pltUi.update2(dt = [T[1],T[1]],
                      value = [robot.getInfo("x"),robot.getInfo("y")])


def setupUI(maFenetre):
    #Setup Robot
    robot = Robot(x = 0, y = 0, th = 90)
    robotUi = RobotUi(robot = robot, frame = maFenetre.frame1,
                      root = maFenetre.root,
                      imagePath = "Ressources/Robot2.png", ratio=0.5)
    robot.attach(robotUi)
    robotControllerUi = RobotControllerUi(robot = robot, frame = maFenetre.frame2,
                                          phi_range = 1,
                                          resolution = 0.01)
    robot.attach(robotControllerUi)
    
    #Courbe
    pltUi = PltUi(frame = maFenetre.frame3, size = 2)
    pltUi.update2(dt =[0,0],
                 value = [robot.getInfo("x"),robot.getInfo("y")])
    
    #fenetre
    maFenetre.addUi(robotUi)
    # maFenetre.addUi(robotControllerUi)
    maFenetre.addUi(pltUi)

    return robot,pltUi


if __name__=="__main__":
    # Parse the command-line arguments, ignoring unknown ones
    parser = parsing()
    logger = Log.loggerInit(parser)
    logger.info("Initialisation du logger")
    #COnfiguration de la simulation
    classModules = importSimu()
    className = 'MotorConfig'
    if className in classModules:
        ConfigFile = getattr(classModules[className], className)
    config = ConfigFile()
    
 
    # Utilisation de la classe Fenetre et PltUi
    maFenetre = Fenetre("Fenêtre avec 3 Frames", 600, 800)
    
    #Creation du du simulateur
    simu = Simulateur( ) 
    config.setSimu(maFenetre, simu)
    simu.setConfig(config = config)

    #Affichage de la fenetre
    maFenetre.afficher()
    
    
    logger.info("Fin du programme")
    
    os._exit(os.X_OK)

    
