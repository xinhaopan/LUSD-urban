from PyQt5.QtWidgets import QFileDialog,QDialog

from GUIFile.Validation_GUI import *
from ScriptFile.LoadData import *

class childWindow_4(QDialog, Ui_Dialog_4):
    def __init__(self, input_callback=None, parent=None):
        super(childWindow_4, self).__init__(parent)
        self.child_4 = Ui_Dialog_4()
        self.child_4.setupUi(self)
        self.child_4.retranslateUi(self)
        self.input_callback = input_callback
        self.child_4.pushButton.clicked.connect(self.open_groud)
        self.child_4.pushButton_2.clicked.connect(self.open_sim)
        self.child_4.pushButton_3.clicked.connect(self.Kappa)
        self.child_4.pushButton_4.clicked.connect(self.closeWindow)

    def open_groud(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "TIFF Files(*.tif)")
        self.child_4.lineEdit.setText(fileName)

    def open_sim(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "TIFF Files(*.tif)")
        self.child_4.lineEdit_2.setText(fileName)

    def closeWindow(self):
        self.destroy()

    def Kappa(self): # 计算并输出kappa系数和总体精度
        Ground_Truth = LoadData(self.child_4.lineEdit.text()) # 使用LoadDate方法，读进该控件中存放路径对应的影像，影像的空值部分已经被赋予0值
        Simulated_Result = LoadData(self.child_4.lineEdit_2.text())
        urban_ID = int(self.child_4.lineEdit_3.text()) # 读进城市对应的ID，转换为int型

        NoUrbanIndex1 = np.where((Ground_Truth != urban_ID) & (Ground_Truth != 0)) # 不是城市也不是背景的地方
        Ground_Truth[NoUrbanIndex1] = 1 # 非城市非背景的部分赋值为1
        UrbanIndex1 = np.where(Ground_Truth == urban_ID) # 是城市的地方
        Ground_Truth[UrbanIndex1] = 2 # 城市 赋值为2

        NoUrbanIndex2 = np.where((Simulated_Result != urban_ID) & (Simulated_Result != 0))
        Simulated_Result[NoUrbanIndex2] = 1
        UrbanIndex2 = np.where(Simulated_Result == urban_ID)
        Simulated_Result[UrbanIndex2] = 2

        Ground_Truth = np.array(Ground_Truth).reshape(-1) # 降维，二维变成一维的
        Simulated_Result = np.array(Simulated_Result).reshape(-1)

        result = 10 * Ground_Truth + Simulated_Result #实际城市在十位，模拟结果城市在个位
        Acc_22 = np.size(np.where(result == 22)) # 实际和结果都是城市
        Acc_11 = np.size(np.where(result == 11)) # 实际和结果都不是城市
        Acc_21 = np.size(np.where(result == 21)) # 实际是城市，结果不是城市
        Acc_12 = np.size(np.where(result == 12)) # 实际不是城市，结果是城市
        TotalNum = float(Acc_22 + Acc_11 + Acc_21 + Acc_12) # 像元总数
        kappa = (float(TotalNum * (Acc_22 + Acc_11) - (float(Acc_21 + Acc_11) * (Acc_12 + Acc_11) +      # 计算kappa系数的公式
                                                       float(Acc_21 + Acc_22) * (Acc_12 + Acc_22)))) / (
                            TotalNum ** 2 - (float(Acc_21 + Acc_11) * (Acc_12 + Acc_11) +
                                             float(Acc_21 + Acc_22) * (Acc_12 + Acc_22)))

        TotalNum = Acc_22 + Acc_11 + Acc_21 + Acc_12
        OverAccury = float(Acc_22 + Acc_11) / TotalNum # 分类正确的像元数量除以总的像元数量得到总体精度

        self.child_4.textBrowser.append("kappa = {}".format(kappa)) # 在该控件上新的一行输出kappa= 结果
        self.child_4.textBrowser.append("OverallAccuracy = {}".format(OverAccury))
        return kappa