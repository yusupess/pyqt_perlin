# Form implementation generated from reading ui file 'TeacherFrame.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TeacherFrame(object):
    def setupUi(self, TeacherFrame):
        TeacherFrame.setObjectName("TeacherFrame")
        TeacherFrame.resize(536, 411)
        self.verticalLayout = QtWidgets.QVBoxLayout(TeacherFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lay_line1 = QtWidgets.QHBoxLayout()
        self.lay_line1.setObjectName("lay_line1")
        self.lay_login = QtWidgets.QVBoxLayout()
        self.lay_login.setSpacing(0)
        self.lay_login.setObjectName("lay_login")
        self.login_lbl = QtWidgets.QLabel(parent=TeacherFrame)
        self.login_lbl.setObjectName("login_lbl")
        self.lay_login.addWidget(self.login_lbl)
        self.login_edt = QtWidgets.QLineEdit(parent=TeacherFrame)
        self.login_edt.setObjectName("login_edt")
        self.lay_login.addWidget(self.login_edt)
        self.lay_line1.addLayout(self.lay_login)
        self.lay_fio = QtWidgets.QVBoxLayout()
        self.lay_fio.setSpacing(0)
        self.lay_fio.setObjectName("lay_fio")
        self.fio_lbl = QtWidgets.QLabel(parent=TeacherFrame)
        self.fio_lbl.setObjectName("fio_lbl")
        self.lay_fio.addWidget(self.fio_lbl)
        self.fio_edt = QtWidgets.QLineEdit(parent=TeacherFrame)
        self.fio_edt.setObjectName("fio_edt")
        self.lay_fio.addWidget(self.fio_edt)
        self.lay_line1.addLayout(self.lay_fio)
        self.lay_line1.setStretch(0, 1)
        self.lay_line1.setStretch(1, 2)
        self.verticalLayout.addLayout(self.lay_line1)
        self.lay_line2 = QtWidgets.QHBoxLayout()
        self.lay_line2.setObjectName("lay_line2")
        self.lay_phone = QtWidgets.QVBoxLayout()
        self.lay_phone.setSpacing(0)
        self.lay_phone.setObjectName("lay_phone")
        self.phone_lbl = QtWidgets.QLabel(parent=TeacherFrame)
        self.phone_lbl.setObjectName("phone_lbl")
        self.lay_phone.addWidget(self.phone_lbl)
        self.phone_edt = QtWidgets.QLineEdit(parent=TeacherFrame)
        self.phone_edt.setObjectName("phone_edt")
        self.lay_phone.addWidget(self.phone_edt)
        self.lay_line2.addLayout(self.lay_phone)
        self.lay_email = QtWidgets.QVBoxLayout()
        self.lay_email.setObjectName("lay_email")
        self.email_lbl = QtWidgets.QLabel(parent=TeacherFrame)
        self.email_lbl.setObjectName("email_lbl")
        self.lay_email.addWidget(self.email_lbl)
        self.email_edt = QtWidgets.QLineEdit(parent=TeacherFrame)
        self.email_edt.setObjectName("email_edt")
        self.lay_email.addWidget(self.email_edt)
        self.lay_line2.addLayout(self.lay_email)
        self.verticalLayout.addLayout(self.lay_line2)
        self.lay_comment = QtWidgets.QVBoxLayout()
        self.lay_comment.setSpacing(0)
        self.lay_comment.setObjectName("lay_comment")
        self.comment_lbl = QtWidgets.QLabel(parent=TeacherFrame)
        self.comment_lbl.setObjectName("comment_lbl")
        self.lay_comment.addWidget(self.comment_lbl)
        self.comment_edt = QtWidgets.QTextEdit(parent=TeacherFrame)
        self.comment_edt.setObjectName("comment_edt")
        self.lay_comment.addWidget(self.comment_edt)
        self.verticalLayout.addLayout(self.lay_comment)

        self.retranslateUi(TeacherFrame)
        QtCore.QMetaObject.connectSlotsByName(TeacherFrame)

    def retranslateUi(self, TeacherFrame):
        _translate = QtCore.QCoreApplication.translate
        TeacherFrame.setWindowTitle(_translate("TeacherFrame", "Frame"))
        self.login_lbl.setText(_translate("TeacherFrame", "Login"))
        self.fio_lbl.setText(_translate("TeacherFrame", "Fullname N. P."))
        self.phone_lbl.setText(_translate("TeacherFrame", "phone"))
        self.email_lbl.setText(_translate("TeacherFrame", "email"))
        self.comment_lbl.setText(_translate("TeacherFrame", "Comment"))
