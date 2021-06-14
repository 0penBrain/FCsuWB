from PySide2 import QtWidgets, QtCore
import FreeCADGui as Gui

#FIXME The context menu is offset when scaler is enabled

class SSSManager(QtCore.QObject):

    class SSScaler(QtCore.QObject):

        class SSSGv(QtWidgets.QGraphicsView):

            scaleChanged = QtCore.Signal(float)

            def __init__(self, wid, parent = None):
                super(SSSManager.SSScaler.SSSGv, self).__init__(parent)
                gs = QtWidgets.QGraphicsScene(self)
                self.wid = QtWidgets.QGraphicsProxyWidget()
                self.wid.setWindowFlags(QtCore.Qt.BypassGraphicsProxyWidget)
                self.wid.setFlag(QtWidgets.QGraphicsItem.ItemClipsChildrenToShape, True)
#                self.wid.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
                self.wid.setWidget(wid)
                gs.addItem(self.wid)
                self.setScene(gs)
                self.show()
                self.wheelAngle = 0

            def resizeEvent(self, ev = None):
                if ev:
                    super(SSSManager.SSScaler.SSSGv, self).resizeEvent(ev)
                self.setSceneRect(QtCore.QRect(0, 0, self.frameGeometry().width()-2*self.frameWidth(), self.frameGeometry().height()-2*self.frameWidth()))
                self.wid.setGeometry(QtCore.QRect(0, 0, self.sceneRect().width()/self.wid.scale(), self.sceneRect().height()/self.wid.scale()))

            def wheelEvent(self, ev):
                if ev.modifiers() == QtCore.Qt.ControlModifier:
                    ev.accept()
                    self.wheelAngle += ev.angleDelta().y()
                    scale = 0
                    if self.wheelAngle >= 120:
                        self.wheelAngle = self.wheelAngle % 120
                        if self.wid.scale() < 1.5:
                            scale = self.wid.scale() + 0.1
                    elif self.wheelAngle <= -120:
                        self.wheelAngle = (self.wheelAngle + 119) % 120 - 119
                        if self.wid.scale() > 0.5:
                            scale = self.wid.scale() - 0.1
                    if scale != 0:
                        self.scaleChanged.emit(scale)
                    return
                else:
                    self.wheelAngle = 0
                ev.ignore()
                super(SSSManager.SSScaler.SSSGv, self).wheelEvent(ev)

        def __init__(self, sw):
            super(SSSManager.SSScaler, self).__init__(sw)
            tv = sw.findChild(QtWidgets.QTableView)
            tvp = tv.parent()
            tvidx = tvp.layout().indexOf(tv)
            tv.setParent(None)
            self.gv = SSSManager.SSScaler.SSSGv(tv, tvp)
            tvp.layout().insertWidget(tvidx, self.gv)
            self.sli = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, tv)
            self.sli.setRange(5,15)
            self.sli.setValue(10)
            self.sli.setSingleStep(1)
            self.sli.setPageStep(1)
            self.sli.valueChanged.connect(self.onSliChange)
            self.gv.scaleChanged.connect(self.onScaleChange)
            Gui.getMainWindow().statusBar().addWidget(self.sli)
            self.sli.show()
            Gui.getMainWindow().centralWidget().subWindowActivated.connect(self.onSWChange)
            sw.setProperty('sssclr', 'running')
            self.destroyed.connect(self.sli.deleteLater)

        def onScaleChange(self,scale):
            self.sli.setValue(round(scale*10))

        def onSliChange(self, value):
            self.gv.wid.setScale(value/10)
            self.gv.resizeEvent()

        def onSWChange(self, sw):
            if sw == self.parent():
                self.sli.show()
            else:
                self.sli.hide()

    def __new__(cls, *args):
        if not hasattr(Gui.getMainWindow(), 'sssmgr'):
            return super().__new__(cls)
        else:
            return None

    def __init__(self, parent = None):
        super(SSSManager, self).__init__(parent)
        Gui.getMainWindow().centralWidget().subWindowActivated.connect(self.onSWChange)
        setattr(Gui.getMainWindow(), 'sssmgr', self)
        self.onSWChange(Gui.getMainWindow().centralWidget().activeSubWindow())

    def onSWChange(self, sw):
        if sw and sw.widget().metaObject().className() == 'SpreadsheetGui::SheetView' and not sw.property('sssclr'):
            SSSManager.SSScaler(sw)

SSSManager(Gui.getMainWindow())
