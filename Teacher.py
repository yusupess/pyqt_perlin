from PyQt6.QtWidgets import QTableView, QMessageBox, QDialog
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtSql import QSqlQueryModel
from PyQt6.QtCore import pyqtSlot


class Model(QSqlQueryModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        sql = """select id, f_fio, f_phone, f_email,
                 f_comment from teacher;"""
        self.setQuery(sql)


class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)
    
    @pyqtSlot()
    def add(self):
        # QMessageBox.information(self, 'Учитель', 'Добавление')
        dia = Dialog(parent=self)
        dia.exec()

    @pyqtSlot()
    def update(self):
        QMessageBox.information(self, 'Учитель', 'Редактирование')

    @pyqtSlot()
    def delete(self):
        QMessageBox.information(self, 'Учитель', 'Удаление')


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        fio_lbl = QLabel('Фамилия И. О.', parent=self)
        self.__fio_edt = QLineEdit(parent=self)

        phone_lbl = QLabel('Телефон', parent=self)
        self.__phone_edt = QLineEdit(parent=self)

        email_lbl = QLabel('e-mail', parent=self)
        self.__email_edt = QLineEdit(parent=self)

        comment_lbl = QLabel('Примечание', parent=self)
        self.__comment_edt = QTextEdit(parent=self)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)
        lay.addWidget(fio_lbl)
        lay.addWidget(self.__fio_edt)
        lay.addWidget(phone_lbl)
        lay.addWidget(self.__phone_edt)
        lay.addWidget(email_lbl)
        lay.addWidget(self.__email_edt)
        lay.addWidget(comment_lbl)
        lay.addWidget(self.__comment_edt)
        
        # горизонтальный слой для кнопок "ОК" и "Отмена"
        lay2 = QHBoxLayout()
        lay2.addWidget(ok_btn)
        lay2.addWidget(cancel_btn)
        # добавляем горизонтальный слой кнопок(ОК и Отмена) в общий вертикальный слой
        lay.addLayout(lay2)
        #  подключаем кнопку "Отмена"
        cancel_btn.clicked.connect(self.reject)












