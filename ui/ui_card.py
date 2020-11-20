from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QPainter, QPen
from PyQt5 import QtCore
from ui.ui_add_edit import AddEditWindow
from utils import helpers


class ElementCard(QWidget):
    def __init__(self, title, cost, is_active, images):
        super().__init__()
        self.addEditWindow = AddEditWindow()
        self.imagenumber = 0
        self.title = title
        self.cost = cost
        self.is_active_d = is_active
        self.imagelist = images
        self.initUI()
        self.label.setMouseTracking(True)
        self.frame_color = QtCore.Qt.darkGray
        self.setMinimumHeight(400)
        self.setMaximumSize(250, 400)

    def initUI(self):

        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignHCenter)

        self.rb_group = QButtonGroup()
        self.radio0 = QRadioButton()
        self.radio1 = QRadioButton()
        self.radio2 = QRadioButton()
        self.radio3 = QRadioButton()

        self.radio0.setChecked(True)

        self.rb_group.addButton(self.radio0)
        self.rb_group.addButton(self.radio1)
        self.rb_group.addButton(self.radio2)
        self.rb_group.addButton(self.radio3)

        self.rb_group.setId(self.radio0, 0)
        self.rb_group.setId(self.radio1, 1)
        self.rb_group.setId(self.radio2, 2)
        self.rb_group.setId(self.radio3, 3)

        hbox.addWidget(self.radio0)
        hbox.addWidget(self.radio1)
        hbox.addWidget(self.radio2)
        hbox.addWidget(self.radio3)

        self.rb_group.buttonClicked.connect(self.rbPressEvent)

        self.name = QLabel(self.title)
        # * Обрезаем текст если он слишком длинный чтобы разметка карточки не ломалась
        txt = ''
        for text in self.title.split()[:4]:
            txt = txt + text
        if len(txt) >= 25:
            self.name.setText(self.title[:25] + '...')
            self.name.setToolTip(self.title)
        self.price = QLabel(str(int(self.cost)) + ' руб.')
        self.is_active = QLabel('Неактивен' if not self.is_active_d else '')

        self.name.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setWordWrap(True)
        self.price.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setWordWrap(True)
        self.is_active.setAlignment(QtCore.Qt.AlignHCenter)
        self.name.setWordWrap(True)

        self.name.setFont(QFont('Tahoma', 13, QFont.Normal))
        self.price.setFont(QFont('Tahoma', 15, QFont.Normal))

        self.setLayout(layout)
        self.label = QLabel()
        self.label.setMouseTracking(True)
        layout.addWidget(self.label)
        layout.addLayout(hbox)
        layout.addWidget(self.name)
        layout.addWidget(self.price)
        layout.addWidget(self.is_active)

        self.resize(200, 300)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showimage(0)

    def showimage(self, imagenumber):
        directory = "images/"
        pixmap = QPixmap(directory + self.imagelist[imagenumber])
        print(self.imagelist)

        self.label.setPixmap(pixmap)
        self.label.setFixedHeight(220)
        self.label.setScaledContents(True)

    def mouseMoveEvent(self, event):
        pos_x = event.pos().x()
        width = self.label.width()
        if pos_x <= width/4:
            self.radio0.setChecked(True)
        elif width/4 <= pos_x <= width/2:
            self.radio1.setChecked(True)
        elif width/2 <= pos_x <= width/1.3:
            self.radio2.setChecked(True)
        else:
            self.radio3.setChecked(True)
        try:
            self.showimage(self.rb_group.checkedId())
        except:
            print("Одна кратинка")

    def rbPressEvent(self):
        self.showimage(self.rb_group.checkedId())

    # ? Цвет рамки заднего фона карточки

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.is_active_d:
            painter.setBrush(QtCore.Qt.white)
        else:
            painter.setBrush(QtCore.Qt.gray)
        painter.setPen(QPen(self.frame_color, 5))

        painter.drawRect(self.rect())

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        edit_action = contextMenu.addAction('Редактировать')
        delete_action = contextMenu.addAction('Удалить')
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == delete_action:
            helpers.show_popup('Title', 'Message', self.popup_button)
        elif action == edit_action:
            # self.addEditWindow.input1.setText(self.name.text())
            # self.addEditWindow.input2.setText(self.price.text())
            self.addEditWindow.displayInfo()

    # ? Функция которая принимает ответ с диалогового окна
    def popup_button(self, i):
        msg = i.text()
        if msg == '&Yes':
            self.close()

    def mousePressEvent(self, event):
        if self.frame_color == QtCore.Qt.darkGray:
            self.frame_color = QtCore.Qt.blue
        elif self.frame_color == QtCore.Qt.blue:
            self.frame_color = QtCore.Qt.darkGray
