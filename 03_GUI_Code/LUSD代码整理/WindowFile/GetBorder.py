from PyQt5.QtWidgets import QFileDialog,QDialog,QMessageBox

import skimage
from skimage.external import tifffile as tiff
from skimage import morphology as sm

from GUIFile.GetBorder_GUI import *
from ScriptFile.WriteTiff import *

class childWindow_7(QDialog, Ui_Dialog_7): # 计算未来面积
    def __init__(self, input_callback=None, parent=None):
        super(childWindow_7, self).__init__(parent)
        self.child_7 = Ui_Dialog_7()
        self.child_7.setupUi(self)
        self.child_7.retranslateUi(self)
        # self.input_callback = input_callback
        self.child_7.pushButton.clicked.connect(self.Open_Simulation)
        self.child_7.pushButton_2.clicked.connect(self.Open_Result)
        self.child_7.pushButton_3.clicked.connect(self.start)
        self.child_7.pushButton_4.clicked.connect(self.closeWindow)

    def Open_Simulation(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read TIFF file", "D:\panxi\Desktop\yanjidata\data",
                                                         "TIFF Files(*.tif)")
        self.child_7.lineEdit.setText(fileName)

    def Open_Result(self):
        # fileName = QFileDialog.getExistingDirectory(self, "Read TIFF file", "C:/Users")
        path, datatype = QFileDialog.getSaveFileName(self,
                                                     r'创建tiff并保存',
                                                     r'D:\panxi\Desktop\yanjidata\data',
                                                     r'TiffFiles(*.tif)')
        # 设置文件扩展名过滤,注意用双分号间隔
        self.child_7.lineEdit_3.setText(path)

    def closeWindow(self):
        self.destroy()

    def start(self):
        file = self.child_7.lineEdit.text()
        urbanFID = int(self.child_7.lineEdit_2.text())
        result_path = self.child_7.lineEdit_3.text()
        self.UGBs(file, urbanFID,result_path)

    def SaveTiff(self,file, raster, path):
        lucc = gdal.Open(file)
        im_width = lucc.RasterXSize
        im_height = lucc.RasterYSize
        im_bands = lucc.RasterCount
        im_geotrans = lucc.GetGeoTransform()
        im_proj = lucc.GetProjection()
        WriteTiff(raster, im_width, im_height, im_bands, im_geotrans, im_proj, path)
        QMessageBox.information(self, '!', 'Finish')

    def UGBs(self,file, urbanFID,result_path):
        raster = tiff.imread(file)
        index1 = np.where(raster != urbanFID)
        index2 = np.where(raster == urbanFID)
        raster[index1] = False
        raster[index2] = True

        kernel = sm.octagon(5, 1)
        img_close = sm.closing(raster, kernel)
        img_open = sm.opening(img_close, kernel)
        path = result_path
        self.SaveTiff(file, img_open, path)