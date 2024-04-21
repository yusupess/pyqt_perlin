import sys
from Application import Application
from MainWindow import MainWindow

import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

app = Application(sys.argv) # создаем обьект приложения


main_window = MainWindow()  # создаем главное окно
main_window.showMaximized()  

result = app.exec()   # запускает приложение
sys.exit(result)

