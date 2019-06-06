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
        
        #### status変数 #####
        self.name_ = "aa"
        
        
        #### Mainフレームのパーツ ####
        self.ui.pushButton_basicAnalysis.clicked.connect(self.confAnalysis)
        self.ui.pushButton_machineStart.clicked.connect(self.confLaerning)
        
        
        #### Optical tab #####
        ## groupBox_place
        self.ui.comboBox_region.activated.connect()
        self.ui.comboBox_country.activated.connect()
        self.ui.comboBox_hospital.activated.connect()
        self.ui.comboBox_device.activated.connect()
        
        ## groupBox_period
        self.ui.radioButton_periodAll.toggled.connect()
        self.ui.radioButton_period1y.toggled.connect()
        self.ui.radioButton_period05y.toggled.connect()
        self.ui.radioButton_period1m.toggled.connect()
        self.ui.radioButton_period1w.toggled.connect()
        self.ui.radioButton_period1d.toggled.connect()
        
        ## groupBox_gender
        self.ui.radioButton_genderAll.toggled.connect()
        self.ui.radioButton_genderF.toggled.connect()
        self.ui.radioButton_genderM.toggled.connect()
        
        ## groupBox_age
        self.ui.lineEdit_rangeAge1.textEdited.connect()
        self.ui.lineEdit_rangeAge2.textEdited.connect()
        
        ## groupBox_optdata
        self.ui.radioButton_optDataUlna.toggled.connect()
        self.ui.radioButton_optDataRadius.toggled.connect()
        self.ui.checkBox_optDataPhantom.stateChanged.connect()
        
        ## groupBox_arm
        self.ui.radioButton_armAll.toggled.connect()
        self.ui.radioButton_armLeft.toggled.connect()
        self.ui.radioButton_armRight.toggled.connect()
        
        self.ui.pushButton_optset.clicked.connect(self.confLaerning)
        
        
        #### Bone tab #####
        ## groupBox_bone
        self.ui.radioButton_boneUlna.toggled.connect()
        self.ui.radioButton_boneRadius.toggled.connect()
        self.ui.radioButton_boneFemur.toggled.connect()
        self.ui.radioButton_boneLumbar.toggled.connect()
        self.ui.comboBox_boneUlna.activated.connect()
        self.ui.comboBox_boneRadius.activated.connect()
        self.ui.comboBox_boneNeck.activated.connect()
        self.ui.comboBox_boneLumbar.activated.connect()
        
        self.ui.pushButton_boneSet.clicked.connect()
        
        ## groupBox_other
        """""
        self.ui.checkBox_otherAge
        self.ui.checkBox_otherHand
        self.ui.checkBox_otherBmi
        self.ui.checkBoax_otherHight
        self.ui.checkBox_otherWeight
        self.ui.checkBox_otherDiabates
        self.ui.checkBox_otherDialysis
        self.ui.checkBox_otherArmFrac
        self.ui.checkBox_otherArtifical
        self.ui.checkBox_otherDrug
        self.ui.checkBox_otherPrivFrac
        self.ui.checkBox_otherSmoking
        self.ui.checkBox_otherOsteo
        self.ui.checkBox_otherHipFrac
        self.ui.checkBox_otherRheumat
        self.ui.checkBox_otherAlcohol
        
        self.ui.pushButton_otherSet.clicked.connect()
        """""
        
        #### Machine laerning tab ####
        self.ui.comboBox_machineModel
        self.ui.textEdit_machinePara
        
        self.ui.radioButton_crossLoo
        self.ui.radioButton_cross5per
        self.ui.radioButton_cross10per
        self.ui.radioButton_cross20per
        self.ui.radioButton_cross30per
        
        self.ui.pushButton_machineSet
        
        
    def confLaerning(self):
        print("Start !!!!")
        
    def confAnalysis(self):
        print("Analysis !!!!")
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())