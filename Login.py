"""Здесь описано окно для ввода логина и пароля."""
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSlot
import settings as st
from hashlib import sha1


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

def check_password(password, password_hash, salt):
    check = st.global_salt + password + salt
    psw_hash = sha1(check).hexdigest()
    return psw_hash == password_hash
    

class ChangePassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        lay = QVBoxLayout(self)

        lay_first = QVBoxLayout()
        lay_first.setSpacing(0)
        lay_first.addWidget(QLabel('Введите новый пароль', parent=self))
        self.__new_pass1 = QLineEdit(parent=self)
        self.__new_pass1.setEchoMode(QLineEdit.EchoMode.Password)
        lay_first.addWidget(self.__new_pass1)
        lay.addLayout(lay_first)

        lay_second = QVBoxLayout()
        lay_second.setSpacing(0)
        lay_second.addWidget(QLabel('Повторите новый пароль', parent=self))
        self.__new_pass2 = QLineEdit(parent=self)
        self.__new_pass2.setEchoMode(QLineEdit.EchoMode.Password)
        lay_second.addWidget(self.__new_pass2)
        lay.addLayout(lay_second)
        
        lay_ok_button = QHBoxLayout()
        lay_ok_button.addStretch()
        ok = QPushButton('OK', parent=self)
        lay_ok_button.addWidget(ok)
        lay.addLayout(lay_ok_button)

        ok.clicked.connect(self.pass_validate)
    
    @property
    def pswd_frst(self):
        return self.__new_pass1
    
    @property
    def pswd_scnd(self):
        return self.__new_pass2

    @pyqtSlot()
    def pass_validate(self):
        if self.__new_pass1.text().strip() and self.__new_pass1.text().strip() == self.__new_pass2.text().strip():
            self.accept()
            print("accept")
        else:
            self.reject()
            print('reject')
    




