from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
import psycopg2
import settings as st


# SELECT_ALL = """select * from student_"""



class Model(QAbstractTableModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.refill()

    def rowCount(self, parent_index) -> int:
        if parent_index.isValid():
            return 0
        return 10
    
    def columnCount(self, parent_index) -> int:
        return 0 if parent_index.isValid() else 1
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            r = index.row()
            c = index.column()
            return f'{r=}, {c=}'
        else:
            return None
        
    def refill(sef):
