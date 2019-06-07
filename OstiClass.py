#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 10:55:53 2019
3333
@author: miurakaname
"""
import sys
import pandas as pa
import numpy as np
from os import chdir, getcwd
#import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from mainUi import Ui_OptiClassMain

workspace = getcwd()


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
        self.place = [0,0,0,0]
        self.ui.comboBox_region.activated.connect(lambda:self.placeState(self.ui.comboBox_region.currentIndex(),0))
        self.ui.comboBox_country.activated.connect(lambda:self.placeState(self.ui.comboBox_country.currentIndex(),1))
        self.ui.comboBox_hospital.activated.connect(lambda:self.placeState(self.ui.comboBox_hospital.currentIndex(),2))
        self.ui.comboBox_device.activated.connect(lambda:self.placeState(self.ui.comboBox_device.currentIndex(),3))
        
        
        ## groupBox_period
        self.period = 0
        self.ui.radioButton_periodAll.toggled.connect(lambda:self.periodState(0))
        self.ui.radioButton_period1y.toggled.connect(lambda:self.periodState(365))
        self.ui.radioButton_period05y.toggled.connect(lambda:self.periodState(183))
        self.ui.radioButton_period1m.toggled.connect(lambda:self.periodState(30))
        self.ui.radioButton_period1w.toggled.connect(lambda:self.periodState(7))
        self.ui.radioButton_period1d.toggled.connect(lambda:self.periodState(1))
        """""
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
        print(self.place)
        print(self.period)
        
    def confAnalysis(self):
        print("Analysis !!!!")
        
    def placeState(self,state,n):
        self.place[n] = state
        print(self.place)
        
    def periodState(self,n):
        self.period = n

        
    # ノイズ除去
    def noiseCancel(self, y):
        threshold_1 = 40
        threshold_2 = 5
        for i in range(len(y)):
            for j in range(len(y[i])-2):
                if abs(y[i][j]-y[i][j + 1]) > threshold_1:
                    aveIr = (y[i][j] + y[i][j+2])/2
                    y[i][j+1] = aveIr
        for i in range(len(y)):
            for j in range(len(y[i])-2):
                if abs(y[i][j]-y[i][j + 1]) > threshold_2:
                    y[i][j+1] = (y[i][j] + y[i][j+2])/2
            if abs(y[i][-1]-y[i][-2]) > threshold_2:
                y[i][-1] = y[i][-2]
        return np.array(y)
    
    
    #### 読み込み関係の関数 ####
    def readOBD(self, df_):
        #obdの読み込み
        chdir("OBD")
        
        def reader(col):
            #colは obdRadius, obdUlnar, obdPhantom の３種類です。
        
            #
            obd = []
            try:
                for i in range(len(df_)):
                    csv_df = pa.read_csv(df_[col][i], header=10)
                    csv_list = self.noiseCancel(csv_df.as_matrix().T[1:9])
                    obd.append(csv_list)
                    #csv_df = pa.read_csv(files[i], header=8,nrows=1)
                    #mes_point.append(csv_df.as_matrix())
            finally:
                pass
            return obd
        
        obdRadius = []; obdUlnar = []; obdPhantom = []
        obdRadius = self.dataModificaton(reader("obdRadius"))
        obdUlnar = self.dataModificaton(reader("obdUlnar"))
        #obdPhantom = dataModificaton(reader("obdPhantom"))
        chdir(workspace)
        return obdRadius, obdUlnar, obdPhantom
    
        
    def dataModificaton(self, list_obd):#引数の形は(n,8,m)である必要がある
        #入射光強度　（注意：電圧ではない）
        int_gr_light = 6*(10**6) 
        int_ir_light = 3.5*(10**6)
        int_Ir_light = 5.5*(10**6)
        
        list_obd = np.array(list_obd)
        dist = []
        for i in list_obd:
            gr = np.log10((i[0]+i[1]-i[6]-i[7])/(2*int_gr_light))
            ir = np.log10((i[2]+i[3]-i[6]-i[7])/(2*int_ir_light))
            Ir = np.log10((i[4]+i[5]-i[6]-i[7])/(2*int_Ir_light))
            dist.append([gr,ir,Ir])
        return np.array(dist)
        
    
    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())