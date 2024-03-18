from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSlot


SELECT_ONE = """select f_fio, f_phone, f_email, f_comment
                from teacher
                where id = %s ;
            """


class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Учитель')

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
        lay.setSpacing(15)

        lay_fam = QVBoxLayout()
        # наводим красоту. устанавливаем расстояние м\у элементами
        lay_fam.setSpacing(0)
        lay_fam.addWidget(fio_lbl)
        lay_fam.addWidget(self.__fio_edt)
        lay.addLayout(lay_fam)

        lay3 = QHBoxLayout()
        
        lay_phn = QVBoxLayout()
        lay_phn.setSpacing(0)
        lay_phn.addWidget(phone_lbl)
        lay_phn.addWidget(self.__phone_edt)
        lay3.addLayout(lay_phn)
        
        lay_em = QVBoxLayout()
        lay_em.setSpacing(0)
        lay_em.addWidget(email_lbl)
        lay_em.addWidget(self.__email_edt)
        lay3.addLayout(lay_em)
        
        lay.addLayout(lay3)

        lay_com = QVBoxLayout()
        lay_com.setSpacing(0)
        lay_com.addWidget(comment_lbl)
        lay_com.addWidget(self.__comment_edt)
        lay.addLayout(lay_com)
        
        # горизонтальный слой для кнопок "ОК" и "Отмена"
        lay2 = QHBoxLayout()
        # доавляем пустое пространство чтобы кнопки ок и Отмена были в правом углу
        lay2.addStretch()
        lay2.addWidget(ok_btn)
        lay2.addWidget(cancel_btn)
        # добавляем горизонтальный слой кнопок(ОК и Отмена) в общий вертикальный слой
        lay.addLayout(lay2)
        #  подключаем кнопку "Отмена"
        cancel_btn.clicked.connect(self.reject)
        #  подключаем кнопку "Ок"
        ok_btn.clicked.connect(self.finish)
    
    #слот это в-ция которая реагирует на какоето событие
    @pyqtSlot()
    def finish(self):
        if self.fio is None:
            return
        self.accept()       


    @property
    def fio(self):
        result = self.__fio_edt.text().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
    
    @fio.setter
    def fio(self, value):
        self.__fio_edt.setText(value)
    
    @property
    def phone(self):
        result = self.__phone_edt.text().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
        
    @phone.setter
    def phone(self, value):
        self.__phone_edt.setText(value)
    
    @property
    def comment(self):
        # toPlainText() выполняет ту же функцию что и text()
        result = self.__comment_edt.toPlainText().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
    
    @comment.setter
    def comment(self, value):
        self.__comment_edt.setPlainText(value)

    @property
    def email(self):
        result = self.__email_edt.text().strip()
        if result:
            return result
        
    @email.setter
    def email(self, value):
        self.__email_edt.setText(value)
