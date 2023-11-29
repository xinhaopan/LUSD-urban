# 计算邻域的代码
from ScriptFile.LoadData import *

def GetNeighborEffect(Lucc_filename, AffectedCells, WindowSize,urban_FID): # 传入开始年份的影像数据，非城市非背景位置对应的索引并进行降维后的，邻域窗口大小,城市像元对应的值
    LuccData = gdal.Open(Lucc_filename)  # 使用gdal打开影像
    LuccData1 = LoadData(Lucc_filename) # 使用该函数加载数据
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
    NeighborEffect = np.zeros([nRows, nCols]) # 声明一个矩阵用来存放结果
    elementsNum = np.size(AffectedCells)  # 获取非城市非背景的总像元数
    center = WindowSize // 2 # 邻域窗口中心
    M_Max = 0.0  # 计算邻域空间内所有像元据中心点距离倒数之和

     # 计算分母
    for i in range(WindowSize): # 计算一个邻域窗口内所有像元据中心点距离倒数之和
        for j in range(WindowSize):
            if i * j != center * center:
                M_Max = M_Max + round((1.0 / ((i - center) ** 2 + (j - center) ** 2) ** 0.5), 8)
    # 计算分子
    for k in range(elementsNum): # 由该像元的索引找到它的实际位置
        t = AffectedCells[k]  # AffectedCells是非城市栅格的索引
        j = t // nCols  # j是行，i是列
        i = t % nCols

        Value_U = 0.0
        # 判断该像元的位置是否超出范围
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
                    if LuccData1[n][m] == urban_FID:
                        PixelEffect = round((1 / (((m - i) ** 2 + (n - j) ** 2) ** 0.5)), 8)  # 当前一个城市像元对该单元的影响
                        Value_U = Value_U + PixelEffect  # 邻域内所有像素对单元影响之和
        Value_U_S = round((100.0 * Value_U // M_Max),8)  #标准化
        NeighborEffect[j][i] = Value_U_S
    return NeighborEffect