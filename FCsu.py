from PySide2 import QtWidgets
import FreeCAD as App
import FreeCADGui as Gui
        
import defaultcfg
config = defaultcfg.cfg
try:
    import usercfg
    config.update(usercfg.cfg)
except ModuleNotFoundError:
    App.Console.PrintLog("No user configuration, using default\n")

for wid in Gui.getMainWindow().findChildren(QtWidgets.QWidget, 'fcsu'):
    wid.deleteLater()
    
if config['clearNavIndictor']:
    Gui.getMainWindow().statusBar().findChild(QtWidgets.QPushButton, 'NavigationIndicator').deleteLater()

if config['custBarEnabled']:
    from statusbar.helpers import *
    from statusbar.widgets import *
    custBar = eval(config['custBar'])
    ctb = sbwidget.statusBarWid(custBar, Gui.getMainWindow().statusBar())
    ctb.setObjectName('fcsu')
    Gui.getMainWindow().statusBar().addPermanentWidget(ctb)
    Gui.getMainWindow().statusBar().setVisible(True)

if config['windowSplitterEnabled']:
    from windowsplitter import winsplit

if config['fontSizerEnabled']:
    from fontsizer import fontsizer
    for dwid in Gui.getMainWindow().findChildren(QtWidgets.QDockWidget):
        fontsizer.DockWFontSizer(dwid.objectName())
