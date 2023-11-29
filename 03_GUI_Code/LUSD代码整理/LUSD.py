from __future__ import division
import sys

from PyQt5.QtWidgets import QSplashScreen

from WindowFile.mainWindow import *
from PyQt5.QtCore import Qt


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    splash = QSplashScreen()
    splash.setPixmap(QPixmap('../res/load.jpg'))
    splash.show()
    # splash.showMessage('Welcome to the LUSD model!',Qt.AlignBottom | Qt.AlignCenter, Qt.black)

    window = mywindow()
    window.actionArea.triggered.connect(window.Prediction_area.show)
    window.actionCalibration.triggered.connect(window.Calibration.show)
    window.actionSimulation.triggered.connect(window.Simulation.show)
    window.actionValidation.triggered.connect(window.Validation.show)
    window.actionAbout.triggered.connect(window.About.show)
    window.actionApplication.triggered.connect(window.Border.show)

    window.areaButton.clicked.connect(window.Prediction_area.show)
    window.calibrationButton.clicked.connect(window.Calibration.show)
    window.simulationButton.clicked.connect(window.Simulation.show)
    window.ValidationButton.clicked.connect(window.Validation.show)
    window.ApplicationButton.clicked.connect(window.Border.show)

    window.show()

    splash.finish(window)

    sys.exit(app.exec_())