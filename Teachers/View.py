from PyQt6.QtWidgets import QTableView, QMessageBox, QAbstractItemView, QHeaderView
from PyQt6.QtCore import pyqtSlot
import settings as st
import psycopg2

from .Model import Model
from .Dialog import Dialog


SELECT_ONE = """select f_fio, f_phone, f_email, f_comment
                from teacher
                where id = %s ;
            """


class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)
        
        # чтобы выбирать всю строку, а не одну ячейку
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # чтобы убатть возможность выбора нескольких строк
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # чтобы скрыть колонку id
        self.hideColumn(0)
        # запретить перенос по пробелу хотя у меня итак не переносилось
        self.setWordWrap(False)
        # чтобы нельзя было изменять высоту строк
        vh = self.verticalHeader()
        vh.setSectionResizeMode(QHeaderView.ResizeMode.Fixed) 
        # чтобы длина солбцов подбиралась под содержимое ячеек
        hh = self.horizontalHeader()
        hh.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # чтобы таблица растянулась по горизонтали за счет четвертой колонки
        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

    @pyqtSlot()
    def add(self):
        # QMessageBox.information(self, 'Учитель', 'Добавление')
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.fio, dia.phone, dia.email, dia.comment)

    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        row = self.currentIndex().row()
        id_teacher = self.model().record(row).value(0)
        # подключаемся к базе данных
        conn = psycopg2.connect(**st.db_params)
        # создаем курсор
        cursor = conn.cursor()
        data = (id_teacher,)
        cursor.execute(SELECT_ONE, data)
        # считываем строку из базы даных и записываем в строки диалогового окна
        dia.fio, dia.phone, dia.email, dia.comment = cursor.fetchone()
        # после счиьываения обязательно закываем подключение к базе
        conn.close()
        if dia.exec():
            self.model().update(id_teacher, dia.fio,
                                dia.phone, dia.email,
                                dia.comment
                                )

    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_teacher = self.model().record(row).value(0)
        # при удалении выходит окно для подтверждения
        ans = QMessageBox.question(self, 'Учитель', 'ВЫ уверены?')
        if ans == QMessageBox.StandardButton.Yes:
            self.model().delete(id_teacher)

