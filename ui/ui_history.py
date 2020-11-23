from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from utils import config, styleSheet


class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel('История товара отсутствует')
        self.vBoxLayout = QVBoxLayout()
        self.productsale = QComboBox()
        self.query = ''

        self.tableWidget = QTableWidget()
        self.setStyleSheet(f'QComboBox{{{styleSheet.TEXT_EDIT}\nfont: 13pt Tahoma;}}')
        self.setWindowIcon(QtGui.QIcon('images/beauty_logo.ico'))
        self.setWindowTitle('История продаж')
        self.resize(1100, 500)

        self.initUi()

    def initUi(self):
        products = config.execute_query('SELECT Title FROM Product')
        for product in products:
            self.productsale.addItem(product[0])
        self.productsale.currentTextChanged.connect(self.change_product)
        self.vBoxLayout.addWidget(self.productsale)
        self.setLayout(self.vBoxLayout)

    def creatingTables(self, query):
        result = config.execute_query(query)
        if not result:
            self.label.setFont(QFont('Tahoma', 20, QFont.Bold))
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.vBoxLayout.addWidget(self.label)
            return False
        
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem('ID'))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem('Дата продажи'))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem('Товар'))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem('Количество'))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem('Клиент'))

        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 170)
        self.tableWidget.setColumnWidth(2, 400)
        # ? Сортировка даты по убыванию
        self.tableWidget.sortItems(1, QtCore.Qt.DescendingOrder)

        self.vBoxLayout.addWidget(self.tableWidget)

    def show_history(self):
        self.show()

    def change_product(self):
        query = f"SELECT * FROM ProductSale WHERE ProductID = '{self.productsale.currentText()}'"
        self.setWindowTitle(f'История товара "{self.productsale.currentText()}"')
        result = config.execute_query(query)
        if result:
            self.label.setVisible(False)
            self.tableWidget.setVisible(True)
            self.creatingTables(query)
        else:
            self.label.setVisible(True)
            self.label.setFont(QFont('Tahoma', 20, QFont.Bold))
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.vBoxLayout.addWidget(self.label)
            self.tableWidget.setVisible(False)
