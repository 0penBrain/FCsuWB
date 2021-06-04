from PySide2 import QtWidgets
import FreeCADGui as Gui

def closeAllDWButCV():
    for dwid in Gui.getMainWindow().findChildren(QtWidgets.QDockWidget):
        if dwid.objectName() != 'Combo View':
            dwid.hide()
