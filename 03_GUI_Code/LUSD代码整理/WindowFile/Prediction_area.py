import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QDialog,QFileDialog
from GUIFile.Prediction_area_GUI import *
from sklearn.linear_model import LinearRegression

class childWindow(QDialog, Ui_Dialog):   # 计算方程
    def __init__(self, input_callback=None, parent=None):
        super(childWindow, self).__init__(parent)
        self.child = Ui_Dialog()
        self.child.setupUi(self)
        self.child.retranslateUi(self)
        self.child.pushButton.clicked.connect(self.open_calexcel)
        self.child.pushButton_2.clicked.connect(self.open_prexcel)
        self.child.pushButton_5.clicked.connect(self.Prediction_area)
        self.child.pushButton_6.clicked.connect(self.savetext)
        self.child.pushButton_7.clicked.connect(self.close)

    def savetext(self):
        StrText = self.child.textBrowser.toPlainText()
        path, datatype = QFileDialog.getSaveFileName(self,
                                                     r'创建txt并保存',
                                                     r'D:\panxi\Desktop\yanjidata\data',
                                                     r'Files(*.txt)')
        if path:
            qS = str(StrText)
            f = open(path, 'w')
            print(f.write('{}'.format(qS)))
            f.close()

    def open_calexcel(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read Excel file", "D:\panxi\Desktop\yanjidata\data",
                                                         "Excel Files(*.xlsx)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child.lineEdit.setText(fileName)

    def open_prexcel(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read Excel file", "D:\panxi\Desktop\yanjidata\data",
                                                         "Excel Files(*.xlsx)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child.lineEdit_2.setText(fileName)

    def CityCounts(self, calculation, prediction, sheet1, sheet2): # 传入两个文件的路径和表格sheet1
        df = pd.read_excel(calculation, sheet1) # 创建一个数组写入每列的值
        # df.columns = ['Year', 'Y', 'Population']
        df = df.rename(columns={'Urban Pixels': 'Y'})
        Y = np.array(df.Y) # 获取标签为Y的一列
        X = df.drop(['Y'], axis=1) # 在X中删除Y列
        try:
            X = X.drop(['Year'],axis = 1) # 如果有Years列也删除掉
        except:
            pass

        model = LinearRegression() # 使用线性回归
        model.fit(X, Y) # 传入X Y
        para = [pa for pa in model.coef_] # 返回值的第一项为常数项，后面的为X项系数
        para.insert(0, model.intercept_)
        r2 = model.score(X, Y.T) # 得到R方

        print("R2:{0}".format(r2))
        print("interception:{0}".format(para[0]))
        print("coefficient:{0}".format(para[1:]))
        self.child.textBrowser.append("R2:{0}".format(r2))
        self.child.textBrowser.append("interception:{0}".format(para[0])) # 常数项
        self.child.textBrowser.append("coefficient:{0}".format(para[1:])) # X项系数

        df2 = pd.read_excel(prediction, sheet1) # 读取预测表，并变为一个矩阵
        try:
            df2 = df2.drop(['Year'],axis = 1)
        except:
            pass
        row = df2.shape[0] # 使用的列数
        df2.insert(0, 'cone', [1] * row)
        citycount = []
        for i in range(row):
            array = np.array(df2.iloc[i]) # 读取第i个数
            CityCount = np.dot(array, para) # 代入方程计算结果
            citycount.append(CityCount) # 保存结果
        return citycount

    def Prediction_area(self):
        calculation = self.child.lineEdit.text()
        prediction = self.child.lineEdit_2.text()
        sheet1 = 'Sheet1'
        sheet2 = 'Sheet1'
        CityCount = [int(i) for i in self.CityCounts(calculation, prediction, sheet1, sheet2)]
        print(CityCount)
        self.child.textBrowser.append("Predicted urban pixels: {}".format(CityCount))
        return CityCount
