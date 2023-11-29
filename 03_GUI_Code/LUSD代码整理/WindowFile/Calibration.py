import os
import time

from GUIFile.Calibration_GUI import *
from WindowFile.SetInheritance import *

from ScriptFile.GetNeighborEffect import *
from ScriptFile.Monte_Carlo import *


class childWindow_2(QDialog, Ui_Dialog_2):  #计算权重
    def __init__(self, input_callback=None, parent=None):
        super(childWindow_2, self).__init__(parent)
        self.child_2 = Ui_Dialog_2()
        self.child_2.setupUi(self)
        self.child_2.retranslateUi(self)
        self.child_2.pushButton.clicked.connect(self.open_startyear) # 该按钮绑定打开开始年份的槽函数
        self.child_2.pushButton_2.clicked.connect(self.open_endyear) # 该按钮绑定打开结束年份的槽函数
        self.child_2.pushButton_8.clicked.connect(self.WeightCal) # 该按钮绑定计算权重的槽函数
        # 回调函数
        self.child_2.input_callback = input_callback
        self.childui_6 = childWindow_5(self.input_callback, self) # 实例化该子窗体，并调用回调的值
        self.childui_6.setWindowTitle("Set Inheritance") # 设置该子子窗体的标题
        self.child_2.pushButton_5.clicked.connect(lambda:self.childui_6.show()) # 按钮连接打开该子子窗体的槽函数
        #self.child_2.pushButton_5.clicked.connect(self.openSetInheritance)
        self.child_2.input_callback = input_callback

        self.child_2.tableWidget.doubleClicked.connect(self.importpath) # 表格中单元格双击绑定传入路径的槽函数

        self.child_2.urban_FID = 0 # 在该窗体中定义城市值
        self.child_2.Types = [] # 定义一个列表存放用地类型标签
        self.child_2.TypeFID = [] # 定义一个列表存放用地类型对应的值
        self.child_2.TypeResistanc = [] # 定义一个列表存放用地类型的继承性

        # 设置进度条暂未成功
    # def openSetInheritance(self):
    #     self.childui_6 = childWindow_5(self.input_callback, self)  # 实例化该子窗体，并调用回调的值
    #     self.childui_6.setWindowTitle("Set Inheritance") # 设置该子子窗体的标题
    #     self.childui_6.show()

    def input_callback(self, *args):
        print(args[:])
        self.child_2.urban_FID,self.child_2.Types,self.child_2.TypeFID,self.child_2.TypeResistance = args[:] # 将回调的值分（城市用地类型值、用地类型名称、对应值和继承性）放入这三个变量中


    def importpath(self): # 传入路径槽函数
        column = self.child_2.tableWidget.currentIndex().column() # 返回双击的列的索引
        row = self.child_2.tableWidget.currentIndex().row() # 返回双击的行的索引
        print(column,row)
        if column == 1: # 如果双击的是第2列
            fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                             "All Files (*)") # 打开该窗口，可以返回所选文件的路径和文件类型
            importpath = QTableWidgetItem(fileName) # 路径转换为QTableWidgetItem型（特定类型，只有该类型可以写入表格中）的，放入该变量中
            self.child_2.tableWidget.setItem(row, column, importpath) # 将该值显示在表格中的对应单元格

    def open_startyear(self):
        # fileName = QFileDialog.getExistingDirectory(self, "Read TIFF file", "C:/Users")
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "All Files (*)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_2.lineEdit.setText(fileName) # 文件路径放入该控件中
        self.child_2.startyear = fileName # 文件路径对应的值存入该变量中

    def open_endyear(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "All Files (*)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_2.lineEdit_2.setText(fileName)
        self.child_2.endyear = fileName

    def AddTxt(self,txtpath, labels, i): # 用于写入输出权重txt文件的标签
        lines = []
        f = open(txtpath, 'r')  # 打开对应的文件，以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
        for line in f:
            lines.append(line) # 将文件中的数据逐行放到lines变量中
        f.close() # 关闭文件
        lines.insert(i, ' '.join(labels) + '\n') # 将标题放到lines的最前面并换行
        s = ''.join(lines) # 将该数组存入该变量中，并变为str型的，方便写入
        f = open(txtpath, 'w') # 打开该文件，以重写的方式
        f.write(s) # 写入结果
        f.close() # 关闭文件
        del lines[:] # 删除该变量释放内存

    def WeightCal(self):  # 这些设置的参数都需要接收到窗口中用户赋予的值
        start = time.clock()  # 开始计时
        savepath = os.path.dirname(self.child_2.lineEdit.text()) # 将传入路径设置为默认保存路径，该函数可以返回路径（去掉文件名）
        os.chdir(savepath)  # 设置环境变量，这样后面调用该文件夹里的文件时就可以写相对路径了
        StartYear = self.child_2.startyear
        EndYear = self.child_2.endyear
        Constraint = ''

        labels = [] # 该数列放标签
        paths = [] # 该数列放路径
        for i in range(100):
            try:
                labels.append(self.child_2.tableWidget.item(i, 0).text()) # 通过该循环放入第一列的值，当值为空时会报错，用pass跳出
            except:
                pass
        print(labels)

        for i in range(100):
            try:
                paths.append(self.child_2.tableWidget.item(i, 1).text())
            except:
                pass
        print(paths)

        if len(paths) < 1: # 如果路径小于1
            print('输入数据过少，请增加数据')
        groups = int(self.child_2.lineEdit_3.text())
        Step = int(self.child_2.lineEdit_6.text())
        npts1 = len(paths) + 2  # 每组权重包含npts1个数值，输入的len个加上邻域和继承性
        WindowSize = int(self.child_2.lineEdit_8.text())
        DisturbConst = float(self.child_2.lineEdit_7.text())

        # ----------------------------------------------------------------------------------------------
        urban_old = LoadData(StartYear) # 读进开始年份，转换为数组
        urban_new = LoadData(EndYear)
        sz = np.shape(urban_old) # 返回该数据的行列数
        nRows, nCols = sz[0], sz[1]  # 0是数据的列数，1是数据的行数
        urban_old = np.array(urban_old).reshape(-1) # 降维为1维
        try:
            for label in labels:
                i = labels.index(label)
                globals()[label] = LoadData(paths[i]).reshape(-1)  # 这个for循环是以用户输入的label为变量名读取栅格数据
        except: # 当labels为空时跳出循环
            pass

        urban_FID = int(self.child_2.urban_FID)
        Types = self.child_2.Types
        TypeFID = self.child_2.TypeFID
        TypeResistance = self.child_2.TypeResistance
        CellCountForAdd = np.sum(urban_new == urban_FID) - np.sum(urban_old == urban_FID)  # 新增加的城市像元个数
        LoopNumber = CellCountForAdd // Step  # 计算循环次数

        Pk = np.zeros([nRows, nCols]).reshape(-1) # 定义一个和输入数据行列数量相同的数组，并转换为1维
        Vk = 1 + (-np.log(np.random.rand(nRows, nCols))) ** DisturbConst  # 定义存放随机干扰系数的数组，并存入随机干扰系数
        Vk = Vk.reshape(-1)

        OverAccury = np.zeros([groups, npts1 + 2])  # 定义数组存储权重和模拟精度参数,+2是为了存放精度参数
        LUCCNoNan_index = np.where(~np.isnan(urban_old))  # 非nan值的索引，即去除背景值，返回非背景值的索引
        LUCCNan_index = np.where(np.isnan(urban_old)) # 返回背景值的索引
        S_labels = ["S_{0}_A".format(label) for label in labels] # 根据输入的label名字重新定义一组数组的名字
        for S_label in S_labels:
            globals()[S_label] = np.zeros([nRows, nCols]).reshape(-1) # 以这些值命名新的数组，用于存放原图层非城市部分与权重相乘的结果
        # ---------------------------开始执行循环，用于得到模拟权重--------------------------------------------------
        Monte_CarLo_Weight1 = Monte_Carlo(groups, npts1)  # 生成蒙特卡罗权重矩阵
        print("开始计算邻域")
        start2 = time.clock()  # 开始计时
        NeighborEffect = np.zeros([nRows, nCols])  # 定义邻域影像（二维数组）
        LUCCNoUrban_urban_old = np.where((urban_old != urban_FID) & (urban_old != 0)) # 返回非城市非背景位置对应的索引
        AffectedCells = np.array(LUCCNoUrban_urban_old).reshape(-1) # 降维
        NeighborEffect = GetNeighborEffect(StartYear, AffectedCells, WindowSize,urban_FID) # 生成邻域图层
        LABELS = ["label{0}".format(labels.index(label)) for label in labels]  # 新建一个列表，其元素是后面权重的变量名
        end2 = time.clock() - start2
        print("计算邻域用时", start2, "s")

        for m in range(groups):  # 循环groups次
            start1 = time.clock()
            urban_old[LUCCNan_index] = 0
            LUCCNoUrban_urban_old = np.where((urban_old != urban_FID) & (urban_old != 0))  # 取非城市栅格索引
            # 将第m组权重分配给各影响因子
            Weight = Monte_CarLo_Weight1[m, :] # 存入该组的权重
            weight_index = 0
            for LABEL in LABELS:  # 此循环是用来根据用户输入的数据来赋值权重给变量
                globals()[LABEL] = Weight[weight_index] # 该组权重放入该全局变量中
                weight_index += 1
            for label in labels:
                i = labels.index(label) # labels数列中的label放入i中
                globals()[S_labels[i]][LUCCNoUrban_urban_old] = globals()[label][LUCCNoUrban_urban_old] * globals()[LABELS[i]] # 各个图层乘以权重求和结果
                # label图层的非城市地方索引 = 该图层非城市地方的值 * 权重

            urban_Copy = np.array(urban_old)  # 设置一个LUCC数据的拷贝，用来存储模拟结果
            urban_new = LoadData(EndYear)  # 修改 读入结束年份的数据
            refdata = urban_new.reshape(-1) # 降维


            for a in range(1, LoopNumber + 2):
                LUCCNoURBAN2 = np.where((urban_Copy != urban_FID) & (urban_Copy != 0))
                # 调入邻域计算函数计算第i次循环下的邻域影响
                N_Weight = Weight[-2] # 邻域的权重
                Nk_U = NeighborEffect * N_Weight # 邻域图层 * 权重
                Nk_U = np.array(Nk_U).reshape(-1) # 降维

                for Type in Types:
                    name = "I_{0}".format(Type) # 命名不同的用地类型
                    i = Types.index(Type) # 存放该用地类型的索引
                    globals()[name] = np.zeros([nRows, nCols]).reshape(-1) # 降维该用地类型
                    globals()[name][np.where(urban_old == TypeFID[i])] = TypeResistance[i] # 将该用地类型的继承性存入对应的位置，这里一种用地类型对应一个图层，图层中只有该用地类型对应的继承性，无其他值

                I_Weight = Weight[-1] # 继承性权重
                I_Type = np.zeros([nRows, nCols]).reshape(-1)
                for Type in Types: # 该循环将所有用地类型加到一个图层
                    name = "I_{0}".format(Type)
                    I_Type += globals()[name]

                Ik = I_Type * I_Weight  # 继承性乘以权重

                Pk = np.zeros([nRows, nCols]).reshape(-1)
                S_LABELS_A = np.zeros([nRows, nCols]).reshape(-1)
                for S_label in S_labels: # 所有图层乘以权重和的结果图层求和
                    S_LABELS_A[LUCCNoURBAN2] += globals()[S_label][LUCCNoURBAN2]

                Pk[LUCCNoURBAN2] = (S_LABELS_A[LUCCNoURBAN2] - Ik[LUCCNoURBAN2] +
                                             Nk_U[LUCCNoURBAN2]) * Vk[LUCCNoURBAN2]

                if Constraint != "":
                    Pk[LUCCNoURBAN2] = Pk[LUCCNoURBAN2] * constraint[LUCCNoURBAN2]

                PkSort_R_Index = np.argsort(-Pk)  # 降序索引

                if a < LoopNumber + 1: # 每次循环存入一个步长
                    # print(a,Step,LoopNumber)
                    # print(np.size(np.where(urban_Copy == urban_FID)))
                    urban_Copy[PkSort_R_Index[0:Step]] = urban_FID  # 提取概率最高的赋值为城市
                    # print(np.size(np.where(urban_Copy == urban_FID)))
                else: # 最后一次存入余数
                    # print(a,LoopNumber + 1, (CellCountForAdd % Step))
                    urban_Copy[PkSort_R_Index[0:(CellCountForAdd % Step)]] = urban_FID
                    # print(np.size(np.where(urban_Copy == urban_FID)))

            end1 = time.clock() - start1
            print("模拟到第", m, "组,该组用时", end1, "s")


            # 将土地利用图变为1-2二值图，用于精度评估，这部分注释可以看Validation窗体
            LUCCNoUrban_Copy_Index = np.where((urban_Copy != urban_FID) & (urban_Copy != urban_FID))
            urban_Copy[LUCCNoUrban_Copy_Index] = 1
            LUCCUrban_Copy_Index = np.where(urban_Copy == urban_FID)
            urban_Copy[LUCCUrban_Copy_Index] = 2

            refdata_NAN_index = np.where(np.isnan(refdata))
            refdata[refdata_NAN_index] = 0
            LUCCNoUrban_refdata_Index = np.where((refdata != urban_FID) & (refdata != 0))
            refdata[LUCCNoUrban_refdata_Index] = 1
            LUCCUrban_refdata_Index = np.where(refdata == urban_FID)
            refdata[LUCCUrban_refdata_Index] = 2

            # 打开参考图层，计算kappa系数，并把结果保存到文件中，比较各自模拟的结果
            result = 10 * refdata + urban_Copy.reshape(-1)
            Acc_22 = np.size(np.where(result == 22))
            Acc_11 = np.size(np.where(result == 11))
            Acc_21 = np.size(np.where(result == 21))
            Acc_12 = np.size(np.where(result == 12))

            for u in range(npts1):
                OverAccury[m][u] = Weight[u] # 将前面npts个权重先放入变量中

            TotalNum = Acc_22 + Acc_11 + Acc_21 + Acc_12
            OverAccury[m][-2] = float(Acc_22 + Acc_11) / TotalNum # 倒数第二个数放入总体精度
            OverAccury[m][-1] = (float( # 最后一个数放入kappa
                float(TotalNum) * (Acc_22 + Acc_11) - (float(Acc_21 + Acc_11) * (Acc_12 + Acc_11) +
                                                       float(Acc_21 + Acc_22) * (Acc_12 + Acc_22)))) / (
                                            TotalNum * float(TotalNum) - (float(Acc_21 + Acc_11) * (Acc_12 + Acc_11) +
                                                                          float(Acc_21 + Acc_22) * (Acc_12 + Acc_22)))
            #         print(Acc_12 + Acc_21 )

           #  PkSort_R_Index = []
           # print('PkSort_R_Index 是'.format(PkSort_R_Index))

        maxval = np.max(OverAccury[:, -1])  # 读OverAccury最后一列的最大值，即最大kappa系数
        row_index = np.where(OverAccury == maxval)[0]  # 读取最大kappa系数所在的行的索引值，用以下句调用
        Weight_Serial1 = OverAccury[row_index]  # kappa系数最大值的权重

        labels.append('NeighborhoodEffect')
        labels.append('Inheritance')
        labels.append('OverallAccuracy')
        labels.append('Kappa')
        txt1 = "Weight_kappa_max.txt"
        f = open(txt1, 'w+')
        np.savetxt(txt1, Weight_Serial1, fmt='%.03f', delimiter=' ')  # 写入txt文档
        self.AddTxt(txt1, labels, 0) # 调用该函数写入标题
        f.close()

        txt = "Weight.txt"
        f = open(txt, 'w+')
        np.savetxt(txt, OverAccury, fmt='%.03f')
        self.AddTxt(txt, labels, 0)
        f.close()

        #for r in range(groups):
           # list_new = [str(x) for x in list(OverAccury[r])]
           # f.write(','.join(list_new) + '\n')
           # print(OverAccury[r])

        elapsed = (time.clock() - start)  # 结束时间
        print("权重生成用时：", elapsed, "s")

        # self.input_callback(groups,DisturbConst)

        print("All the results were saved in the {0} file under {1} directory.  The result with the highest Kappa index was saved in the {2} file under the same directory.".format("weight.txt",savepath,"weight_kappa_max.txt"))
        self.child_2.textBrowser.append("All the results were saved in the {0} file under {1} directory.  The result with the highest Kappa index was saved in the {2} file under the same directory.".format("weight.txt",savepath,"weight_kappa_max.txt"))
        # 在该控件上打印结果
        # self.child_2.input_callback(Step,WindowSize,DisturbConst)
