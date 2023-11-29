import gdal
import numpy as np
import os
import pandas as pd
import random
import time
from openpyxl import Workbook


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

def LoadData1(filename):
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
        data[index] = 3
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


# 计算蒙特卡罗邻域
def GetNeighborEffect(startyear_filename, WindowSize):
    raster = gdal.Open(startyear_filename)
    urbanData1 = LoadData(startyear_filename)
    if raster == None:
        print(startyear_filename + '文件无法打开')

    nRows = raster.RasterYSize  # 行数
    nCols = raster.RasterXSize  # 列数
    Width = WindowSize // 2
    center = WindowSize // 2

    NeighborEffect = np.zeros([nRows, nCols])  # 创建图层用于存储邻域影响的值

    AffectedCellsWhere = np.argwhere(urbanData1 == 1)  # 存入所有城市像元的位置

    M_Max = 0.0  # 计算邻域空间内所有像元据中心点距离倒数之和
    for i in range(WindowSize):
        for j in range(WindowSize):
            if i * j != center * center:
                M_Max = M_Max + round((1.0 / ((i - center) ** 2 + (j - center) ** 2) ** 0.5), 8)

    # 逐个模拟非城市像元对邻域内城市像元的影响，结果相加
    k = 0
    for j, i in AffectedCellsWhere:  # j是行X，i是列Y
        k += 1
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

        # 循环逐个计算某城市像元对其邻域内非城市像元的影响
        # m、n是邻域内的非城市像元，i、j是中心的城市像元
        for m in range(YStart, int(YEnd) + 1): # 列
            for n in range(XStart, int(XEnd) + 1): # 行
                if m != i or n != j:  # 当搜索不为自身
                    if urbanData1[n][m] != 1:  # 城市像元为1，这里找非城市像元
                        # 计算该城市像元对邻域内非城市像元的影响
                        PixelEffect = round((1 / ((m - i) ** 2 + (n - j) ** 2) ** 0.5), 8)  # 当前一个像素对单元的影响
                        NeighborEffect[n][m] += PixelEffect  # 邻域内所有像素对单元影响之和

    NeighborEffect = 100 * NeighborEffect // M_Max  # 标准化

    return NeighborEffect  # 返回空间邻域影响图层


# 处理土地覆盖图层
def get_lulc_value_arr(lucFilePath):
    lulc_arr = LoadData(lucFilePath)
    inheritancePath = path + r"\lulc\inheritance.xlsx"
    inheritance_df = pd.read_excel(inheritancePath)  # 导入土地覆盖赋继承性值的表格

    raster = gdal.Open(lucFilePath)
    nRows = raster.RasterYSize  # 行数
    nCols = raster.RasterXSize  # 列数
    lulc_value_arr = np.zeros([nRows, nCols])
    for i in range(inheritance_df.shape[0]):  # 逐行读入赋值表，给相应的地类复制
        lulc_value_arr[np.where(lulc_arr == inheritance_df.iloc[i, 0])] = inheritance_df.iloc[i, 2]
    return lulc_value_arr  # 返回赋值后的图层


# 获取某目录下所有tif文件
def getTiffFileName(filepath, suffix):
    L1 = []
    L2 = []
    for root, dirs, files in os.walk(filepath):  # 遍历该文件夹
        for file in files:  # 遍历刚获得的文件名files
            (filename, extension) = os.path.splitext(file)  # 将文件名拆分为文件名与后缀
            if (extension == suffix):  # 判断该后缀是否为.c文件
                L1.append(filepath + "/" + file)
                L2.append(filename)
    return L1, L2


# 蒙特卡罗生成groups组随机数并存放到MonteCarlo_df中
def Monte_Carlo(numParameters):
    x0 = np.random.rand(numParameters - 1)
    ratio = sum(x0) / 100
    x1 = x0 // ratio
    parameters = x1.tolist()
    parameters.append(100 - sum(parameters))
    random.shuffle(parameters)  # 顺序随机重新排列
    return parameters


def Monte_Carlo_groups(numParameters):
    parameters = Monte_Carlo(numParameters)  # 生成数量含土地利用图层和邻域图层
    while min(parameters) == 0:  # 如果存在0则重新生成，知道没有0才跳出循环
        parameters = Monte_Carlo(numParameters)
    return parameters  # 返回表

def getDevelop(nRows, nCols, numParameters, inputPathFiles, Monte_Carlo_list, NeighborEffect_arr):
    developmentPotential_arr = np.zeros([nRows, nCols])  # 存放发展潜力
    for i in range(len(Monte_Carlo_list) - 2):  # 逐个权重拿出并与对于图层相乘后累加
        developmentPotential_arr += LoadData(inputPathFiles[i]) * Monte_Carlo_list[i]
    developmentPotential_arr = developmentPotential_arr - Monte_Carlo_list[-2] * get_lulc_value_arr(
        inputPathFiles[-1])  # 减去继承性图层x权重
    developmentPotential_arr[np.where(developmentPotential_arr < 0)] = 0  # 小于0的地方设置为0
    developmentProbability_arr = developmentPotential_arr + Monte_Carlo_list[-1] * NeighborEffect_arr  # 加上邻域x权重

    return developmentPotential_arr, developmentProbability_arr  # 返回发展概率和发展潜力

# 精度评价部分
def getOAKappe(pred_arr, true_arr):
    OA_kappa_arr = pred_arr * 10 + true_arr

    TP = np.size(np.where(OA_kappa_arr == 11))  # 结果、实际都是城市
    FP = np.size(np.where(OA_kappa_arr == 10))  # 结果是城市，实际不是城市
    FN = np.size(np.where(OA_kappa_arr == 1))  # 结果不是，实际是城市
    TN = np.size(np.where(OA_kappa_arr == 0))  # 结果，实际都不是城市
    TotalNum = TP + FP + FN + TN
    OverAccury = (TP + TN) / TotalNum
    kappa = (float((TP + TN) * TotalNum) - float(((FN + TN) * (FP + TN) + (FN + TP) * (FP + TP)))) / (
            float(TotalNum * TotalNum) - float(((FN + TN) * (FP + TN) + (FN + TP) * (FP + TP))))
    return OverAccury, kappa


def getFOM(true_arr, pred_arr, startYear_arr):
    changeTrue = true_arr - startYear_arr
    changePred = pred_arr - startYear_arr
    A = np.sum(np.where((changeTrue == 1) & (changePred == 0)))
    B = np.sum(np.where((changeTrue == 1) & (changePred == 1)))
    C = np.sum(np.where((changeTrue == 0) & (changePred == 1)))
    return B / (A + B + C)



if __name__ == '__main__':
    starttime = time.perf_counter()
    print("开始运行时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    beginyear = 2000  
    endyear = 2010
    groups = 10
    WindowSize = 5
    
    # 计算发展潜力、发展概率的参数
    path = os.getcwd()
    filepath = path + "/" + "simulationdata"  # 存放计算发展潜力数据的目录
    suffix = ".tif"
    inputPathFiles, inputNames = getTiffFileName(filepath, suffix)
    inputNames.append("lulc")
    inputNames.append("Neighbor")
    lucFilePath = path + "/" + r"lulc\ZYlulc.tif" # 存放土地利用数据的目录
    inputPathFiles.append(lucFilePath)
    numParameters = len(inputNames)  # 生成随机数个数
    startyear_filename = path + "/urban/" + "urban" + str(beginyear) + ".tif"
    NeighborEffect_arr = GetNeighborEffect(startyear_filename, WindowSize)
    
    urban_arr = LoadData(path + "/" + "urban/urban" + str(endyear) + ".tif")
    endYearCount = np.sum(urban_arr == 1) # 模拟未来则直接输入未来的城市像元数量
    urbanOld_arr = LoadData(path + "/urban/" + "urban" + str(beginyear) + ".tif")
    PiexlNumber = endYearCount - np.sum(urbanOld_arr == 1)
    
    raster = gdal.Open(path + "/" +"urban/urban{}.tif".format(beginyear))
    nRows = raster.RasterYSize  # 行数
    nCols = raster.RasterXSize  # 列数
    
    im_width = raster.RasterXSize  # 栅格矩阵的列数
    im_height = raster.RasterYSize  # 栅格矩阵的行数
    im_bands = raster.RasterCount  # 波段数
    im_geotrans = raster.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = raster.GetProjection()  # 获取投影信息
    for group in range(groups):     #循环groups次
        starttime1 = time.perf_counter()
        urbanOld_arr = LoadData(path + "/urban/" + "urban" + str(beginyear) + ".tif")
        Monte_Carlo_list = Monte_Carlo_groups(numParameters) # 可直接在此输入对应图层的权重，注意顺序，一般与simulationdata文件中一致，倒数第二个是lulc权重，最后一个是邻域权重

        developmentPotential_arr, developmentProbability_arr = getDevelop(nRows, nCols, numParameters, inputPathFiles,
                                                                          Monte_Carlo_list, NeighborEffect_arr)
        
        developmentProbability_arr[np.where(urbanOld_arr == 1)] = 0
        ResultPath = path + "/" +"result_LUSD" + "/sim" + str(group).zfill(3)
        if not os.path.exists(ResultPath):
            os.makedirs(ResultPath)
    
        ResultFile2 = ResultPath + "/" + "Probability_arr_" + str(group) + ".tif"
        WriteTiff(developmentProbability_arr, im_width, im_height, im_bands, im_geotrans, im_proj, ResultFile2)
    
        ResultFile3 = ResultPath + "/" + "NeighborEffect_arr_" + str(group) + ".tif"
        WriteTiff(NeighborEffect_arr, im_width, im_height, im_bands, im_geotrans, im_proj, ResultFile3)

        print(inputNames)
        print(Monte_Carlo_list)
    
        PkSort_R_Index = np.argsort(-developmentProbability_arr)  #降序索引
        Pk = developmentProbability_arr.reshape(-1)
        urbanOld_arr = urbanOld_arr.reshape(-1)
        PkSort_R_Index = np.argsort(-Pk)  #降序索引
        urbanOld_arr[PkSort_R_Index[0:PiexlNumber]] = 1  #提取概率最高的赋值为城市[0:PkSort_R_Index]] = 1  #提取概率最高的赋值为城市

        urbanOld_arr = np.array(urbanOld_arr).reshape([nRows, nCols])
        ResultFile = ResultPath + "/" + "simurban" + str(endyear) + "_" + str(group) + ".tif"
        WriteTiff(urbanOld_arr, im_width, im_height, im_bands, im_geotrans, im_proj, ResultFile)
    
        endtime_year = time.perf_counter()
        timeUse = endtime_year - starttime
        # print("模拟本组结束时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    
        print("模拟第" + str(group) + "组完成，用时：" + str(timeUse) + "s，开始对本组进行精度计算，waiting...")
    
        # 精度评价
        startYear_arr = LoadData(path + "/" + r"urban\urban" + str(beginyear) + ".tif")
        pred_arr = urbanOld_arr
        true_arr = LoadData(path + "/" + r"urban\urban" + str(endyear) + ".tif")
        use_arr = LoadData1(path + "/" +  r"simulationdata\road1.tif")
        
        startYear_arr[np.where(use_arr == 3)] = 3
        pred_arr[np.where(use_arr == 3)] = 3
        true_arr[np.where(use_arr == 3)] = 3
    
        OverAccury, kappa = getOAKappe(pred_arr, true_arr)
        Fom = getFOM(true_arr, pred_arr, startYear_arr)
        print("OverAccury,kappa,Fom:" + str(OverAccury) + " " + str(kappa) + " " + str(Fom))
    
        if group == 0:
            workbook = Workbook()
            save_file = path + "/result_LUSD/" + "参数和精度.xlsx"
            worksheet1 = workbook.active 
            worksheet1.append([" "] + inputNames + ["OverAccury","Kappa","FOM"])
     
        worksheet1.append([group] + Monte_Carlo_list + [OverAccury,kappa,Fom])
        workbook.save(filename=save_file)

        print([group] + Monte_Carlo_list + [OverAccury,kappa,Fom])

        endtime_year = time.perf_counter()
        timeUse = endtime_year - starttime1
        print("计算本组结束时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("计算第" + str(group) + "组完成，用时：" + str(timeUse) + "s")
        print("")

    print("计算全部结束时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("")
