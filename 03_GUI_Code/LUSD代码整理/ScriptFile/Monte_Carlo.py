from goto import with_goto
import numpy as np

@with_goto
def Monte_Carlo(groups, npts): #利用蒙特卡洛算法得到权重矩阵
    wei = np.zeros([groups, npts]) #定义一个groups行，npts列的空矩阵
    for p in range(groups):
        label.begin
        arr = np.random.rand(npts-1)*(100+npts-1) # 生成均匀分布的随机数，值在[0,100+npts-1]之间
        num = arr.astype(int)+1 # 将arr数组转换成int形，+1是为了没有0值
        sortarr = np.argsort(num) # 对num矩阵进行排序，得到从小到大数的索引
        wei[p][0] = num[sortarr[0]] # sortarr[0]是num最小值的索引，所以这里是返回num数组的最小值
                                    # 这里是给权重矩阵第p行第1列的数赋值

        for i in range(1,npts-1):   # 该循环是为了给权重矩阵第i列每个数赋值
            wei[p][i] = num[sortarr[i]]-num[sortarr[i-1]] # 按照大小顺序相减，+1是为了没有0值
            wei[p][npts-1] = 100 - num[sortarr[npts-2]]    # +1是为了没有0值，(100+npts-1)是为了没有负数 100减去最大的那个数，放到最后
                                        # 因为蒙特卡罗算法本身就是基于随机数的算法，所以这里可以使用该方式使矩阵值全都大于0
        for i in range(1, npts):
            if wei[p, i] <= 0: # 判断该组是否有小于0的数
                #print("第" ,p, "组")
                goto.begin # 如果存在小于0的从label.begin处开始，该组重新计算
    label.end
    return wei