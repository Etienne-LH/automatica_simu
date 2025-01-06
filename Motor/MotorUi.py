import tkinter as tk

from PIL import Image, ImageTk
import numpy as np
from Utilitaires.Observer import Observer
import time 
import logging

from ModuleUi import ModuleUi

class MotorUi(ModuleUi):
    def updateValues(self):
        self.logger.debug("Le MotorUI prend connaissance des nouvelles valeurs")
        orientation = self.module.getInfo("theta")
        self.imgOrient = np.rad2deg(orientation)
