"""Здесь описано окно для ввода логина и пароля."""
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout


class LoginPassword(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QVBoxLayout(self)

        lay_login = QVBoxLayout()
        lay_login.setSpacing(0)
        login_tit = QLabel('Логин', parent=self)
        self.__login_edt = QLineEdit(parent=self)
        lay_login.addWidget(login_tit)
        lay_login.addWidget(self.__login_edt)
        lay.addLayout(lay_login)

        lay_pwd = QVBoxLayout()
        lay_pwd.setSpacing(0)
        password_tit = QLabel('Пароль', parent=self)
        self.__password_edt = QLineEdit(parent=self)
        # для то го чтобы пароль при вводе отображался звездочками
        # PyQt5:  self.__password_edt.setEchoMode(QLineEdit.Password)
        self.__password_edt.setEchoMode(QLineEdit.EchoMode.Password)
        lay_pwd.addWidget(password_tit)
        lay_pwd.addWidget(self.__password_edt)
        lay.addLayout(lay_pwd)

        lay_btn = QHBoxLayout()
        lay_btn.addStretch()
        ok = QPushButton('OK', parent=self)
        cancel = QPushButton('Отмена', parent=self)
        lay_btn.addWidget(ok)
        lay_btn.addWidget(cancel)
        
        lay.addLayout(lay_btn)

        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

    @property
    def login(self):
        return self.__login_edt.text().strip()

    @property
    def password(self):
        return self.__password_edt.text().strip()   





