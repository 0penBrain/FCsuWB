from PySide2 import QtWidgets, QtCore, QtGui
import FreeCADGui as Gui

class WinSplitter(QtCore.QObject):

    class SplitWindow(QtWidgets.QDialog):
        
        closed = QtCore.Signal(object)
    
        def __init__(self, wid, res, title, parent = None):
            flag = QtCore.Qt.Window
            if QtGui.QGuiApplication.instance().keyboardModifiers() == QtCore.Qt.ShiftModifier:
                flag = QtCore.Qt.Tool
            super(WinSplitter.SplitWindow, self).__init__(parent, flag)
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)
            self.setGeometry(wid.geometry())
            lay = QtWidgets.QVBoxLayout(self)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(0)
            self.wid = wid
            print(self.wid.sizeHint())
            lay.addWidget(self.wid)
            self.setLayout(lay)
            self.res = res
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
