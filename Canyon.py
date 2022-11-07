import zipfile
import numpy as np
from mayavi import mlab

# 读取压缩 hgt 文件。北纬36-37度，西经113-114度地形高程数据
hgt = zipfile.ZipFile('./data/N36W113.hgt.zip').read('N36W113.hgt')
# 处理地形数据
data = np.fromstring(hgt, '>i2')    # 从str中读取数组，格式为 2 字节，大端
data.shape = (3601, 3601)           # 调整大小为 3601 * 3601 = 12967201 的二维格式
data = data.astype(np.float32)      # 将数据类型转换为 float 32 位
data = data[:1000, 900:1900]        # 取其中的 1000 * 1000 数据
data[data == -32768] = data[data > 0].min()                                     # 将其中的无效值替换为大于 0 的最小值
# 渲染地形 hgt 的数据 data
mlab.figure(size=(800, 640), bgcolor=(0.16, 0.28, 0.46))                        # 创建一个指定大小和背景色的 scene
mlab.surf(data, colormap='gist_earth', warp_scale=0.2, vmin=1200, vmax=1610)    # 可视化平面，指定颜色与放缩的最值
# 清空内存
del data
# 创建交互式的可视化窗口
mlab.view(azimuth=-5.9, elevation=83, distance=570, focalpoint=[5.3, 20, 238])  # 设置照相机的位置
mlab.show()                                                                     # 开始与图像交互
