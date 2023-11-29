import webbrowser

from GUIFile.mainWindow_GUI import * # 主窗体
from WindowFile.Prediction_area import * # 预测未来城市面积的子窗体
from WindowFile.Calibration import * # 校准模型（计算权重）的子窗体
from WindowFile.Simulation import * # 模拟结果的子窗体
from WindowFile.Validation import * # 计算kappa和总精度的子窗体
from WindowFile.About import * # 显示about的子窗体
from WindowFile.GetBorder import * # 提取边界子窗体

from PyQt5.QtWidgets import QGraphicsPixmapItem,QGraphicsScene,QGraphicsView,QGraphicsItem
from PyQt5.QtGui import QPixmap,QImage,qRgb
from PyQt5.QtCore import pyqtSlot,Qt


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('LUSD')
        self.Prediction_area = childWindow(self)
        self.Prediction_area.setWindowTitle('Area')
        self.Calibration = childWindow_2(self)
        self.Calibration.setWindowTitle('Calibration')
        self.Simulation = childWindow_3(self)
        self.Simulation.setWindowTitle('Simulation')
        self.Validation = childWindow_4(self)
        self.Validation.setWindowTitle('Validation')
        self.SetLanduse = childWindow_5(self)
        self.SetLanduse.setWindowTitle('Set Inheritance')
        self.About = childWindow_6(self)
        self.About.setWindowTitle('About')
        self.Border = childWindow_7(self)
        self.Border.setWindowTitle('Urban growth boundary')

        self.actionOpen.triggered.connect(self.open_function)
        self.actionOpen_2.triggered.connect(self.open_function)
        self.actionWhole.triggered.connect(self.pushbutton_showimage)
        self.actionClear.triggered.connect(self.close)
        self.actionUser_Guide_2.triggered.connect(self.UserGuide)

        # self.graphicsView.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        # self.graphicsView.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        # self.scene = QGraphicsScene()
        # self.graphicsView.setScene(self.scene)
        # self.image_item = QGraphicsPixmapItem()
        # self.image_item.setFlag(QGraphicsItem.ItemIsMovable)
        # size = self.image_item.pixmap().size()
        # self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # # 调整图片在中间
        # self.image_item.setPos(-size.width() / 2, -size.height() / 2)
        # self.zoomscale = 1
        # self.actionZoomIn.triggered.connect(self.on_zoomin_clicked)
        # self.actionZoomOut.triggered.connect(self.on_zoomout_clicked)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)

    def UserGuide(self): # 打开帮助文档
        path = os.path.abspath(os.path.dirname(os.getcwd()))
        os.chdir(path)
        try:
            webbrowser.open('Guide.pdf')
        except:
            print("No User Guide.pdf!")
        return

    def open_function(self): # 打开影像
        fileName, filetype = QFileDialog.getOpenFileName(self, "Read LULC file", "C:/Users/Keren/Desktop/flus/data",
                                                         "TIF Files(*.tif)")
        # 设置文件扩展名过滤,注意用双分号间隔
        self.listWidget.addItem(fileName)

    def pushbutton_showimage(self): # 全屏显示图像
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
