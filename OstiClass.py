#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:55:53 2019
3333
@author: miurakaname
"""
import sys
from PyQt5 import QtWidgets
from mainUi import Ui_OptiClassMain

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_OptiClassMain()
        self.ui.setupUi(self)

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())