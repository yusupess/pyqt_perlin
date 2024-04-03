"""Зджесь мы создаем строку меню в нашем окне."""

from PyQt6.QtWidgets import QMenuBar, QMenu, QApplication, QDockWidget
from PyQt6.QtCore import pyqtSlot, pyqtSignal
from PyQt6.QtGui import QActionGroup


class ViewMenu(QMenu):

    def __init__(self, parent=None):
        title = QApplication.translate('MainMenu.ViewMenu', 'View')
        super().__init__(title, parent)

        title = QApplication.translate('MainMenu.ViewMenu', 'Windows')
        self.__windows_menu = self.addMenu(title)

        title = QApplication.translate('MainMenu.ViewMenu', 'Tool bars')
        self.__toolbars_menu = self.addMenu(title)

    def add_window(self, wid: QDockWidget):
        self.__windows_menu.addAction(wid.toggleViewAction())


class MainMenu(QMenuBar):
    
    # сигнал для передачи главному окну о включении режима учителей
    teacher_mode_request = pyqtSignal()
    student_mode_request = pyqtSignal()
    stgroup_mode_request = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        teacher_menu = self.addMenu('Учитель')
        self.__teacher_menu_action = teacher_menu.menuAction()
        self.__teacher_add = teacher_menu.addAction('Добавить')
        self.__teacher_edit = teacher_menu.addAction('Редактировать')
        self.__teacher_delete = teacher_menu.addAction('Удалить')

        student_menu = self.addMenu('Студент')
        self.__student_menu_action = student_menu.menuAction()
        self.__student_add = student_menu.addAction('Добавить')
        self.__student_edit = student_menu.addAction('Редактировать')
        self.__student_delete = student_menu.addAction('Удалить')

        stgroup_menu = self.addMenu('Группа')
        self.__stgroup_menu_action = stgroup_menu.menuAction()
        self.__stgroup_add = stgroup_menu.addAction('Добавить')
        self.__stgroup_edit = stgroup_menu.addAction('Редактировать')
        self.__stgroup_delete = stgroup_menu.addAction('Удалить')

        mode_menu = self.addMenu('Режимы')
        mode_action_group = ag = QActionGroup(self)
        self.__mode_menu_action = mode_menu.menuAction()
        self.__teacher_mode_action = act = mode_menu.addAction('Учителя')
        act.setCheckable(True)
        # для того чтобы сделать режим переключение, 
        # т.е при выборе другого подменю галочка на этом пропадет
        ag.addAction(act)
        act.toggled.connect(self.toggle_teacher_mode)
        # для того чтобы кнопка учитель не отображадась при старте приложения

        self.__student_mode_action = act = mode_menu.addAction('Студенты')
        act.setCheckable(True)
        ag.addAction(act)
        # для того чтобы кнопка ученик не отображадась при старте приложения
        act.toggled.connect(self.toggle_student_mode)
        self.__stgroup_mode_action = act = mode_menu.addAction('Группы')
        act.setCheckable(True)
        ag.addAction(act)
        # для того чтобы кнопка группы не отображадась при старте приложения
        act.toggled.connect(self.toggle_stgroup_mode)
        
        self.__view_menu = vm = ViewMenu(parent=self)
        self.addMenu(vm)
        
        help_menu = self.addMenu('Справка')
        self.__about = help_menu.addAction('О программе...')
        self.__about_qt = help_menu.addAction('О библиотеке Qt...')

        self.toggle_teacher_mode(False)
        self.toggle_student_mode(False)
        self.toggle_stgroup_mode(False)

    # функция для блокировки меню в случае непраильного логина\пароля
    def lock(self):
        self.__mode_menu_action.setEnabled(False)
    
    @pyqtSlot(bool)
    def toggle_teacher_mode(self, enable):
        if not enable:
            # просто прятать пункты меню неправильно.
            # надо обязательно отключить
            self.__teacher_add.setEnabled(False)
            self.__teacher_edit.setEnabled(False)
            self.__teacher_delete.setEnabled(False)
            self.__teacher_menu_action.setEnabled(False)
            self.__teacher_menu_action.setVisible(False)
        else:
            # создаем сигнал при включении режима учителя
            self.teacher_mode_request.emit()

    @pyqtSlot(bool)
    def toggle_student_mode(self, enable):
        if not enable:
            self.__student_add.setEnabled(False)
            self.__student_edit.setEnabled(False)
            self.__student_delete.setEnabled(False)
            self.__student_menu_action.setEnabled(False)
            self.__student_menu_action.setVisible(False)
        else:
            # создаем сигнал при включении режима учителя
            self.student_mode_request.emit()
    
    @pyqtSlot(bool)
    def toggle_stgroup_mode(self, enable):
        if not enable:
            self.__stgroup_add.setEnabled(False)
            self.__stgroup_edit.setEnabled(False)
            self.__stgroup_delete.setEnabled(False)
            self.__stgroup_menu_action.setEnabled(False)
            self.__stgroup_menu_action.setVisible(False)

        else:
            # создаем сигнал при включении режима учителя
            self.stgroup_mode_request.emit()
    
    @property
    def about(self):
        return self.__about
    
    @property
    def about_qt(self):
        return self.__about_qt
    
    # dock_widgets это список из открытых припаркованных окон
    def set_mode_stgroup(self, widget, dock_widgets=[]):
        self.__stgroup_add.triggered.connect(widget.add)
        self.__stgroup_delete.triggered.connect(widget.delete)
        self.__stgroup_edit.triggered.connect(widget.update)
        
        self.__stgroup_add.setEnabled(True)
        self.__stgroup_edit.setEnabled(True)
        self.__stgroup_delete.setEnabled(True)
        self.__stgroup_menu_action.setEnabled(True)
        self.__stgroup_menu_action.setVisible(True)
        for wid in dock_widgets:
            self.__view_menu.add_window(wid)

    def set_mode_student(self, widget, dock_widgets=[]):
        self.__student_add.triggered.connect(widget.add)
        self.__student_delete.triggered.connect(widget.delete)
        self.__student_edit.triggered.connect(widget.update)

        self.__student_add.setEnabled(True)
        self.__student_edit.setEnabled(True)
        self.__student_delete.setEnabled(True)
        self.__student_menu_action.setEnabled(True)
        self.__student_menu_action.setVisible(True)
        for wid in dock_widgets:
            self.__view_menu.add_window(wid)

    def set_mode_teacher(self, widget):
        self.__teacher_add.triggered.connect(widget.add)
        self.__teacher_delete.triggered.connect(widget.delete)
        self.__teacher_edit.triggered.connect(widget.update)

        self.__teacher_add.setEnabled(True)
        self.__teacher_edit.setEnabled(True)
        self.__teacher_delete.setEnabled(True)
        self.__teacher_menu_action.setEnabled(True)
        self.__teacher_menu_action.setVisible(True)

