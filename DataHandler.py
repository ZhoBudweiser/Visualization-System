import zipfile
import numpy as np


class DataHandler:
    dataSource = np.array(0)

    def getDataSource(self, path, filename):
        # 读取压缩 hgt 文件。北纬36-37度，西经113-114度地形高程数据
        hgt = zipfile.ZipFile(path).read(filename)
        # 处理地形数据
        data = np.fromstring(hgt, '>i2')  # 从str中读取数组，格式为 2 字节，大端
        self.dataSource = self.dataPreProcess(data)

    @staticmethod
    def dataPreProcess(data):
        data.shape = (3601, 3601)  # 调整大小为 3601 * 3601 = 12967201 的二维格式
        data = data.astype(np.float32)  # 将数据类型转换为 float 32 位
        data = data[:1000, 900:1900]  # 取其中的 1000 * 1000 数据
        data[data == -32768] = data[data > 0].min()  # 将其中的无效值替换为大于 0 的最小值
        return data
