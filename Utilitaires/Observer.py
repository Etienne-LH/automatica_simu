class Observer:
    """
    @brief Classe de base pour tous les observateurs.
    """
    def update(self, message):
        """
        @brief Méthode appelée pour notifier l'observateur d'un changement.
        @param message Le message ou les données envoyées à l'observateur.
        """
        pass

class Subject:
    """
    @brief Classe de base pour tous les sujets observables.
    """
    def __init__(self):
        """
        @brief Constructeur initialisant la liste des observateurs.
        """
        self.observers = []

    def attach(self, observer):
        """
        @brief Ajoute un observateur à la liste.
        @param observer L'observateur à ajouter.
        """
        self.observers.append(observer)

    def detach(self, observer):
        """
        @brief Retire un observateur de la liste.
        @param observer L'observateur à retirer.
        """
        self.observers.remove(observer)

    def notify(self, message):
        """
        @brief Notifie tous les observateurs d'un changement.
        @param message Le message ou les données à envoyer aux observateurs.
        """
        for observer in self.observers:
            self.logger.debug(f"Envoie d'un message à l'observeur : {message}")
            observer.update(message)

class ConcreteObserver(Observer):
    """
    @brief Un observateur concret qui réagit aux notifications.
    """
    def update(self, message):
        """
        @brief Réagit à la notification reçue.
        @param message Le message ou les données reçues.
        """
        print(f"ConcreteObserver a reçu le message: {message}")

class ConcreteSubject(Subject):
    """
    @brief Un sujet concret qui peut changer d'état et notifier les observateurs.
    """
    def changeState(self, message):
        """
        @brief Change l'état du sujet et notifie les observateurs.
        @param message Le message ou les données à envoyer aux observateurs.
        """
        print(f"ConcreteSubject change d'état avec le message: {message}")
        self.notify(message)

# Exemple d'utilisation
if __name__ == "__main__":
    subject = ConcreteSubject()
    observer1 = ConcreteObserver()
    observer2 = ConcreteObserver()

    subject.attach(observer1)
    subject.attach(observer2)

    subject.changeState("Nouvel état 1")
    subject.changeState("Nouvel état 2")