#!/usr/bin/env python3
'''
	implementation of FORTUNES algorithm with extensive depiction of how data is handled
	this is a prepartion to verify own algorithms in C++
	
	the program is interactive and uses tkinter for gui
'''

import os, traceback, inspect
import math, re

import tkinter as tk 
from PIL import Image, ImageTk

from seqDiagram import SeqDiagram

fontCanvas=("Ubuntu Mono", 12, "normal")

seqDiagram = SeqDiagram()

def formatFloatOrNone(f):
	result = "-"
	if f != None:
		result = "{:.2f}".format(f)
	return result

def circle(s0,s1,s2):
	'''
		calculates a circle based on 3 points (have to be passed as site-objects)
		returns the center of the circle and the radius
	'''
	seqDiagram.call()
	x0,y0 = s0.getX(), s0.getY()
	x1,y1 = s1.getX(), s1.getY()
	x2,y2 = s2.getX(), s2.getY()
	k1x = 2 * (x1 - x0)
	k1y = 2 * (y1 - y0)
	k2x = 2 * (x2 - x0)
	k2y = 2 * (y2 - y0)
	k1 = x1 * x1 + y1 * y1 - x0 * x0 - y0 * y0
	k2 = x2 * x2 + y2 * y2 - x0 * x0 - y0 * y0
	mx,my,r = math.nan, math.nan, math.nan
	m = k1x * k2y - k2x * k1y
	if (m == 0):
		# all three points are on a line
		pass
	else:
		mx = k1 * k2y - k2 * k1y
		my = k1x * k2 - k2x * k1
		mx /= m
		my /= m
		d0x, d0y = x0 - mx, y0 - my
		d1x, d1y = x1 - mx, y1 - my
		d2x, d2y = x2 - mx, y2 - my
		r = math.sqrt(d0x*d0x + d0y*d0y)
		# print (mx,my, math.sqrt(d0x*d0x + d0y*d0y), math.sqrt(d1x*d1x + d1y*d1y), math.sqrt(d2x*d2x + d2y*d2y))
	# seqDiagram.comment(formatFloatOrNone(x0) + "," + formatFloatOrNone(y0) + "\\t" + formatFloatOrNone(x1) + "," + formatFloatOrNone(y1) + "\\t" + formatFloatOrNone(x2) + "," + formatFloatOrNone(y2) + "\\nCenter:" + formatFloatOrNone(mx) + "," + formatFloatOrNone(my) + ", radius:"  + formatFloatOrNone(r))
	return mx,my,r

def arcCircle(p):
	'''
		calculates the circle based on the arcs
	'''
	seqDiagram.call()
	return circle(p[0].getSite(),p[1].getSite(),p[2].getSite())

class MCanvas:
	'''
		the graphical display
		a thin wrapper that recalculate coordinate-values from 0-100 to the actual size of the canvas
	'''
	def __init__(self,canvas):
		seqDiagram.call()
		self.canvas = canvas
		self.canvasSize = 10
		self.sizeW = 50
		self.sizeH = 50
		self.sweepline = None
	
	def resize(self, outerY, outerX):
		seqDiagram.call(y=outerY, x=outerX)
		self.canvasSize = min(outerX, outerY) - 10
		self.sizeH, self.sizeW = self.canvasSize, self.canvasSize
		self.canvas.config(width=self.sizeW, height=self.sizeH)
		seqDiagram.comment("set Canvas to height: " + str(self.sizeH))

	def xy(self,y,x):
		# seqDiagram.call(y=y, x=x)
		nx = x / 100 * (self.canvasSize - 10) + 5
		ny = y / 100 * (self.canvasSize - 10) + 5
		# print (y,x,ny,nx)
		# seqDiagram.ret(ny=ny,nx=nx)
		return ny,nx

	def drawSweepline(self, d):
		seqDiagram.call(d=d)
		if self.sweepline == None:
			self.sweepline = self.canvas.create_line(1, 1, 50, 50, width=2, fill="#000", activefill = "#f00", tags=('sweepline'))
		displaySweepline = d * self.sizeW / 100
		self.canvas.coords(self.sweepline, displaySweepline, 10, displaySweepline, self.sizeH - 10)

	def clear(self):
		seqDiagram.call()
		self.canvas.delete("arc")

	def drawSite(self, site):
		seqDiagram.call(site=site)
		x,y = self.xy(site.getX() , site.getY())
		self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="#000", fill="#8cf", width=2, tags=('sites'))

	def drawArc(self,arc):
		pass

	def drawPolygon(self,polygon,mode=0):
		seqDiagram.call()
		line = []
		first = True
		for i in range(len(polygon) - 1):
			p1x,p1y = self.xy(polygon[i][0],polygon[i][1])
			p2x,p2y = self.xy(polygon[i+1][0],polygon[i+1][1])
			if p1x >= 0 or p2x >= 0:
				if first:
					line.extend([p1x,p1y])
					first = False
				line.extend([p2x,p2y])
		# print (line)
		width,fill=1,"#44f"
		self.canvas.create_line(*line, width=width, fill=fill, activefill = "#f00", tags=('arc'))

	def drawCircle(self, x,y,r, outline="#cef"):
		seqDiagram.call()
		lx,ly = self.xy(x - r, y - r)
		ux,uy = self.xy(x + r, y + r)
		self.canvas.create_oval(lx,ly,ux,uy, outline=outline, fill="", width=5, tags=('circle'))
		kx,ky = self.xy(x,y)
		# center of the circle
		self.canvas.create_oval(kx-7,ky-7,kx+7,ky+7, outline="#000", fill="#fa6", width=1, tags=('circle'))

class Site:
	'''
		basic data
		this denotation is common for fortunes algorithm
		so you can look up the description of this class in any explanation of fortunes algorithm
	'''
	nextSiteId = 0
	def __init__(self,y,x):
		seqDiagram.call(y=y,x=x)
		self.id = Site.nextSiteId
		self.x = x
		self.y = y
		self.neighbor = []
		Site.nextSiteId += 1

	def getId(self):
		return self.id

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def __str__(self):
		# return "[" + str(self.x) + "," + str(self.y) + "]"
		return "[" + str(self.id) + "]"

	def draw(self,canvas,d):
		seqDiagram.call(d=d)
		seqDiagram.comment(str(self))
		# print ("Site.draw\t", self)
		canvas.drawSite(self)
		if self.x < d:
			polygon = []
			# for i in range(-amountPoints,amountPoints):
			for y in range(0,101,1):
				# das ist die zentrale Formel für die beachline eines Punktes Py,Px zur Beachline d
				x=(self.y*self.y + self.x*self.x + y*y - 2*y*self.y - d*d) / (2*self.x - 2*d)
				polygon.append([x,y])
				# line.extend(canvas.xy(x,y))
				# print (line)
			# seqDiagram.comment("polygon:" + str(polygon))
			canvas.drawPolygon(polygon)
		py,px = canvas.xy(self.y,self.x)
		canvas.canvas.create_text(px+15,py,fill="#060",font=fontCanvas, text=str(self.id), tags=('sites'))

	def dist(self,y,d):
		seqDiagram.call(y=y,d=d)
		# calculate the distance to the arc
		# y is the point of the y-axis where the arc is calculated
		# d is the sweepline
		dist = math.nan
		q = 2*self.getX() - 2*d
		if q != 0:
			dist = d - (self.getY()*self.getY() + self.getX()*self.getX() + y*y - 2*y*self.getY() - d*d) / q
		seqDiagram.ret(dist=dist)
		return dist
		
	def __lt__(self, other):
		result = other.getX() - self.getX() > 0
		if other.getX() == self.getX():
			result = other.getY() - self.getY() > 0
		return result

class Sites:
	def __init__(self):
		seqDiagram.call()
		self.sites = []

	def add(self, y, x):
		seqDiagram.call(y=y,x=x)
		self.sites.append(Site(y,x))

	def __getitem__(self, key):
		return self.sites[key]

	def __len__(self):
		return self.sites.__len__()

	def sort(self):
		return self.sites.__len__()

	def draw(self, canvas):
		seqDiagram.call()
		# print ("Sites.draw")
		canvas.canvas.delete("sites")
		for site in self.sites:
			canvas.drawSite(site)

class BeachArc:
	next_id = 0
	def __init__(self,site):
		seqDiagram.call()
		self.site = site
		self.nextTop = None
		self.nextBottom = None
		self.active = True
		# the arc that is the basis for the edge
		self.edgeArc = None
		self.circleEvent = None
		self.id = BeachArc.next_id
		BeachArc.next_id += 1
		seqDiagram.comment("new Arc: " + str(self.id) + "\\nto Site: " + str(site), color="#cff")

	def getSite(self):
		return self.site

	def getId(self):
		return self.id
		
	def getAllId(self):
		'''
			ids of the arcs
		'''
		seqDiagram.call()
		seqDiagram.comment("id=" + str(self.id))
		idTop,idCenter,idBottom = None,None,None
		if self.nextTop != None:
			if self.nextTop.getActive():
				idTop = self.nextTop.getId()
		if self.active:
			idCenter = self.id
		if self.nextBottom != None:
			if self.nextBottom.getActive():
				idBottom = self.nextBottom.getId()
		return idTop,idCenter,idBottom
		
	def getSiteIds(self):
		'''
			ids of the sites
		'''
		seqDiagram.call()
		seqDiagram.comment("id=" + str(self.id))
		idTop,idCenter,idBottom = None,None,None
		if self.nextTop != None:
			if self.nextTop.getActive():
				idTop = self.nextTop.getSite().getId()
		if self.active:
			idCenter = self.getSite().id
		if self.nextBottom != None:
			if self.nextBottom.getActive():
				idBottom = self.nextBottom.getSite().getId()
		return idTop,idCenter,idBottom

	def setNextTop(self, arc):
		seqDiagram.call()
		if arc == None:
			seqDiagram.comment("set Next Top " + str(self.getId()) + ": None")
		else:
			seqDiagram.comment("set Next Top " + str(self.getId()) + ": " + str(arc.getId()))
		self.nextTop = arc

	def setNextBottom(self, arc):
		seqDiagram.call()
		if arc == None:
			seqDiagram.comment("set Next Bottom " + str(self.getId()) + ": None")
		else:
			seqDiagram.comment("set Next Bottom " + str(self.getId()) + ": " + str(arc.getId()))
		self.nextBottom = arc

	def getNextTop(self):
		seqDiagram.call()
		seqDiagram.ret(ret=self.nextTop)
		return self.nextTop

	def getNextBottom(self):
		seqDiagram.call()
		seqDiagram.ret(ret=self.nextBottom)
		return self.nextBottom

	def getActive(self):
		return self.active
		
	def remove(self):
		seqDiagram.call()
		nextTop = self.nextTop
		nextBottom = self.nextBottom
		if nextTop != None:
			nextTop.setNextBottom(nextBottom)
		if nextBottom != None:
			nextBottom.setNextTop(nextTop)
		self.active = False
		return nextTop,nextBottom

	def setEdgeArc(self, arc):
		seqDiagram.call()
		seqDiagram.comment("set: " + str(arc.getSite()))
		self.edgeArc = arc

#	def getSiteX(self):
#		return self.site.getX()

	def copy(self):
		seqDiagram.call()
		ba = BeachArc(self.getSite())
		ba.setNextBottom(self.getNextBottom())
		ba.setNextTop(self.getNextTop())
		return ba
		
	def dist(self, site = None):
		'''
			distance to the arc from a site
			is used to estimate the arc that is closest to a site
		'''
		seqDiagram.call(site=site)
		y,x = None, None
		if site == None:
			# @TODO self site2 wird nirgendwo belegt
			if self.site2 != None:
				y,x = self.site.getY(), self.site.getX()
				site == self.site2
		else:
			y,x = site.getY(), site.getX()
			site = self.site
		return site.dist(y,x)
		
	def edgeLimits(self,d):
		'''
			the edge to the arc behind
			is used for drawing
			very like dispensable
			use 'getIntersectionspointsToNextArcs'
		'''
		seqDiagram.call(d=d)
		limitLow,limitHigh = None, None
		if self.edgeArc != None:
			seqDiagram.comment("EdgeArc for " + str(self.getSite()) + " is " + str(self.edgeArc.getSite()))
			Py,Px = self.site.getY(), self.site.getX()
			Qy,Qx = self.edgeArc.getSite().getY(), self.edgeArc.getSite().getX()
			a2 = Qx-Px
			a1 = 2*Py*d - 2*Qy*d - 2*Py*Qx + 2*Px*Qy
			a0 = Px*d*d - Qx*d*d + Qy*Qy*d + Qx*Qx*d - Py*Py*d - Px*Px*d - Px*Qy*Qy - Px*Qx*Qx + Py*Py*Qx + Px*Px*Qx
			aa = a1*a1 - 4*a2*a0
			if 0 <= aa:
				# the two solution
				limitHigh = 0.5 * (- math.sqrt(a1*a1 - 4*a2*a0) - a1) / a2
				limitLow = 0.5 * (  math.sqrt(a1*a1 - 4*a2*a0) - a1) / a2
			# print ("BeachArc.edgeLimits\t" + str(self) + "\t" + str(self.edgeArc) + "\tlimit: " + str(limitLow) + "," + str(limitHigh))
		else:
			seqDiagram.comment("no EdgeArc for " + str(self.getSite()))
		seqDiagram.ret(limitLow=formatFloatOrNone(limitLow),limitHigh=formatFloatOrNone(limitHigh))
		return limitLow,limitHigh
		
	def beachValueAt(self,d,y):
		seqDiagram.call(d=d,y=y)
		return 0
		
	def circleCoor(self):
		'''
			get center and radius for the arc
		'''
		mx,my,r = math.nan, math.nan, math.nan
		if self.nextTop != None and self.nextBottom != None:
			x0,y0 = self.nextTop.getSite().getX(), self.nextTop.getSite().getY()
			x1,y1 = self.getSite().getX(), self.getSite().getY()
			x2,y2 = self.nextBottom.getSite().getX(), self.nextBottom.getSite().getY()
			k1x = 2 * (x1 - x0)
			k1y = 2 * (y1 - y0)
			k2x = 2 * (x2 - x0)
			k2y = 2 * (y2 - y0)
			k1 = x1 * x1 + y1 * y1 - x0 * x0 - y0 * y0
			k2 = x2 * x2 + y2 * y2 - x0 * x0 - y0 * y0
			m = k1x * k2y - k2x * k1y
			if (m == 0):
				# all three points are on a line
				pass
			else:
				mx = k1 * k2y - k2 * k1y
				my = k1x * k2 - k2x * k1
				mx /= m
				my /= m
				d0x, d0y = x0 - mx, y0 - my
				d1x, d1y = x1 - mx, y1 - my
				d2x, d2y = x2 - mx, y2 - my
				r = math.sqrt(d0x*d0x + d0y*d0y)
		return mx,my,r
		
	def circle(self):
		'''
			return the event
		'''
		seqDiagram.call()
		result = math.nan
		mx,my,r = self.circleCoor()
		if mx != math.nan and r != math.nan:
			result = mx + r
		return result
		
	def getIntersectionspointsToArc(self,arc,sweepline):
		'''
			returns a tuple
		'''
		seqDiagram.call(x=formatFloatOrNone(sweepline))
		seqDiagram.comment(str(self.getId()) + " " + str(arc.getId()), color="#cff")
		limitLow,limitHigh = None, None
		Py,Px = self.site.getY(), self.site.getX()
		Qy,Qx = arc.getSite().getY(), arc.getSite().getX()
		a2 = Qx-Px
		a1 = 2*Qy*(sweepline - Px) - 2*Py*(sweepline - Qx)
		a0 = Px*sweepline*sweepline - Qx*sweepline*sweepline + Qy*Qy*sweepline + Qx*Qx*sweepline - Py*Py*sweepline - Px*Px*sweepline - Px*Qy*Qy - Px*Qx*Qx + Py*Py*Qx + Px*Px*Qx
		aa = a1*a1 - 4*a2*a0
		if 0 <= aa:
			if a2 == 0:
				if Py < Qy:
					limitHigh = 0.5 * (Qy + Py)
					limitLow = None
				else:
					limitHigh = None
					limitLow = 0.5 * (Qy + Py)
			else:
				limitHigh = 0.5 * (- math.sqrt(aa) + a1) / a2
				limitLow = 0.5 * (math.sqrt(aa) + a1) / a2
				seqDiagram.comment ("Px,Py,Qx,Qy,d:\t" + str(Px) + ", " + str(Py) + ", " + str(Qx) + ", " + str(Qy) + ", " + str(sweepline) + "\\n" + str(limitHigh) + ", " + str(limitLow), "#ddd")
		return limitHigh, limitLow
	
	def getIntersectionspointsToNextArcs(self,d):
		'''
			utilize maxima for all the formulas
			the result of this method are intersectionPoints to the next arcs above and below the actual arc
			depending on the sweepline
			the intersection M between the two arcs defined py the sites P and Q satiesfies these both equations
				eq1: 0 = (Qx - Mx)^2 + (Qy - My)^2 - (d - Mx)^2;
				eq2: 0 = (Px - Mx)^2 + (Py - My)^2 - (d - Mx)^2;
				solution: solve([eq1, eq2], [Mx,My]);
			it is important to keep in mind, that there are usually two solutions to this equation, and one of them is misleading
			
			to get a more comprehensible form, and because we are only interested in My
				eq_sub : expand(eq1 - eq2);
				Mx_expr : rhs(first(solve(eq_sub, Mx)));
				eqMy : subst(Mx = Mx_expr, eq1);
			to get a quadratic equation 'a*My*My + b*My + c' for My
				a: ratcoef(rhs(eqMy), My, 2);
				b: ratcoef(rhs(eqMy), My, 1);
				c: ratcoef(rhs(eqMy), My, 0);
			with
				My = ( -b + sqrt(b * b - 4 * a *c) / (2 * a) , ( -b - sqrt(b * b - 4 * a *c) / (2 * a)
			we see some repeating terms for a,b,c, which are a0, a1, a2 (see below)
			we also need the derivation, 
				normally when an arc becomes zero, the arc should be closed
				but in some circumstances this also applies when an arc just have been created
				so we must know if the arc is shrinking or growing 
				dUp: factor(diff(rhs(first(solve(eqMy,My))), d));
				d0: ratcoef(factor(diff(rhs(eqMy), d)), My, 0);
				
			the solution from chatGPT is similar
				b2 = Qx-Px
				b1 = Qy*(d-Px) - Py*(d-Qx)
				b0 = (d-Px)*(d-Qx) * ((Py-Qy)*(Py-Qy) + (Px-Qx)*(Px-Qx))
				
				My = (b1 + sqrt(b0)) / b2, (b1 - sqrt(b0)) / b2
		'''
		# print ("BeachArc.getLimits.1\t",self.site,d)
		seqDiagram.call(x=formatFloatOrNone(d))
		seqDiagram.comment(str(self.site), color="#cff")
		limitLow,limitHigh = None, None
		limitLowNone,limitHighNone = None, None
		if self.nextTop != None:
			limitHigh,limitLowNone = self.getIntersectionspointsToArc(self.nextTop,d)
			# print ("BeachArc.getLimits.2\t",limitHigh,limitLowNone)
		if self.nextBottom != None:
			limitHighNone,limitLow = self.getIntersectionspointsToArc(self.nextBottom,d)
			# print ("BeachArc.getLimits.3\t",limitHighNone,limitLow)
		if limitLow != None and limitHigh != None and limitHigh < limitLow:
			print ("Alarm", str(self), limitHigh, limitLow)
		seqDiagram.ret(limitLow=formatFloatOrNone(limitLow),limitHigh=formatFloatOrNone(limitHigh))
		return limitLow,limitHigh
	
	def setCircleEvent(self,circleEvent):
		seqDiagram.call()
		if self.circleEvent != None:
			seqDiagram.comment ("arc [" + str(self.id) + "] deactivate CircleEvent: " + str(self.circleEvent))
			self.circleEvent.deactivate()
		seqDiagram.comment ("arc [" + str(self.id) + "] set CircleEvent: " + str(circleEvent))
		self.circleEvent = circleEvent
	
	def __str__(self):
		idTop, idBottom = "-","-"
		if self.nextTop != None:
			idTop = self.nextTop.getId()
		if self.nextBottom != None:
			idBottom = self.nextBottom.getId()
		# "{" + str(self.id) + ":" +str(self.site) + "[" + str(idBottom) + "," + str(idTop) + "]" + "}"
		return "{" + str(self.id) + ":" +str(self.site) + "}"
		
	def draw(self,canvas,d):
		'''
			draw the complete Arc
		'''
		seqDiagram.call()
		Py,Px = self.site.getY(), self.site.getX()
		if Px < d:
			intersectionLow, intersectionHigh = self.getIntersectionspointsToNextArcs(d)
			if intersectionLow == None:
				intersectionLow = 0
			else:
				if intersectionLow < 0:
					intersectionLow = 0
				elif intersectionLow > 101:
					intersectionLow = 101
			if intersectionHigh == None:
				intersectionHigh = 101
			else:
				if intersectionHigh < 0:
					intersectionHigh = 0
				elif intersectionHigh > 101:
					intersectionHigh = 101
			bottom, top = self.getNextBottom(), self.getNextTop()
			bottomT, topT = "-", "-"
			if bottom != None:
				bottomT = str(bottom.getId())
			if top != None:
				topT = str(top.getId())
			print ("draw Canvas", self.id, "(", self.getSite().getId(), ")", bottomT, topT, intersectionLow, intersectionHigh)
			line = []
			# for i in range(-amountPoints,amountPoints):
			for loopy in range(round(intersectionLow * 10),round(intersectionHigh * 10),1):
				# das ist die zentrale Formel für die beachline eines Punktes Py,Px zur Beachline d
				y = 0.1 * loopy
				x=(Py*Py + Px*Px + y*y - 2*y*Py - d*d) / (2*Px - 2*d)
				line.extend(canvas.xy(x,y))
			if len(line) > 3:
				canvas.canvas.create_line(*line, width=5, fill="#0f0", activefill = "#f00", tags=('arc'))
			centerY = 0.5 * intersectionHigh + 0.5 * intersectionLow
			centerX = (Py*Py + Px*Px + centerY*centerY - 2*centerY*Py - d*d) / (2*Px - 2*d)
			centerY, centerX = canvas.xy(centerY, centerX)
			canvas.canvas.create_text(centerX+25,centerY,fill="#000",font=fontCanvas, text=str(self.id), tags=('arc'))
			cPy,cPx = canvas.xy(Py, Px)
			canvas.canvas.create_line([centerX, centerY, cPx, cPy], width=5, fill="#0ff", activefill = "#f00", tags=('arc'))
			print (">!!<", self, intersectionLow, intersectionHigh)

	def l(self):
		# eq1	(y-P1y)^2+(x-P1x)^2=(d-x)^2
		# eqq:	(y-P1y)*(y-P1y)+(x-P1x)*(x-P1x)=(y-P2y)*(y-P2y)+(x-P2x)*(x-P2x);
		#
		# intersectionpoints (x,y) of two arcs 
		# the arcs are determined by P,Q
		# sweepline ist d
		# 
		# eq1: x = (Px*Px + Py*Py + y*y - 2*Py*y-d*d) / (2*(Px - d));
		# eqm: (Px*Px + Py*Py + y*y - 2*Py*y-d*d) / (2*(Px - d)) = (Qx*Qx + Qy*Qy + y*y - 2*Qy*y-d*d) / (2*(Qx - d));
		#
		pass
		
class Beachline:
	def __init__(self, sites = None):
		seqDiagram.call()
		self.arcs = []
		# self.sites = sites
		
	def addSite(self, site):
		'''
			go along the beachline and find the arc, which fits to the given site
			adding a new site creates two new arcs
			- one arc is the arc for the new site
			- the new site splits the closest arc into an upper an lower arc
		'''
		seqDiagram.call(site=site)
		newCircles = []
		if len(self.arcs) == 0:
			seqDiagram.comment("first Arc in Beachline", color="#fff")
			self.arcs.append(BeachArc(site))
		else:
			bestIndex = None
			seqDiagram.comment("Elements in Beachline: " + str(len(self.arcs)), color="#fff")
			# find the Arc-Element with the matchin upper and lower limit
			seqDiagram.groupStart("find best beachArc\\n" + str(site.getX()) + " " + str(site.getY()), color="#fda")
			
			siteL = []
			for i in range(len(self.arcs)):
				limitLow, limitHigh = self.arcs[i].getIntersectionspointsToNextArcs(site.getX())
				siteL.append((site.getId(), limitLow, limitHigh))
			# print ("siteL", site.getY(), siteL)
			for i in range(len(self.arcs)):
				# go through all the arcs
				actualArc = self.arcs[i]
				# print("Beachline.addSite.1\tSite: ",site,"\t",actualArc)
				# first test, is the arc inside the limits
				isInsideLimits = True
				limitLow, limitHigh = actualArc.getIntersectionspointsToNextArcs(site.getX())
				# first limitTest
				print (">!<", i, actualArc, limitLow, limitHigh, site.getY())
				if limitLow != None and site.getY() <= limitLow:
					isInsideLimits = False
				if limitHigh != None and site.getY() > limitHigh:
					isInsideLimits = False
				if limitLow == None and limitHigh == None:
					if actualArc.getSite().getX() < site.getX():
						pass
					else:
						isInsideLimits = False
				if isInsideLimits:
					seqDiagram.comment(str(actualArc.getId()) + " is inside limits: " + str(site.getY()) + " [" + formatFloatOrNone(limitLow) + "," + formatFloatOrNone(limitHigh) + "]" , color="#fff")
					bestIndex = i
				else:
					seqDiagram.comment(str(actualArc.getId()) + " is outside limits: " + str(site.getY()) + " [" + formatFloatOrNone(limitLow) + "," + formatFloatOrNone(limitHigh) + "]", color="#fff")
			seqDiagram.groupEnd("find best beachArc")
			if bestIndex == None:
				# the very unusual case, that the diagram starts with several points at the same sweepline
				seqDiagram.comment("parallel sites start")
			else:
				# beachArc found at bestIndex
				seqDiagram.groupStart("add beachArc", color="#efc")
				# insert new Arc on existing Arc
				newArc = BeachArc(site)
				# the arc that fits the projection of the site event
				bestArc = self.arcs[bestIndex]
				seqDiagram.comment("closest arc: " + str(bestArc.getId()) , color="#fff")
				bestArcCopy = bestArc.copy()

				# insert the two new ArcElements
				self.arcs[bestIndex+1:bestIndex+1] = [newArc, bestArcCopy]
				seqDiagram.comment("set the new Arc id = " + str(newArc.getId()) + " between: " + str(bestArcCopy.getId()) + ", " + str(bestArc.getId()), color="#fff")
				bestArcCopy.setNextBottom(newArc)
				bestArc.setNextTop(newArc)
				newArc.setNextBottom(bestArc)
				newArc.setNextTop(bestArcCopy)
				# edgearc is obsolet
				newArc.setEdgeArc(bestArc)
				if bestArcCopy.getNextTop() != None:
					bestArcCopy.getNextTop().setNextBottom(bestArcCopy)
				# index of the new arc, make it obsolet. work with neightbors
				addIndex = bestIndex+1
				
				# calculate the length of the neighboring arcs
				nextArcTop = bestArc.getIntersectionspointsToNextArcs(site.getX());
				nextArcBottom = bestArcCopy.getIntersectionspointsToNextArcs(site.getX());
				# print ("Beachline.addSite\tadd arc \tSite: ",site, "\tnewArc", newArc,"\tbestArcAbove", bestArc, "\tbestArcBelow", bestArcCopy, "\taddIndex:", addIndex)
				seqDiagram.groupEnd("add beachArc")
				# Set the CircleEvents
				seqDiagram.groupStart("calculate CircleEvents", color="#bdf")
				# add the circleEvents
				c1,c2 = None, None
				if addIndex > 1:
					# c1 = arcCircle(pc1)
					c1 = self.arcs[addIndex-1].circle()
					# print ("circle1", c1, "=", c1Alt)
					# print ("Beachline.addSite\tcirc above\tSite: ",c1,"\t", self.arcs[addIndex-2], self.arcs[addIndex-1], self.arcs[addIndex])
					seqDiagram.comment("circle for arc " + str(self.arcs[addIndex-1].getId()) + " above x:" + formatFloatOrNone(c1))
				if addIndex < len(self.arcs)-2:
					# c2 = arcCircle(pc2)
					c2 = self.arcs[addIndex+1].circle()
					# print ("circle1", c2, "=", c2Alt)
					# print ("Beachline.addSite\tcirc below\tSite: ",c2,"\t", self.arcs[addIndex+2], self.arcs[addIndex+1], self.arcs[addIndex])
					seqDiagram.comment("circle for arc " + str(self.arcs[addIndex+1].getId()) + " below x:" + formatFloatOrNone(c2))
				if c1 != None and not math.isnan(c1):
					newCircles.append(EventCircle(self.arcs[addIndex-1]))
				if c2 != None and not math.isnan(c2):
					newCircles.append(EventCircle(self.arcs[addIndex+1]))
				seqDiagram.groupEnd("set CircleEvents")
				
		# print("Beachline.addSite\tfinished\tSite: ",site,"\t",self, newCircles)
		return newCircles

	def removeArc(self, arc):
		seqDiagram.call(arc=arc)
		# print ("beachline before removing the arc", self)
		# print ("removeArc", arc)
		index = None
		arcId = arc.getId()
		arcTop = arc.getNextTop()
		arcBottom = arc.getNextBottom()
		seqDiagram.comment("remove Arc: " + str(arcId) + "\\nmerge Arcs: " + str(arcTop.getId()) + " " + str(arcBottom.getId()))
		if arcTop != None:
			arcTop.setNextBottom(arcBottom)
		if arcBottom != None:
			arcBottom.setNextTop(arcTop)
		for i in range(len(self.arcs)):
			if self.arcs[i].getId() == arcId:
				index = i
		if index != None:
			# self.arcs[index].remove()
			self.arcs.pop(index)
		# print ("beachline after removing the arc", self)

	def __str__(self):
		result=""
		result = "\t".join([str(a) for a in self.arcs])
		return "((\t" + result + "\t))"

	def drawBeach(self, canvas, d):
		# print ("Beachline.drawBeach")
		seqDiagram.groupStart("draw Beachline", color="#cfd")
		seqDiagram.call(d=d)
		for arc in self.arcs:
			seqDiagram.groupStart("draw Arc", color="#bfd")
			seqDiagram.comment("draw Arc: " + str(arc) + "\tSites:" + str(arc.getSiteIds()))
			arc.draw(canvas,d)
			seqDiagram.groupEnd("draw Arc")
		seqDiagram.groupEnd("draw Beachline")

class Event:
	'''
		events can be sorted
	'''
	nextEventId = 0
	def __init__(self):
		self.id = Event.nextEventId
		# seqDiagram.call(_id=self.id)
		Event.nextEventId += 1
		self.active = True
		
	def getId(self):
		return self.id
		
	def deactivate(self):
		seqDiagram.call()
		self.active = False
		
	def __lt__(self, other):
		result = other.getX() - self.getX() > 0
		# if other.getX() == self.getX():
		#	result = other.getId() - self.getId() > 0
		return result

class EventSite(Event):
	def __init__(self,site):
		seqDiagram.call()
		super().__init__()
		self.site = site
		seqDiagram.comment(str(self.site))

	def getY(self):
		return self.site.getY()
		
	def getX(self):
		return self.site.getX()

	def handleEvent(self, beachline):
		seqDiagram.groupStart("siteEvent", color="#dfb")
		seqDiagram.call()
		# print ("EventSite.handleEvent\t",self.site)
		result = beachline.addSite(self.site)
		self.active = False
		# seqDiagram.ret()
		seqDiagram.comment(str(beachline))
		seqDiagram.groupEnd("siteEvent")
		return result
		
	def draw(self,canvas,d):
		seqDiagram.groupStart("draw EventSite", color="#dfd")
		seqDiagram.call()
		self.site.draw(canvas,d)
		seqDiagram.groupEnd("draw EventSite")
		
	def __str__(self):
		return ".site " + "-+"[self.active] + str(self.site) + " !" + formatFloatOrNone(self.getX())

class EventCircle(Event):
	def __init__(self,arc):
		# parameter is an triple of arcs, with p[1] the central arc
		seqDiagram.call()
		super().__init__()
		self.arc = arc
		self.site = arc.getSite()
		self.mx = self.arc.circle()
		# historical Data for Display
		self.histX, self.histY, self.histR = self.arc.circleCoor()

	def getX(self):
		return self.mx
		
	def handleEvent(self, beachline):
		seqDiagram.groupStart("circleEvent", color="#cffdff")
		seqDiagram.call()
		newCircles = []
		if self.active:
			self.deactivate()
			
			seqDiagram.comment("d = " + formatFloatOrNone(self.getX()))
			bottomValue, topValue = self.arc.getIntersectionspointsToNextArcs(self.getX())
			seqDiagram.comment("arc [" + str(self.arc.getId()) + "] Bottom/Top = " + formatFloatOrNone(bottomValue) + ", " + formatFloatOrNone(topValue))

			# p0l,p0h = self.arcs[0].getIntersectionspointsToNextArcs(self.getX())
			# p1l,p2h = self.arcs[1].getIntersectionspointsToNextArcs(self.getX())
			# p2l,p2h = self.arcs[2].getIntersectionspointsToNextArcs(self.getX())

			# stored Beachline
			# arcTop0, arcCenter0, arcBottom0 = self.arcs[0].getId(), self.arcs[1].getId(), self.arcs[2].getId()
			# arcTop0, arcCenter0, arcBottom0 = self.sites[0], self.sites[1], self.sites[2]
			# actual Beachline
			# arcTop1, arcCenter1, arcBottom1 = self.arc.getSiteIds()
			# seqDiagram.comment("initial IDs: " + str(arcTop0) + " " + str(arcCenter0) + " " + str(arcBottom0) + "\\nactual IDs: " + str(arcTop1) + " " + str(arcCenter1) + " " + str(arcBottom1) + "\\n" + str(beachline))
			# seqDiagram.comment(str(beachline))
			# test if the arcs are still consecutive and the edge has really collapsed
			# if arcTop0 == arcTop1 and arcCenter0 == arcCenter1 and arcBottom0 == arcBottom1 and abs(topValue - bottomValue) < 1e-6:
			if topValue != None and bottomValue != None and abs(topValue - bottomValue) < 1e-6:
				# self.arc.beachValueAt(self.getX(),bottomValue)
				seqDiagram.groupStart("removeArc " + str(self.arc.getId()), color="#afedff")
				# the stored beachline is still relevant
				arcTop = self.arc.getNextTop()
				arcBottom = self.arc.getNextBottom()
				beachline.removeArc(self.arc)
				seqDiagram.comment(str(beachline))
				seqDiagram.groupEnd()
				# do new Circles evolve
				seqDiagram.groupStart("Test for new CircleEvents ", color="#afedff")
				if arcTop != None and arcBottom != None:
					c1,c2 = None, None
					# pc1,pc2 = None, None
					# arcTopTop = arcTop.getNextTop()
					# arcBottomBottom = arcBottom.getNextBottom()
					seqDiagram.comment("arcTop:" + str(arcTop) + "\tarcBottom:" + str(arcBottom))
					# if arcTopTop != None:
					#	pc1 = arcTopTop,arcTop,arcBottom
					#	c1 = arcCircle(pc1)
					# if arcBottomBottom != None:
					#	pc2 = arcTop,arcBottom,arcBottomBottom
					#	c2 = arcCircle(pc2)
					cTop = arcTop.circle()
					cBottom = arcBottom.circle()
					if cTop != None and not math.isnan(cTop):
						if cTop > self.getX():
							newCircle = EventCircle(arcTop)
							newCircles.append(newCircle)
						else:
							seqDiagram.comment("circleEvents for Arc [" + str(arcTop.getId()) + "]: " + formatFloatOrNone(cTop) + " is behind sweep " + formatFloatOrNone(self.getX()))
					else:
						seqDiagram.comment("Arc Top is None")
					if cBottom != None and not math.isnan(cBottom):
						if cBottom > self.getX():
							newCircle = EventCircle(arcBottom)
							newCircles.append(newCircle)
						else:
							seqDiagram.comment("circleEvents for Arc [" + str(arcBottom.getId()) + "]: " + formatFloatOrNone(cBottom) + " is behind sweep " + formatFloatOrNone(self.getX()))
					else:
						seqDiagram.comment("Arc Bottom is None")
				seqDiagram.groupEnd()
			else:
				# arc will not get removed
				# this should not happen, since Circle-Events should get deactivated
				reason = ""
				if topValue == None or bottomValue == None:
					reason = "arc ?= " + formatFloatOrNone(topValue)  + ", " + formatFloatOrNone(bottomValue)
				elif abs(topValue - bottomValue) > 1e-6:
					reason = "arc >= " + formatFloatOrNone(topValue - bottomValue)
				seqDiagram.comment("outdated circleEvent: " + reason, "#f44")
			self.open = False
			# seqDiagram.ret()
			# newCircles = []
		else:
			seqDiagram.comment("Circle-Event for arc " + str(self.arc.getId()) + " not active")
		seqDiagram.groupEnd("circleEvent")
		return newCircles
	
	def attachToArc(self):
		seqDiagram.call()
		self.arc.setCircleEvent(self)
		
	def getArcId(self):
		result = "no Arc"
		if self.arc != None:
			result = self.arc.getId()
		return result
	
	def draw(self,canvas,d):
		if self.getX() >= d:
			seqDiagram.groupStart("draw EventCircle", color="#afa")
			seqDiagram.call()
			color = "#cef"
			if self.active:
				color = "#8bf"
			canvas.drawCircle(self.histX, self.histY, self.histR,color)
			labelY,labelX = canvas.xy(self.histY,self.histX + self.histR)
			actualSideIds = self.arc.getSiteIds()
			actualArcTop, actualArcCenter, actualArcBottom = self.arc.getAllId()
			# first Ids are the Sides
			label = "arc: " + str(self.arc.getId()) + " -> " + str(self.arc.getSite().getId())
			canvas.canvas.create_text(labelX+60, labelY, fill="#00f", font=fontCanvas, text=label, tags=('circle'))
			seqDiagram.groupEnd("draw EventCircle")
		else:
			seqDiagram.call()

	def __str__(self):
		status = "-+"[self.active]
		return ".circle : " + status + str(self.arc) + " !" + formatFloatOrNone(self.getX())

class EventQueue:
	def __init__(self):
		seqDiagram.call()
		self.events = []
		self.index = 0
		self.beachline = None
		
	def addQueue(self,event):
		seqDiagram.call()
		seqDiagram.comment("actual event: " + formatFloatOrNone(self.events[self.index].getX()) + "\\nnew event: " + formatFloatOrNone(event.getX()) + "\\nclass:" + str(event))
		self.events.append(event)
		self.events.sort()

	def addSites(self,sites):
		seqDiagram.call()
		for site in sites:
			self.events.append(EventSite(site))
		self.events.sort()

	def out(self):
		'''
			log all events to the User
			@TODO: create a textwindow
		'''
		for k in range(len(self.events)):
			print ("EventQueue", self.events[k])
			
	def stepQueue(self):
		seqDiagram.call()
		actualEvent = self.events[self.index]
		seqDiagram.comment("event = " + str(actualEvent))
		# print ("queue step",self.index)
		if self.beachline == None:
			self.beachline = Beachline()
		result = actualEvent.handleEvent(self.beachline)
		# seqDiagram.comment("EventQueue.step\tresult: " + str(result))
		if result != None and len(result) > 0:
			seqDiagram.groupStart("add EventCircle", color="#afa")
			for circleElement in result:
				# print ("EventQueue.step\tresult: ",elem)
				print ("***", str(actualEvent), str(circleElement))
				self.addQueue(circleElement)
				circleElement.attachToArc()
			seqDiagram.groupEnd()
		self.index += 1
		# printQueue=[]
		# for i in range(len(self.events)):
		#	printQueue.append(str(i) + ":" + str(self.events[i]))
		# print("Queue[" + str(self.index) + "]", ", ".join(printQueue))
		print ("***Beachline", self.beachline)
		return self.index < len(self.events)
		
	def stepValue(self):
		seqDiagram.call()
		result = 9999999
		if self.index < len(self.events):
			result = self.events[self.index].getX()
		seqDiagram.ret(nextStep=result)
		return result
		
	def draw(self,canvas,d):
		seqDiagram.call()
		# self.beachline.drawBeach(canvas,d)
		if self.beachline != None:
			self.beachline.drawBeach(canvas,d)
		for event in self.events:
			event.draw(canvas,d)
			
	def getBeachline(self):
		return self.beachline

if False:
	# Test Sequenzdiagram
	class ClassA2():
		def __init__(self):
			seqDiagram.call()
			self.p = None

		def sub2(self, p):
			seqDiagram.groupStart("group 2", color="#afa")
			seqDiagram.call()
			self.p = p
			self.p.feedback()
			print ("sub2")
			seqDiagram.groupEnd("sub2")
			
	
	class ClassA1():
		def __init__(self):
			seqDiagram.call()
			self.a2 = ClassA2()
			
		def sub1(self):
			seqDiagram.groupStart("group 1", color="#afa")
			seqDiagram.call()
			print ("sub1")
			self.a2.sub2(self)
			seqDiagram.groupEnd("sub1")
			
		def feedback(self):
			seqDiagram.call()
			print ("feedback")
	
	print ("start sequenztest")
	seqDiagram.log("anything")
	a1 = ClassA1()
	a1.sub1()
	seqDiagram.log("hear her scream")
	print ("len seqDiagram", len(seqDiagram))
	seqDiagram.out()


if __name__ == "__main__":
	app = tk.Tk()
	app.title("Voronoi Test 2")
	
	h,w = 1000,2400
	hs, ws = app.winfo_screenheight(), app.winfo_screenwidth()
	x, y = (ws/2) - (w/2), (hs/2) - (h/2)
	app.geometry('%dx%d+%d+%d' % (w, h, x, y))
	
	valueSweepline = tk.DoubleVar()
	valueSweepline.set(0)
	
	canvasSize = 50
	def redraw():
		'''
			redraw the canvas,
			mcanvas is a wrapper for the canvas, that features some draw-commands
		'''
		global voronoiCanvas, canvasSize, sites, valueSweepline
		global mcanvas
		print ("\n**** redraw")
		seqDiagram.call()
		
		# clear the canvas
		mcanvas.canvas.delete("hline")
		mcanvas.canvas.delete("circle")
		mcanvas.canvas.delete("sites")
		mcanvas.canvas.delete("arc")
		# beachArc global counter reset
		BeachArc.next_id = 0
		# read the value from the tk-scaler
		d = valueSweepline.get()
		
		# new Queue
		queue = EventQueue()
		queue.addSites(sites)
		#for site in sites:
		#	queue.addQueue(EventSite(site))
		# queue.out()
		
		# do all the steps until the sweepline is reached
		seqDiagram.comment("sweepline = " + str(d), color="#cff")
		b = True
		while b:
			seqDiagram.groupStart("stepQueue", color="#fdc")
			b = queue.stepQueue()
			# queue.out()
			value = queue.stepValue()
			if value > d:
				b = False
			seqDiagram.comment(str(queue.getBeachline()))
			seqDiagram.groupEnd("stepQueue")
		mcanvas.drawSweepline(d)
		# draw all events and event-related
		queue.draw(mcanvas, d)
		if False:
			for site in sites:
				print ("***** redraw.drawsite", site, d)
				site.draw(mcanvas)
				a = BeachArc(site)
				a.draw(mcanvas,d)
		# sites.draw(mcanvas)

	def resizeCanvas(event):
		global mcanvas
		seqDiagram.groupStart("resize")
		print ("**** call resizeCanvas")
		mcanvas.canvas.delete("arc")
		mcanvas.canvas.delete("hline")
		mcanvas.canvas.delete("sites")
		mcanvas.canvas.delete("circle")
		mcanvas.resize(event.widget.winfo_height(), event.widget.winfo_width())
		redraw()
		# canvasSize = min(event.widget.winfo_width() / 3, event.widget.winfo_height() / 2)
		# voronoiCanvas.config(width=canvasSize * 3 - 10, height=canvasSize * 2 - 10)
		# canvas.delete("all")
		seqDiagram.groupEnd("resize")
		seqDiagram.out().reset()

	sweeplineID = None
	def moveSweepline(event):
		global voronoiCanvas, canvasSize, sweeplineID, valueSweepline, sites
		global mcanvas
		seqDiagram.groupStart("moveSweepline")
		print ("**** move sweepline")
		Event.nextEventId = 0
		redraw()
		# totalW, totalH = canvasSize * 3 - 10, canvasSize * 2 - 10
		# if sweeplineID == None:
		#	sweeplineID = voronoiCanvas.create_line(1, 1, 50, 50, width=2, fill="#000", activefill = "#f00", tags=('sweepline'))
		# displaySweepline = valueSweepline.get() * totalW / 100
		# voronoiCanvas.coords(sweeplineID, displaySweepline, 10, displaySweepline, totalH - 10)
		# sites.draw(voronoiCanvas)
		seqDiagram.groupEnd("moveSweepline")
		# seqDiagram.hideElements(["beachArc"])
		# print ("### test SeqDiagram start")
		# test of groups:
		# hiding / showing elements based on their class / id
		
		seqDiagram.activate()
		result = seqDiagram.getMetaInfo()
		# print ("### test SeqDiagram end")
		# print(result.outItems())
		# print(result.outItems(reverseOrder = True, unique = True))
		# print(result.outClasses())
		# print(result.outClasses(reverseOrder = True))
		# print("len:",result.outValue())
		
		# 'EventCircle', 'EventQueue', 'Site', 'EventSite', 'Beachline', 'BeachArc'
		lastEvent = result.getLastOfClass('EventSite', 1)
		lastEvent.extend(result.getLastOfClass('EventCircle', 1))
		# print ("getLastOfClass", lastEvent)
		# seqDiagram.activate()
		lastEvent = []
		seqDiagram.activate(lastEvent)
		# resultC = seqDiagram.displayStructure()
		seqDiagram.out().reset()

	# create all Frames
	#	mainFrame
	#		voronoiFrame
	#			voronoiFrameCanvas
	#				voronoiCanvas
	#			voronoiFrameSweep
	#				sliderSweep
	mainFrame = tk.Frame(app, bd=0, bg="#aaa", relief=tk.SUNKEN)
	voronoiFrame = tk.Frame(mainFrame, bd=0, bg="#aaa", relief=tk.SUNKEN)
	voronoiFrameCanvas = tk.Frame(voronoiFrame, bd=0, bg="#aaa", relief=tk.SUNKEN)
	voronoiFrameSweep = tk.Frame(voronoiFrame, bd=0, bg="#aaa", relief=tk.SUNKEN)
	sliderSweep = tk.Scale(voronoiFrameSweep, from_=0, to=150, resolution=0.1, orient=tk.HORIZONTAL, tickinterval=10,showvalue = 1, variable=valueSweepline, command=moveSweepline)
	voronoiCanvas = tk.Canvas(voronoiFrameCanvas, width=canvasSize, height=canvasSize, background='#efe')
	voronoiFrameCanvas.bind("<Configure>", resizeCanvas)
	# log widget
	# textFrame = tk.Frame(mainFrame, bd=0, bg="#aaf", relief=tk.SUNKEN)
	# scrollbar = tk.Scrollbar(textFrame, orient="vertical")
	# text=tk.Text(textFrame, yscrollcommand=scrollbar.set, wrap="none", bd=1, bg="#ffe", relief=tk.SUNKEN, width = 50, padx = 10, pady = 10, font=("Ubuntu Mono", 12, "normal"))
	# scrollbar.config(command=text.yview)
	
	# pack all Frames
	mainFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	voronoiFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
	voronoiFrameCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	voronoiFrameSweep.pack(side=tk.TOP, fill=tk.BOTH, expand=0)
	sliderSweep.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	voronoiCanvas.pack(side=tk.TOP, fill=tk.NONE, expand=0)

	# textFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
	# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
	# text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
	
	# set the log Window
	seqDiagram.getWidget(mainFrame)
	
	# seqDiagram.setTextField(text)
	
	seqDiagram.addParticipantOrder("Main", 0)
	seqDiagram.addParticipantOrder("Sites", 30)
	seqDiagram.addParticipantOrder("Site", 31)
	seqDiagram.addParticipantOrder("EventQueue", 10)
	seqDiagram.addParticipantOrder("EventSite", 11)
	seqDiagram.addParticipantOrder("EventCircle", 12)
	seqDiagram.addParticipantOrder("Beachline", 20)
	seqDiagram.addParticipantOrder("BeachArc", 21)
	seqDiagram.addParticipantOrder("MCanvas", 40)
	
	sites = Sites()
	# sites.add(75,5)
	# sites.add(30,20)
	# sites.add(70,20)
	# sites.add(50,25)
	# sites.add(30,50)
	# sites.add(70,50)
	# sites.add(80,40)
	
	if False:
		sites.add(10,50)
		sites.add(80,50)
		sites.add(50,50)
		sites.add(20,50)
		sites.add(90,50)
		sites.add(60,50)
		sites.add(30,50)
		sites.add(70,50)
		sites.add(40,50)

	if True:
		sites.add(10,50)
		sites.add(80,51)
		sites.add(50,52)
		sites.add(20,53)
		sites.add(90,54)
		sites.add(60,55)
		sites.add(30,56)
		sites.add(70,57)
		sites.add(40,58)

	# sites.add(75,10)
	# sites.add(25,15)
	# sites.add(70,40)
	# sites.add(15,45)
	# sites.add(20,50)
	# sites.add(30,55)
	# sites.add(65,60)
	# sites.add(55,65)
	
	# sites.add(60,10)
	# sites.add(40,20)
	# sites.add(80,40)
	# sites.add(15,45)
	# sites.add(35,45)
	# sites.add(25,70)
	# sites.add(20,80)
	
	# sites.add(50,5)
	# sites.add(95,40)
	# sites.add(40,50.1)
	# sites.add(70,50.2)
	# sites.add(30,50.3)
	# sites.add(20,85)
	# sites.add(85,90)

	# beachline = Beachline(sites)
	mcanvas = MCanvas(voronoiCanvas)
	# sites.draw(mcanvas)
	
	print ("id canvasSize", id(canvasSize))
	app.mainloop()





