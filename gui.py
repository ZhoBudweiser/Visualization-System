import os
import numpy as np
from DataHandler import DataHandler
from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel
from traits.api import HasTraits, Instance, Button, File, Str, HTML, on_trait_change
from traitsui.api import Group, Item, View, VGroup, HSplit, VSplit, VGrid, Tabbed
from mayavi.core.api import PipelineBase
from traitsui.menu import Menu, MenuBar, ToolBar, Action, ActionGroup, StandardMenuBar
from matplotlib.figure import Figure
from MPLFigureEditor import MPLFigureEditor
from numpy import sin, cos, linspace, pi
from message import Error, Message
import networkx as nx
import matplotlib.pyplot as plt


def picker_callback(picker):
    print(picker.pick_position)
    print(picker.selection_point)
    model.states += str(Message("点击位置：" + str(picker.pick_position)))
    model.states += str(Message("选择结点：" + str(picker.selection_point)))
    x1, y1, z1 = picker.selection_point
    mlab.figure(model.plane.mayavi_scene)
    mlab.points3d(x1, y1, z1, color=(1, 0, 0), resolution=100)
    mlab.figure(model.scene.mayavi_scene)
    mlab.points3d(x1, y1, z1, color=(1, 0, 0), resolution=100)

class Layout(HasTraits):

    # 定义窗口中的变量
    scene = Instance(MlabSceneModel, ())
    plane = Instance(MlabSceneModel, ())
    # plot = Instance(PipelineBase)
    processBtn = Button(u'分割地形')
    showBtn = Button(u'展示拓扑')
    fileDir = File()
    stateText = Str()
    states = HTML()
    menu = Instance(Menu)
    style = Str("terrain")
    figure = Instance(Figure, ())
    process = Action(name="分割地形", action="do_process")
    show = Action(name="展示拓扑", action="do_show")

    fileProcess = [
        Action(name="关闭", action="_on_close")
    ]
    styles = [
        Action(name="多彩", action="do_gist_earth", enabled_when="fileDir"),
        Action(name="雪地", action="do_blues", enabled_when="fileDir"),
        Action(name="草地", action="do_summer", enabled_when="fileDir"),
        Action(name="地图", action="do_vega", enabled_when="fileDir"),
        Action(name="常规", action="do_terrain", enabled_when="fileDir"),
    ]
    style_map = {
        'gist_earth': "多彩",
        'Blues': "雪地",
        'summer': "草地",
        'Vega20b': "地图",
        'terrain': "常规",
    }

    dataHandler = DataHandler()

    def do_process(self):
        pass
        # nx.draw(self.g, ax=self.axes, with_labels=True, pos=self.pos)
        # self.figure.canvas.show()

    def do_show(self):
        self.g = nx.Graph()
        self.g.add_edge('1', '2')
        self.g.add_edge('2', '3')
        self.g.add_edge('1', '4')
        self.g.add_edge('2', '4')

        self.pos = nx.spring_layout(self.g)
        self.axes = self.figure.add_subplot(111)
        nx.draw(self.g, ax=self.axes, with_labels=True, pos=self.pos)
        self.figure.canvas.show()

    def _processBtn_fired(self):
        pass

    def _showBtn_fired(self):
        g = nx.Graph()
        g.add_edge('1', '2')
        g.add_edge('2', '3')
        g.add_edge('1', '4')
        g.add_edge('2', '4')

        fixed_position = {'1': [1, 1], '2': [1.5, 0.8], '3': [1.7, 2.8], '4': [0.6, 3.3]}
        pos = nx.spring_layout(g, pos=fixed_position)

        colors = []
        for i in range(g.number_of_nodes()):
            if i == 2:
                colors.append('#ff0000')
            else:
                colors.append('#1f7814')

        axes = self.figure.add_subplot(111)

        # fig, ax = plt.subplots()
        nx.draw(g, ax=axes, with_labels=True, pos=pos, node_color=colors)  # add colors
        self.figure.canvas.show()

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

    # 当主场景被激活更新图形
    @on_trait_change('scene.activated')
    def init_scene_plot(self):
        figure = mlab.figure(self.scene.mayavi_scene)
        picker = figure.on_mouse_pick(picker_callback, type='point', button='Left')
        figure = mlab.figure(self.plane.mayavi_scene)
        picker = figure.on_mouse_pick(picker_callback, type='point', button='Left')
        picker.tolerance = 0.01
        # self.do_show()
        # figure = mlab.gcf()
        # figure.scene.disable_render = True
        # # 用mlab.points3d建立红色和白色小球的集合
        # x1, y1, z1 = np.random.random((3, 2))
        # red_glyphs = mlab.points3d(x1, y1, z1, color=(1, 0, 0),
        #                            resolution=10)
        # figure.scene.disable_render = False
        # # 绘制选取框，并放在第一个小球上
        # outline = mlab.outline(line_width=3)
        # outline.outline_mode = 'cornered'
        # outline.bounds = (x1[0] - 0.1, x1[0] + 0.1,
        #                   y1[0] - 0.1, y1[0] + 0.1,
        #                   z1[0] - 0.1, z1[0] + 0.1)

    # 定义监听函数、更新视图
    @on_trait_change('fileDir')
    def load_plot(self):
        if not self.fileDir:
            return
        self.states += str(Message("加载文件："+self.fileDir.split('/')[-1]))
        # self.do_show()
        # 处理地形数据
        try:
            self.dataHandler.getDataSource(self.fileDir.split('/')[-1])
            # 渲染地形 hgt 的数据 data
            figure = mlab.figure(self.plane.mayavi_scene)
            mlab.clf()
            self.plane.mlab.imshow(self.dataHandler.dataSource, colormap=self.style)
            # figure.on_mouse_pick(picker_callback, type='cell', button='Left')
            figure = mlab.figure(self.scene.mayavi_scene)
            mlab.clf()
            self.scene.mlab.surf(self.dataHandler.dataSource, colormap=self.style, warp_scale=0.2)  # 可视化平面，指定颜色与放缩的最值
            # figure.on_mouse_pick(picker_callback, type='world', button='Left')
            self.states += str(Message("加载成功！"))
        except:
            self.states += str(Error("文件格式错误！"))

    # 切换风格
    @on_trait_change('style')
    def change_style(self):
        if not self.fileDir:
            return
        try:
            figure = mlab.figure(self.plane.mayavi_scene)
            mlab.clf()
            self.plane.mlab.imshow(self.dataHandler.dataSource, colormap=self.style)
            figure = mlab.figure(self.scene.mayavi_scene)
            mlab.clf()
            self.scene.mlab.surf(self.dataHandler.dataSource, colormap=self.style, warp_scale=0.2)
            self.states += str(Message("风格切换为："+self.style_map[self.style]))
        except:
            self.states += str(Error("风格转换失败！"))

    # 定义视图的布局
    _diagram = HSplit(
        VSplit(
            Item('plane', editor=SceneEditor(), width=500, show_label=False),
            Item('figure', editor=MPLFigureEditor(), show_label=False),
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
    # _buttons = HSplit(
    #     Item('processBtn', style="simple", show_label=False),
    #     Item('showBtn', style="simple", show_label=False)
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
            Menu(fileProcess[0], process, show, name='文件'),
            Menu(styles[0], styles[1], styles[2], styles[3], styles[4], name='风格'),
        ),
        # menubar=StandardMenuBar,
        # buttons=_buttons,
        width=1800,
        height=1200,
        resizable=True
    )


if __name__ == "__main__":
    model = Layout()
    model.configure_traits()
