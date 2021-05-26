from PySide import QtGui, QtCore
import FreeCAD as App
import FreeCADGui as Gui

##### Status bar helper

class custToolButton(QtGui.QToolButton):

    def __init__(self, text='', midButFunc = None, rightButFunc = None, parent = None):
        self.custText = text
        super(custToolButton, self).__init__(parent)
        self.resetText()
        self.midButFunc = midButFunc
        self.rightButFunc = rightButFunc

    def resetText(self):
        self.setText(self.custText)

    def actionEvent(self, event):
        super(custToolButton, self).actionEvent(event)
        self.resetText()

    def setDefaultAction(self, action):
        super(custToolButton, self).setDefaultAction(action)
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
            return super(custToolButton, self).mousePressEvent(event)

class custDockToggler(custToolButton):

    def __init__(self, dock, text, midButFunc = None, rightButFunc = None, parent = None):
        if not not Gui.getMainWindow().findChild(QtGui.QDockWidget, dock):
            super(custDockToggler, self).__init__(text, midButFunc, rightButFunc, parent)
            self.setDefaultAction(Gui.getMainWindow().findChild(QtGui.QDockWidget, dock).toggleViewAction())
        else:
            raise ValueError('Widget not found')

class custFuncRunner(custToolButton):

    def __init__(self, text, func, funcArgs = [], midButFunc = None, rightButFunc = None, parent = None):
        super(custFuncRunner, self).__init__(text, midButFunc, rightButFunc, parent)
        self.func = func
        self.funcArgs = funcArgs
        act = QtGui.QAction(text)
        act.triggered.connect(self.runFunc)
        self.setDefaultAction(act)

    def runFunc(self):
        self.func(*self.funcArgs)

class custCmdRunner(custFuncRunner):

    def __init__(self, text, cmdArgs, midButFunc = None, rightButFunc = None, parent = None):
        super(custCmdRunner, self).__init__(text, Gui.runCommand, cmdArgs, midButFunc, rightButFunc, parent)

class custParamToggler(custFuncRunner):

    def __init__(self, text, group, param, midButFunc = None, rightButFunc = None, parent = None):
        super(custParamToggler, self).__init__(text, group, param, midButFunc, rightButFunc, parent)
        self.defaultAction().setCheckable(True)
        self.defaultAction().setChecked(App.ParamGet(group).GetBool(param, True))

    def runFunc(self, state):
        App.ParamGet(self.func).SetBool(self.funcArgs, state)

class visibilityTool(custToolButton):

    def __init__(self, text='V', parent = None):
        super(visibilityTool, self).__init__(text, parent = parent)
        lay = QtGui.QVBoxLayout()
        QtGui.QLayout.setAlignment(lay, QtCore.Qt.AlignHCenter)
        self.wid = QtGui.QWidget(Gui.getMainWindow())
        self.wid.hide()
        self.wid.setLayout(lay)
        self.lab = QtGui.QLabel("100 %")
        lay.addWidget(self.lab)
        self.sli = QtGui.QSlider(QtCore.Qt.Orientation.Vertical)
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
        self.wid.move(self.mapTo(self.wid.parent(),QtCore.QPoint(0,0)) - QtCore.QPoint(self.wid.width()/2-self.width()/2, self.wid.height()))
        self.wid.update()
        return super(visibilityTool, self).paintEvent(event)

    @staticmethod
    def showParent(child):
        for parent in child.InList:
            if str(parent) in ['<body object>','<Part object>']:
                parent.ViewObject.Visibility = True
            if str(parent) not in ['<App::Link object>']:
                visibilityTool.showParent(parent)

    @staticmethod
    def showSelected():
        if App.ActiveDocument:
            for obj in App.ActiveDocument.Objects:
                if (str(obj) in ['<Part::PartFeature>','<body object>','<Part object>','<App::Link object>']) or (str(obj)[:13]=='<PartDesign::'):
                    obj.ViewObject.Visibility = False
            objs = Gui.Selection.getSelection()
            for obj in objs:
                obj.ViewObject.Visibility = True
                visibilityTool.showParent(obj)

#    @staticmethod
#    def allVisible():
#        if App.ActiveDocument:
#            for obj in App.ActiveDocument.Objects:
#                if len(obj.InList) == 0           : 
#                    visible = True
#                else:
#                    visible = False
#                for parent in obj.InList:
#                    if str(parent) == '<Part::PartFeature>':
#                        visible = False
#                        break
#                    if str(parent) == '<Part object>':
#                        visible = True
#                if (str(obj) in ['<Part::PartFeature>','<body object>','<Part object>','<App::Link object>']):
#                    obj.ViewObject.Visibility = visible

    @staticmethod
    def allVisible():
        if App.ActiveDocument:
            for obj in App.ActiveDocument.Objects:
                if str(obj) in ['<Part::PartFeature>','<body object>','<Part object>','<App::Link object>','<App::LinkElement object>','<App::LinkGroup object>'] :
                    print(obj.Name)
                    visible = True
                    for parent in obj.InList:
                        if str(parent) == '<Part::PartFeature>':
                            visible = False
                            break
                    print(visible)
                    obj.Visibility = visible

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            visibilityTool.showSelected()
            return True
        elif event.buttons() == QtCore.Qt.MidButton:
            Gui.SendMsgToActiveView('ViewFit')
            return True
        elif event.buttons() == QtCore.Qt.RightButton:
            visibilityTool.allVisible()
            return True
        return super(visibilityTool, self).mousePressEvent(event)

    def wheelEvent(self, event):
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
            self.wid.show()
            self.timer.start()
        return True

    def onSliChanged(self, value=0):
        self.timer.start()
        if value != 0:
            self.lab.setText(str(value) + " %")
            objs = Gui.Selection.getSelection()
            if len(objs) == 0 and App.ActiveDocument:
                objs = App.ActiveDocument.Objects
            for obj in objs:
                if hasattr(obj,'ViewObject'):
                    if hasattr(obj.ViewObject,'Transparency'):
                        obj.ViewObject.Transparency = 95-value

    def timerTO(self):
         if not self.sli.isSliderDown():
            self.wid.hide()
            self.timer.stop()

class statusBarWid(QtGui.QWidget):

    def __init__(self, buttList):
        super(statusBarWid, self).__init__()
        lay = QtGui.QHBoxLayout()
        for butt in buttList:
            try:
                lay.addWidget(butt[0](*butt[1], parent=self))
            except ValueError:
                pass
        lay.setContentsMargins(0,0,0,0)
        self.setLayout(lay)
        
import defaultcfg
config = defaultcfg.cfg
try:
    import usercfg
    config.update(usercfg.cfg)
except ModuleNotFoundError:
    App.Console.PrintLog("No user configuration, using default\n")

for wid in Gui.getMainWindow().findChildren(QtGui.QWidget, 'fcsu'):
    wid.deleteLater()

if config['custBarEnabled']:
    from statusbar.helpers import *
    custBar = eval(config['custBar'])
    ctb = statusBarWid(custBar)
    ctb.setObjectName('fcsu')
    Gui.getMainWindow().statusBar().addPermanentWidget(ctb)
    Gui.getMainWindow().statusBar().setVisible(True)
    
if config['fontSizerEnabled']:
    from fontsizer import *
    for dwid in Gui.getMainWindow().findChildren(QtGui.QDockWidget):
        fontsizer.DockWFontSizer(dwid.objectName())
