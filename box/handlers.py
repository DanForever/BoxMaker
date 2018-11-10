import adsk.core

from . import value
from . import part
from . import joint
from . import utility

# Event handler for the execute event.
class Execute( adsk.core.CommandEventHandler ):
	def __init__( self ):
		super().__init__()
	
	def notify( self, args ):
		try:
			eventArgs = adsk.core.CommandEventArgs.cast( args )
			inputs = eventArgs.command.commandInputs

			# Grab the design object (from which we can access the component hierarchy)
			app = adsk.core.Application.get()
			product = app.activeProduct
			design = adsk.fusion.Design.cast( product )
			
			parameters 						= value.Parameters()
			parameters.name 				= inputs.itemById( value.Inputs.RootComponentName.id ).value
			parameters.width 				= inputs.itemById( value.Inputs.BoxWidth.id ).value
			parameters.length 				= inputs.itemById( value.Inputs.BoxLength.id ).value
			parameters.height 				= inputs.itemById( value.Inputs.BoxHeight.id ).value
			parameters.materialThickness 	= inputs.itemById( value.Inputs.MaterialThickness.id ).value
			
			root = utility.CreateComponent( design.activeComponent, parameters.name ).component
			
			print( "\nCreating Base:" )
			base = part.Base()
			base.Create( root, parameters )
			
			adsk.doEvents()
			
			print( "\nCreating Side:" )
			side = part.Side()
			side.Create( root, parameters )
			joint.Join( root, base, side, adsk.core.Point3D.create( 0, 0, 1 ) )
			
			adsk.doEvents()
			
			print( "\nCreating Side2:" )
			side2 = side.Clone()
			offset = ( parameters.width - parameters.materialThickness )
			joint.Join( root, side2, side, adsk.core.Point3D.create( 1, 0, 0 ), offset )
			
			adsk.doEvents()
			
			print( "\nCreating Top:" )
			top = part.Top()
			top.Create( root, parameters )
			joint.Join( root, base, top, adsk.core.Point3D.create( 1, 0, 0 ) )
			
			adsk.doEvents()
			
			print( "\nCreating Top2:" )
			top2 = top.Clone()
			offset = ( parameters.length - parameters.materialThickness )
			joint.Join( root, top2, top, adsk.core.Point3D.create( 0, 0, 1 ), offset )
			
			adsk.doEvents()
			
			#Cut the parts out of each other
			# Currently bugged, not sure why (works if the parent component is the document root)
			top.Cut( base )
			top.Cut( side )
			
			top2.Cut( base )
			top2.Cut( side )
			
			side.Cut( base )
			side2.Cut( base )
			
		except:
			import traceback
			print( 'Execute.Notify() Exception:\n{}'.format( traceback.format_exc() ) )

class Create(adsk.core.CommandCreatedEventHandler):
	def __init__( self ):
		super().__init__()

	def addValueInput( self, inputs, values ):
		default = adsk.core.ValueInput.createByReal( values.default )
		inputs.addValueInput( values.id, values.name, values.unit, default )

	def notify( self, args ):
		try:
			# Get the command that was created.
			cmd = adsk.core.Command.cast( args.command )
			
			cmd.isExecutedWhenPreEmpted = False
			cmd.okButtonText = "Create Box"
			
			# Get the CommandInputs collection associated with the command.
			inputs = cmd.commandInputs
			inputs.addStringValueInput( value.Inputs.RootComponentName.id, value.Inputs.RootComponentName.name )
			
			self.addValueInput( inputs, value.Inputs.MaterialThickness )
			self.addValueInput( inputs, value.Inputs.BoxWidth )
			self.addValueInput( inputs, value.Inputs.BoxLength )
			self.addValueInput( inputs, value.Inputs.BoxHeight )
			
			self.executeHandler = Execute()
			cmd.execute.add( self.executeHandler )
			
		except:
			import traceback
			print( 'Create.Notify() Exception:\n{}'.format( traceback.format_exc() ) )