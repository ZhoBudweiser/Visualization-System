from tvtk.api import tvtk
from tvtkfunc import ivtk_scene,event_loop

s = tvtk.CubeSource(x_length=1.0, y_length=2.0, z_length=3.0)
m = tvtk.PolyDataMapper(input_connection=s.output_port)
a = tvtk.Actor(mapper=m)
# win = ivtk_scene(a)
# win.scene.isometric_view()
# event_loop()
#
# 创建一个Renderer，将Actor添加进去
r = tvtk.Renderer(background=(0, 0, 0))
r.add_actor(a)
# 创建一个RenderWindow(窗口)，将Renderer添加进去
w = tvtk.RenderWindow(size=(300,300))
w.add_renderer(r)
# 创建一个RenderWindowInteractor（窗口的交互工具)
i = tvtk.RenderWindowInteractor(render_window=w)
# 开启交互
i.initialize()
i.start()