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
    # topo = File()
    stateText = Str()
    menu = Instance(Menu)
    recalc = Action(name="打开", action="do_recalc")

    style_gist_earth = Action(name="多彩", action="do_gist_earth")
    style_blues = Action(name="雪地", action="do_blues")
    style_summer = Action(name="草地", action="do_summer")
    style_vega = Action(name="深彩", action="do_vega")
    style_terrain = Action(name="常规", action="do_terrain")

    style = Str("terrain")

    dataHandler = DataHandler()

    def do_gist_earth(self):
        self.style = 'gist_earth'

    def do_blues(self):
        self.style = 'Blues'

    def do_summer(self):
        self.style = 'summer'

    def do_vega(self):
        self.style = 'Vega20b'

    def do_terrain(self):
        self.style = 'terrain'

    def do_recalc(self):
        pass

    def _processBtn_fired(self):
        pass

    def _showBtn_fired(self):
        pass

    @on_trait_change('style')
    def change_style(self):
        if not self.fileDir:
            return
        self.scene.mlab.clf()
        # 处理地形数据
        self.dataHandler.getDataSource(self.fileDir.split('/')[-1])
        # 渲染地形 hgt 的数据 data
        self.plot = self.scene.mlab.surf(self.dataHandler.dataSource, colormap=self.style, warp_scale=0.2)  # 可视化平面，指定颜色与放缩的最值

    # 定义监听函数、更新视图绘制
    @on_trait_change('fileDir')
    def load_plot(self):
        self.scene.mlab.clf()
        # 处理地形数据
        self.dataHandler.getDataSource(self.fileDir.split('/')[-1])
        # 渲染地形 hgt 的数据 data
        self.plot = self.scene.mlab.surf(self.dataHandler.dataSource, colormap=self.style, warp_scale=0.2)  # 可视化平面，指定颜色与放缩的最值
        # 创建交互式的可视化窗口
        # self.scene.mlab.view(azimuth=-5.9, elevation=83, distance=570, focalpoint=[5.3, 20, 238])  # 设置照相机的位置
    # 当场景被激活更新图形
    # @on_trait_change('scene.activated')
    # def update_plot(self):
    #     # 如果plot未绘制则生成plot3d
    #     if self.plot is None:
    #         # 创建交互式的可视化窗口
    #         self.scene.mlab.view(azimuth=-5.9, elevation=83, distance=570, focalpoint=[5.3, 20, 238])  # 设置照相机的位置
    #         # 处理地形数据
    #         self.dataHandler.getDataSource('./data/N36W113.hgt.zip', 'N36W113.hgt')
    #         # 渲染地形 hgt 的数据 data
    #         self.plot = self.scene.mlab.surf(self.dataHandler.dataSource, colormap='gist_earth', warp_scale=0.2, vmin=1200, vmax=1610)  # 可视化平面，指定颜色与放缩的最值
    #     # 如果数据有变化，将数据更新即重新赋值
    #     else:
    #         pass

    # 定义视图的布局
    _diagram = HSplit(
        VSplit(
            Item('stateText', style="custom", height=375, width=375, show_label=False),
            Item('stateText', style="custom", height=375, width=375, show_label=False)
        ),
        Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=750, width=900, show_label=False)
    )
    _bar = HSplit(
        Item('fileDir', style="simple", height=10, width=375, show_label=False),
        Item('menu', style="simple", height=10, width=900, show_label=False)
    )
    _buttons = VGrid(
        Item('processBtn', show_label=False),
        Item('showBtn', show_label=False),
        columns=8
    )
    # _directory = Group(
    #     # Item('fileDir', style="simple", height=10, width=250, show_label=False),
    #     Item('topo', style="custom", height=740, width=250, show_label=False)
    # )
    _states = Group(
        Item('stateText', style="custom", height=200, width=1275, show_label=False)
    )

    view = View(
        VSplit(
            _bar,
            _diagram,
            _states,
            _buttons
        ),
        title='地形分割与拓扑关系构建可视化系统',
        menubar=MenuBar(
            Menu(recalc, name='文件'),
            Menu(style_gist_earth, style_blues, style_summer, style_vega, style_terrain, name='风格'),
        ),
        resizable=True
    )


if __name__ == "__main__":
    model = Layout()
    model.configure_traits()
