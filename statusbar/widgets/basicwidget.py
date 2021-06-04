from PySide2 import QtWidgets, QtCore
import FreeCAD as App
import FreeCADGui as Gui

class ToolButton(QtWidgets.QToolButton):

    def __init__(self, text='', midButFunc = None, rightButFunc = None, parent = None):
        self.custText = text
        super(ToolButton, self).__init__(parent)
        self.resetText()
        self.midButFunc = midButFunc
        self.rightButFunc = rightButFunc

    def resetText(self):
        self.setText(self.custText)

    def actionEvent(self, event):
        super(ToolButton, self).actionEvent(event)
        self.resetText()

    def setDefaultAction(self, action):
        super(ToolButton, self).setDefaultAction(action)
        self.resetText()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MidButton:
            if self.midButFunc:
                self.midButFunc()
            elif self.rightButFunc:
                self.rightButFunc()
            return True
        elif event.button() == QtCore.Qt.RightButton:
            if self.rightButFunc:
                self.rightButFunc()
            elif self.midButFunc:
                self.midButFunc()
            return True
        else:
            return super(ToolButton, self).mousePressEvent(event)

class FuncRunner(ToolButton):

    def __init__(self, text, func, funcArgs = [], midButFunc = None, rightButFunc = None, parent = None):
        super(FuncRunner, self).__init__(text, midButFunc, rightButFunc, parent)
        self.func = func
        self.funcArgs = funcArgs
        act = QtWidgets.QAction(text)
        act.triggered.connect(self.runFunc)
        self.setDefaultAction(act)

    def runFunc(self):
        self.func(*self.funcArgs)
