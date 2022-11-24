# By Pierre Haessig, https://gist.github.com/pierre-haessig/9838326
from pyface.qt import QtGui, QtCore

import matplotlib
# We want matplotlib to use a QT backend
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from traits.api import Any, Instance
from traitsui.qt4.editor import Editor
from traitsui.qt4.basic_editor_factory import BasicEditorFactory

class _MPLFigureEditor(Editor):

    scrollable  = True

    def init(self, parent):
        self.control = self._create_canvas(parent)
        self.set_tooltip()

    def update_editor(self):
        pass

    def _create_canvas(self, parent):
        """ Create the MPL canvas. """
        # matplotlib commands to create a canvas
        mpl_canvas = FigureCanvas(self.value)
        return mpl_canvas

class MPLFigureEditor(BasicEditorFactory):

    klass = _MPLFigureEditor


if __name__ == "__main__":
    # Create a window to demo the editor
    from traits.api import HasTraits, Int, Float, on_trait_change
    from traitsui.api import View, Item
    from numpy import sin, cos, linspace, pi

    class Test(HasTraits):

        figure = Instance(Figure, ())
        n = Int(11)
        a = Float(0.5)

        view = View(Item('figure', editor=MPLFigureEditor(), show_label=False),
                    Item('n'),
                    Item('a'),
                    width=400,
                    height=300,
                    resizable=True)

        def __init__(self):
                super(Test, self).__init__()
                axes = self.figure.add_subplot(111)
                self._t = linspace(0, 2*pi, 200)
                self.plot()

        @on_trait_change('n,a')
        def plot(self):
            t = self._t
            a = self.a
            n = self.n
            axes = self.figure.axes[0]
            if not axes.lines:
                axes.plot(sin(t)*(1+a*cos(n*t)), cos(t)*(1+a*cos(n*t)))
            else:
                l = axes.lines[0]
                l.set_xdata(sin(t)*(1+a*cos(n*t)))
                l.set_ydata(cos(t)*(1+a*cos(n*t)))
            canvas = self.figure.canvas
            if canvas is not None:
                canvas.draw()

    ##############
    # This works #
    ##############
    t = Test()
    t.configure_traits()

    # class Container(HasTraits):
    #     p1 = Instance(Test)
    #     p2 = Instance(Test)
    #
    #     view = View(
    #         Item("p1", style='custom'),
    #         Item("p2", style='custom')
    #     )
    #
    # ##############
    # # This fails #
    # ##############
    # c = Container(p1=Test(), p2=Test())
    # c.configure_traits()

