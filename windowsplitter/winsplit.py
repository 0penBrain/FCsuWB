from PySide2 import QtWidgets, QtCore
import FreeCADGui as Gui

class WinSplitter(QtCore.QObject):

    class SplitWindow(QtWidgets.QMainWindow):
    
        def __init__(self, wid, res, title):
            super(WinSplitter.SplitWindow, self).__init__()
            self.wid = wid
            self.res = res
            self.setCentralWidget(self.wid)
            self.setWindowTitle(title)
            self.show()
    
        def closeEvent(self, ev):
            self.res.layout().addWidget(self.wid)
            super(WinSplitter.SplitWindow, self).closeEvent(ev)

    def __new__(cls):
        if not hasattr(Gui.getMainWindow(), 'winsplitter'):
            return super().__new__(cls)
        else:
            return None

    def __init__(self):
        super(WinSplitter, self).__init__()
        Gui.getMainWindow().centralWidget().findChild(QtWidgets.QTabBar).tabBarDoubleClicked.connect(self.onTBDC)
        setattr(Gui.getMainWindow(), 'winsplitter', self)
        self.splitwin = []

    def onTBDC(self, idx):
        if idx >= 0:
            sw = Gui.getMainWindow().centralWidget().subWindowList()[idx]
            self.splitwin.append(WinSplitter.SplitWindow(sw.widget(), sw, sw.windowTitle()))

WinSplitter()
