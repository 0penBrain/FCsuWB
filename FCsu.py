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
                if (str(obj) in ['<Part::PartFeature>','<body object>','<Part object>','<App::Link object>']) or (str(obj)[:13]=="<PartDesign::"):
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
            Gui.SendMsgToActiveView("ViewFit")
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

##### Dock widget font sizer

class DockWFontSizer(QtCore.QObject):

    def __init__(self, dockWidName):
        super(DockWFontSizer, self).__init__()
        self.dWid = Gui.getMainWindow().findChild(QtGui.QDockWidget, dockWidName)
        if self.dWid:
            initialPS = QtGui.QApplication.font().pointSize()
            self.font = QtGui.QFont(self.dWid.font())
            self.titleWid = QtGui.QWidget()
            lay = QtGui.QHBoxLayout()
            self.sliFS = QtGui.QSlider(QtCore.Qt.Horizontal)
            self.sliFS.setSliderPosition(initialPS)
            self.sliFS.setMaximum(initialPS)
            self.sliFS.setMinimum(int(initialPS/2))
            self.sliFS.setPageStep(1)
            self.sliFS.valueChanged.connect(self.changeFS)
            self.sliFS.sliderReleased.connect(self.changeFS)
            lay.addWidget(QtGui.QLabel("Size : "))
            lay.addWidget(self.sliFS)
            self.titleWid.setLayout(lay)
            self.timer = QtCore.QTimer(self)
            self.timer.setInterval(2500)
            self.timer.timeout.connect(self.titleBarTO)
            self.dWid.installEventFilter(self)
            setattr(self.dWid, "fontSizer", self)

    @staticmethod
    def changeFSRec(wid, fs):
        if hasattr(wid, 'font') and wid.font().pointSize() != fs and str(wid.__class__).find('QAction') == -1:
            newFont = QtGui.QFont(wid.font())
            newFont.setPointSize(fs)
            wid.setFont(newFont)
            for childWid in wid.children():
                DockWFontSizer.changeFSRec(childWid, fs)

    def changeFS(self, fs=0):
        self.timer.start()
        if fs != 0:
            DockWFontSizer.changeFSRec(self.dWid, fs)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and event.buttons() == QtCore.Qt.MidButton:
            self.dWid.setTitleBarWidget(self.titleWid)
            self.timer.start()
            return True
        else:
            return False

    def titleBarTO(self):
        if not self.sliFS.isSliderDown():
            self.dWid.setTitleBarWidget(None)
            self.timer.stop()

class AboutInfo(QtCore.QObject):
  def eventFilter(self, obj, ev):
    if obj.metaObject().className() == "Gui::Dialog::AboutDialog":
      if ev.type() == ev.ChildPolished:
        if hasattr(obj, 'on_copyButton_clicked'):
          obj.on_copyButton_clicked()
          QtGui.QApplication.instance().postEvent(obj, QtGui.QCloseEvent())
    return False

def getFCInfo():
    ai=AboutInfo()
    QtGui.QApplication.instance().installEventFilter(ai)
    Gui.runCommand("Std_About")
    QtGui.QApplication.instance().removeEventFilter(ai)
    del ai

def run():

## Set status bar helpers

    custBar = [
        [visibilityTool, []]
#        ,[custParamToggler, ['E', 'User parameter:BaseApp/Preferences/View', 'EnableSelection']]
#        ,[custParamToggler, ['E', 'User parameter:BaseApp/Preferences/View', 'EnableSelection', lambda:Gui.runCommand('Std_ExportGraphviz',0)]]
        ,[custDockToggler, ['Report view','R', Gui.getMainWindow().findChild(QtGui.QTextEdit, 'Report view').clear]]
        ,[custDockToggler, ['Python console', 'Y', Gui.getMainWindow().findChild(QtGui.QPlainTextEdit, 'Python console').onClearConsole]]
        ,[custDockToggler, ['Combo View', 'C', getFCInfo]]
        ,[custDockToggler, ['Selection view', 'S']]
        ,[custDockToggler, ['Property view', 'P']]
        ,[custDockToggler, ['Tree view', 'T']]
        ,[custCmdRunner, ['D', ['Std_DependencyGraph',0]]]
    ]

    for wid in Gui.getMainWindow().findChildren(QtGui.QWidget, "fcsu"):
        wid.deleteLater()
    
    ctb = statusBarWid(custBar)
    ctb.setObjectName("fcsu")
    Gui.getMainWindow().statusBar().addPermanentWidget(ctb)
    Gui.getMainWindow().statusBar().setVisible(True)

## Set Dock widgets font sizers

    for dwid in Gui.getMainWindow().findChildren(QtGui.QDockWidget):
        DockWFontSizer(dwid.objectName())

if __name__ == '__main__':
    run()
