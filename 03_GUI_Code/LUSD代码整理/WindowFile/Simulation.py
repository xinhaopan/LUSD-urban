import time
import os

from PyQt5.QtWidgets import QMessageBox

from GUIFile.Simulation_GUI import *
from WindowFile.SetInheritance import *

from ScriptFile.GetNeighborEffect import *
from ScriptFile.WriteTiff import *

np.set_printoptions(suppress=True) #关闭科学计数法

class childWindow_3(QDialog, Ui_Dialog_3): # 计算未来面积
    def __init__(self, input_callback=None, parent=None):
        super(childWindow_3, self).__init__(parent)
        self.child_3 = Ui_Dialog_3()
        self.child_3.setupUi(self)
        self.child_3.retranslateUi(self)
        # self.input_callback = input_callback
        self.child_3.pushButton.clicked.connect(self.open_startyear2)
        self.child_3.pushButton_10.clicked.connect(self.open_ProbabilityPath)
        self.child_3.pushButton_12.clicked.connect(self.open_ResultPath)
        self.child_3.pushButton_6.clicked.connect(self.ProbabilityCal)
        self.child_3.pushButton_5.clicked.connect(self.open_Constraint)
        self.child_3.pushButton_7.clicked.connect(self.close)

        # 回调子界面6
        self.childui_6 = childWindow_5(self.input_callback, self)
        self.childui_6.setWindowTitle("Set Inheritance")
        self.child_3.pushButton_8.clicked.connect(lambda: self.childui_6.show())
        self.child_3.input_callback = input_callback

        self.child_3.tableWidget.doubleClicked.connect(self.importpath)

        # self.childui_6 = childWindow_5(self.input_callback, self)

        self.child_3.urban_FID = 0
        self.child_3.Types = []
        self.child_3.TypeFID = []
        self.child_3.TypeResistanc = []

        self.child_3.Step = 0
        self.child_3.DisturbConst = 0
        self.child_3.WindowSize = 0

    def input_callback(self, *args):
        print(args[:])
        self.child_3.urban_FID, self.child_3.Types, self.child_3.TypeFID, self.child_3.TypeResistance = args[:]

    def input_callback1(self, *args):
        print(args[:])
        self.child_3.Step,self.child_3.WindowSize, self.child_3.DisturbConst = args[:]

    def importpath(self):
        column = self.child_3.tableWidget.currentIndex().column()
        row = self.child_3.tableWidget.currentIndex().row()
        print(column,row)
        if column == 1:
            fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                             "All Files (*)")
            importpath = QTableWidgetItem(fileName)
            self.child_3.tableWidget.setItem(row, column, importpath)

    def open_startyear2(self):
        # fileName = QFileDialog.getExistingDirectory(self, "Read TIFF file", "C:/Users")
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "All Files (*)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_3.lineEdit.setText(fileName)
        self.child_3.startyear = fileName

    def open_ResultPath(self): # 设置存储路径
        # fileName = QFileDialog.getExistingDirectory(self, "Read TIFF file", "C:/Users")
        path, datatype = QFileDialog.getSaveFileName(self,
                                                     r'创建tiff并保存',
                                                     r'D:\panxi\Desktop\yanjidata\data',
                                                     r'TiffFiles(*.tif)')
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_3.lineEdit_9.setText(path)
        self.child_3.ResultPath = path

    def open_ProbabilityPath(self):
        # fileName = QFileDialog.getExistingDirectory(self, "Read TIFF file", "C:/Users")
        path, datatype = QFileDialog.getSaveFileName(self,
                                                     r'创建tiff并保存',
                                                     r'D:\panxi\Desktop\yanjidata\data',
                                                     r'TiffFiles(*.tif)')
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_3.lineEdit_7.setText(path)
        self.child_3.ProbabilityPath = path

    def open_Constraint(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "All Files (*)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_3.lineEdit_5.setText(fileName)
        self.child_3.Constraint = fileName

    def ProbabilityCal(self):
        start = time.clock()  # 开始计时
        # os.chdir(self.child_3.lineEdit.text())  # 设置环境变量，这样后面调用该文件夹里的文件时就可以写相对路径了
        StartYear = self.child_3.startyear

        LUCC_OLD = gdal.Open(StartYear)
        im_width = LUCC_OLD.RasterXSize  # 栅格矩阵的列数
        im_height = LUCC_OLD.RasterYSize  # 栅格矩阵的行数
        im_bands = LUCC_OLD.RasterCount  # 波段数
        im_geotrans = LUCC_OLD.GetGeoTransform()  # 获取仿射矩阵信息
        im_proj = LUCC_OLD.GetProjection()  # 获取投影信息

        ResultPath = self.child_3.ResultPath
        Probability = self.child_3.ProbabilityPath
        Constraint = ''  # 这就是那个可选的RestrictedData
        try:
            if len(self.child_3.Constraint) > 0:
                Constraint = self.child_3.lineEdit_5.text()
        except:
            pass

        urban = LoadData(StartYear)

        Step = int(self.child_3.lineEdit_10.text())
        DisturbConst = float(self.child_3.lineEdit_11.text())
        WindowSize = int(self.child_3.lineEdit_12.text())
        CityCount_Last = int(self.child_3.lineEdit_2.text())

        if Step == 0:
            Step = 1000

        if DisturbConst == 0:
            DisturbConst = 0.1

        if WindowSize == 0:
            WindowSize = 5

        # Step = 100  # Step,disturbConst和windowsize这三个变量在第二个窗口定义后要一直保留在内存中，因为第三步还需要调用
        # DisturbConst = 0.1

        urban_FID = int(self.child_3.urban_FID)
        Types = self.child_3.Types
        TypeFID = self.child_3.TypeFID
        TypeResistance = self.child_3.TypeResistance

        # WindowSize = 5
        size = np.shape(urban)
        nCols, nRows = size[1], size[0]
        urban = np.array(urban).reshape(-1)
        # urban_FID = 5  # 设置城市用地的代码 ，这里是必须有这个urban_FID的，在SetLanduse中你得显示出这个让用户输入 ppppppp

        labels = []
        paths = []
        suitabilitys = []
        for i in range(100):
            try:
                labels.append(self.child_3.tableWidget.item(i, 0).text())
            except:
                pass
        print(labels)

        for i in range(100):
            try:
                paths.append(self.child_3.tableWidget.item(i, 1).text())
            except:
                pass
        print(paths)

        for i in range(100):
            try:
                suitabilitys.append(int(self.child_3.tableWidget.item(i, 2).text()))
            except:
                pass
        print('--------')
        print(suitabilitys)
        Weight_Serial1 = np.array(suitabilitys, dtype=float)
        CellCountForAdd = CityCount_Last - np.sum(urban == urban_FID)  # CityCount_Last是窗口1的结果

        if len(labels) < 1:
            print('输入数据过少，请增加数据')
        try:
            for label in labels:
                i = labels.index(label)
                globals()[label] = LoadData(paths[i]).reshape(-1)  # 这个for循环是以用户输入的label为变量名读取栅格数据
        except:
            pass

        S_labels = ["S_{0}_A".format(label) for label in labels]
        for S_label in S_labels:
            globals()[S_label] = np.zeros([nRows, nCols]).reshape(-1)
        LoopNumber = CellCountForAdd // Step  # 计算循环次数
        Pk = np.zeros([nRows, nCols]).reshape(-1)
        Vk = 1 + (-np.log(np.random.rand(nRows, nCols))) ** DisturbConst  # 随机干扰系数
        Vk = Vk.reshape(-1)

        weight_index = 0
        LABELS = ["label{0}".format(labels.index(label)) for label in labels]  # 新建一个列表，其元素是后面权重的变量名
        weight_index = 0
        try:
            for LABEL in LABELS:  # 此循环是用来根据用户输入的数据来赋值权重给变量
                globals()[LABEL] = Weight_Serial1[weight_index]
                weight_index += 1
        except:
            pass

        LUCCNan_Index = np.where(np.isnan(urban))
        urban[LUCCNan_Index] = 0
        LUCCNoURBAN = np.where((urban != urban_FID) & (urban != 0))
        try:
            for label in labels:
                i = labels.index(label)
                globals()[S_labels[i]][LUCCNoURBAN] = globals()[label][LUCCNoURBAN] * globals()[LABELS[i]]
        except:
            pass

        urban_Copy = np.array(urban)  # 设置一个LUCC数据的拷贝
        NeighborEffect = np.zeros([nRows, nCols])
        # ----------------------------------循环模拟-------------------------------------
        for num in range(1, LoopNumber + 2):
            LUCCNoURBAN2 = np.where((urban_Copy != urban_FID) & (urban_Copy != 0))
            AffectedCells = np.array(LUCCNoURBAN2).reshape(-1)
            N_Weight = Weight_Serial1[-2]
            NeighborEffect = GetNeighborEffect(StartYear, AffectedCells, WindowSize,urban_FID)
            Nk_U = NeighborEffect * N_Weight
            Nk_U = np.array(Nk_U).reshape(-1)

            for Type in Types:
                name = "I_{0}".format(Type)
                i = Types.index(Type)
                globals()[name] = np.zeros([nRows, nCols]).reshape(-1)
                globals()[name][np.where(urban == int(TypeFID[i]))] = TypeResistance[i]

            I_Weight = Weight_Serial1[-1]
            I_Type = np.zeros([nRows, nCols]).reshape(-1)
            for Type in Types:
                name = "I_{0}".format(Type)
                I_Type += globals()[name]

            Ik = I_Type * I_Weight  # 计算非城镇像元的转换概率
            Pk = np.zeros([nRows, nCols]).reshape(-1)
            S_LABELS_A = np.zeros([nRows, nCols]).reshape(-1)
            for S_label in S_labels:
                S_LABELS_A[LUCCNoURBAN2] += globals()[S_label][LUCCNoURBAN2]
            Pk[LUCCNoURBAN2] = (S_LABELS_A[LUCCNoURBAN2] - Ik[LUCCNoURBAN2] + Nk_U[LUCCNoURBAN2]) * Vk[LUCCNoURBAN2]
            if Constraint != "":
                constraint = LoadData(Constraint).reshape(-1)
                Pk[LUCCNoURBAN2] = Pk[LUCCNoURBAN2] * constraint[LUCCNoURBAN2]

            if num == 1:
                gailv = np.array(Pk).reshape([nRows, nCols])
                gailv1 = gailv/gailv.max() # 标准化后输出

            PkSort_R_Index = np.argsort(-Pk)  # 降序索引

            if num < LoopNumber + 1:
                urban_Copy[PkSort_R_Index[0:Step]] = urban_FID  # 提取概率最高的赋值为城市
                print(np.size(np.where(urban_Copy == urban_FID)))
            else:
                urban_Copy[PkSort_R_Index[0:(CellCountForAdd % Step)]] = urban_FID
        # ----------------------------------结果保存-------------------------------------

        urban_Copy = np.array(urban_Copy).reshape([nRows, nCols])
        WriteTiff(urban_Copy, im_width, im_height, im_bands, im_geotrans, im_proj, ResultPath)  # 写入tif文件
        WriteTiff(gailv1, im_width, im_height, im_bands, im_geotrans, im_proj, Probability)
        elapsed = (time.clock() - start)
        print("模拟用时:", elapsed, "s")
        print("模拟成功！")
        QMessageBox.information(self, '!', 'Finish')
