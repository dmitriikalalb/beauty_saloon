from PyQt5.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PyQt5.QtGui import (QFont, QIcon)
from PyQt5.QtWidgets import *
from utils import config


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamily(u"Roboto Thin")
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.table = QTableView(self.centralwidget)
        self.table.setObjectName(u"table")
        self.table.resize(640, 480)

        self.verticalLayout.addWidget(self.label)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        MainWindow.setWindowIcon(QIcon('../resources/beauty_logo.ico'))
        # ! self.label.setText(QCoreApplication.translate("MainWindow", u"<strong>Салон красоты</strong>", None))
        if config.create_connection():
            query = 'SELECT * FROM Manufacturer'
            self.table.setModel(config.display_data(query))
