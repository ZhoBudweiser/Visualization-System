import zipfile
import numpy as np


class DataHandler:
    dataSource = np.array(0)
    SAMPLES_SIZE = 3601
    VOID = -32768
    x0 = 0
    x1 = 1000
    y0 = 900
    y1 = 1900

    def getDataSource(self, filename):
        filename = './data/' + filename
        with open(filename, 'rb') as hgt_data:
            hgt = np.fromfile(hgt_data, np.dtype('>i2'))
        # 读取压缩 hgt 文件。北纬36-37度，西经113-114度地形高程数据
        # hgt = zipfile.ZipFile(path).read(filename)
        # 处理地形数据
        # data = np.fromstring(hgt, '>i2')  # 从str中读取数组，格式为 2 字节，大端
        self.dataSource = self.dataPreProcess(hgt)

    def dataPreProcess(self, data):
        data.shape = (self.SAMPLES_SIZE, self.SAMPLES_SIZE)  # 调整大小为 3601 * 3601 = 12967201 的二维格式
        data = data.astype(np.float32)  # 将数据类型转换为 float 32 位
        data = data[self.x0:self.x1, self.y0:self.y1]  # 取其中的 1000 * 1000 数据
        data[data == self.VOID] = data[data > 0].min()  # 将其中的无效值替换为大于 0 的最小值
        return data
