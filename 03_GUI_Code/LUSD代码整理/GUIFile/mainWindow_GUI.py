# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow_GUI1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(494, 365)
        MainWindow.setFixedSize(494, 365)
    # 设置只显示关闭按钮
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.simulationButton = QtWidgets.QPushButton(self.centralwidget)
        self.simulationButton.setGeometry(QtCore.QRect(200, 100, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.simulationButton.setFont(font)
        self.simulationButton.setStyleSheet("background-color: rgb(70, 193, 193);\n"
"background-color: rgb(127,189,236);")
        self.simulationButton.setObjectName("simulationButton")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, -10, 591, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.ValidationButton = QtWidgets.QPushButton(self.centralwidget)
        self.ValidationButton.setGeometry(QtCore.QRect(200, 190, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.ValidationButton.setFont(font)
        self.ValidationButton.setStyleSheet("background-color: rgb(151,200,240);")
        self.ValidationButton.setObjectName("ValidationButton")
        self.ApplicationButton = QtWidgets.QPushButton(self.centralwidget)
        self.ApplicationButton.setGeometry(QtCore.QRect(200, 280, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.ApplicationButton.setFont(font)
        self.ApplicationButton.setStyleSheet("background-color: rgb(170,208,247);")
        self.ApplicationButton.setObjectName("ApplicationButton")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(232, 140, 23, 47))
        self.label_6.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("../res/arrow6.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.areaButton = QtWidgets.QPushButton(self.centralwidget)
        self.areaButton.setGeometry(QtCore.QRect(140, 20, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.areaButton.setFont(font)
        self.areaButton.setStyleSheet("background-color: rgb(120,183,234);")
        self.areaButton.setObjectName("areaButton")
        self.calibrationButton = QtWidgets.QPushButton(self.centralwidget)
        self.calibrationButton.setGeometry(QtCore.QRect(260, 20, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.calibrationButton.setFont(font)
        self.calibrationButton.setStyleSheet("background-color: rgb(120,183,234);")
        self.calibrationButton.setObjectName("calibrationButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, -30, 381, 381))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../res/background.png"))
        self.label.setScaledContents(True)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(190, 50, 31, 41))
        self.label_4.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../res/arrow2.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(270, 50, 31, 41))
        self.label_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../res/arrow3.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(232, 230, 23, 47))
        self.label_7.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("../res/arrow6.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label.raise_()
        self.areaButton.raise_()
        self.calibrationButton.raise_()
        self.simulationButton.raise_()
        self.line.raise_()
        self.ValidationButton.raise_()
        self.ApplicationButton.raise_()
        self.label_6.raise_()
        self.label_4.raise_()
        self.label_2.raise_()
        self.label_7.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 494, 26))
        self.menubar.setStyleSheet("background-color: rgb(195,219,243);")
        self.menubar.setObjectName("menubar")
        self.menuArea = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.menuArea.setFont(font)
        self.menuArea.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.menuArea.setTabletTracking(False)
        self.menuArea.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.menuArea.setObjectName("menuArea")
        self.menuCalibration = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.menuCalibration.setFont(font)
        self.menuCalibration.setObjectName("menuCalibration")
        self.menuSimulation = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.menuSimulation.setFont(font)
        self.menuSimulation.setStyleSheet("border-color: rgb(0, 0, 0);")
        self.menuSimulation.setObjectName("menuSimulation")
        self.menuValidation = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.menuValidation.setFont(font)
        self.menuValidation.setObjectName("menuValidation")
        self.menuApplication = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.menuApplication.setFont(font)
        self.menuApplication.setObjectName("menuApplication")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuHelp.sizePolicy().hasHeightForWidth())
        self.menuHelp.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.menuHelp.setFont(font)
        self.menuHelp.setStyleSheet("")
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../res/Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setText("")
        self.actionOpen.setObjectName("actionOpen")
        self.actionWhole = QtWidgets.QAction(MainWindow)
        self.actionWhole.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../res/Full.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionWhole.setIcon(icon2)
        self.actionWhole.setText("")
        self.actionWhole.setObjectName("actionWhole")
        self.actionZoomIn = QtWidgets.QAction(MainWindow)
        self.actionZoomIn.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../res/Zoomin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon3)
        self.actionZoomIn.setText("")
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut = QtWidgets.QAction(MainWindow)
        self.actionZoomOut.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../res/Zoomout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon4)
        self.actionZoomOut.setText("")
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionMove = QtWidgets.QAction(MainWindow)
        self.actionMove.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../res/Pan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMove.setIcon(icon5)
        self.actionMove.setText("")
        self.actionMove.setObjectName("actionMove")
        self.actionLUSD_Calibration = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme("res/Open.png")
        self.actionLUSD_Calibration.setIcon(icon)
        self.actionLUSD_Calibration.setObjectName("actionLUSD_Calibration")
        self.actionLUSD_simulation = QtWidgets.QAction(MainWindow)
        self.actionLUSD_simulation.setObjectName("actionLUSD_simulation")
        self.actionProbability_Calculation = QtWidgets.QAction(MainWindow)
        self.actionProbability_Calculation.setObjectName("actionProbability_Calculation")
        self.actionCalibration = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.actionCalibration.setFont(font)
        self.actionCalibration.setObjectName("actionCalibration")
        self.actionOpen_2 = QtWidgets.QAction(MainWindow)
        self.actionOpen_2.setObjectName("actionOpen_2")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionSimulation = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.actionSimulation.setFont(font)
        self.actionSimulation.setObjectName("actionSimulation")
        self.actionUser_Guide = QtWidgets.QAction(MainWindow)
        self.actionUser_Guide.setObjectName("actionUser_Guide")
        self.actionValidation = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.actionValidation.setFont(font)
        self.actionValidation.setObjectName("actionValidation")
        self.actionHelp_User = QtWidgets.QAction(MainWindow)
        self.actionHelp_User.setObjectName("actionHelp_User")
        self.actionArea = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.actionArea.setFont(font)
        self.actionArea.setObjectName("actionArea")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.actionAbout.setFont(font)
        self.actionAbout.setObjectName("actionAbout")
        self.actionUser_Guide_2 = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.actionUser_Guide_2.setFont(font)
        self.actionUser_Guide_2.setObjectName("actionUser_Guide_2")
        self.actionApplication = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.actionApplication.setFont(font)
        self.actionApplication.setObjectName("actionApplication")
        self.menuArea.addAction(self.actionArea)
        self.menuCalibration.addAction(self.actionCalibration)
        self.menuSimulation.addAction(self.actionSimulation)
        self.menuValidation.addAction(self.actionValidation)
        self.menuApplication.addAction(self.actionApplication)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionUser_Guide_2)
        self.menubar.addAction(self.menuArea.menuAction())
        self.menubar.addAction(self.menuCalibration.menuAction())
        self.menubar.addAction(self.menuSimulation.menuAction())
        self.menubar.addAction(self.menuValidation.menuAction())
        self.menubar.addAction(self.menuApplication.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.simulationButton.setText(_translate("MainWindow", "Simulation"))
        self.ValidationButton.setText(_translate("MainWindow", "Validation"))
        self.ApplicationButton.setText(_translate("MainWindow", "Application"))
        self.areaButton.setText(_translate("MainWindow", "Area"))
        self.calibrationButton.setText(_translate("MainWindow", "Calibration"))
        self.menuArea.setTitle(_translate("MainWindow", "Area"))
        self.menuCalibration.setTitle(_translate("MainWindow", "Calibration"))
        self.menuSimulation.setTitle(_translate("MainWindow", "Simulation"))
        self.menuValidation.setTitle(_translate("MainWindow", "Validation"))
        self.menuApplication.setTitle(_translate("MainWindow", "Application"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open"))
        self.actionWhole.setToolTip(_translate("MainWindow", "Full"))
        self.actionZoomIn.setToolTip(_translate("MainWindow", "Zoom in"))
        self.actionZoomOut.setToolTip(_translate("MainWindow", "Zoom out"))
        self.actionMove.setToolTip(_translate("MainWindow", "Move"))
        self.actionLUSD_Calibration.setText(_translate("MainWindow", "Calibration"))
        self.actionLUSD_simulation.setText(_translate("MainWindow", "Simulation"))
        self.actionProbability_Calculation.setText(_translate("MainWindow", "Simulation"))
        self.actionCalibration.setText(_translate("MainWindow", "Calibration"))
        self.actionOpen_2.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionClear.setText(_translate("MainWindow", "Close"))
        self.actionSimulation.setText(_translate("MainWindow", "Simulation"))
        self.actionUser_Guide.setText(_translate("MainWindow", "User Guide"))
        self.actionValidation.setText(_translate("MainWindow", "Validation"))
        self.actionHelp_User.setText(_translate("MainWindow", "User Guide"))
        self.actionArea.setText(_translate("MainWindow", "Area"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionUser_Guide_2.setText(_translate("MainWindow", "User Guide"))
        self.actionApplication.setText(_translate("MainWindow", "Urban growth boundary"))

