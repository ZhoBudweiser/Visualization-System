import zipfile
import numpy as np
import richdem as rd

# ------------------------------------------------------------------

# import sys
# import os
# sys.path.insert(1, os.environ["HOMEDRIVE"]+os.environ["HOMEPATH"]+'/Documents/GitHub/arcgis-scripts')
import archook
archook.get_arcpy(pro=True)
import arcpy
# try:
#     import archook
#     archook.get_arcpy(pro=True)
#     import arcpy
#     # from arcpy import env
#     # from arcpy.sa import *
# except ImportError:
#     # do whatever you do if arcpy isnt there.
#     print(ImportError)

help(arcpy)

# env.workspace = "C:/sapyexamples/data"
# outWatershed = Watershed("flowdir", "pourpoint")
# outWatershed.save("C:/sapyexamples/output/outwtrshd01")

# ---------------------------------------------------------------


# # 读取压缩 hgt 文件。北纬36-37度，西经113-114度地形高程数据
# hgt = zipfile.ZipFile('./data/N36W113.hgt.zip').read('N36W113.hgt')
# # 处理地形数据
# data = np.fromstring(hgt, '>i2')    # 从str中读取数组，格式为 2 字节，大端
# data.shape = (3601, 3601)           # 调整大小为 3601 * 3601 = 12967201 的二维格式
# data = data.astype(np.float32)      # 将数据类型转换为 float 32 位
# # data = data[:1000, 900:1900]        # 取其中的 1000 * 1000 数据
# data[data == -32768] = data[data > 0].min()
# rda = rd.rdarray(data, no_data=-9999)
# np.save('out.npy', rda)

# 0. 导入预处理的数据
beau = rd.rdarray(np.load('out.npy'), no_data=-9999)
# beaufig = rd.rdShow(beau, ignore_colours=[0], axes=False, cmap='jet', figsize=(8, 5.5))

# 1. 洼地填充
# # 方式一
# beau_filled = rd.FillDepressions(beau, in_place=False)
# beaufig_filled = rd.rdShow(beau_filled, ignore_colours=[0], axes=False, cmap='jet', vmin=beaufig['vmin'], vmax=beaufig['vmax'], figsize=(8, 5.5))
#
# # 展示填充效果
# beau_diff = beau_filled - beau
# beaufig_diff = rd.rdShow(beau_diff, ignore_colours=[0], axes=False, cmap='jet', figsize=(8, 5.5))

# 方式二
beau_epsilon = rd.FillDepressions(beau, epsilon=True, in_place=False)
# # 展示填充效果
# beau_eps_diff = beau_epsilon - beau
# beaufig_eps_diff = rd.rdShow(beau_eps_diff, ignore_colours=[0], axes=False, cmap='jet', figsize=(8, 5.5))
# # 展示填充效果
# beau_diffeps_diff = beau_epsilon - beau_filled
# beaufig_diffeps_diff = rd.rdShow(beau_diffeps_diff, ignore_colours=[0], axes=False, cmap='jet', figsize=(8, 5.5))

# 2. 流向计算
# rd.FillDepressions(beau_epsilon, epsilon=True, in_place=True)
accum_d8 = rd.FlowAccumulation(beau_epsilon, method='D8')
d8_fig = rd.rdShow(accum_d8, zxmin=450, zxmax=550, zymin=550, zymax=450, figsize=(8, 5.5), axes=False, cmap='jet')
