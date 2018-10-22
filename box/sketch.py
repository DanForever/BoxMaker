
import adsk.core

import math

from . import utility

class Sketch():
	def __init__( self ):
		self.parent = None
		self.sketch = None
		
		self.x = 0
		self.y = 0
		
		self.mainProfile = None
		self.profilesToIgnore = []
		self.profilesToExtrude = []
		
		self.centresToIgnore = []
		self.centresToExtrude = []
		
	def GetProfilesToExtrude( self ):
		profiles = adsk.core.ObjectCollection.create()
		
		profiles.add( self.mainProfile )
		
		for profile in self.profilesToExtrude:
			profiles.add( profile )
		
		return profiles
	
	def _AnalyseProfiles( self ):
		self.mainProfile = None
		self.profilesToIgnore = []
		self.profilesToExtrude = []
		
		for i in range( self.sketch.profiles.count ):
			profile = self.sketch.profiles.item( i )
			areaProperties = profile.areaProperties()
			
			centreX = areaProperties.centroid.x
			centreY = areaProperties.centroid.y
			centre = ( centreX, centreY )
			
			if utility.IsXYInList( centre, self.centresToExtrude ):
				self.profilesToExtrude.append( profile )
				print( "Found profile for extrude: {}".format( centre ) )
				
			elif not utility.IsXYInList( centre, self.centresToIgnore ):
				self.mainProfile = profile
				print( "Found main profile: {}".format( centre ) )
				
			else:
				print( "Ignored profile {}".format( centre ) )
		
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
			
	def _CreateTabs( self, length, height, xCount, yCount, xOffset = 0, yOffset = 0 ):
		x = 0
		for i in range( xCount ):
			y = 0
			for j in range( yCount ):
				x = i * length + xOffset
				x2 = x + length
				
				y = j * height + yOffset
				y2 = y + height
				
				start = adsk.core.Point3D.create( x, y, 0 )
				end = adsk.core.Point3D.create( x2, y2, 0 )
				
				self.sketch.sketchCurves.sketchLines.addTwoPointRectangle( start, end )
				
				centreX = ( start.x + end.x ) / 2
				centreY = ( start.y + end.y ) / 2
				centre = ( centreX, centreY )
				
				# We are only interested in extruding every other tab (so ignore evens)
				if xCount > 1 and i % 2 != 0:
					self.centresToExtrude.append( centre )
					print( "Added Tab {} along X with centre {}".format( i, centre ) )
				elif yCount > 1 and j % 2 != 0:
					self.centresToExtrude.append( centre )
					print( "Added Tab {} along Y with centre {}".format( j, centre ) )
				else:
					self.centresToIgnore.append( centre )
		
	def AddTabsAlongBottom( self, materialThickness ):
		count, length = self._CalculateTabLength( self.x )
		self._CreateTabs( length, materialThickness, count, 1 )
		
		self._AnalyseProfiles()
		
	def AddTabsAlongBottomAndSides( self, materialThickness ):
		bCount, bLength = self._CalculateTabLength( self.x )
		self._CreateTabs( bLength, materialThickness, bCount, 1 )
		
		sCount, sLength = self._CalculateTabLength( self.y - materialThickness )
		self._CreateTabs( materialThickness, sLength, 1, sCount, yOffset = materialThickness )
		
		sCount, sLength = self._CalculateTabLength( self.y - materialThickness )
		self._CreateTabs( materialThickness, sLength, 1, sCount, xOffset = self.x - materialThickness, yOffset = materialThickness )
		
		self._AnalyseProfiles()