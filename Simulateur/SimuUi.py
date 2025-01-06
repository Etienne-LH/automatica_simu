import tkinter as tk
from tkinter import ttk
import threading
import time
from PIL import Image, ImageTk
import logging
import numpy as np

class SimuUi:
    def __init__(self, frame, root, simu):
        """
        Initialise l'interface utilisateur pour la simulation.

        @param frame: Le cadre dans lequel les widgets seront ajoutés.
        @param root: La fenêtre principale de l'application.
        """
        self.logger = logging.getLogger('__name__')
        self.frame = frame
        self.root = root
        self.running = False
        self.paused = False
        self.simuThread = None
        self.modeRt = tk.BooleanVar(value=False)
        self.speed = 1.0

        # Chemins des images
        self.startImagePath = "Ressources/Start.png"
        self.pauseImagePath = "Ressources/Pause.png"
        self.reloadImagePath = "Ressources/Refresh.png"
        self.ProcessImagePath = "Ressources/Process.png"

        # Positions des éléments
        self.modeRow = 0
        self.dtRow = 1
        self.startEndRow = 2
        self.speedRow = 3
        self.actionRow = 4

        # Initialisation des widgets
        self.createModeCheckbox()
        self.createDtEntry()
        self.createStartEndEntries()
        self.createSpeedScale()
        self.createActionImage()
        self.createReloadButton()
        self.createProcessButton()

        # Masquer les champs de temps de départ et d'arrêt en mode RT
        self.toggleStartEndEntries()

        self.simu = simu

    def createModeCheckbox(self) -> None:
        """
        Crée la case à cocher pour choisir le mode de simulation.
        """
        self.modeLabel = ttk.Label(self.frame, text="Mode RT:")
        self.modeLabel.grid(row=self.modeRow, column=0, pady=5)
        self.modeCheckbutton = ttk.Checkbutton(self.frame, text="RT", variable=self.modeRt, command=self.toggleStartEndEntries)
        self.modeCheckbutton.grid(row=self.modeRow, column=1, pady=5)

    def createDtEntry(self) -> None:
        """
        Crée un champ de saisie pour la valeur de dt.
        """
        self.dtLabel = ttk.Label(self.frame, text="dt (s):")
        self.dtLabel.grid(row=self.dtRow, column=0, pady=5)
        self.dtEntry = ttk.Entry(self.frame)
        self.dtEntry.grid(row=self.dtRow, column=1, pady=5)
        self.dtEntry.insert(0, "0.01")  # Valeur par défaut

    def createStartEndEntries(self) -> None:
        """
        Crée des champs de saisie pour les valeurs de départ et de fin en mode non RT.
        """
        self.startValueLabel = ttk.Label(self.frame, text="Valeur de départ (s):")
        self.startValueLabel.grid(row=self.startEndRow, column=0, pady=5)
        self.startValueEntry = ttk.Entry(self.frame)
        self.startValueEntry.grid(row=self.startEndRow, column=1, pady=5)
        self.startValueEntry.insert(0, "0")  # Valeur par défaut

        self.endValueLabel = ttk.Label(self.frame, text="Valeur de fin (s):")
        self.endValueLabel.grid(row=self.startEndRow, column=2, pady=5)
        self.endValueEntry = ttk.Entry(self.frame)
        self.endValueEntry.grid(row=self.startEndRow, column=3, pady=5)
        self.endValueEntry.insert(0, "10")  # Valeur par défaut

    def createSpeedScale(self) -> None:
        """
        Crée une jauge pour la vitesse de la simulation.
        """
        self.speedLabel = ttk.Label(self.frame, text="Vitesse de la simulation:")
        self.speedLabel.grid(row=self.speedRow, column=0, pady=5)
        self.speedValueLabel = ttk.Label(self.frame, text=self.speed)
        self.speedValueLabel.grid(row=self.speedRow, column=2, pady=5)
        self.speedScale = ttk.Scale(self.frame, from_=0.1, to=10, orient=tk.HORIZONTAL, command=self.updateSpeed)
        self.speedScale.grid(row=self.speedRow, column=1, pady=5)
        self.speedScale.set(1)  # Valeur par défaut

    def createActionImage(self) -> None:
        """
        Crée une image cliquable pour démarrer, recharger ou mettre en pause la simulation.
        """
        self.actionImageLabel = ttk.Label(self.frame)
        self.actionImageLabel.grid(row=self.actionRow, column=1, pady=10)
        self.updateActionImage("start")
        self.actionImageLabel.bind("<Button-1>", self.handleActionClick)

    def createReloadButton(self) -> None:
        """
        Crée un bouton pour recharger la simulation.
        """
        self.reloadImage = Image.open(self.reloadImagePath)
        self.reloadImage = self.reloadImage.resize((50, 50), Image.LANCZOS)
        self.reloadImageTk = ImageTk.PhotoImage(self.reloadImage)
        self.reloadButton = ttk.Button(self.frame, image=self.reloadImageTk, command=self.reloadSimulation)
        self.reloadButton.grid(row=self.actionRow, column=2, pady=10)

    def createProcessButton(self) -> None :
        """
        Crée un bouton pour calculer la simulation en mode non rt
        """
        self.processImage = Image.open(self.ProcessImagePath)
        self.processImage = self.processImage.resize((50, 50), Image.LANCZOS)
        self.processImageTk = ImageTk.PhotoImage(self.processImage)
        self.processButton = ttk.Button(self.frame, image=self.processImageTk, command=self.processSimulation)
        self.processButton.grid(row=self.actionRow, column=0, pady=10)
    
    def processSimulation(self) -> None:
        """
        Permet de charger une simulation
        """
        if self.modeRt.get():
            return
        
        T = np.arange(float(self.startValueEntry.get()), float(self.endValueEntry.get()), float(self.dtEntry.get()), dtype=float)
        self.simu.calculSimulation(T = T)

    
    def updateSpeed(self, value) -> None:
        """
        Met à jour la vitesse de la simulation.

        @param value: La nouvelle valeur de la vitesse.
        """
        self.speed = float(value)
        self.speedValueLabel.config(text = value)

    def handleActionClick(self, event) -> None:
        """
        Gère les clics sur l'image d'action.

        @param event: L'événement de clic.
        """
        if not self.running:
            self.startSimulation()
        elif self.paused:
            self.resumeSimulation()
        else:
            self.pauseSimulation()

    def startSimulation(self) -> None:
        """
        Démarre la simulation.
        """
        self.logger.info("Start simulation clicked")
        self.running = True
        self.paused = False
        
        self.simu.startSimulation(step = float(self.dtEntry.get()),
                                  speed = self.speed,
                                  isRt = self.modeRt.get())
        #self.simuThread.start()
        self.updateActionImage("pause")

    def pauseSimulation(self) -> None:
        """
        Met en pause la simulation.
        """
        self.paused = True
        self.simu.pause()
        self.updateActionImage("start")

    def resumeSimulation(self) -> None:
        """
        Reprend la simulation.
        """
        self.paused = False
        self.simu.resume()
        self.updateActionImage("pause")

    def reloadSimulation(self) -> None:
        """
        Recharge la simulation.
        """
        self.stopSimulation()
        self.running = False
        #self.startSimulation()

    def stopSimulation(self) -> None:
        """
        Arrête la simulation.
        """
        self.running = False
        self.paused = False
        self.simu.stop()
        #if self.simuThread:
        #    self.simuThread.join(timeout=0.2)
        self.updateActionImage("start")

    def updateActionImage(self, action: str) -> None:
        """
        Met à jour l'image d'action en fonction de l'action en cours.

        @param action: L'action en cours ("start", "pause").
        """
        if action == "start":
            imagePath = self.startImagePath
        elif action == "pause":
            imagePath = self.pauseImagePath
        else:
            return

        image = Image.open(imagePath)
        image = image.resize((50, 50), Image.LANCZOS)
        self.actionImage = ImageTk.PhotoImage(image)
        self.actionImageLabel.config(image=self.actionImage)

    def toggleStartEndEntries(self) -> None:
        """
        Affiche ou masque les champs de saisie pour les valeurs de départ et de fin en fonction du mode de simulation.
        """
        if self.modeRt.get():
            self.startValueLabel.grid_forget()
            self.startValueEntry.grid_forget()
            self.endValueLabel.grid_forget()
            self.endValueEntry.grid_forget()
            self.processButton.grid_forget()
        else:
            self.startValueLabel.grid(row=self.dtRow, column=2, pady=5)
            self.startValueEntry.grid(row=self.dtRow, column=3, pady=5)
            self.endValueLabel.grid(row=self.dtRow, column=4, pady=5)
            self.endValueEntry.grid(row=self.dtRow, column=5, pady=5)
            self.processButton.grid(row= self.actionRow, column=0, pady=5)


    def updateUi(self) -> None:
        """
        Met à jour l'interface utilisateur.
        """
        pass
