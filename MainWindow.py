from PyQt6.QtWidgets import (QDockWidget,
                             QMainWindow,
                             QMessageBox,
                             QApplication,
                             QFrame,)
                             
from PyQt6.QtCore import pyqtSlot, Qt
from MainMenu import MainMenu
import Teachers, Students, StGroups
from Login import LoginPassword, ChangePassword, check_password
from Login import password_hash
import psycopg2
import settings as st
from datetime import datetime


SELECT_LOGIN = """
                  select id, f_login, f_password_hash,
                         f_enabled, f_expire, f_role,
                         f_salt
                   from appuser
                   where f_login = %s ;
               """

UPDATE_PHASH = """update appuser set f_password_hash = %s
                  where id = %s ;"""


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)
 
        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)
        main_menu.teacher_mode_request.connect(self.teacher_mode_on)
        main_menu.student_mode_request.connect(self.student_mode_on)
        main_menu.stgroup_mode_request.connect(self.stgroup_mode_on)

        if not self.authorize():
            main_menu.lock()
    
    @property
    def all_docks(self):
        return [x for x in self.children() if isinstance(x, QDockWidget)]

    def authorize(self):
        dia = LoginPassword(self)
        if not dia.exec():
            return False
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (dia.login, )
        cursor.execute(SELECT_LOGIN, data)
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return False
        id_user, login, pwd_hash, enabled, expire, role, salt = data
        # print(f'id_user= {id_user}, login= {login}')
        # print(f"password_hash = {pwd_hash}, enabled={enabled}")
        # print(f"expire={expire}, role={role}")
        if not enabled:
            return False
        if expire is not None:
            if expire < datetime.now():
                return False
        if pwd_hash is None:
            if dia.password is not None:
                return False
            dia2 = ChangePassword(parent=self)
            if not dia2.exec():
                return False
            data = (password_hash(dia2.password, salt), id_user)
            conn = psycopg2.connect(**st.db_params)
            cursor = conn.cursor()
            cursor.execute(UPDATE_PHASH, data)
            # строчка для сохранения обновления в базе данных
            conn.commit()
            conn.close()
        else:
            if not check_password(dia.password, pwd_hash, salt):
                return False
        QApplication.instance().set_authorized(login, role)
        return True

    @pyqtSlot()
    def about(self):
        title = 'Управление заданиями для учащихся'
        text = ('Программа для управления задачами\n' + 
                'и заданиями для учащихся школы')
        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, 'Управление заданиями для учащихся')

    @pyqtSlot()
    def teacher_mode_on(self):
        # сначала надо убрать старое окно
        # это как раз и есть то окно которое было раньше
        old = self.centralWidget()
        # теперь новое окно создаем
        v = Teachers.View(parent=self)
        self.setCentralWidget(v)
        # menu Bar выдает ссылку на главное меню
        self.menuBar().set_mode_teacher(v)
        # удаляем старое окно если оно было
        if old is not None:
            # deleteLater удаляет само окно после того
            # когда сигналы все выполнит
            old.deleteLater()

    @pyqtSlot()
    def student_mode_on(self):
        if self.mode_off(Students.View):
            old = self.centralWidget()
            v = Students.View(parent=self)
            self.setCentralWidget(v)
            # создаем припаркованное окно
            dock_title = QApplication.translate('MainWindow', 'Groups')
            dock_widget = QDockWidget(dock_title, parent=self)
            docked_window = QFrame(parent=dock_widget)
            docked_window.setStyleSheet('background: green')
            dock_widget.setWidget(docked_window)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_widget)
            
            self.menuBar().set_mode_student(v, [dock_widget])

    @pyqtSlot()
    def stgroup_mode_on(self):
        if self.mode_off(StGroups.View):
            v = StGroups.View(parent=self)
            self.setCentralWidget(v)
            # создаем припаркованное окно
            dock_title = QApplication.translate('MainWindow', 'Students')
            dock_widget = QDockWidget(dock_title, parent=self)
            
            # docked_window = QFrame(parent=dock_widget)
            docked_window = StGroups.GrpStudent.View(parent=dock_widget)
            
            dock_widget.setWidget(docked_window)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_widget)

            self.menuBar().set_mode_stgroup(v, [dock_widget])
            print('stgroup_mode_on')

    # если  atype указан -> то old имеет тип atype
    def mode_off(self, atype=None):
        old = self.centralWidget()
        if old is None:
            return True
        if atype is not None and isinstance(old, atype):
            return False
        self.setCentralWidget(None)
        old.deleteLater()
        for d in self.all_docks:
            d.deleteLater()
        return True
    
    

    


