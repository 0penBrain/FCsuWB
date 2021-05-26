from PySide import QtCore, QtGui

class AboutInfo(QtCore.QObject):
    def eventFilter(self, obj, ev):
        if obj.metaObject().className() == 'Gui::Dialog::AboutDialog':
            if ev.type() == ev.ChildPolished:
                if hasattr(obj, 'on_copyButton_clicked'):
                    QtGui.QApplication.instance().removeEventFilter(self)
                    obj.on_copyButton_clicked()
                    QtCore.QMetaObject.invokeMethod(obj, 'reject', QtCore.Qt.QueuedConnection)
                    return False
                
def getFCInfo():
    ai=AboutInfo()
    QtGui.QApplication.instance().installEventFilter(ai)
    Gui.runCommand('Std_About')
    del ai
            
