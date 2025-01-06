from tkinter import ttk
import tkinter as tk

import logging

class Fenetre:
    def __init__(self, titre="Ma Fenêtre", largeur=1500, hauteur=1500):
        #log
        self.logger = logging.getLogger('__name__')
        
        self.root = tk.Tk()
        self.root.title(titre)
        #self.root.geometry(f"{largeur}x{hauteur}")
        #self.root.attributes('-zoomed',True)
        self.root.state("zoomed")
        # Création du PanedWindow horizontal
        self.panedWindowHorizontal = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.panedWindowHorizontal.pack(fill=tk.BOTH, expand=True)

        # Ajout des sous-fenêtres horizontales
        self.frame1 = ttk.Frame(self.panedWindowHorizontal, width=300, height=800, relief=tk.SUNKEN)
        self.panedWindowHorizontal.add(self.frame1, weight=1)

        # Création du PanedWindow vertical pour ajouter les frames 2 et 3
        self.panedWindowVertical = ttk.PanedWindow(self.panedWindowHorizontal, orient=tk.VERTICAL)
        self.panedWindowHorizontal.add(self.panedWindowVertical, weight=3)

        # Ajout des sous-fenêtres verticales
        self.frame2 = ttk.Frame(self.panedWindowVertical, width=300, height=400, relief=tk.SUNKEN)
        self.frame3 = ttk.Frame(self.panedWindowVertical, width=300, height=400, relief=tk.SUNKEN)

        self.panedWindowVertical.add(self.frame2)
        self.panedWindowVertical.add(self.frame3)


        self.uiWidgets = []

    def afficher(self):
        self.logger.info("Affichage de la fenetre")
  
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.update()
        self.root.mainloop()

    
    def onClose(self):
        self.logger.info("Fermeture de la fenetre")

        running = False
        self.root.destroy()
        self.root.quit()


    def addUi(self,ui):
        self.uiWidgets.append(ui)

    def update(self):
        for ui in self.uiWidgets:
            ui.updateUi()
        freq = 60

        self.root.after(int(1000/freq), self.update)