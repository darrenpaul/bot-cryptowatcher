import os
import re
import sys
import glob
from pprint import pprint
try:
    from PySide2.QtWidgets import *
    from PySide2.QtCore import *
    from PySide2.QtGui import *
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *

# ROOTDIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(ROOTDIR.replace("{sep}environment".format(sep=os.sep), ""))
# from utils import utils, client_manager, temp_manager
# import environment


class Launcher(QMainWindow):
    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent)
        self.__build_ui()
        self.__style_interface()

    def __build_ui(self):
        self.__build_windows()
        # self.__build_widgets()

    def __build_windows(self):
        self.setWindowTitle("Launcher")
        self.setFixedSize(300, 600)

    def __build_widgets(self):
        self.widgets = Widgets()
        self.setCentralWidget(self.widgets)

    def __style_interface(self):
        QApplication.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet("background-color:#263238; color:#ececec;")


class Widgets(QWidget):
    def __init__(self):
        super(Widgets, self).__init__()

        self.__load_temp()

        self.grid = QGridLayout()

        self.__build_client()

    def __build_client(self):
        if hasattr(self, "clientGroup"):
            self.clientGroup.setParent(None)

        self.clientGroup = QGroupBox("")
        self.clientGroup.setStyleSheet("QGroupBox{border: 0px;};")

        self.clientCb = QComboBox(self)
        self.clientCb.addItems(client_manager.get_clients())
        self.projectCb = QComboBox(self)
        self.projectCb.addItems(client_manager.get_projects(self.__get_client()))

        grid = QGridLayout()
        grid.addWidget(QLabel("Client"), 1, 0)
        grid.addWidget(QLabel("Project"), 1, 1)
        grid.addWidget(self.clientCb, 2, 0)
        grid.addWidget(self.projectCb, 2, 1)

        self.clientGroup.setLayout(grid)

        self.clientCb.currentIndexChanged.connect(self.__update_project)

        self.grid.addWidget(self.clientGroup, 1, 0)
        self.setLayout(self.grid)

        if "client" in self.tempSettings:
            index = self.clientCb.findText(self.tempSettings["client"], Qt.MatchFixedString)
            if index >= 0:
                self.clientCb.setCurrentIndex(index)

        if "project" in self.tempSettings:
            index = self.projectCb.findText(self.tempSettings["project"], Qt.MatchFixedString)
            if index >= 0:
                self.projectCb.setCurrentIndex(index)



def main():
    app = QApplication([])
    foo = Launcher()
    foo.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

