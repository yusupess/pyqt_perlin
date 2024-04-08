from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import pyqtSlot

from .Model import Model

class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)
    
    @pyqtSlot(int)
    def select_group(self, id_group=None):
        self.model().refill(id_group)