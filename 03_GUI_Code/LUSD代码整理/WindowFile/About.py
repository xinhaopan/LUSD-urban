import os
from PyQt5.QtWidgets import QDialog,QGraphicsPixmapItem,QGraphicsScene
from PyQt5.QtGui import QPixmap

from GUIFile.About_GUI import *

class childWindow_6(QDialog, Ui_Dialog_6):
    def __init__(self, input_callback=None, parent=None):
        super(childWindow_6, self).__init__(parent)
        self.child_7 = Ui_Dialog_6()
        self.child_7.setupUi(self)
        self.child_7.retranslateUi(self)
        self.input_callback = input_callback
        path = os.getcwd() # 获取当前路径
        os.chdir(path)
        item = QGraphicsPixmapItem(QPixmap('../res/about.png'))
        scene = QGraphicsScene()
        scene.addItem(item)
        self.child_7.graphicsView.setScene(scene)