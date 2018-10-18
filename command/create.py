import adsk.core

from . import value
from . import execute

class Handler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
        
    def addValueInput( self, inputs, values ):
        default = adsk.core.ValueInput.createByReal( values.default )
        inputs.addValueInput( values.id, values.name, values.unit, default )
        
    def notify(self, args):
        # Get the command that was created.
        cmd = adsk.core.Command.cast( args.command )

        # Get the CommandInputs collection associated with the command.
        inputs = cmd.commandInputs
        inputs.addStringValueInput( value.Inputs.RootComponentName.id, value.Inputs.RootComponentName.name )

        self.addValueInput( inputs, value.Inputs.MaterialThickness )
        self.addValueInput( inputs, value.Inputs.BoxWidth )
        self.addValueInput( inputs, value.Inputs.BoxLength )
        self.addValueInput( inputs, value.Inputs.BoxHeight )

        self.executeHandler = execute.Handler()
        cmd.execute.add( self.executeHandler )