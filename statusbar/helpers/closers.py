from PySide2 import QtWidgets
import FreeCADGui as Gui

dwstate = []

def saveDWState(overwrite = False):
    global dwstate
    if not dwstate or overwrite:
        dwstate = [dw for dw in Gui.getMainWindow().findChildren(QtWidgets.QDockWidget) if dw.isVisible()]

def restoreDWState(clear = True):
    global dwstate
    if dwstate:
        for dw in dwstate:
            dw.show()
        if clear:
            dwstate.clear()

def closeAllDWButCV():
    global dwstate
    dws = Gui.getMainWindow().findChildren(QtWidgets.QDockWidget)
    if len(dws) == 1 and dws[0].objectName() == 'Combo View' or dwstate:
        restoreDWState()
    else:
        saveDWState()
        for dw in dws:
            if dw.objectName() != 'Combo View':
                dw.hide()

Gui.getMainWindow().mainWindowClosed.connect(restoreDWState) #FIXME : signal is sent after window settings are saved, no signal before
