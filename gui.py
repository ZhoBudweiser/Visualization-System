import zipfile
import numpy as np
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import Group, Item, View
from mayavi.core.api import PipelineBase


class Layout(HasTraits):
    # 定义窗口中的变量
    scene = Instance(MlabSceneModel, ())
    plot = Instance(PipelineBase)

    # 定义监听函数、更新视图绘制
    # 当场景被激活更新图形
    @on_trait_change('scene.activated')
    def update_plot(self):
        # 如果plot未绘制则生成plot3d
        if self.plot is None:
            # 读取压缩 hgt 文件。北纬36-37度，西经113-114度地形高程数据
            hgt = zipfile.ZipFile('./data/N36W113.hgt.zip').read('N36W113.hgt')
            # 处理地形数据
            data = np.fromstring(hgt, '>i2')  # 从str中读取数组，格式为 2 字节，大端
            data.shape = (3601, 3601)  # 调整大小为 3601 * 3601 = 12967201 的二维格式
            data = data.astype(np.float32)  # 将数据类型转换为 float 32 位
            data = data[:1000, 900:1900]  # 取其中的 1000 * 1000 数据
            data[data == -32768] = data[data > 0].min()  # 将其中的无效值替换为大于 0 的最小值
            # 渲染地形 hgt 的数据 data
            # self.scene.mlab.figure(size=(800, 640), bgcolor=(0.16, 0.28, 0.46))  # 创建一个指定大小和背景色的 scene
            self.plot = self.scene.mlab.surf(data, colormap='gist_earth', warp_scale=0.2, vmin=1200, vmax=1610)  # 可视化平面，指定颜色与放缩的最值
            # 清空内存
            del data
            # 创建交互式的可视化窗口
            self.scene.mlab.view(azimuth=-5.9, elevation=83, distance=570, focalpoint=[5.3, 20, 238])  # 设置照相机的位置

        # 如果数据有变化，将数据更新即重新赋值
        else:
            pass

    # 定义视图的布局
    view = View(
        Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=750, width=900, show_label=False),
        # Group('_', 'n_meridional', 'n_longitudinal'),
        resizable=True
    )


if __name__ == "__main__":
    model = Layout()
    model.configure_traits()
