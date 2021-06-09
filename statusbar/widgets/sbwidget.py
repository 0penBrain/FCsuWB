from PySide2 import QtWidgets, QtCore
import FreeCAD as App
import FreeCADGui as Gui

from . import basicwidget

class DockToggler(basicwidget.ToolButton):

    def __init__(self, dock, text, midButFunc = None, rightButFunc = None, parent = None):
        if not not Gui.getMainWindow().findChild(QtWidgets.QDockWidget, dock):
            super(DockToggler, self).__init__(text, midButFunc, rightButFunc, parent)
            self.setDefaultAction(Gui.getMainWindow().findChild(QtWidgets.QDockWidget, dock).toggleViewAction())
        else:
            raise ValueError('Widget not found')

class CmdRunner(basicwidget.FuncRunner):

    def __init__(self, text, cmdArgs, midButFunc = None, rightButFunc = None, parent = None):
        super(CmdRunner, self).__init__(text, Gui.runCommand, cmdArgs, midButFunc, rightButFunc, parent)

class ParamToggler(basicwidget.FuncRunner):

    def __init__(self, text, group, param, midButFunc = None, rightButFunc = None, parent = None):
        super(ParamToggler, self).__init__(text, group, param, midButFunc, rightButFunc, parent)
        self.defaultAction().setCheckable(True)
        self.defaultAction().setChecked(App.ParamGet(group).GetBool(param, True))

    def runFunc(self, state):
        App.ParamGet(self.func).SetBool(self.funcArgs, state)

class VisibilityTool(basicwidget.ToolButton):

    def __init__(self, text='V', parent = None):
        super(VisibilityTool, self).__init__(text, parent = parent)
        lay = QtWidgets.QVBoxLayout()
        QtWidgets.QLayout.setAlignment(lay, QtCore.Qt.AlignHCenter)
        self.wid = QtWidgets.QWidget(self, QtCore.Qt.ToolTip)
        self.wid.hide()
        self.wid.setLayout(lay)
        self.lab = QtWidgets.QLabel("100 %", self.wid)
        lay.addWidget(self.lab)
        self.sli = QtWidgets.QSlider(QtCore.Qt.Orientation.Vertical, self.wid)
        self.sli.setRange(5,100)
        self.sli.setValue(100)
        self.sli.setSingleStep(5)
        self.sli.setPageStep(5)
        self.sli.valueChanged.connect(self.onSliChanged)
        self.sli.sliderReleased.connect(self.onSliChanged)
        lay.addWidget(self.sli)
        lay.setAlignment(self.sli, QtCore.Qt.AlignHCenter)
        self.wid.adjustSize()
        self.wid.setAutoFillBackground(True)
        self.wheelAngle = 0
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(2500)
        self.timer.timeout.connect(self.timerTO)

    def paintEvent(self, event):
        self.wid.move(self.mapToGlobal(QtCore.QPoint(0,0)) - QtCore.QPoint(self.wid.width()/2-self.width()/2, self.wid.height()))
        self.wid.update()
        return super(VisibilityTool, self).paintEvent(event)

    @staticmethod
    def showParent(child):
        for parent in child.InList:
            if str(parent) in ['<body object>','<Part object>']:
                parent.ViewObject.Visibility = True
            if str(parent) not in ['<App::Link object>']:
                VisibilityTool.showParent(parent)

    @staticmethod
    def showSelected(): #FIXME : problems to be solved with Link
        if App.ActiveDocument:
            for obj in App.ActiveDocument.Objects:
                if (str(obj) in ['<Part::PartFeature>','<body object>','<Part object>','<App::Link object>']) or (str(obj)[:13]=='<PartDesign::'):
                    obj.ViewObject.Visibility = False
            objs = Gui.Selection.getSelection()
            for obj in objs:
                obj.ViewObject.Visibility = True
                VisibilityTool.showParent(obj)

    @staticmethod
    def allVisible(): #FIXME : problems to be solved with Link
        if App.ActiveDocument:
            for obj in App.ActiveDocument.Objects:
                if str(obj) in ['<Part::PartFeature>','<body object>','<Part object>','<App::Link object>','<App::LinkElement object>','<App::LinkGroup object>'] :
                    visible = True
                    for parent in obj.InList:
                        if str(parent) == '<Part::PartFeature>':
                            visible = False
                            break
                    obj.Visibility = visible

    def mousePressEvent(self, event):
        if not Gui.ActiveDocument or str(Gui.ActiveDocument.ActiveView) != 'View3DInventor':
            event.ignore()
            super(VisibilityTool, self).mousePressEvent(event)
            return
        event.accept()
        if event.buttons() == QtCore.Qt.LeftButton:
            VisibilityTool.showSelected()
            return
        elif event.buttons() == QtCore.Qt.MidButton:
            Gui.SendMsgToActiveView('ViewFit')
            return
        elif event.buttons() == QtCore.Qt.RightButton:
            VisibilityTool.allVisible()
            return

    def wheelEvent(self, event):
        if not Gui.ActiveDocument or str(Gui.ActiveDocument.ActiveView) != 'View3DInventor':
            event.ignore()
            return
        event.accept()
        if self.wid.isVisible():
            self.wheelAngle += event.angleDelta().y()
            if self.wheelAngle >= 120:
                self.wheelAngle -= 120
                self.sli.setValue(self.sli.value() + self.sli.singleStep())
            elif self.wheelAngle <= -120:
                self.wheelAngle += 120
                self.sli.setValue(self.sli.value() - self.sli.singleStep())
        else:
            self.wheelAngle = 0
            objs = Gui.Selection.getSelection()
            if len(objs) == 0 and App.ActiveDocument:
                objs = App.ActiveDocument.Objects
            value = 100
            if objs:
                value = 95-min([obj.ViewObject.Transparency for obj in objs if hasattr(obj,'ViewObject') and hasattr(obj.ViewObject,'Transparency')])
            self.sli.setValue(value)
            self.wid.show()
            self.timer.start()

    def onSliChanged(self, value=0):
        self.timer.start()
        if value != 0:
            self.lab.setText(str(value) + " %")
            objs = Gui.Selection.getSelection()
            if len(objs) == 0 and App.ActiveDocument:
                objs = App.ActiveDocument.Objects
            for obj in objs:
                if hasattr(obj,'ViewObject') and hasattr(obj.ViewObject,'Transparency'):
                        obj.ViewObject.Transparency = 95-value

    def timerTO(self):
         if not self.sli.isSliderDown():
            self.wid.hide()
            self.timer.stop()

class statusBarWid(QtWidgets.QWidget):

    def __init__(self, buttList, parent = None):
        super(statusBarWid, self).__init__(parent)
        lay = QtWidgets.QHBoxLayout()
        for butt in buttList:
            try:
                lay.addWidget(butt[0](*butt[1], parent=self))
            except ValueError:
                pass
        lay.setContentsMargins(0,0,0,0)
        self.setLayout(lay)
