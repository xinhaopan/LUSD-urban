import gdal
import numpy as np

def LoadData(filename):
    file = gdal.Open(filename) # 使用gdal打开，目的为了看影像能否正常使用
    if file == None: # 如果无法打开
       print (filename+" can't be opened!")
       return
    nb = file.RasterCount # 波段数量

    for i in range(1,nb+1): # 通过该循环将所有波段的空值都赋予0值
        band = file.GetRasterBand(i) # 第i个波段
        background = band.GetNoDataValue() # 存入该波段中的空值
        data = band.ReadAsArray() # 以矩阵的形式读出
        data=data.astype(np.float32) # 转换为float32位的形式
        index = np.where(data == background) # 存入空值值的索引
        data[index] = 0 # 将数据空值部分赋予0，其他地方不变
    return data