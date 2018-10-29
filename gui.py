import os
import re
import time
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

from modules.binance import binance

# ROOTDIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(ROOTDIR.replace("{sep}environment".format(sep=os.sep), ""))
# from utils import utils, client_manager, temp_manager
# import environment


class Launcher(QMainWindow):
    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent)

        self.__build_ui()
        self.__style_interface()
        self.__build_widgets()

        timer = QTimer(self)
        timer.timeout.connect(self.updatePrices)
        timer.start(10000)
        self.updatePrices()


    def __build_ui(self):
        self.__build_windows()
        # self.__build_widgets()

    def __build_windows(self):
        self.setWindowTitle("Launcher")
        self.setFixedSize(600, 600)

    def __build_widgets(self):
        self.widgets = Widgets()
        self.setCentralWidget(self.widgets)

    def __style_interface(self):
        QApplication.setStyle(QStyleFactory.create('plastique'))
        self.setStyleSheet("background-color:#263238; color:#ececec;")

    def updatePrices(self):
        self.widgets.update_watchers()


class Widgets(QWidget):
    def __init__(self):
        super(Widgets, self).__init__()

        self.watchers = []

        self.prices = binance.get_price()

        self.grid = QGridLayout()

        self.__new_currency()

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

    def __new_currency(self):
        self.newCurrencyGroup = QGroupBox("")
        self.newCurrencyGroup.setStyleSheet("QGroupBox{border: 0px;};")
        self.pairs = QComboBox(self)
        self.pairs.addItems(_sort_pairs(binance.get_trading_pairs()))
        self.addCurrencyButton = QPushButton("Add")
        self.addCurrencyButton.clicked.connect(self.__add_new_currency_connect)

        grid = QGridLayout()
        grid.addWidget(QLabel("Add new"), 1, 0)
        grid.addWidget(self.pairs, 1, 1)
        grid.addWidget(self.addCurrencyButton, 1, 2)
        self.newCurrencyGroup.setLayout(grid)
        self.grid.addWidget(self.newCurrencyGroup, 1, 0)
        self.setLayout(self.grid)

    def __add_new_currency_connect(self):
        self.__add_watcher(pair=self.pairs.currentText())

    def __add_watcher(self, pair):
        watcherGroup = QGroupBox("")
        watcherGroup.setStyleSheet("QGroupBox{border: 0px;};")

        lpair = QLabel(pair)
        curPrice = QLabel(self.__get_pair_price(pair=pair))
        watchPrice = QLineEdit("0.0000")

        rgroup = QGroupBox("")
        rgroup.setStyleSheet("QGroupBox{border: 0px;};")

        rlayout = QHBoxLayout()
        rless = QRadioButton("-")
        requal = QRadioButton("=")
        rgreat = QRadioButton("+")

        requal.setChecked(True)
        rlayout.addWidget(rless)
        rlayout.addWidget(requal)
        rlayout.addWidget(rgreat)
        rgroup.setLayout(rlayout)

        grid = QGridLayout()
        grid.addWidget(lpair, 2, 0)
        grid.addWidget(curPrice, 2, 1)
        grid.addWidget(watchPrice, 2, 2)
        grid.addWidget(rgroup, 2, 3)

        watcherGroup.setLayout(grid)

        self.watchers.append({
            "group": watcherGroup, 
            "pair": lpair, 
            "uprice": watchPrice, 
            "cprice": curPrice,
            "radios": {"less": rless, "equal": requal, "great": rgreat}
            })

        self.grid.addWidget(watcherGroup, self.grid.rowCount(), 0)
        self.setLayout(self.grid)

    def __get_pair_price(self, pair):
        for i in self.prices:
            __pair = pair.replace("-", "")
            if __pair == i.get("pair"):
                return i.get("last")
    
    def update_watchers(self):
        print "updating"
        self.prices = binance.get_price()
        for i in self.watchers:
            _pair = i.get("pair").text()
            i.get("cprice").setText(self.__get_pair_price(_pair.replace("-", "")))
            cprice = float(i.get("cprice").text())
            uprice = float(i.get("uprice").text())
            if i.get("radios").get("less").isChecked():
                if cprice < uprice:
                    print "less"
            elif i.get("radios").get("great").isChecked():
                if cprice > uprice:
                    print "great"
            

def main():
    app = QApplication([])
    foo = Launcher()
    foo.show()
    sys.exit(app.exec_())


def _sort_pairs(pairs):
    __pairs = []

    for key, val in pairs.items():
        for i in val:
            __pairs.append(i + "-" + key)
    return __pairs


if __name__ == "__main__":
    main()

