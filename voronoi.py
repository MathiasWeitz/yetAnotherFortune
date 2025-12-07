#!/usr/bin/env python3
'''
	implementation of FORTUNES algorithm with extensive depiction of how data is handled
	this is a prepartion to verify own algorithms in C++
	
	the program is interactive and uses tkinter for gui
'''

import os, traceback, inspect
import math

import tkinter as tk 
from PIL import Image, ImageTk

class SeqDiagram:
	def __init__(self):
		self.reset()
		# the UI on the Applikation should be a TK-Text
		# if no Textfield is given the output goes to the console
		self.textField = None
		# set a priority for every element of a certain class
		# that makes the element of the same class group together
		self.participantOrder = dict()

	def log(self, text):
		self.logList.append(text)
		return self

	def out(self):
		# sort the participant
		pk = list(self.participant.keys())
		pk.sort(key=lambda x:(self.participant[x] not in self.participantOrder, self.participantOrder.get(self.participant[x])))
		
		if self.textField == None:
			print ("participant main as \"Main\"")
			for key, value in self.participant.items():
				print ("participant " + key + " as \"" + value + "\"")
			print ()
			for value in self.logList:
				print (value)
		else:
			lastBox=None
			for tag in self.textField.tag_names():
				self.textField.tag_delete(tag)
			self.textField.tag_config("part", foreground="blue")
			self.textField.delete("1.0", "end")
			self.textField.insert("end", "participant main as \"Main\"\n", "part")
			for key in pk:
				if self.participant.get(key) != lastBox:
					if lastBox != None:
						self.textField.insert("end", "end box\n", "part")
					lastBox = self.participant.get(key)
					self.textField.insert("end", "box \"" + lastBox + "\" #ccc\n", "part")
				self.textField.insert("end", "participant " + key + " as \"" + self.participant.get(key) + "\"" + "\n", "part")
			if lastBox != None:
				self.textField.insert("end", "end box\n", "part")
			self.textField.insert("end", "\n")
			for value in self.logList:
				self.textField.insert("end", value + "\n")
		return self

	def reset(self):
		self.participant = dict()
		self.logList = list()

	def setTextField(self, field):
		self.textField = field
		
	def addParticipantOrder(self, name, value):
		self.participantOrder[name] = value

	def call(self, **info):
		'''
			call entry
			takes the last two frames from the stack to make an entry
		'''
		frame = inspect.currentframe()
		outer = inspect.getouterframes(frame)
		args1, _1a, _1b, locals1_ = inspect.getargvalues(outer[1].frame)
		args2, _2a, _2b, locals2_ = inspect.getargvalues(outer[2].frame)
		_id1, _id2 = "main", "main"
		_name1, _name2 = "main", "main"
		_func1, _func2 = "", "";
		if args1 and args1[0] == 'self':  # typical for instance methods
			selfObject1=locals1_.get('self')
			_name1 = type(selfObject1).__name__
			_id1 = '_' + str(id(selfObject1))
			if _id1 not in self.participant:
				self.participant[_id1] = _name1
				# print("participant " + _id1 + " as \"" + _name1 + "\"")
			_name1 = self.participant[_id1]
		if args2 and args2[0] == 'self':  # typical for instance methods
			selfObject2=locals2_.get('self')
			_id2 = '_' + str(id(locals2_.get('self')))
			if _id2 not in self.participant:
				self.participant[_id2] = _name2
				# print("participant " + _id2 + " as \"" + _name2 + "\"")
			_name2 = self.participant[_id2]
		if outer[1].function != None:
			if outer[2].function != None:
				# _func = " : " + outer[2].function + " " + str(outer[2].lineno) + " -> " + outer[1].function + " " + str(outer[1].lineno)
				_func = " : " + str(outer[2].lineno) + " " + outer[2].function + " ->\\n" + str(outer[1].lineno)  + " " + outer[1].function
			else:
				# _func = " : " + outer[1].function + " " + str(outer[1].lineno)
				_func = " : " + str(outer[1].lineno) + " " + outer[1].function
		# print ("(0)", info)
		# print ("(1)", _id1, args1, _1a, _1b, locals1_, outer[1])
		# print ("(2)", _id2, args2, _2a, _2b, locals2_, outer[2])
		# print ("(2)", outer[1])
		args = ""
		for key, value in info.items():
			args += "\\t" + key + ":" + str(value)
		if len(args) > 1:
			args = "\\n" + args
		self.log(_id2 + " -> " + _id1 + _func + args)
		# self.log ("activate " + _id1)
		
	def ret(self, **info):
		'''
			return entry
			very similar to call, only the arrow goes into the opposite direction
		'''
		frame = inspect.currentframe()
		outer = inspect.getouterframes(frame)
		args1, _1a, _1b, locals1_ = inspect.getargvalues(outer[1].frame)
		args2, _2a, _2b, locals2_ = inspect.getargvalues(outer[2].frame)
		_id1, _id2 = "main", "main"
		_name1, _name2 = "main", "main"
		if args1 and args1[0] == 'self':
			selfObject1=locals1_.get('self')
			_name1 = type(selfObject1).__name__
			_id1 = '_' + str(id(selfObject1))
			if _id1 not in self.participant:
				self.participant[_id1] = _name1
			_name1 = self.participant[_id1]
		if args2 and args2[0] == 'self':
			selfObject2=locals2_.get('self')
			_id2 = '_' + str(id(locals2_.get('self')))
			if _id2 not in self.participant:
				self.participant[_id2] = _name2
			_name2 = self.participant[_id2]
		args = ""
		for key, value in info.items():
			args += "\\t" + key + ":" + str(value)
		if len(args) > 1:
			args = " : " + args
		self.log(_id2 + " <- " + _id1 + args)
		# self.log ("deactivate " + _id1)

	def groupStart(self, name, color="#ddd"):
		self.log("group" + color + " " + color + " " + name)

	def groupEnd(self):
		self.log("end")

	def comment(self, comment, color="#eea"):
		frame = inspect.currentframe()
		outer = inspect.getouterframes(frame)
		args, _1, _2, locals_ = inspect.getargvalues(outer[1].frame)
		_id = "main"
		_name = "main"
		if args and args[0] == 'self':
			selfObject=locals_.get('self')
			_name = type(selfObject).__name__
			_id = '_' + str(id(selfObject))
			if _id not in self.participant:
				self.participant[_id] = _name
			_name = self.participant[_id]
		self.log("note over " + _id + " " + color + ": " + comment)

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
	seqDiagram.comment(str(x0) + "," + str(y0) + "\\n" + str(x1) + "," + str(y1) + "\\n" + str(x2) + "," + str(y2))
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
	return mx,my,r

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

	def drawCircle(self, x,y,r):
		seqDiagram.call()
		lx,ly = self.xy(x - r, y - r)
		ux,uy = self.xy(x + r, y + r)
		self.canvas.create_oval(lx,ly,ux,uy, outline="#cef", fill="", width=5, tags=('circle'))
		kx,ky = self.xy(x,y)
		# center of the circle
		self.canvas.create_oval(kx-7,ky-7,kx+7,ky+7, outline="#000", fill="#fa6", width=1, tags=('circle'))

class Site:
	'''
		basic data
		this denotation is common for fortunes algorithm
		so you can look up the description of this class in any explanation of fortunes algorithm
	'''
	def __init__(self,y,x):
		seqDiagram.call(y=y,x=x)
		self.x = x
		self.y = y
		self.neighbor = []

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def __str__(self):
		return "[" + str(self.x) + "," + str(self.y) + "]"

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

	def dist(self,y,d):
		seqDiagram.call(y=y,d=d)
		# calculate the distance to the beachline
		# y is the point of the y-axis where the beachline is calculated
		# d is the sweepline
		dist = d - (self.getY()*self.getY() + self.getX()*self.getX() + y*y - 2*y*self.getY() - d*d) / (2*self.getX() - 2*d)
		# print("		calculateDist", dist, self, y, d)
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
		# the arc that is the basis for the edge
		self.edgeArc = None
		self.id = BeachArc.next_id
		BeachArc.next_id += 1
		seqDiagram.comment(str(site), color="#cff")

	def getSite(self):
		return self.site

	def getId(self):
		return self.id

	def setNextTop(self, arc):
		seqDiagram.call()
		if arc == None:
			seqDiagram.comment("set Next Top: None")
		else:
			seqDiagram.comment("set Next Top: " + str(arc.getSite()))
		self.nextTop = arc

	def setNextBottom(self, arc):
		seqDiagram.call()
		if arc == None:
			seqDiagram.comment("set Next Bottom: None")
		else:
			seqDiagram.comment("set Next Bottom: " + str(arc.getSite()))
		self.nextBottom = arc

	def getNextTop(self):
		seqDiagram.call()
		return self.nextTop

	def getNextBottom(self):
		seqDiagram.call()
		return self.nextBottom

	def setEdgeArc(self, arc):
		seqDiagram.call()
		seqDiagram.comment("set: " + str(arc.getSite()))
		self.edgeArc = arc

	def getSiteX(self):
		return self.site.getX()

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
		
	def getIntersectionspointsToNextArcs(self,d):
		'''
			intersectionPoints to the next arcs above and below the actual arc
			depending on the sweepline
		'''
		# print ("BeachArc.getLimits.1\t",self.site,d)
		seqDiagram.call(x=d)
		seqDiagram.comment(str(self.site), color="#cff")
		limitLow,limitHigh = None, None
		if self.nextTop != None:
			Py,Px = self.site.getY(), self.site.getX()
			Qy,Qx = self.nextTop.getSite().getY(), self.nextTop.getSite().getX()
			a2 = Qx-Px
			a1 = 2*Py*d - 2*Qy*d - 2*Py*Qx + 2*Px*Qy
			a0 = Px*d*d - Qx*d*d + Qy*Qy*d + Qx*Qx*d - Py*Py*d - Px*Px*d - Px*Qy*Qy - Px*Qx*Qx + Py*Py*Qx + Px*Px*Qx
			aa = a1*a1 - 4*a2*a0
			if 0 <= aa:
				# the two solution (only the limitHigh is actually needed)
				limitHigh = 0.5 * (- math.sqrt(a1*a1 - 4*a2*a0) - a1) / a2
				limitLowNone = 0.5 * (  math.sqrt(a1*a1 - 4*a2*a0) - a1) / a2
			# print ("BeachArc.getLimits.2\t",limitHigh,limitLowNone)
		if self.nextBottom != None:
			Py,Px = self.site.getY(), self.site.getX()
			Qy,Qx = self.nextBottom.getSite().getY(), self.nextBottom.getSite().getX()
			a2 = Qx-Px
			a1 = 2*Py*d - 2*Qy*d - 2*Py*Qx + 2*Px*Qy
			a0 = Px*d*d - Qx*d*d + Qy*Qy*d + Qx*Qx*d - Py*Py*d - Px*Px*d - Px*Qy*Qy - Px*Qx*Qx + Py*Py*Qx + Px*Px*Qx
			aa = a1*a1 - 4*a2*a0
			if 0 <= aa:
				# the two solution (only the limitLow is actually needed)
				limitHighNone = 0.5 * (- math.sqrt(a1*a1 - 4*a2*a0) - a1) / a2
				limitLow = 0.5 * (  math.sqrt(a1*a1 - 4*a2*a0) - a1) / a2
			# print ("BeachArc.getLimits.3\t",limitHighNone,limitLow)
		seqDiagram.ret(limitLow=formatFloatOrNone(limitLow),limitHigh=formatFloatOrNone(limitHigh))
		return limitLow,limitHigh
		
	def __str__(self):
		idTop, idBottom = "-","-"
		if self.nextTop != None:
			idTop = self.nextTop.getId()
		if self.nextBottom != None:
			idBottom = self.nextBottom.getId()
		return "{" + str(self.id) + ":" +str(self.site) + "[" + str(idBottom) + "," + str(idTop) + "]" + "}"
		
	def draw(self,canvas,d):
		'''
			draw the complete Arc
		'''
		seqDiagram.call()
		Py,Px = self.site.getY(), self.site.getX()
		if Px < d:
			line = []
			# for i in range(-amountPoints,amountPoints):
			for y in range(0,101,1):
				# das ist die zentrale Formel für die beachline eines Punktes Py,Px zur Beachline d
				x=(Py*Py + Px*Px + y*y - 2*y*Py - d*d) / (2*Px - 2*d)
				line.extend(canvas.xy(x,y))
			# print (line)
			canvas.canvas.create_line(*line, width=1, fill="#000", activefill = "#f00", tags=('arc'))
			if False:
				y1,y2 = self.getLimits(d)
				x1=(Py*Py + Px*Px + y1*y1 - 2*y1*Py - d*d) / (2*Px - 2*d)
				x2=(Py*Py + Px*Px + y2*y2 - 2*y2*Py - d*d) / (2*Px - 2*d)
				canvas.canvas.create_line(*canvas.xy(x1,y1),*canvas.xy(x2,y2), width=5, fill="#6cc", activefill = "#f00", tags=('hline'))
				
				y1s = round(max(y1,0) * 10)
				y2s = round(min(y2,101) * 10)
				line = []
				# for i in range(-amountPoints,amountPoints):
				for ys in range(y1s,y2s,1):
					y = 0.1 * ys
					# das ist die zentrale Formel für die beachline eines Punktes Py,Px zur Beachline d
					x=(Py*Py + Px*Px + y*y - 2*y*Py - d*d) / (2*Px - 2*d)
					line.extend(canvas.xy(x,y))
				canvas.canvas.create_line(*line, width=3, fill="#00f", activefill = "#f00", tags=('arc'))
				
				print ("altArch",y1,y2)
		
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
		'''
		seqDiagram.call(site=site)
		newCircles = []
		if len(self.arcs) == 0:
			seqDiagram.comment("first Arc in Beachline", color="#fff")
			self.arcs.append(BeachArc(site))
		else:
			bestIndex, bestDist = None, 9999999999
			seqDiagram.comment("Elements in Beachline: " + str(len(self.arcs)), color="#fff")
			# find the Arc-Element with the matchin upper and lower limit
			seqDiagram.groupStart("find best beachArc", color="#dfb")
			for i in range(len(self.arcs)):
				# go through all the arcs
				actualArc = self.arcs[i]
				# print("Beachline.addSite.1\tSite: ",site,"\t",actualArc)
				# first test, is the arc inside the limits
				isInsideLimits = True
				limitLow,limitHigh = actualArc.getIntersectionspointsToNextArcs(site.getX())
				# first limitTest
				if limitLow != None and site.getY() <= limitLow:
					isInsideLimits = False
				if limitHigh != None and site.getY() > limitHigh:
					isInsideLimits = False
				if isInsideLimits:
					seqDiagram.comment(str(i) + " is inside limits: " + str(site.getY()) + " [" + formatFloatOrNone(limitLow) + "," + formatFloatOrNone(limitHigh) + "]" , color="#fff")
					# @TODO bestDist is not needed anymore, limits should be sufficient, remove it when possible
					d = actualArc.dist(site)
					print ("Beachline.addSite\tarc fits\tSite: ",site,"\tindex: ",i,"\tarc: ",actualArc,"\tlimits: ",limitLow,limitHigh,"\tdistance",d)
					if d < bestDist:
						seqDiagram.comment("arc is closest: " + str(i), color="#fff")
						bestDist = d
						bestIndex = i
				else:
					seqDiagram.comment(str(i) + " is outside limits: " + str(site.getY()) + " [" + formatFloatOrNone(limitLow) + "," + formatFloatOrNone(limitHigh) + "]", color="#fff")
					# print ("Beachline.addSite\tarc unfit\tSite: ",site,"\tindex: ",i,"\tarc: ",actualArc,"\tlimits: ",limitLow,limitHigh)
			seqDiagram.groupEnd()
			if bestIndex == None:
				print ("!!! addSite Fehler")
			else:
				seqDiagram.groupStart("add beachArc", color="#efc")
				# insert new Arc on existing Arc
				bestArc = self.arcs[bestIndex]
				seqDiagram.comment("best arc: " + str(bestIndex) + " " + str(bestArc.getSite()) , color="#fff")
				newArc = BeachArc(site)
				bestArcCopy = bestArc.copy()
				# insert the two new ArcElements
				self.arcs[bestIndex+1:bestIndex+1] = [newArc, bestArcCopy]
				bestArcCopy.setNextBottom(newArc)
				bestArc.setNextTop(newArc)
				newArc.setNextBottom(bestArc)
				newArc.setNextTop(bestArcCopy)
				newArc.setEdgeArc(bestArc)
				if bestArcCopy.getNextTop() != None:
					bestArcCopy.getNextTop().setNextBottom(bestArcCopy)
				addIndex = bestIndex+1
				# print ("Beachline.addSite\tadd arc \tSite: ",site, "\tnewArc", newArc,"\tbestArcAbove", bestArc, "\tbestArcBelow", bestArcCopy, "\taddIndex:", addIndex)
				seqDiagram.groupEnd()
				if True:
					seqDiagram.groupStart("set CircleEvents", color="#bdf")
					# add the circleEvents
					c1,c2 = None, None
					if addIndex > 1:
						c1 = circle(self.arcs[addIndex-2].getSite(),self.arcs[addIndex-1].getSite(),self.arcs[addIndex].getSite())
						# print ("Beachline.addSite\tcirc above\tSite: ",c1,"\t", self.arcs[addIndex-2], self.arcs[addIndex-1], self.arcs[addIndex])
						seqDiagram.comment("circle above x:" + formatFloatOrNone(c1[0]) + ", y:" + formatFloatOrNone(c1[1]) + ", r:" + formatFloatOrNone(c1[2]))
					if addIndex < len(self.arcs)-2:
						c2 = circle(self.arcs[addIndex+2].getSite(),self.arcs[addIndex+1].getSite(),self.arcs[addIndex].getSite())
						# print ("Beachline.addSite\tcirc below\tSite: ",c2,"\t", self.arcs[addIndex+2], self.arcs[addIndex+1], self.arcs[addIndex])
						seqDiagram.comment("circle below x:" + formatFloatOrNone(c2[0]) + ", y:" + formatFloatOrNone(c2[1]) + ", r:" + formatFloatOrNone(c2[2]))
					if c1 == None:
						if c2 != None:
							newCircles.append(EventCircle(c2))
					else:
						newCircles.append(EventCircle(c1))
						if c2 != None:
							if c1[0] != c2[0] or c1[1] != c2[1] or c1[2] != c2[2]:
								newCircles.append(EventCircle(c2))
					seqDiagram.groupEnd()
				
		print("Beachline.addSite\tfinished\tSite: ",site,"\t",self, newCircles)
		return newCircles
			
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
			# limitLow, limitHigh = arc.getLimits(d)
			limitLow, limitHigh = arc.edgeLimits(d)
			limitLow2, limitHigh2 = arc.getIntersectionspointsToNextArcs(d)
			# print arc
			edgeArcP = str(arc.edgeArc)
			if arc.edgeArc == None:
				edgeArcP += "\t\t"
			# print ("\tBeachline.drawBeach\t" + str(arc) + "\t" + edgeArcP + "\t" + str(limitLow) + " " + str(limitHigh) + "\t" + str(limitLow2) + " " + str(limitHigh2))
			if limitLow != None and limitHigh != None:
				Py,Px = arc.getSite().getY(), arc.getSite().getX()
				if Px - d != 0:
					xLow=(Py*Py + Px*Px + limitLow*limitLow - 2*limitLow*Py - d*d) / (2*Px - 2*d)
					xHigh=(Py*Py + Px*Px + limitHigh*limitHigh - 2*limitHigh*Py - d*d) / (2*Px - 2*d)
					line = [*canvas.xy(xLow, limitLow), *canvas.xy(xHigh, limitHigh)]
					canvas.canvas.create_line(*line, width=3, fill="#000", activefill = "#f00", tags=('arc'))
			seqDiagram.groupEnd()
		seqDiagram.groupEnd()

class Event:
	'''
		events can be sorted
	'''
	nextEventId = 0
	def __init__(self):
		self.id = Event.nextEventId
		# seqDiagram.call(_id=self.id)
		Event.nextEventId += 1
		self.open = True
		
	def getId(self):
		return self.id
		
	def __lt__(self, other):
		result = other.getX() - self.getX() > 0
		if other.getX() == self.getX():
			result = other.getId() - self.getId() > 0
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
		seqDiagram.call()
		# print ("EventSite.handleEvent\t",self.site)
		result = beachline.addSite(self.site)
		self.open = False
		# seqDiagram.ret()
		return result
		
	def draw(self,canvas,d):
		seqDiagram.groupStart("draw EventSite", color="#dfd")
		seqDiagram.call()
		self.site.draw(canvas,d)
		seqDiagram.groupEnd()
		
	def __str__(self):
		return ".site\t" + str(self.id) + "\t" + "-+"[self.open] + " " + str(self.site)

class EventCircle(Event):
	def __init__(self,coor):
		seqDiagram.call()
		super().__init__()
		self.mx = coor[0]
		self.my = coor[1]
		self.r = coor[2]
		# seqDiagram.out()

	def getY(self):
		return self.my
		
	def getX(self):
		'''
			the circle is defined by the point were the event happens
			and that is on the right edge
		'''
		return self.mx + self.r
		
	def handleEvent(self, beachline):
		seqDiagram.call()
		# print ("EventCircle.handleEvent\t")
		self.open = False
		# seqDiagram.ret()
		return None
		
	def draw(self,canvas,d):
		seqDiagram.groupStart("draw EventCircle", color="#afa")
		seqDiagram.call()
		canvas.drawCircle(self.mx,self.my,self.r)
		seqDiagram.groupEnd()
		
	def __str__(self):
		return ".circle\t" + str(self.id) + "\t" + "-+"[self.open] + " ["+str(self.mx+self.r) + "," + str(self.my) + "]"

class EventQueue:
	def __init__(self):
		seqDiagram.call()
		self.events = []
		self.index = 0
		self.beachline = None
		
	def addQueue(self,event):
		seqDiagram.call()
		seqDiagram.comment("actual event: " + formatFloatOrNone(self.events[self.index].getX()) + "\\nnew event: " + formatFloatOrNone(event.getX()))
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
			
	def stepQueue(self,canvas = None):
		seqDiagram.call()
		actualEvent = self.events[self.index]
		seqDiagram.comment("index = " + str(self.index) + ", x = " + str(actualEvent.getX()))
		# print ("queue step",self.index)
		if self.beachline == None:
			self.beachline = Beachline()
		result = actualEvent.handleEvent(self.beachline)
		print ("EventQueue.step\tresult: ",result)
		if result != None:
			for circleElement in result:
				# print ("EventQueue.step\tresult: ",elem)
				self.addQueue(circleElement)
		self.index += 1
		# for newCircleElements in result:
		#	if canvas != None:
		#		canvas.drawCircle(newCircleElements)
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
		for event in self.events:
			event.draw(canvas,d)
		if self.beachline != None:
			self.beachline.drawBeach(canvas,d)

if __name__ == "__main__":
	app = tk.Tk()
	app.title("Voronoi Test 2")
	
	h,w = 600,1200
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
			b = queue.stepQueue(mcanvas)
			# queue.out()
			value = queue.stepValue()
			if value > d:
				b = False
			seqDiagram.groupEnd()
		
		# draw all events and event-related
		queue.draw(mcanvas, valueSweepline.get())
		
		if False:
			for site in sites:
				print ("***** redraw.drawsite", site, d)
				site.draw(mcanvas)
				a = BeachArc(site)
				a.draw(mcanvas,d)
		
		mcanvas.drawSweepline(valueSweepline.get())
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
		seqDiagram.groupEnd()
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
		seqDiagram.groupEnd()
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
	textFrame = tk.Frame(mainFrame, bd=0, bg="#aaf", relief=tk.SUNKEN)
	scrollbar = tk.Scrollbar(textFrame, orient="vertical")
	text=tk.Text(textFrame, yscrollcommand=scrollbar.set, wrap="none", bd=1, bg="#ffe", relief=tk.SUNKEN, width = 50, padx = 10, pady = 10, font=("Ubuntu Mono", 12, "normal"))
	scrollbar.config(command=text.yview)
	
	# pack all Frames
	mainFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	voronoiFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
	voronoiFrameCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	voronoiFrameSweep.pack(side=tk.TOP, fill=tk.BOTH, expand=0)
	sliderSweep.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
	voronoiCanvas.pack(side=tk.TOP, fill=tk.NONE, expand=0)
	textFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
	text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
	
	seqDiagram.setTextField(text)
	
	seqDiagram.addParticipantOrder("Main", 0)
	seqDiagram.addParticipantOrder("Sites", 30)
	seqDiagram.addParticipantOrder("Site", 31)
	seqDiagram.addParticipantOrder("EventQueue", 10)
	seqDiagram.addParticipantOrder("EventSite", 11)
	seqDiagram.addParticipantOrder("EventCircle", 12)
	seqDiagram.addParticipantOrder("Beachline", 20)
	seqDiagram.addParticipantOrder("BeachArc", 21)
	seqDiagram.addParticipantOrder("MCanvas", 40)
	
	sites = Sites();
	sites.add(40,20)
	sites.add(50,42)
	sites.add(60,10)
	sites.add(25,70)
	sites.add(80,40)
	sites.add(25,40)
	sites.add(20,80)
	
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





