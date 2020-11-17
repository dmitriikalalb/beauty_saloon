from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, QVBoxLayout
from ui.ui_card import ElementCard


class SquareLabel(QLabel):
    def __init__(self, parent=None):
        super(SquareLabel, self).__init__(parent)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(223, 230, 248))
        self.setPalette(p)
        self.setMouseTracking(True)

        self.setFixedSize(300, 300)
        self.setScaledContents(True)

    def mouseMoveEvent(self, event):
        print("On Hover", event.pos().x(), event.pos().y())

    def mousePressEvent(self, event):
        print(event)


class SuperEdit(QWidget):
    def __init__(self, data, parent=None):
        super(SuperEdit, self).__init__(parent)
        counter = 0
        row = 0
        layout = QGridLayout()
        layout.setContentsMargins(2, 2, 2, 2)

        for name in range(0, 15):
            card = QVBoxLayout()

            # label = SquareLabel(self)
            # label.setText(name)

            if counter >= 4:
                counter = 0
                row = 1

            card.addWidget(ElementCard())
            layout.addLayout(card, row, counter)
            counter += 1
        self.setLayout(layout)
