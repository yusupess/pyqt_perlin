from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import pyqtSlot

from .Model import Model
from .DialogOld import DialogOld

"""Представление поазывающее список студентов входящих в группу."""
class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)
    
    @pyqtSlot(int)
    def select_group(self, id_group=None):
        self.model().refill(id_group)
    
    @pyqtSlot()
    def add_old_student(self):
        id_group = self.model().id_group
        if id_group is None:
            return
        dia = DialogOld(id_group, parent=self)
        dia.exec()
