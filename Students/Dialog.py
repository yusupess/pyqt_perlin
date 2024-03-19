from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSlot

from .Ui_StudentFrame import Ui_StudentFrame

class _Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_StudentFrame()
        self.ui.setupUi(self)

class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Ученик')

        self.__frame = _Frame(parent=self)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)
        lay.setSpacing(15)

        lay.addWidget(self.__frame)


        
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
        result = self.__frame.ui.fio_edt.text().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
    
    @fio.setter
    def fio(self, value):
        self.__frame.ui.fio_edt.setText(value)
    
    @property
    def comment(self):
        # toPlainText() выполняет ту же функцию что и text()
        result = self.__frame.ui.comment_edt.toPlainText().strip()
        # if not result:
        #     return None
        # return result
        if result:
            return result
    
    @comment.setter
    def comment(self, value):
        self.__frame.ui.comment_edt.setPlainText(value)

    @property
    def email(self):
        result = self.__frame.ui.email_edt.text().strip()
        if result:
            return result
        
    @email.setter
    def email(self, value):
        self.__frame.ui.email_edt.setText(value)

    @property
    def login(self):
        result = self.__frame.ui.login_edt.text().strip()
        if result:
            return result
        
    @login.setter
    def login(self, value):
        self.__frame.ui.login_edt.setText(value)
        