import tkinter as tk

from PIL import Image, ImageTk
import numpy as np
from Utilitaires.Observer import Observer
import time 

import logging

class RobotUi(Observer):
    def __init__(self, robot, root,frame, imagePath, ratio=1.0):
        super().__init__()
        self.logger = logging.getLogger('__name__')

        self.robot = robot
        self.frame = frame
        self.root = root
        self.imagePath = imagePath
        self.ratio = ratio
        self.image = None
        self.photo = None
        self.oldOrient = 0
        self.orientation = 0
        self.resized = False

        # Canvas pour afficher le robot
        self.canvas = tk.Canvas(self.frame, width=100, height=100)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # self.canvas.create_rectangle(0, 0, 500,500, fill='red')
        self.lastRefresh = 0
        self.freq = 30
        self.create = False
        
        self.x = 0
        self.y = 0

        self.dx = 0
        self.dy = 0
        self.ecart = 0.001

    def isTimeOk(self) -> bool:
        elapsedTime = time.time() - self.lastRefresh
        if elapsedTime > (1/self.freq):
            self.lastRefresh = time.time()
            return True
        return False
        
    def updateValues(self):
        self.logger.debug("Le RobotUi prend connaissance des nouvelles valeurs")
        state = self.robot.getState()
        self.orientation = np.rad2deg(state[2])
        
        #Position
        x :float = state[0]
        y :float = state[1]

        self.dx += x - self.x
        self.dy += y - self.y

        self.x = x
        self.y = y
        
        
    def update(self, message):
        """
        @brief Réagit à la notification reçue.
        @param message Le message ou les données reçues.
        """
        match message:
            case "state": self.updateValues()
    
    def updateUi(self):
         # Charger l'image PNG
        if self.image is None:
            self.logger.debug("On charge l'image du robot")
            self.image = Image.open(self.imagePath)
        
        # Redimensionner l'image en fonction du ratio
        if not self.resized:
            self.logger.debug("On redimensionne l'image du robot")
            width, height = self.image.size
            new_size = (int(width * self.ratio), int(height * self.ratio))
            self.image = self.image.resize(new_size, Image.LANCZOS)
            self.image = self.image.convert('RGBA')
            self.resized = True
            self.centre = (new_size[0]/2,new_size[1]/2 )

        # Appliquer la rotation en fonction de l'orientation
        if self.photo is None or self.oldOrient != self.orientation:
                self.logger.debug("On change l'orientation l'image du robot")
                rotated_image = self.image.rotate(-self.orientation, 
                                                  center =self.centre,
                                                  fillcolor = (255, 255, 255, 0))
                if not self.create:
                    self.logger.debug("On creer l'imageTK du robot")
                    self.photo = ImageTk.PhotoImage(rotated_image)
                else:
                    self.logger.debug("On paste l'imageTK du robot")
                    self.photo.paste(rotated_image)
                self.oldOrient = self.orientation

        if not self.create:
            self.logger.debug("On creer l'image du robot sur le canva")
            self.img = self.canvas.create_image(self.x, self.y, image=self.photo, anchor=tk.CENTER)
            self.create = True
        else:
            self.logger.debug(f"On bouge l'image robot sur le canva. dx = {self.dx}, dy = {self.dy}, imf = {self.img}")
            self.canvas.move(self.img,self.dx,self.dy)
            self.dx = 0
            self.dy = 0


        