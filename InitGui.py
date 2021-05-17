import FreeCADGui as Gui
import FreeCAD as App

def run_FCsu(name):
    if name != "NoneWorkbench": #Dock widgets aren't created in None WB
        # run this function only once
        Gui.getMainWindow().workbenchActivated.disconnect(run_FCsu)
        App.Console.PrintMessage("FC_SU macro is enabled")
        import FCsu
        FCsu.run()

# this is important because InitGui.py files are passed to the exec() function
# and the runMacro wouldn't be visible outside. So explicitly add it to __main__
import __main__
__main__.run_FCsu = run_FCsu

# connect the function with the workbenchActivated signal
Gui.getMainWindow().workbenchActivated.connect(run_FCsu)
