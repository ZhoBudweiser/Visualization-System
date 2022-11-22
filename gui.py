import os
from DataHandler import DataHandler
from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
from traits.api import HasTraits, Instance, Button, File, Str, HTML, on_trait_change
from traitsui.api import Group, Item, View, VGroup, HSplit, VSplit, VGrid, Tabbed
from mayavi.core.api import PipelineBase
from traitsui.menu import Menu, MenuBar, ToolBar, Action, ActionGroup
from message import Error, Message

class Layout(HasTraits):

    # 定义窗口中的变量
    scene = Instance(MlabSceneModel, ())
    plane = Instance(MlabSceneModel, ())
    # plot = Instance(PipelineBase)
    processBtn = Button(u'分割地形')
    showBtn = Button(u'展示拓扑')
    fileDir = File()
    # topo = File()
    stateText = Str()
    states = HTML()
    menu = Instance(Menu)

    recalc = Action(name="打开", action="do_recalc")

    process = Action(name="分割地形", action="do_process")
    show = Action(name="展示拓扑", action="do_show")

    style_gist_earth = Action(name="多彩", action="do_gist_earth", enabled_when="fileDir")
    style_blues = Action(name="雪地", action="do_blues", enabled_when="fileDir")
    style_summer = Action(name="草地", action="do_summer", enabled_when="fileDir")
    style_vega = Action(name="地图", action="do_vega", enabled_when="fileDir")
    style_terrain = Action(name="常规", action="do_terrain", enabled_when="fileDir")

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

    def do_process(self):
        pass

    def do_show(self):
        pass

    def _processBtn_fired(self):
        pass

    def _showBtn_fired(self):
        pass

    # 定义监听函数、更新视图绘
    @on_trait_change('fileDir, style')
    def load_plot(self):
        if not self.fileDir:
            return
        mlab.figure(self.plane.mayavi_scene)
        mlab.clf()
        mlab.figure(self.scene.mayavi_scene)
        mlab.clf()
        # 处理地形数据
        try:
            self.dataHandler.getDataSource(self.fileDir.split('/')[-1])
            # 渲染地形 hgt 的数据 data
            mlab.figure(self.plane.mayavi_scene)
            self.plane.mlab.imshow(self.dataHandler.dataSource, colormap=self.style)
            mlab.figure(self.scene.mayavi_scene)
            self.scene.mlab.surf(self.dataHandler.dataSource, colormap=self.style, warp_scale=0.2)  # 可视化平面，指定颜色与放缩的最值
        except:
            self.states += str(Error("文件格式错误！"))
            # print(self.states)
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
            Item('plane', editor=SceneEditor(), width=500, show_label=False),
            Item('stateText', style="custom", show_label=False),
            style='simple'
        ),
        Item('scene', width=900, height=0.5, editor=SceneEditor(scene_class=MayaviScene), show_label=False)
    )
    _bar = Group(
        Item('fileDir', style="simple", height=10, show_label=False)
    )
    _buttons = [
        process,
        show,
    ]
    # _directory = Group(
    #     # Item('fileDir', style="simple", height=10, width=250, show_label=False),
    #     Item('topo', style="custom", height=740, width=250, show_label=False)
    # )
    _states = Group(
        Item('states', style="readonly", height=200, show_label=False)
    )

    view = View(
        VSplit(
            _bar,
            _diagram,
            _states,
            # _buttons
        ),
        title='地形分割与拓扑关系构建可视化系统',
        menubar=MenuBar(
            Menu(recalc, name='文件'),
            Menu(style_gist_earth, style_blues, style_summer, style_vega, style_terrain, name='风格'),
        ),
        buttons=_buttons,
        resizable=True
    )


if __name__ == "__main__":
    model = Layout()
    model.configure_traits()
