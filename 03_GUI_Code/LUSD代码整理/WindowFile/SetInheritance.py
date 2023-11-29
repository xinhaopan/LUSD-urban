from PyQt5.QtWidgets import QDialog,QFileDialog
from PyQt5.QtWidgets import QTableWidgetItem
from GUIFile.SetInheritance_GUI import *
import numpy as np
import pandas as pd

class childWindow_5(QDialog, Ui_Dialog_5): # 设置继承性和土地利用类型
    # urban_FID_signal = pyqtSignal(int)

    def __init__(self, input_callback=None, parent=None):
        super(childWindow_5, self).__init__(parent)
        self.child_6 = Ui_Dialog_5()
        self.child_6.setupUi(self)
        self.child_6.retranslateUi(self)
        self.child_6.input_callback = input_callback
        self.child_6.pushButton_4.clicked.connect(self.open_Inheritance)

        self.child_6.pushButton_2.clicked.connect(self.getdata)
        self.child_6.pushButton.clicked.connect(self.close)

    def open_Inheritance(self): # 打开继承性表格
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read Excel file", "D:\panxi\Desktop\yanjidata\data",
                                                         "Excel Files(*.xlsx)")
        # 设置文件扩展名过滤,注意用双分号间隔
        if fileName:
            self.child_6.lineEdit.setText(fileName) # 表格路径写到控件中
            Inheritance = self.child_6.lineEdit.text()
            df_I = np.array(pd.read_excel(Inheritance,'Sheet1',header=None)) # 将表中的数据以数组方式读出
            for m in range(np.shape(df_I)[0]):
                for n in range(np.shape(df_I)[1]):
                    Inher = str(df_I[m][n]) # 该单元格内容转换为str型
                    item_Inher = QTableWidgetItem(Inher) # 转换为该类型
                    self.child_6.tableWidget.setItem(m, n, item_Inher) # 写入对应的单元格
                    print(Inher)


    def getdata(self):
        Types = []
        TypeFID = []
        TypeResistance = []
        for i in range(16):
            try:
                Types.append(self.child_6.tableWidget.item(i, 1).text())
            except:
                pass
        print(Types)

        for i in range(16):
            try:
                TypeFID.append(self.child_6.tableWidget.item(i, 0).text())
            except:
                pass
        print(TypeFID)

        for i in range(16):
            try:
                TypeResistance.append(self.child_6.tableWidget.item(i, 2).text())
            except:
                pass
        print(TypeResistance)

        city = int(Types.index("urban")) # 获取城市对应的值
        urban_FID = TypeFID[city]
        print(urban_FID)
        self.child_6.input_callback(urban_FID,Types,TypeFID,TypeResistance) # 回调函数输出该内容
        print("input callback finished")
        # self.child_6.destroy()
        # self.urban_FID_signal.emit(urban_FID)