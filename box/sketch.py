
import adsk.core

import math

class Sketch():
	def __init__( self ):
		self.parent = None
		self.sketch = None
		
		self.x = 0
		self.y = 0
		
		self.mainProfile = None
		self.lowerTabProfiles = []
		
		self.lowerTabHeight = 0
		self.lowerTabCentres = []
		
	def GetProfilesToExtrude( self ):
		profiles = adsk.core.ObjectCollection.create()
		
		profiles.add( self.mainProfile )
		
		for profile in self.lowerTabProfiles:
			profiles.add( profile )
		
		return profiles
		
	def Create( self, parent, constructionPlane, x, y ):
		
		self.parent = parent
		self.x = x
		self.y = y
		
		startPoint = adsk.core.Point3D.create( 0, 0, 0 )
		endPoint = adsk.core.Point3D.create( x, y, 0 )
		
		self.sketch = self.parent.sketches.add( constructionPlane )
		self.sketch.sketchCurves.sketchLines.addTwoPointRectangle( startPoint, endPoint )
		
		# At this point, all we've done is create a rectangle, and if we leave it at that
		# (Which we do if this is the base of the box), then that whole rectangle is what we
		# want to extrude.
		profile = self.sketch.profiles.item( 0 )
		self.mainProfile = profile
		
	def _CalculateTabLength( self, length ):
		maxSize = 2
		tabCount = 1
		tabSize = maxSize + 1
		
		while( tabSize > maxSize ):
			tabCount += 2
			tabSize = length / tabCount
			
		return tabCount, tabSize
	
	def _ExtractMainProfile( self ):
		lowerTabCentreY = self.lowerTabHeight / 2
		
		for i in range( self.sketch.profiles.count ):
			profile = self.sketch.profiles.item( i )
			areaProperties = profile.areaProperties()
			middleX = areaProperties.centroid.x
			middleY = areaProperties.centroid.y
			
			if not math.isclose( middleY, lowerTabCentreY ):
				self.mainProfile = profile
				return
	
	def _ExtractTabProfiles( self ):
		targetCentreY = self.lowerTabHeight / 2
		
		for i in range( self.sketch.profiles.count ):
			profile = self.sketch.profiles.item( i )
			areaProperties = profile.areaProperties()
			middleX = areaProperties.centroid.x
			middleY = areaProperties.centroid.y
			
			if math.isclose( middleY, targetCentreY ):
				for targetCentreX in self.lowerTabCentres:
					if math.isclose( middleX, targetCentreX ):
						self.lowerTabProfiles.append( profile )
						break
		
	def _CreateTabs( self, count, length, height ):
		self.lowerTabHeight = height
		x = 0
		
		for i in range( count ):
			x2 = x + length
			
			start = adsk.core.Point3D.create( x, 0, 0 )
			end = adsk.core.Point3D.create( x2, height, 0 )
			
			self.sketch.sketchCurves.sketchLines.addTwoPointRectangle( start, end )
			
			print( "Added Tab X:{} Y:{} -> X:{} Y:{}".format( x, 0, x2, height ) )
			
			# We are only interested in extruding every other tab (so ignore evens)
			if i % 2 != 0:
				centre = ( start.x + end.x ) / 2
				self.lowerTabCentres.append( centre )
				print( "Tab stored with a centre of: {}".format( centre ) )
			
			x = x2
		
	def AddTabsAlongBottom( self, height ):
		
		count, length = self._CalculateTabLength( self.x )
		self._CreateTabs( count, length, height )
		
		self._ExtractMainProfile()
		self._ExtractTabProfiles()