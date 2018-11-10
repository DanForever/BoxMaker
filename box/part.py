import copy

import adsk.core

from . import sketch
from . import body
from . import utility

class Part():
	def __init__( self ):
		self.parent = None
		self.occurrence = None
		self.component = None
		
		self.sketch = None
		self.body = None

	def Clone( self ):
		clone = copy.copy( self )
		
		clone.isClone = True
		
		transform = adsk.core.Matrix3D.create()
		clone.occurrence = self.parent.occurrences.addExistingComponent( self.component, transform )
		clone.component = clone.occurrence.component
		
		return clone
		
	def Cut( self, target ):
		
		print( "Cutting {} from {}".format( self.occurrence.name, target.occurrence.name ) )
		
		targetBody = target.component.bRepBodies.item( 0 ).createForAssemblyContext( target.occurrence )
		
		tools = adsk.core.ObjectCollection.create()
		tool = self.component.bRepBodies.item(0).createForAssemblyContext( self.occurrence )
		tools.add( tool )
		
		input = self.parent.features.combineFeatures.createInput( targetBody, tools )
		input.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
		input.isKeepToolBodies = True
		
		cut = self.parent.features.combineFeatures.add( input )
		cut.name = "Cut {} from {}".format( self.occurrence.name, target.occurrence.name )

class Base( Part ):
	def __init__( self ):
		Part.__init__( self )
		
	def Create( self, parent, parameters ):
		self.parent = parent
		
		self.occurrence = utility.CreateComponent( self.parent, "Base" )
		self.component = self.occurrence.component
		
		constructionPlane = self.parent.xZConstructionPlane
		
		self.sketch = sketch.Sketch()
		self.sketch.Create( self.component, constructionPlane, parameters.width, parameters.length )
		
		self.body = body.Body()
		self.body.Extrude( self.component, self.sketch, parameters.materialThickness )
		
class Side( Part ):
	def __init__( self ):
		Part.__init__( self )
		
	def Create( self, parent, parameters ):
		self.parent = parent
		
		self.occurrence = utility.CreateComponent( self.parent, "Side" )
		self.component = self.occurrence.component
		
		constructionPlane = self.parent.yZConstructionPlane
		
		self.sketch = sketch.Sketch()
		self.sketch.Create( self.component, constructionPlane, parameters.length, parameters.height )
		self.sketch.AddTabsAlongBottom( parameters.materialThickness )
		
		self.body = body.Body()
		self.body.Extrude( self.component, self.sketch, parameters.materialThickness )

class Top( Part ):
	def __init__( self ):
		Part.__init__( self )
		
	def Create( self, parent, parameters ):
		self.parent = parent
		
		self.occurrence = utility.CreateComponent( self.parent, "Top" )
		self.component = self.occurrence.component
		
		constructionPlane = self.parent.xYConstructionPlane
		
		self.sketch = sketch.Sketch()
		self.sketch.Create( self.component, constructionPlane, parameters.width, parameters.height )
		self.sketch.AddTabsAlongBottomAndSides( parameters.materialThickness )
		
		self.body = body.Body()
		self.body.Extrude( self.component, self.sketch, -parameters.materialThickness )
		