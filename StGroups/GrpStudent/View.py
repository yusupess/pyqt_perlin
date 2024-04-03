from PyQt6.QtWidgets import QTableView

from .Model import Model

class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)
        