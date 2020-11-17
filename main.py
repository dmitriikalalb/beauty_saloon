import sys
from PyQt5.QtWidgets import QApplication

from ui.ui_main import SuperEdit

if __name__ == '__main__':
    names = ['Name 1', 'Name 2', 'Name 3', 'Name 4', 'Name 1', 'Name 2', 'Name 3']
    app = QApplication([])
    editor = SuperEdit(names)
    editor.show()
    app.exec_()