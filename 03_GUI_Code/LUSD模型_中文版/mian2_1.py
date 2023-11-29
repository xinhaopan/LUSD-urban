from __future__ import division
import sys
import numpy as np
import gdal
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sklearn.linear_model import LinearRegression
import time
from goto import with_goto
import pandas as pd
import os

from mainWindow_m import *  # 导入创建的GUI类
from area_cal import *
from probability_cal import *
from suit_cal import *
from validation import *
from SetLabel import *
from SetLandUse import *

np.set_printoptions(suppress=True) #关闭科学计数法


@with_goto
def Monte_Carlo(groups, npts):  # 利用蒙特卡洛算法得到权重矩阵
    wei = np.zeros([groups, npts])  # 定义一个groups行，npts列的空矩阵
    for p in range(groups):
        label.begin
        arr = np.random.rand(npts - 1) * (100 + npts - 1)  # 生成均匀分布的随机数，值在[0,100+npts-1]之间
        num = arr.astype(int) + 1  # 将arr数组转换成int形，+1是为了没有0值
        sortarr = np.argsort(num)  # 对num矩阵进行排序，得到从小到大数的索引
        wei[p][0] = num[sortarr[0]]  # sortarr[0]是num最小值的索引，所以这里是返回num数组的最小值
        # 这里是给权重矩阵第p行第1列的数赋值

        for i in range(1, npts - 1):  # 该循环是为了给权重矩阵第i列每个数赋值
            wei[p][i] = num[sortarr[i]] - num[sortarr[i - 1]]  # 按照大小顺序相减，+1是为了没有0值
            wei[p][npts - 1] = 100 - num[sortarr[npts - 2]]  # +1是为了没有0值，(100+npts-1)是为了没有负数
            # 因为蒙特卡罗算法本身就是基于随机数的算法，所以这里可以使用该方式使矩阵值全都大于0
        for i in range(1, npts):
            if wei[p, i] <= 0:
                # print("第" ,p, "组")
                goto.begin
    label.end
    return wei


def GetNeighborEffect(Lucc_filename, AffectedCells, WindowSize):
    LuccData = gdal.Open(Lucc_filename)
    LuccData1 = LoadData(Lucc_filename)
    if LuccData == None:
        print(Lucc_filename + '文件无法打开')
        return
    nRows = LuccData.RasterYSize  # 行数
    nCols = LuccData.RasterXSize  # 列数
    Width = WindowSize // 2
    XStart = 0  # 标记窗口的起始终止位置
    XEnd = 0
    YStart = 0
    YEnd = 0
    NeighborEffect = np.zeros([nRows, nCols])
    elementsNum = np.size(AffectedCells)  # 获取该矩阵的总元素数
    center = WindowSize // 2
    M_Max = 0.0  # 计算邻域空间内所有像元据中心点距离倒数之和

    for i in range(WindowSize):
        for j in range(WindowSize):
            if i * j != center * center:
                M_Max = M_Max + round((1.0 / ((i - center) ** 2 + (j - center) ** 2) ** 0.5), 8)

    for k in range(elementsNum):
        t = AffectedCells[k]  # AffectedCells是非城市栅格的索引
        j = t // nCols  # j是行，i是列
        i = t % nCols

        Value_U = 0.0
        if (j - Width) < 0:  # 如果行小于下界
            XStart = 0
        else:
            XStart = j - Width
        if (j + Width) > (nRows - 1):  # 如果行大于上界
            XEnd = nRows - 1
        else:
            XEnd = j + Width
        if (i - Width) < 0:  # 如果列小于下界
            YStart = 0
        else:
            YStart = i - Width
        if (i + Width) > (nCols - 1):  # 如果列大于上界
            YEnd = nCols - 1
        else:
            YEnd = i + Width

        for m in range(YStart, YEnd + 1):
            for n in range(XStart, XEnd + 1):
                if m != i or n != j:  # 当搜索不为自身
                    if LuccData1[n][m] == 5:
                        PixelEffect = round((1 / (((m - i) ** 2 + (n - j) ** 2) ** 0.5)), 8)  # 当前一个像素对单元的影响
                        Value_U = Value_U + PixelEffect  # 邻域内所有像素对单元影响之和
        Value_U_S = round((100.0 * Value_U // M_Max), 8)  # 标准化
        NeighborEffect[j][i] = Value_U_S
    return NeighborEffect


def LoadData(filename):
    file = gdal.Open(filename)
    if file == None:
        print(filename + " can't be opened!")
        return
    nb = file.RasterCount

    for i in range(1, nb + 1):
        band = file.GetRasterBand(i)
        background = band.GetNoDataValue()
        data = band.ReadAsArray()
        data = data.astype(np.float32)
        index = np.where(data == background)
        data[index] = 0
    return data


def WriteTiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, path):
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape
        # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, im_width, im_height, im_bands, datatype)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('LUSD-urban')
        self.areaCal = childWindow(self)
        self.areaCal.setWindowTitle('Area Calculation')
        self.suitCal = childWindow_2(self)
        self.suitCal.setWindowTitle('Suitability Calculation')
        self.probCal = childWindow_3(self)
        self.probCal.setWindowTitle('Probability Calculation')
        self.valid = childWindow_4(self)
        self.valid.setWindowTitle('Precision Validation')
        self.setLabel = childWindow_5(self)
        self.valid.setWindowTitle('Set Label')
        self.setLanduse = childWindow_6(self)
        self.valid.setWindowTitle('Set Land Use')
        self.actionOpen.triggered.connect(self.open_function)
        self.actionOpen_2.triggered.connect(self.open_function)
        self.actionWhole.triggered.connect(self.pushbutton_showimage)
        self.actionClear.triggered.connect(self.close)
        self.actionUser_Guide.triggered.connect(self.open_Guide)

        self.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.image_item = QGraphicsPixmapItem()
        self.image_item.setFlag(QGraphicsItem.ItemIsMovable)
        size = self.image_item.pixmap().size()
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 调整图片在中间
        self.image_item.setPos(-size.width() / 2, -size.height() / 2)
        self.zoomscale = 1
        self.actionZoomIn.triggered.connect(self.on_zoomin_clicked)
        self.actionZoomOut.triggered.connect(self.on_zoomout_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def open_Guide(self):
        f = open('D:\Mr.Pan\Work\FutureLandUseSim_v2PythonCode\Guide.pdf', 'r')

    def open_function(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read LULC file", "C:/Users/Keren/Desktop/flus/data",
                                                         "TIF Files(*.tif)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.listWidget.addItem(fileName)

    def pushbutton_showimage(self):
        self.scene.clear()
        self.graphicsView.setScene(self.scene)
        try:
            fileName = self.listWidget.currentItem().text()
        except:
            error1 = QMessageBox.critical(self, "Input Error", "Select image to be shown.",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            print(error1)
            return
        else:
            print('Image shows properly')
        dataset = gdal.Open(fileName)
        image_width = dataset.RasterXSize  # 栅格矩阵的列数
        image_height = dataset.RasterYSize  # 栅格矩阵的行数
        im_data = dataset.ReadAsArray(0, 0, image_width, image_height)
        print(im_data.dtype.name)
        im_show = np.array([im_data])
        if im_data.dtype.name == 'uint8':
            im_max = np.max(im_show)
            im_min = np.min(im_show)
            print(im_max)
            print(im_min)
            QIm = QImage(im_show.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                         image_width * 1,
                         QImage.Format_Indexed8)
            for i in range(im_min, im_max + 1, 1):
                value = qRgb(np.random.randint(1, 255), np.random.randint(1, 255), np.random.randint(1, 255))
                QIm.setColor(i, value)
        else:
            im_show = np.array(im_data, dtype=np.uint8)
            QIm = QImage(im_show.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                         image_width * 1,
                         QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(QIm).scaled(self.graphicsView.width(), self.graphicsView.height())
        self.image_item = QGraphicsPixmapItem(pix)
        self.scene.addItem(self.image_item)
        self.image_item.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.image_item)
        self.graphicsView.setScene(self.scene)
    @pyqtSlot()
    def on_zoomin_clicked(self):
        self.zoomscale = self.zoomscale + 0.05
        self.image_item.setScale(self.zoomscale)

    @pyqtSlot()
    def on_zoomout_clicked(self):
        self.zoomscale = self.zoomscale - 0.05
        self.image_item.setScale(self.zoomscale)

    def wheelEvent(self, event):
        '''滚轮事件'''
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.graphicsView.scale(zoomFactor, zoomFactor)

class childWindow(QDialog, Ui_Dialog):   # 计算方程
    def __init__(self, input_callback=None, parent=None):
        super(childWindow, self).__init__(parent)
        self.child = Ui_Dialog()
        self.child.setupUi(self)
        self.child.retranslateUi(self)
        self.child.pushButton.clicked.connect(self.open_calexcel)
        self.child.pushButton_2.clicked.connect(self.open_prexcel)
        self.child.pushButton_5.clicked.connect(self.AreaCal)
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

    def CityCounts(self,calculation, prediction, sheet1, sheet2):
        df = pd.read_excel(calculation, sheet1)
        Y = np.array(df.Y)
        X = df.drop(['Y'], axis=1)
        model = LinearRegression()
        model.fit(X, Y.T)
        para = [pa for pa in model.coef_]
        para.insert(0, model.intercept_)
        r2 = model.score(X, Y.T)

        print("R2:{0}".format(r2))
        print("interception:{0}".format(para[0]))
        print("coefficient:{0}".format(para[1:]))
        self.child.textBrowser.append("R2:{0}".format(r2))
        self.child.textBrowser.append("interception:{0}".format(para[0]))
        self.child.textBrowser.append("coefficient:{0}".format(para[1:]))

        df2 = pd.read_excel(prediction, sheet1)
        row = df2.shape[0]
        df2.insert(0, 'cone', [1] * row)
        citycount = []
        for i in range(row):
            array = np.array(df2.iloc[i])
            CityCount = np.dot(array, para)
            citycount.append(CityCount)
        return citycount


    def AreaCal(self):
            calculation = self.child.lineEdit.text()
            prediction = self.child.lineEdit_2.text()

            calculation = self.child.lineEdit.text()
            prediction = self.child.lineEdit_2.text()
            sheet1 = 'Sheet1'
            sheet2 = 'Sheet1'
            CityCount = [int(i) for i in self.CityCounts(calculation, prediction, sheet1, sheet2)]
            print(CityCount)
            self.child.textBrowser.append("Predicted urban land area : {}".format(CityCount))
            return CityCount
    # CityCount = AreaCal()

class childWindow_2(QDialog, Ui_Dialog_2):  #计算权重
    def __init__(self, input_callback=None, parent=None):
        super(childWindow_2, self).__init__(parent)
        self.child_2 = Ui_Dialog_2()
        self.child_2.setupUi(self)
        self.child_2.retranslateUi(self)
        self.child_2.pushButton.clicked.connect(self.open_startyear)
        self.child_2.pushButton_2.clicked.connect(self.open_endyear)
        self.child_2.pushButton_8.clicked.connect(self.SuitabilityCal)
        # 回调函数
        self.child_2.input_callback = input_callback

        self.childui_6 = childWindow_6(self.input_callback, self)
        self.child_2.pushButton_5.clicked.connect(lambda:self.childui_6.show())
        self.child_2.input_callback = input_callback

        self.child_2.tableWidget.doubleClicked.connect(self.importpath)

        self.child_2.urban_FID = 0
        self.child_2.Types = []
        self.child_2.TypeFID = []
        self.child_2.TypeResistanc = []


        self.child_2.lineEdit.setText("D:\panxi\Desktop\yanjidata\data\lulc2000.tif")
        self.child_2.lineEdit_2.setText("D:\panxi\Desktop\yanjidata\data\lulc2010.tif")

        self.child_2.item00 = QTableWidgetItem("1")  # 我们要求它可以修改，所以使用默认的状态即可
        self.child_2.item01 = QTableWidgetItem("D:\panxi\Desktop\yanjidata\data\dem.tif")
        self.child_2.item02 = QTableWidgetItem("20")
        self.child_2.item10 = QTableWidgetItem("2")
        self.child_2.item11 = QTableWidgetItem("D:\panxi\Desktop\yanjidata\data\city.tif")
        self.child_2.item12 = QTableWidgetItem("50")

        self.child_2.tableWidget.setItem(0, 0, self.child_2.item00)
        self.child_2.tableWidget.setItem(0, 1, self.child_2.item01)
        self.child_2.tableWidget.setItem(0, 2, self.child_2.item02)
        self.child_2.tableWidget.setItem(1, 0, self.child_2.item10)
        self.child_2.tableWidget.setItem(1, 1, self.child_2.item11)
        self.child_2.tableWidget.setItem(1, 2, self.child_2.item12)

        self.child_2.lineEdit_3.setText("5")
        self.child_2.lineEdit_6.setText("100")
        self.child_2.lineEdit_7.setText("0.1")
        self.child_2.lineEdit_8.setText("5")


    def input_callback(self, *args):
        print(args[:])
        self.child_2.urban_FID,self.child_2.Types,self.child_2.TypeFID,self.child_2.TypeResistance = args[:]


    def importpath(self):
        column = self.child_2.tableWidget.currentIndex().column()
        row = self.child_2.tableWidget.currentIndex().row()
        print(column,row)
        if column == 1:
            fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                             "All Files (*)")
            importpath = QTableWidgetItem(fileName)
            self.child_2.tableWidget.setItem(row, column, importpath)

    def open_startyear(self):
        # fileName = QFileDialog.getExistingDirectory(self, "Read TIFF file", "C:/Users")
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "All Files (*)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_2.lineEdit.setText(fileName)
        self.child_2.startyear = fileName

    def open_endyear(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "All Files (*)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_2.lineEdit_2.setText(fileName)
        self.child_2.endyear = fileName

    def SuitabilityCal(self):  # 这些设置的参数都需要接收到窗口中用户赋予的值
        start = time.clock()  # 开始计时
        # savepath = os.path.dirname(self.child_2.lineEdit.text())
        # os.chdir(savepath)  # 设置环境变量，这样后面调用该文件夹里的文件时就可以写相对路径了
        # StartYear = self.child_2.startyear
        # EndYear = self.child_2.endyear
        os.chdir('D:\\panxi\\Desktop\\yanjidata\\data')  # 设置环境变量，这样后面调用该文件夹里的文件时就可以写相对路径了
        StartYear = "lulc2000.tif"
        EndYear = "lulc2010.tif"

        Constraint = ''

        labels = []
        paths = []
        number = []
        for i in range(16):
            try:
                labels.append(self.child_2.tableWidget.item(i, 2).text())
            except:
                pass
        print(labels)

        for i in range(16):
            try:
                paths.append(self.child_2.tableWidget.item(i, 1).text())
            except:
                pass
        print(paths)

        for i in range(16):
            try:
                number.append(self.child_2.tableWidget.item(i, 0).text())
            except:
                pass
        print(number)

        if len(paths) < 1:
            print('输入数据过少，请增加数据')
        groups = int(self.child_2.lineEdit_3.text())
        Step = int(self.child_2.lineEdit_6.text())
        npts1 = len(paths) + 2  # 每组权重包含npts1个数值，为可选数据数加2
        WindowSize = int(self.child_2.lineEdit_8.text())
        DisturbConst = float(self.child_2.lineEdit_7.text())

        # ----------------------------------------------------------------------------------------------
        urban_old = LoadData(StartYear)
        urban_new = LoadData(EndYear)
        sz = np.shape(urban_old)
        nRows, nCols = sz[0], sz[1]  # 数据的列数，#数据的行数
        urban_old = np.array(urban_old).reshape(-1)
        for label in labels:
            i = labels.index(label)
            globals()[label] = LoadData(paths[i]).reshape(-1)  # 这个for循环是以用户输入的label为变量名读取栅格数据

        urban_FID = int(self.child_2.urban_FID)
        Types = self.child_2.Types
        TypeFID = self.child_2.TypeFID
        TypeResistance = self.child_2.TypeResistance
        CellCountForAdd = np.sum(urban_new == urban_FID) - np.sum(urban_old == urban_FID)  # 新增加的城市像元个数
        LoopNumber = CellCountForAdd // Step  # 计算循环次数

        Pk = np.zeros([nRows, nCols]).reshape(-1)
        Vk = 1 + (-np.log(np.random.rand(nRows, nCols))) ** DisturbConst  # 随机干扰系数
        Vk = Vk.reshape(-1)

        LUCC_OLD = gdal.Open(StartYear)
        im_width = LUCC_OLD.RasterXSize  # 栅格矩阵的列数
        im_height = LUCC_OLD.RasterYSize  # 栅格矩阵的行数
        im_bands = LUCC_OLD.RasterCount  # 波段数
        im_geotrans = LUCC_OLD.GetGeoTransform()  # 获取仿射矩阵信息
        im_proj = LUCC_OLD.GetProjection()  # 获取投影信息

        Vk_11 = np.array(Vk).reshape([nRows, nCols])
        WriteTiff(Vk_11, im_width, im_height, im_bands, im_geotrans, im_proj, "Vk_12.tif")


        OverAccury = np.zeros([groups, npts1 + 2])  # 定义数组存储权重和模拟精度参数,+2是为了存放精度参数
        LUCCNoNan_index = np.where(~np.isnan(urban_old))  # 非nan值的索引，即去除背景值
        LUCCNan_index = np.where(np.isnan(urban_old))
        S_labels = ["S_{0}_A".format(label) for label in labels]
        for S_label in S_labels:
            globals()[S_label] = np.zeros([nRows, nCols]).reshape(-1)
        # ---------------------------开始执行循环，用于得到模拟权重--------------------------------------------------
        Monte_CarLo_Weight1 = Monte_Carlo(groups, npts1)  # 生成蒙特卡罗权重矩阵
        print("开始计算邻域")
        start2 = time.clock()  # 开始计时
        NeighborEffect = np.zeros([nRows, nCols])  # 定义邻域影像（二维数组）
        LUCCNoUrban_urban_old = np.where((urban_old != urban_FID) & (urban_old != 0))
        AffectedCells = np.array(LUCCNoUrban_urban_old).reshape(-1)
        NeighborEffect = GetNeighborEffect(StartYear, AffectedCells, WindowSize)
        LABELS = ["label{0}".format(labels.index(label)) for label in labels]  # 新建一个列表，其元素是后面权重的变量名
        end2 = time.clock() - start2
        print("计算邻域用时", start2, "s")

        for m in range(groups):  # 循环groups次
            start1 = time.clock()
            urban_old[LUCCNan_index] = 0
            LUCCNoUrban_urban_old = np.where((urban_old != urban_FID) & (urban_old != 0))  # 取非城市栅格索引
            # 将第m组权重分配给各影响因子
            Weight = Monte_CarLo_Weight1[m, :]
            weight_index = 0
            for LABEL in LABELS:  # 此循环是用来根据用户输入的数据来赋值权重给变量
                globals()[LABEL] = Weight[weight_index]
                weight_index += 1
            for label in labels:
                i = labels.index(label)
                globals()[S_labels[i]][LUCCNoUrban_urban_old] = globals()[label][LUCCNoUrban_urban_old] * globals()[LABELS[i]] # 各个图层乘以权重求和结果

            urban_Copy = np.array(urban_old)  # 设置一个LUCC数据的拷贝，用来存储模拟结果
            urban_new = LoadData(EndYear)  # 修改
            refdata = urban_new.reshape(-1)


            for a in range(1, LoopNumber + 2):
                LUCCNoURBAN2 = np.where((urban_Copy != urban_FID) & (urban_Copy != 0))
                # 调入邻域计算函数计算第i次循环下的邻域影响
                N_Weight = Weight[-2]
                Nk_U = NeighborEffect * N_Weight
                Nk_U = np.array(Nk_U).reshape(-1)

                for Type in Types:
                    name = "I_{0}".format(Type)
                    i = Types.index(Type)
                    globals()[name] = np.zeros([nRows, nCols]).reshape(-1)
                    globals()[name][np.where(urban_old == TypeFID[i])] = TypeResistance[i]

                I_Weight = Weight[-1]
                I_Type = np.zeros([nRows, nCols]).reshape(-1)
                for Type in Types:
                    name = "I_{0}".format(Type)
                    I_Type += globals()[name]

                Ik = I_Type * I_Weight  # 计算非城镇像元的转换概率

                Pk = np.zeros([nRows, nCols]).reshape(-1)
                S_LABELS_A = np.zeros([nRows, nCols]).reshape(-1)
                for S_label in S_labels:
                    S_LABELS_A[LUCCNoURBAN2] += globals()[S_label][LUCCNoURBAN2]

                # Pk[LUCCNoURBAN2] = (S_LABELS_A[LUCCNoURBAN2] - Ik[LUCCNoURBAN2] + Nk_U[LUCCNoURBAN2]) * Vk[LUCCNoURBAN2]

                Pk_1 = np.zeros([nRows, nCols]).reshape(-1)
                Pk_2 = np.zeros([nRows, nCols]).reshape(-1)
                Pk_1[LUCCNoURBAN2] = S_LABELS_A[LUCCNoURBAN2] - Ik[LUCCNoURBAN2]
                Pk_2[LUCCNoURBAN2] = Pk_1[LUCCNoURBAN2] + Nk_U[LUCCNoURBAN2]
                Pk[LUCCNoURBAN2] = Pk_2[LUCCNoURBAN2] * Vk[LUCCNoURBAN2]

                if Constraint != "":
                    Pk[LUCCNoURBAN2] = Pk[LUCCNoURBAN2] * constraint[LUCCNoURBAN2]


                LUCC_OLD = gdal.Open(StartYear)
                im_width = LUCC_OLD.RasterXSize  # 栅格矩阵的列数
                im_height = LUCC_OLD.RasterYSize  # 栅格矩阵的行数
                im_bands = LUCC_OLD.RasterCount  # 波段数
                im_geotrans = LUCC_OLD.GetGeoTransform()  # 获取仿射矩阵信息
                im_proj = LUCC_OLD.GetProjection()  # 获取投影信息

                PK = np.array(Pk).reshape([nRows, nCols])
                WriteTiff(PK, im_width, im_height, im_bands, im_geotrans, im_proj, "pk{0}.tif".format(m))

                S_LABELS_A = np.array(S_LABELS_A).reshape([nRows, nCols])
                WriteTiff(S_LABELS_A, im_width, im_height, im_bands, im_geotrans, im_proj, "S_LABELS_A{0}.tif".format(m))

                Ik = np.array(Ik).reshape([nRows, nCols])
                WriteTiff(Ik, im_width, im_height, im_bands, im_geotrans, im_proj, "Ik{0}.tif".format(m))

                Nk_U = np.array(Nk_U).reshape([nRows, nCols])
                WriteTiff(Nk_U, im_width, im_height, im_bands, im_geotrans, im_proj,"Nk_U{0}.tif".format(m))

                Pk_1 = np.array(Pk_1).reshape([nRows, nCols])
                WriteTiff(Pk_1, im_width, im_height, im_bands, im_geotrans, im_proj, "Pk_1{0}.tif".format(m))

                Pk_2 = np.array(Pk_2).reshape([nRows, nCols])
                WriteTiff(Pk_2, im_width, im_height, im_bands, im_geotrans, im_proj, "Pk_2{0}.tif".format(m))
                '''
                Vk = np.array(Vk).reshape([nRows, nCols])
                WriteTiff(Vk, im_width, im_height, im_bands, im_geotrans, im_proj, "Vk{0}.tif".format(m))
                
                print(Vk[LUCCNoURBAN2])
                print('--------------------------')
                print(Pk[LUCCNoURBAN2])
                print('--------------------------')
                print(Pk_1[LUCCNoURBAN2])
                print('--------------------------')
                print(Pk_2[LUCCNoURBAN2])
                print('--------------------------')
                '''


                PkSort_R_Index = np.argsort(-Pk)  # 降序索引
                print(PkSort_R_Index )

                if a < LoopNumber + 1:
                    print(a,Step,LoopNumber)
                    print(np.size(np.where(urban_Copy == urban_FID)))
                    urban_Copy[PkSort_R_Index[0:Step]] = urban_FID  # 提取概率最高的赋值为城市
                    print(np.size(np.where(urban_Copy == urban_FID)))
                else:
                    print(a,LoopNumber + 1, (CellCountForAdd % Step))
                    urban_Copy[PkSort_R_Index[0:(CellCountForAdd % Step)]] = urban_FID
                    print(np.size(np.where(urban_Copy == urban_FID)))

            end1 = time.clock() - start1
            #         print("模拟到第", m, "组,该组用时", end1, "s")

            # 输出每组模拟结果


            result = np.array(urban_Copy).reshape([nRows, nCols])
            WriteTiff(result, im_width, im_height, im_bands, im_geotrans, im_proj, "result{0}.tif".format(m))

            PK_new = np.array(Pk).reshape([nRows, nCols])
            WriteTiff(PK_new, im_width, im_height, im_bands, im_geotrans, im_proj, "pk_new{0}.tif".format(m))
            print("输出{}".format(m))


            # 将土地利用图变为1-2二值图，用于精度评估
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
                OverAccury[m][u] = Weight[u]

            TotalNum = Acc_22 + Acc_11 + Acc_21 + Acc_12
            OverAccury[m][-2] = float(Acc_22 + Acc_11) / TotalNum
            OverAccury[m][-1] = (float(
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

        txt1 = "Weight_kappa_max.txt"
        np.savetxt(txt1, Weight_Serial1.reshape(-1),fmt = '%.019f')

        txt = "Weight.txt"
        f = open(txt, 'w')
        for r in range(groups):
            list_new = [str(x) for x in list(OverAccury[r])]
            f.write(','.join(list_new) + '\n')
            print(OverAccury[r])

        elapsed = (time.clock() - start)  # 结束时间
        print("权重生成用时：", elapsed, "s")

        # self.input_callback(groups,DisturbConst)

        print("权重、精度、kappa已经保存到目录下的Weight.txt文件中，kappa最高的结果保存到该目录下Weight_kappa_max.txt文件中")
        self.child_2.textBrowser.append("Weight、 precision and kappa has been saved in the “weight.txt” file under  directory,  and the highest result of kappa is saved in the “weight_kappa_max.txt” file.")
        # self.child_2.input_callback(Step,WindowSize,DisturbConst)




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

        # 回调子界面2参数
        self.childui_2 = childWindow_2(self.input_callback1, self)
        self.child_3.input_callback = input_callback

        # 回调子界面6
        self.childui_6 = childWindow_6(self.input_callback, self)
        self.child_3.pushButton_8.clicked.connect(lambda: self.childui_6.show())
        self.child_3.input_callback = input_callback

        self.child_3.tableWidget.doubleClicked.connect(self.importpath)

        # self.childui_6 = childWindow_6(self.input_callback, self)

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
        StartYear = self.child_3.lineEdit.text()

        ResultPath = self.child_3.lineEdit_9.text()
        Probability = self.child_3.lineEdit_7.text()
        Constraint = ''  # 这就是那个可选的RestrictedData
        try:
            if len(self.child_3.Constraint) > 0:
                Constraint = self.child_3.Constraint
        except:
            pass

        urban = LoadData(StartYear)

        Step = int(self.child_3.lineEdit_10.text())
        DisturbConst = float(self.child_3.lineEdit_11.text())
        WindowSize = int(self.child_3.lineEdit_12.text())
        CityCount_Last = int(self.child_3.lineEdit_2.text())

        if Step == 0:
            Step = 100

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
        # urban_FID = 5  # 设置城市用地的代码 ，这里是必须有这个urban_FID的，在setlanduse中你得显示出这个让用户输入 ppppppp

        labels = []
        paths = []
        number = []
        suitabilitys = []
        for i in range(16):
            try:
                labels.append(self.child_3.tableWidget.item(i, 2).text())
            except:
                pass
        print(labels)

        for i in range(16):
            try:
                paths.append(self.child_3.tableWidget.item(i, 1).text())
            except:
                pass
        print(paths)

        for i in range(16):
            try:
                number.append(self.child_3.tableWidget.item(i, 0).text())
            except:
                pass
        print(number)

        for i in range(16):
            try:
                suitabilitys.append(self.child_3.tableWidget.item(i, 3).text())
            except:
                pass
        print('--------')
        print(suitabilitys)
        Weight_Serial1 = np.array(suitabilitys, dtype=float)
        CellCountForAdd = CityCount_Last - np.sum(urban == urban_FID)  # CityCount_Last是窗口1的结果

        if len(labels) < 1:
            print('输入数据过少，请增加数据')
        for label in labels:
            i = labels.index(label)
            globals()[label] = LoadData(paths[i]).reshape(-1)  # 这个for循环是以用户输入的label为变量名读取栅格数据

        S_labels = ["S_{0}_A".format(label) for label in labels]
        for S_label in S_labels:
            globals()[S_label] = np.zeros([nRows, nCols]).reshape(-1)
        LoopNumber = CellCountForAdd // Step  # 计算循环次数
        Pk = np.zeros([nRows, nCols]).reshape(-1)

        DisturbConst = 0.01
        Vk = 1 + (-np.log(np.random.rand(nRows, nCols))) ** DisturbConst  # 随机干扰系数
        Vk = Vk.reshape(-1)

        LUCC_OLD = gdal.Open(StartYear)
        im_width = LUCC_OLD.RasterXSize  # 栅格矩阵的列数
        im_height = LUCC_OLD.RasterYSize  # 栅格矩阵的行数
        im_bands = LUCC_OLD.RasterCount  # 波段数
        im_geotrans = LUCC_OLD.GetGeoTransform()  # 获取仿射矩阵信息
        im_proj = LUCC_OLD.GetProjection()  # 获取投影信息

        Vk_11 = np.array(Vk).reshape([nRows, nCols])
        WriteTiff(Vk_11, im_width, im_height, im_bands, im_geotrans, im_proj, "Vk_12.tif")

        weight_index = 0
        LABELS = ["label{0}".format(labels.index(label)) for label in labels]  # 新建一个列表，其元素是后面权重的变量名
        weight_index = 0
        for LABEL in LABELS:  # 此循环是用来根据用户输入的数据来赋值权重给变量
            globals()[LABEL] = Weight_Serial1[weight_index]
            weight_index += 1

        LUCCNan_Index = np.where(np.isnan(urban))
        urban[LUCCNan_Index] = 0
        LUCCNoURBAN = np.where((urban != urban_FID) & (urban != 0))
        for label in labels:
            i = labels.index(label)
            globals()[S_labels[i]][LUCCNoURBAN] = globals()[label][LUCCNoURBAN] * globals()[LABELS[i]]

        urban_Copy = np.array(urban)  # 设置一个LUCC数据的拷贝
        NeighborEffect = np.zeros([nRows, nCols])
        # ----------------------------------循环模拟-------------------------------------
        for num in range(1, LoopNumber + 2):
            LUCCNoURBAN2 = np.where((urban_Copy != urban_FID) & (urban_Copy != 0))
            AffectedCells = np.array(LUCCNoURBAN2).reshape(-1)
            N_Weight = Weight_Serial1[-2]
            NeighborEffect = GetNeighborEffect(StartYear, AffectedCells, WindowSize)
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
                Pk[LUCCNoURBAN2] = Pk[LUCCNoURBAN2] * constraint[LUCCNoURBAN2]

            PkSort_R_Index = np.argsort(-Pk)  # 降序索引

            if num < LoopNumber + 1:
                urban_Copy[PkSort_R_Index[0:Step]] = urban_FID  # 提取概率最高的赋值为城市
            else:
                urban_Copy[PkSort_R_Index[0:(CellCountForAdd % Step)]] = urban_FID

            if num == 1:
                gailv = np.array(Pk).reshape([nRows, nCols])

        # ----------------------------------结果保存-------------------------------------


        urban_Copy = np.array(urban_Copy).reshape([nRows, nCols])
        WriteTiff(urban_Copy, im_width, im_height, im_bands, im_geotrans, im_proj, ResultPath)  # 写入tif文件
        WriteTiff(gailv, im_width, im_height, im_bands, im_geotrans, im_proj, Probability)
        elapsed = (time.clock() - start)
        print("模拟用时:", elapsed, "s")
        print("模拟成功！")
        QMessageBox.information(self, '!', 'Finish')

class childWindow_4(QDialog, Ui_Dialog_4):
    def __init__(self, input_callback=None, parent=None):
        super(childWindow_4, self).__init__(parent)
        self.child_4 = Ui_Dialog_4()
        self.child_4.setupUi(self)
        self.child_4.retranslateUi(self)

        self.child_4.pushButton.clicked.connect(self.true_path)
        self.child_4.pushButton_2.clicked.connect(self.result_path)

    def true_path(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "All Files (*)")
        self.child_4.lineEdit.setText(fileName)

    def result_path(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "All Files (*)")
        self.child_4.lineEdit_2.setText(fileName)

    def cal_kappa(self):
        '''
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
        result = np.zeros([nRows, nCols]).reshape(-1)
        result[LUCCNoNan_index] = 10 * refdata[LUCCNoNan_index] + urban_Copy[LUCCNoNan_index]
        Acc_22 = np.size(np.where(result == 22))
        Acc_11 = np.size(np.where(result == 11))
        Acc_21 = np.size(np.where(result == 21))
        Acc_12 = np.size(np.where(result == 12))

        for u in range(npts1):
            OverAccury[m][u] = Weight[u]

        TotalNum = Acc_22 + Acc_11 + Acc_21 + Acc_12
        OverAccury[m][-2] = float(Acc_22 + Acc_11) / TotalNum
        OverAccury[m][-1] = (float(
            float(TotalNum) * (Acc_22 + Acc_11) - (float(Acc_21 + Acc_11) * (Acc_12 + Acc_11) +
                                                   float(Acc_21 + Acc_22) * (Acc_12 + Acc_22)))) / (
                                    TotalNum * float(TotalNum) - (float(Acc_21 + Acc_11) * (Acc_12 + Acc_11) +
                                                                  float(Acc_21 + Acc_22) * (Acc_12 + Acc_22)))
        #         print(Acc_12 + Acc_21 )

    maxval = np.max(OverAccury[:, -1])  # 读OverAccury最后一列的最大值，即最大kappa系数
    row_index = np.where(OverAccury == maxval)[0]  # 读取最大kappa系数所在的行的索引值，用以下句调用
    Weight_Serial1 = OverAccury[row_index]  # kappa系数最大值的权重
    '''


class childWindow_5(QDialog, Ui_Dialog_5):
    def __init__(self, input_callback=None, parent=None):
        super(childWindow_5, self).__init__(parent)
        self.child_5 = Ui_Dialog_5()
        self.child_5.setupUi(self)
        self.child_5.retranslateUi(self)
        self.child_5.input_callback = input_callback


class childWindow_6(QDialog, Ui_Dialog_6): # 设置继承性和土地利用类型
    # urban_FID_signal = pyqtSignal(int)

    def __init__(self, input_callback=None, parent=None):
        super(childWindow_6, self).__init__(parent)
        self.child_6 = Ui_Dialog_6()
        self.child_6.setupUi(self)
        self.child_6.retranslateUi(self)
        self.child_6.input_callback = input_callback

        self.child_6.pushButton_2.clicked.connect(self.getdata)
        self.child_6.pushButton.clicked.connect(self.close)

        self.child_6.item00 = QTableWidgetItem("5")  # 我们要求它可以修改，所以使用默认的状态即可
        self.child_6.item01 = QTableWidgetItem("urban")
        self.child_6.item02 = QTableWidgetItem("100")
        self.child_6.item10 = QTableWidgetItem("2")
        self.child_6.item11 = QTableWidgetItem("water")
        self.child_6.item12 = QTableWidgetItem("50")

        self.child_6.tableWidget.setItem(0,0,self.child_6.item00)
        self.child_6.tableWidget.setItem(0, 1, self.child_6.item01)
        self.child_6.tableWidget.setItem(0, 2, self.child_6.item02)
        self.child_6.tableWidget.setItem(1, 0, self.child_6.item10)
        self.child_6.tableWidget.setItem(1, 1, self.child_6.item11)
        self.child_6.tableWidget.setItem(1, 2, self.child_6.item12)


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

        city = int(Types.index("urban"))
        urban_FID = TypeFID[city]
        print(urban_FID)
        self.child_6.input_callback(urban_FID,Types,TypeFID,TypeResistance)
        print("input callback finished")
        # self.child_6.destroy()
        # self.urban_FID_signal.emit(urban_FID)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    child = childWindow()
    child_2 = childWindow_2()
    window.actionArea_Calculation.triggered.connect(window.areaCal.show)
    window.actionSuitability_Calculation.triggered.connect(window.suitCal.show)
    window.actionProbability_Calculation.triggered.connect(window.probCal.show)
    window.actionPrecision_Validation.triggered.connect(window.valid.show)
    window.show()
    sys.exit(app.exec_())