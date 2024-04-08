from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog, QAbstractItemView, QHeaderView
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import QModelIndex, pyqtSlot, Qt, pyqtSignal
from .Model import Model
from .Dialog import Dialog
import settings as st
import psycopg2



SELECT_ONE = """select f_title, f_comment
                from stgroup
                where id = %s ;
            """


class View(QTableView):
    
    group_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        model = Model(parent=self)
        self.setModel(model)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.hideColumn(0)
        self.setWordWrap(False)
        vh = self.verticalHeader()
        vh.setSectionResizeMode(QHeaderView.ResizeMode.Fixed) 
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

    @pyqtSlot()
    def add(self):
        # QMessageBox.information(self, 'Учитель', 'Добавление')
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.title, dia.comment)

    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        row = self.currentIndex().row()
        id_stgroup = self.model().record(row).value(0)
        # подключаемся к базе данных
        conn = psycopg2.connect(**st.db_params)
        # создаем курсор
        cursor = conn.cursor()
        data = (id_stgroup,)
        cursor.execute(SELECT_ONE, data)
        # считываем строку из базы даных и записываем в строки диалогового окна
        dia.title, dia.comment = cursor.fetchone()
        # после счиьываения обязательно закываем подключение к базе
        conn.close()
        if dia.exec():
            self.model().update(id_stgroup, dia.title,
                                dia.comment
                                )

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_stgroup = self.model().record(row).value(0)
        # при удалении выходит окно для подтверждения
        ans = QMessageBox.question(self, 'Группа', 'ВЫ уверены?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().delete(id_stgroup)

    def currentChanged(self, curr, prev):
        # return super().currentChanged(curr, prev)()
        if curr.isValid():
            id_group = curr.data(Qt.ItemDataRole.UserRole+0 )
        else:
            id_group = None
        self.group_selected.emit(id_group)
        print(id_group)

