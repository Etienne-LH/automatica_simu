import tkinter as tk
from Utilitaires.Observer import Observer


class RobotControllerUi(Observer):
    def __init__(self,robot, frame, phi_range=1, resolution = 0.1):
        super().__init__()
        self.frame = frame
        self.robot = robot
        self.resolution = resolution
        # Création des jauges pour phiD et phiG
        self.label_phiD = tk.Label(frame, text="Vitesse roue droite (phiD):")
        self.label_phiD.pack()
        self.scale_phiD = tk.Scale(frame, from_=-phi_range, to=phi_range, orient=tk.HORIZONTAL,
                                   command=self.on_phiD_change,
                                   resolution = self.resolution,
                                   length=300)
        self.scale_phiD.pack()

        self.label_phiG = tk.Label(frame, text="Vitesse roue gauche (phiG):")
        self.label_phiG.pack()
        self.scale_phiG = tk.Scale(frame, from_=-phi_range/10, to=phi_range/10, orient=tk.HORIZONTAL,
                                   command=self.on_phiG_change,
                                   resolution = self.resolution/10,
                                   length=300)
        self.scale_phiG.pack()

    def on_phiD_change(self, value):
        self.robot.setSpeed(phiD = float(value))

    def on_phiG_change(self, value):
        self.robot.setSpeed(phiG = float(value))

    def set_phiD(self, value):
        self.scale_phiD.set(value)

    def set_phiG(self, value):
        self.scale_phiG.set(value)
        
    def update_robot(self):
        # Mettre à jour les valeurs du robot
        self.robot.set_position(int(self.entryX.get()), int(self.entryY.get()))
        self.robot.set_orientation(int(self.entryOrientation.get()))
        # Redessiner le robot
        self.robotUi.draw()
        
    def update(self, message):
        """
        @brief Réagit à la notification reçue.
        @param message Le message ou les données reçues.
        """
        match message:
            case "speed": 
                self.set_phiD(self.robot.getPhiD())
                self.set_phiG(self.robot.getPhiG())
