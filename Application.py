from PyQt6.QtWidgets import QApplication


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)