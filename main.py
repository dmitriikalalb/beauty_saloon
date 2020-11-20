import sys
from PyQt5.QtWidgets import QApplication

from ui.ui_main import TovarWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TovarWindow()
    editor.show()
    app.exec_()
