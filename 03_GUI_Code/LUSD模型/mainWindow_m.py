# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow_m.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(510, 368)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/3935.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon1)
        self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 510, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLUSD = QtWidgets.QMenu(self.menubar)
        self.menuLUSD.setObjectName("menuLUSD")
        self.menuPrediction = QtWidgets.QMenu(self.menubar)
        self.menuPrediction.setObjectName("menuPrediction")
        self.menuValidation = QtWidgets.QMenu(self.menubar)
        self.menuValidation.setObjectName("menuValidation")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("res/Open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setText("")
        self.actionOpen.setObjectName("actionOpen")
        self.actionWhole = QtWidgets.QAction(MainWindow)
        self.actionWhole.setCheckable(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("res/Full.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionWhole.setIcon(icon3)
        self.actionWhole.setText("")
        self.actionWhole.setObjectName("actionWhole")
        self.actionZoomIn = QtWidgets.QAction(MainWindow)
        self.actionZoomIn.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("res/Zoomin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon4)
        self.actionZoomIn.setText("")
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut = QtWidgets.QAction(MainWindow)
        self.actionZoomOut.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("res/Zoomout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon5)
        self.actionZoomOut.setText("")
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionMove = QtWidgets.QAction(MainWindow)
        self.actionMove.setCheckable(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("res/Pan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMove.setIcon(icon6)
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
        self.actionPrediction_prediction = QtWidgets.QAction(MainWindow)
        self.actionPrediction_prediction.setObjectName("actionPrediction_prediction")
        self.actionOpen_2 = QtWidgets.QAction(MainWindow)
        self.actionOpen_2.setObjectName("actionOpen_2")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionvalidation_Validation = QtWidgets.QAction(MainWindow)
        self.actionvalidation_Validation.setObjectName("actionvalidation_Validation")
        self.actionUser_Guide = QtWidgets.QAction(MainWindow)
        self.actionUser_Guide.setObjectName("actionUser_Guide")
        self.actionHelp_About = QtWidgets.QAction(MainWindow)
        self.actionHelp_About.setObjectName("actionHelp_About")
        self.actionHelp_User = QtWidgets.QAction(MainWindow)
        self.actionHelp_User.setObjectName("actionHelp_User")
        self.menuFile.addAction(self.actionOpen_2)
        self.menuFile.addAction(self.actionClear)
        self.menuLUSD.addAction(self.actionLUSD_Calibration)
        self.menuLUSD.addAction(self.actionLUSD_simulation)
        self.menuPrediction.addAction(self.actionPrediction_prediction)
        self.menuValidation.addAction(self.actionvalidation_Validation)
        self.menuHelp.addAction(self.actionHelp_About)
        self.menuHelp.addAction(self.actionHelp_User)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLUSD.menuAction())
        self.menubar.addAction(self.menuPrediction.menuAction())
        self.menubar.addAction(self.menuValidation.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMove)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionWhole)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomIn)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoomOut)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "Data"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuLUSD.setTitle(_translate("MainWindow", "LUSD"))
        self.menuPrediction.setTitle(_translate("MainWindow", "Prediction"))
        self.menuValidation.setTitle(_translate("MainWindow", "Validation"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen.setToolTip(_translate("MainWindow", "打开文件"))
        self.actionWhole.setToolTip(_translate("MainWindow", "全景模式"))
        self.actionZoomIn.setToolTip(_translate("MainWindow", "放大"))
        self.actionZoomOut.setToolTip(_translate("MainWindow", "缩小"))
        self.actionMove.setToolTip(_translate("MainWindow", "移动"))
        self.actionLUSD_Calibration.setText(_translate("MainWindow", "Calibration"))
        self.actionLUSD_simulation.setText(_translate("MainWindow", "Simulation"))
        self.actionProbability_Calculation.setText(_translate("MainWindow", "Simulation"))
        self.actionPrediction_prediction.setText(_translate("MainWindow", "Prediction of urban land area"))
        self.actionOpen_2.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as..."))
        self.actionClear.setText(_translate("MainWindow", "Close"))
        self.actionvalidation_Validation.setText(_translate("MainWindow", "Validation"))
        self.actionUser_Guide.setText(_translate("MainWindow", "User Guide"))
        self.actionHelp_About.setText(_translate("MainWindow", "About"))
        self.actionHelp_User.setText(_translate("MainWindow", "User Guide"))


