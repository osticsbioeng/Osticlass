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
        self.optState = np.zeros(11)
        self.boneState = ["Ulna","UD","UD","Neck","L1"]
        self.bone_df = pa.DataFrame()
        # 機械学習パラメーター
        self.modelState = 0
        self.parameterState = ""
        self.crossValidState = 0
        
        #### Mainフレームのパーツ ####
        self.ui.pushButton_basicAnalysis.clicked.connect(self.confAnalysis)
        self.ui.pushButton_machineStart.clicked.connect(self.confLaerning)
        
        
        #### Optical tab #####
        ## groupBox_place
        self.ui.comboBox_region.activated.connect(lambda:self.setOptState(self.ui.comboBox_region.currentIndex(),0))
        self.ui.comboBox_country.activated.connect(lambda:self.setOptState(self.ui.comboBox_country.currentIndex(),1))
        self.ui.comboBox_hospital.activated.connect(lambda:self.setOptState(self.ui.comboBox_hospital.currentIndex(),2))
        self.ui.comboBox_device.activated.connect(lambda:self.setOptState(self.ui.comboBox_device.currentIndex(),3))
        
        
        ## groupBox_period
        self.ui.radioButton_periodAll.toggled.connect(lambda:self.setOptState(0,4))
        self.ui.radioButton_period1y.toggled.connect(lambda:self.setOptState(365,4))
        self.ui.radioButton_period05y.toggled.connect(lambda:self.setOptState(183,4))
        self.ui.radioButton_period1m.toggled.connect(lambda:self.setOptState(30,4))
        self.ui.radioButton_period1w.toggled.connect(lambda:self.setOptState(7,4))
        self.ui.radioButton_period1d.toggled.connect(lambda:self.setOptState(1,4))
        
        
        ## groupBox_gender
        self.ui.radioButton_genderAll.toggled.connect(lambda:self.setOptState(0,5))
        self.ui.radioButton_genderF.toggled.connect(lambda:self.setOptState(1,5))
        self.ui.radioButton_genderM.toggled.connect(lambda:self.setOptState(2,5))
        
        
        ## groupBox_age
        self.ui.lineEdit_rangeAge1.textEdited.connect(lambda:self.setOptState(self.ui.lineEdit_rangeAge1.displayText(),6))
        self.ui.lineEdit_rangeAge2.textEdited.connect(lambda:self.setOptState(self.ui.lineEdit_rangeAge2.displayText(),7))
        
        
        ## groupBox_optdata
        self.ui.radioButton_optDataUlna.toggled.connect(lambda:self.setOptState(0,8))
        self.ui.radioButton_optDataRadius.toggled.connect(lambda:self.setOptState(1,8))
        self.ui.checkBox_optDataPhantom.stateChanged.connect(lambda:self.setOptStateCheckBox(self.ui.checkBox_optDataPhantom,9))
        
        
        ## groupBox_arm
        self.ui.radioButton_armAll.toggled.connect(lambda:self.setOptState(0,10))
        self.ui.radioButton_armLeft.toggled.connect(lambda:self.setOptState(1,10))
        self.ui.radioButton_armRight.toggled.connect(lambda:self.setOptState(2,10))
        
        #self.ui.pushButton_optset.clicked.connect(self.confLaerning)
        
        
        #### Bone tab #####
        ## groupBox_bone
        self.ui.radioButton_boneUlna.toggled.connect(lambda:self.setBoneState("Ulna",0))
        self.ui.radioButton_boneRadius.toggled.connect(lambda:self.setBoneState("Radius",0))
        self.ui.radioButton_boneFemur.toggled.connect(lambda:self.setBoneState("Femur",0))
        self.ui.radioButton_boneLumbar.toggled.connect(lambda:self.setBoneState("Lumbar",0))
        self.ui.comboBox_boneUlna.activated.connect(lambda:self.setBoneState(self.ui.comboBox_boneUlna.currentText(),1))
        self.ui.comboBox_boneRadius.activated.connect(lambda:self.setBoneState(self.ui.comboBox_boneRadius.currentText(),2))
        self.ui.comboBox_boneNeck.activated.connect(lambda:self.setBoneState(self.ui.comboBox_boneNeck.currentText(),3))
        self.ui.comboBox_boneLumbar.activated.connect(lambda:self.setBoneState(self.ui.comboBox_boneLumbar.currentText(),4))
        
        #self.ui.pushButton_boneSet.clicked.connect()
        
        """""
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
        self.ui.comboBox_machineModel.activated.connect(lambda:self.setMachineLearningModel(self.ui.comboBox_machineModel.currentIndex()))
        #self.ui.textEdit_machinePara.textChanged.connect(lambda:self.setParameter(self.ui.textEdit_machinePara.displayText()))
        
        self.ui.radioButton_crossLoo.toggled.connect(lambda:self.setCrossValid(0))
        self.ui.radioButton_cross5per.toggled.connect(lambda:self.setCrossValid(5))
        self.ui.radioButton_cross10per.toggled.connect(lambda:self.setCrossValid(10))
        self.ui.radioButton_cross20per.toggled.connect(lambda:self.setCrossValid(20))
        self.ui.radioButton_cross30per.toggled.connect(lambda:self.setCrossValid(30))
        
        #self.ui.pushButton_machineSet
        
    def getDatabase(self):
        data_df = pa.read_excel("database.xlsx")
        return data_df
    
    def getIndexName(self):
        index_df = pa.read_excel("index_list.xlsx")
        return index_df
    
    def setBoneData(self):
        data_df = self.getDatabase()
        index_df = self.getIndexName()
        self.bone_df =  pa.DataFrame()
        
        if self.boneState[0]=="Ulna":
            index_df = index_df[index_df['Index Name'].str.contains(self.boneState[0])]
            index_df = index_df[index_df['Index Name'].str.contains(self.boneState[1])]            
        elif self.boneState[0]=="Radius":
            index_df = index_df[index_df['Index Name'].str.contains(self.boneState[0])]
            index_df = index_df[index_df['Index Name'].str.contains(self.boneState[2])]            
        elif self.boneState[0]=="Femur":
            index_df = index_df[index_df['Index Name'].str.contains(self.boneState[3])]
        elif self.boneState[0]=="Lumbar":
            index_df = index_df[index_df['Index Name'].str.contains(self.boneState[4])]
            
        bone_name = index_df.ix[index_df.index[0]]
        self.bone_df[bone_name] = data_df[bone_name]
        print(self.bone_df)
            
    def confLaerning(self):
        self.setBoneData()
        self.w = QtWidgets.QWidget()
        self.w.setWindowTitle('Confirmation')
        # label
        col0_layout1 = QtWidgets.QVBoxLayout()
        col0_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
        
        self.groupBox_conf0 = QtWidgets.QGroupBox("Optical data")
        #box0 = QtWidgets.QHBoxLayout()
        #box0.addLayout(col0_layout1)
        #box0.addLayout(col0_layout2)
        self.groupBox_conf0.setLayout(col0_layout1)
        
            
        self.groupBox_conf1 = QtWidgets.QGroupBox("Bone infomation")
        col1_layout1 = QtWidgets.QVBoxLayout()
        if self.boneState[0]==0:
            col1_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
            col1_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
        elif self.boneState[0]==1:
            col1_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
            col1_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
        elif self.boneState[0]==2:
            col1_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
            col1_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
        elif self.boneState[0]==3:
            col1_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
            col1_layout1.addWidget(QtWidgets.QLabel("Place: %s"%self.optState))
            
        self.groupBox_conf1.setLayout(col1_layout1)
        
        
        self.groupBox_conf2 = QtWidgets.QGroupBox("Machine learning model")
        col0_layout2 = QtWidgets.QVBoxLayout()
        col0_layout2.addWidget(QtWidgets.QLabel("parameter: %s"%self.parameterState))
        self.groupBox_conf2.setLayout(col0_layout2)

        # layout の定義
        grid = QtWidgets.QVBoxLayout()
        grid.addWidget(self.groupBox_conf0)
        grid.addWidget(self.groupBox_conf2)
        self.w.resize( 200, 250)
        self.w.setLayout(grid)
        self.w.show()
        
    def confAnalysis(self):
        print("Analysis !!!!")
        
    def setOptState(self,state,n):
        self.optState[n] = state
        print(self.optState)
        
    def setOptStateCheckBox(self,state,n):
        if state.isChecked() == True:
            self.optState[n] = 1
        else:
            self.optState[n] = 0
    
    def setBoneState(self,state,n):
        self.boneState[n] = state
        print(self.boneState)
        
    def setMachineLearningModel(self,state):
        self.modelState = state
        
    def setCrossValid(self,state):
        self.crossValidState = state
    
    def setParameter(self,state):
        self.parameterState = state
            
        
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