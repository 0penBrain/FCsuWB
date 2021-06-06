from PySide2 import QtWidgets, QtCore
import FreeCADGui as Gui

class WinSplitter(QtCore.QObject):

    class SplitWindow(QtWidgets.QMainWindow):
        
        closed = QtCore.Signal(object)
    
        def __init__(self, wid, res, title, parent = None):
            super(WinSplitter.SplitWindow, self).__init__(parent)
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)
            self.wid = wid
            self.res = res
            self.setCentralWidget(self.wid)
            self.setWindowTitle(title)
            self.show()
    
        def closeEvent(self, ev):
            self.res.layout().addWidget(self.wid)
            self.closed.emit(self)
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

    @QtCore.Slot(int)
    def onTBDC(self, idx):
        if idx >= 0:
            sw = Gui.getMainWindow().centralWidget().subWindowList()[idx]
            for ws in self.splitwin:
                if sw == ws.res:
                    ws.close()
                    return
            ws = WinSplitter.SplitWindow(sw.widget(), sw, sw.windowTitle(), Gui.getMainWindow())
            ws.closed.connect(self.onWinClose)
            self.splitwin.append(ws)
        else:
            while self.splitwin:
                self.splitwin[0].close()
    
    @QtCore.Slot(object)
    def onWinClose(self, obj):
        self.splitwin.remove(obj)

WinSplitter()
