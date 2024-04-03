from PyQt6.QtCore import QAbstractTableModel


class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)