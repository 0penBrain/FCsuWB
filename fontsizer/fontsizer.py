from PySide import QtCore, QtGui
import FreeCADGui as Gui

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
            setattr(self.dWid, 'fontSizer', self)

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
