from PySide import QtGui, QtCore
import FreeCAD as App
import FreeCADGui as Gui

class ToolButton(QtGui.QToolButton):

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
        elif  event.button() == QtCore.Qt.RightButton:
            if self.rightButFunc:
                self.rightButFunc()
            elif self.midButFunc:
                self.midButFunc()
            return True
        else:
            return super(ToolButton, self).mousePressEvent(event)
