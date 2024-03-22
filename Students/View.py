from PyQt6.QtWidgets import QTableView, QMessageBox, QAbstractItemView, QHeaderView
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2

from .Model import Model
from .Dialog import Dialog
import db

SELECT_ONE = """select f_fio, f_email, f_comment
                from student
                where id = %s ;
            """



class View(QTableView):

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
        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
    
    @property
    def pk(self):
        row = self.currentIndex().row()
        return self.model().record(row).value(0)

    @pyqtSlot()
    def add(self):
        # QMessageBox.information(self, 'Учитель', 'Добавление')
        dia = Dialog(parent=self)
        if dia.exec():
            data = db.Student()
            dia.get(data)
            data.insert()  # Эту функцию надо вызывать чуть иначе
            self.model().obnovit()


    @pyqtSlot()
    def update(self):
        # dia = Dialog(parent=self)
        # row = self.currentIndex().row()
        # id_student = self.model().record(row).value(0)
        # # подключаемся к базе данных
        # conn = psycopg2.connect(**st.db_params)
        # # создаем курсор
        # cursor = conn.cursor()
        # data = (id_student,)
        # cursor.execute(SELECT_ONE, data)
        # # считываем строку из базы даных и записываем в строки диалогового окна
        # dia.fio, dia.email, dia.comment = cursor.fetchone()
        # # после счиьываения обязательно закываем подключение к базе
        # conn.close()
        # if dia.exec():
        #     self.model().update(id_student, dia.fio,
        #                         dia.email, dia.comment
        #                         )
        dia = Dialog(parent=self)
        data = db.Student(pk = self.pk).load()
        dia.put(data)
        if dia.exec():
            dia.get(data)
            print(data)


    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_student = self.model().record(row).value(0)
        # при удалении выходит окно для подтверждения
        ans = QMessageBox.question(self, 'Ученик', 'ВЫ уверены?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().delete(id_student)
