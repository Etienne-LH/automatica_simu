import tkinter as tk

from PIL import Image, ImageTk
import numpy as np
from Utilitaires.Observer import Observer
import time 
import logging

class ModuleUi(Observer):
    def __init__(self, module, root,frame, imagePath = None, ratio=1.0):
        super().__init__()
        self.logger = logging.getLogger('__name__')

        self.module = module
        self.frame = frame
        self.root = root

        self.initImage(imagePath, ratio)

        # Canvas pour afficher le module
        self.canvas = tk.Canvas(self.frame, width=100, height=100)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # self.canvas.create_rectangle(0, 0, 500,500, fill='red')
        #self.lastRefresh = 0
        #self.freq = 30

    def initImage(self, imagePath, ratio = 1.0):
        self.imagePath = imagePath
        self.ratio = ratio
        self.image = None
        self.photo = None
        self.oldImgOrient = 0
        self.imgOrient = 0
        self.resized = False

        self.xImg = 0
        self.yImg = 0
        self.ecart= 0.001

        self.dxImg = 0
        self.dyImg = 0

        self.imgIsCreate = False

    #def isTimeOk(self) -> bool:
    #    elapsedTime = time.time() - self.lastRefresh
    #    if elapsedTime > (1/self.freq):
    #        self.lastRefresh = time.time()
    #        return True
    #    return False
    
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
            self.logger.debug("On charge l'image du module")
            self.image = Image.open(self.imagePath)
        
        # Redimensionner l'image en fonction du ratio
        if not self.resized:
            self.logger.debug("On redimensionne l'image du module")
            width, height = self.image.size
            new_size = (int(width * self.ratio), int(height * self.ratio))
            self.image = self.image.resize(new_size, Image.LANCZOS)
            self.image = self.image.convert('RGBA')
            self.resized = True
            self.centre = (new_size[0]/2,new_size[1]/2 )

        # Appliquer la rotation en fonction de l'orientation
        if self.photo is None or self.oldImgOrient != self.imgOrient:
                self.logger.debug("On change l'orientation l'image du module")
                rotated_image = self.image.rotate(-self.imgOrient, 
                                                  center =self.centre,
                                                  fillcolor = (255, 255, 255, 0))
                if not self.imgIsCreate:
                    self.logger.debug("On creer l'imageTK du module")
                    self.photo = ImageTk.PhotoImage(rotated_image)
                else:
                    self.logger.debug("On paste l'imageTK du module")
                    self.photo.paste(rotated_image)
                self.oldImgOrient = self.imgOrient

        if not self.imgIsCreate:
            self.logger.debug("On creer l'image du module sur le canva")
            self.img = self.canvas.create_image(self.xImg, self.yImg, image=self.photo, anchor=tk.CENTER)
            self.imgIsCreate = True
        elif self.dxImg > self.ecart or self.dyImg > self.ecart:
            self.logger.debug(f"On bouge l'image du module sur le canva. dx = {self.dxImg}, dy = {self.dyImg}, imf = {self.img}")
            self.canvas.move(self.img,self.dxImg,self.dyImg)
            self.dxImg = 0
            self.dyImg = 0

    def updateValues(self):
        pass

    
    def move(self, dx = 0, dy = 0):
        self.dxImg += dx
        self.dyImg += dy


        