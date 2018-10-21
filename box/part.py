import adsk.core

from . import sketch
from . import body
from . import utility

class Base():
	def __init__( self ):
		self.parent = None
		self.component = None
		
		self.sketch = None
		self.body = None
		
	def Create( self, parent, parameters ):
		self.parent = parent
		
		self.component = utility.CreateComponent( self.parent, "Base" )
		
		constructionPlane = self.component.xZConstructionPlane
		
		self.sketch = sketch.Sketch()
		self.sketch.Create( self.component, constructionPlane, parameters.width, parameters.length )
		
		self.body = body.Body()
		self.body.Extrude( self.component, self.sketch, parameters.materialThickness )
		
class Side():
	def __init__( self ):
		self.parent = None
		self.component = None
		
		self.sketch = None
		self.body = None
		
	def Create( self, parent, parameters ):
		self.parent = parent
		
		self.component = utility.CreateComponent( self.parent, "Side" )
		
		constructionPlane = self.component.yZConstructionPlane
		
		self.sketch = sketch.Sketch()
		self.sketch.Create( self.component, constructionPlane, parameters.length, parameters.height )
		self.sketch.AddTabsAlongBottom( parameters.materialThickness )
		
		self.body = body.Body()
		self.body.Extrude( self.component, self.sketch, parameters.materialThickness )
		
	def Clone( self ):
		side = Side()
		
		side.parent = self.parent
		side.sketch = self.sketch
		self.body = self.body
		
		transform = adsk.core.Matrix3D.create()
		side.component = self.parent.occurrences.addExistingComponent( self.component, transform )
		
		return side