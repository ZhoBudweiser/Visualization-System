import os
from DataHandler import DataHandler
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
from traits.api import HasTraits, Instance, Button, File, Str, on_trait_change
from traitsui.api import Group, Item, View, VGroup, HSplit, VSplit, VGrid
from mayavi.core.api import PipelineBase
from traitsui.menu import Menu, MenuBar, ToolBar, Action, ActionGroup


class Layout(HasTraits):
    # 定义窗口中的变量
    scene = Instance(MlabSceneModel, ())
    plot = Instance(PipelineBase)
    processBtn = Button(u'分割地形')
    showBtn = Button(u'展示拓扑')
    fileDir = File()
    stateText = Str()
    menu = MenuBar()

    dataHandler = DataHandler()

    def _processBtn_fired(self):
        pass

    # 定义监听函数、更新视图绘制
    # 当场景被激活更新图形
    @on_trait_change('scene.activated')
    def update_plot(self):
        # 如果plot未绘制则生成plot3d
        if self.plot is None:
            # 处理地形数据
            self.dataHandler.getDataSource('./data/N36W113.hgt.zip', 'N36W113.hgt')
            # 渲染地形 hgt 的数据 data
            self.plot = self.scene.mlab.surf(self.dataHandler.dataSource, colormap='gist_earth', warp_scale=0.2, vmin=1200, vmax=1610)  # 可视化平面，指定颜色与放缩的最值
            # 创建交互式的可视化窗口
            self.scene.mlab.view(azimuth=-5.9, elevation=83, distance=570, focalpoint=[5.3, 20, 238])  # 设置照相机的位置

        # 如果数据有变化，将数据更新即重新赋值
        else:
            pass

    _diagram = Group(
        Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=750, width=900, show_label=False)
    )
    _bar = Group(
        Item('menu', style="simple", height=25, width=1000, show_label=False)
    )
    _buttons = VGrid(
        Item('processBtn', show_label=False),
        Item('showBtn', show_label=False),
        columns=8
    )
    _directory = Group(
        Item('fileDir', style="custom", height=750, width=250, show_label=False)
    )
    _states = Group(
        Item('stateText', style="custom", height=200, width=750, show_label=False)
    )
    # 定义视图的布局
    view = View(
        VGroup(
            _bar,
            HSplit(
                _directory,
                VSplit(
                    _diagram,
                    _states,
                    _buttons
                )
            ),
        ),
        title='地形分割与拓扑关系构建可视化系统',
        resizable=True
    )


if __name__ == "__main__":
    model = Layout()
    model.configure_traits()
