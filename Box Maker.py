#Author-Daniel Neve
#Description-

import adsk.core, traceback
from .command import command

_cmd = command.Command()
        
def run(context):
    try:
        global _app, _ui
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        global _cmd
        _cmd.Start()
        
    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        global _cmd, _ui
        _cmd.Stop()

    except:
        if _ui:
            _ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
