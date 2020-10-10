import sys
from PyQt5 import QtCore
from PyQt5.QtGui import (QColor)
from PyQt5.QtWidgets import *

# ? ==> SPLASH SCREEN
from ui.ui_splash_screen import Ui_SplashScreen

# ? ==> MAIN WINDOW
from ui.ui_main import Ui_MainWindow

# ? ==> Глобальные переменные
counter = 0


# * Приложение
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MAIN WINDOW LABEL


# ? Экран загруки (SPLASH SCREEN)
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # ? UI ==> INTERFACE CODES
        # ? REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # ? DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # ? QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # ! Настройка таймера на 35 миллисекунд
        self.timer.start(35)

        # / Смена текста
        # / Первый текст
        self.ui.label_description.setText("<strong>Добро пожаловать</strong> в салон красоты")

        # / Текст который придет на смену первому
        QtCore.QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>Загрузка</strong> Базы данных"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>Загрузка</strong> Интерфейса"))

        # ? SHOW ==> MAIN WINDOW
        self.show()
        # ? ==> END ##

    # ? ==> APP FUNCTIONS
    def progress(self):
        global counter

        # * SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # / Закрыть окно с загрузкой и открыть главное окно
        if counter > 100:
            # ? STOP TIMER
            self.timer.stop()

            # ? Показать MainWindow
            self.main = MainWindow()
            self.main.show()

            # ! Закрыть окно загрузки
            self.close()

        # * Увеличить процент
        counter += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
