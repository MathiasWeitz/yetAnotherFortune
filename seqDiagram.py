#!/usr/bin/env python3

import os, traceback, inspect

fontCanvas=("Ubuntu Mono", 12, "normal")
seqDiagramVerbose = False

'''
	create an instance with
		seqDiagram = SeqDiagram()
	the basic command is
		seqDiagram.call(...)
	which should always be the beginning of a function / method
	arguments can be any list of parameter, which are displayed on the call-arrow of the diagram
	the optional counterpart to 'call' is
		seqDiagram.ret(...)
	which makes a arrow back to the caller with a list of the given values
	to display any comment, value or marker use the command
		seqDiagram.comment("any string", [color = #hex])
	this will make a box on the lifeline of the participant
	
	to make a box around a certain part of the diagram use
		seqDiagram.groupStart("name", [color = #hex])
		seqDiagram.groupEnd()
'''

class SeqDiagramElement:
	def __init__(self, value = None):
		if type(value) != str:
			raise Exception("should be string")
		self.value = value
		self.origin = None
		self.target = None
		self.groupName = None

	def setOrigin(self, origin):
		self.origin = origin
		return self

	def setTarget(self, target):
		# print ("####", self.target)
		self.target = target
		return self

	def getOrigin(self):
		return self.origin

	def getTarget(self):
		return self.target

	def setGroupName(self, groupName):
		# print ("#### setGroupName", groupName)
		self.groupName = groupName
		return self

	def getGroupName(self):
		return self.groupName

	def out(self):
		return self.value
		
	def __str__(self):
		return "<<SeqDiagramElement [" + str(self.origin) + "]->[" + str(self.target) + "] \"" + str(self.groupName) + "\":" + str(self.value) + ">>"

class SeqDiagramResult:
	def __init__(self, seqDiagram):
		self.seqDiagram = seqDiagram
		self.value = 0
		self.valueActive = 0
		self.groups = {}
		self.elems = []

	def getValue(self):
		return self.value

	def getValueActive(self):
		return self.valueActive

	def addActive(self, value):
		if type(value) == int:
			self.valueActive += value
		elif type(value) == SeqDiagramResult:
			self.valueActive += value.getValueActive()

	def getGroup(self):
		return self.groups

	def getElems(self):
		return self.elems

	def __iadd__(self, arg):
		if type(arg) == int:
			self.value += arg
		elif type(arg) == SeqDiagramResult:
			self.value += arg.getValue()
			# self.valueActive += arg.getValueActive()
			for name,group in arg.getGroup().items():
				if name not in self.groups:
					self.groups[name] = []
				self.groups[name].extend(arg.getGroup()[name]) 
			self.elems.extend(arg.getElems())
		else:
			raise Exception("SeqDiagramResult: unvalid type")
		return self

	def __str__(self):
		return "~" + str(self.value) + "(" + str(self.valueActive) + ") " + str(self.groups) + " " + str(self.elems) + "~"

	def addGroup(self, name, elem):
		if name != None:
			if name not in self.groups:
				self.groups[name] = []
			self.groups[name].append(elem)

	def addElem(self, elem):
		self.elems.append(elem)
		
	def outValue(self):
		return self.value

	def outItems(self, reverseOrder = False, unique = False):
		''' 
			id of instances in order of use, multiple entries are normal
			if you use unique, only the first or last appearence is logged
		'''
		li = self.elems
		result = []
		if reverseOrder:
			li = reversed(self.elems)
		for elem in li:
			# print(elem, className)
			if not unique or elem not in result:
				result.append(elem)
		return result

	def outClasses(self, reverseOrder = False):
		'''
			all Classes of Instances in order of their first or last appearance
		'''
		li = self.elems
		result = []
		if reverseOrder:
			li = reversed(self.elems)
		for elem in li:
			className = "main"
			if elem in self.seqDiagram.participant:
				className = self.seqDiagram.participant[elem]
			# print(elem, className)
			if className not in result:
				result.append(className)
		return result

	def getLastOfClass(self, arg, maxElem = 1):
		'''
			get the last $maxElem instances of a class
		'''
		li = reversed(self.elems)
		result = []
		for elem in li:
			className = "main"
			if elem in self.seqDiagram.participant:
				className = self.seqDiagram.participant[elem]
			# print (">>>", elem, className)
			if className == arg and len(result) < maxElem:
				result.append(elem)
		return result

class SeqDiagram:
	actualGroup = None
	def __init__(self):
		self.statusActive = True
		self.parent = None
		self.parentGroup = None
		# the UI on the Applikation should be a TK-Text
		# if no Textfield is given the output goes to the console
		self.textField = None
		# set a priority for every element of a certain class
		# that makes the element of the same class group together
		# key = class-name, value = order
		self.participantOrder = dict()
		# key = object-id, value = classname
		self.participant = dict()
		self.logList = list()
		# store a list of groups, that should not appear in the diagrams
		self.hide = list()

	def log(self, text, target=None, source=None):
		# print ("###!", text, target, source)
		actualGroupName = "None"
		if SeqDiagram.actualGroup != None:
			actualGroupName = str(id(SeqDiagram.actualGroup))
		# print ("***:\t" + actualGroupName + "\t" + str(id(self)) + "\t" + str(text))
		if type(text) == str:
			text = SeqDiagramElement(text)
		if target != None:
			text.setTarget(target)
		if source != None:
			text.setOrigin(source)
		if SeqDiagram.actualGroup == None:
			self.logList.append(text)
		else:
			SeqDiagram.actualGroup.logList.append(text)
		return text

	def getAllParticipants(self):
		'''
			get all participants from the active elements
		'''
		# print ("***:\tgetAllParticipants")
		if self.statusActive:
			for key, value in self.participant.items():
				if key not in self.top().participant:
					# print ("***:\tadd getAllParticipants")
					self.top().participant[key] = value
			for content in self.logList:
				if type(content) != str and type(content) != SeqDiagramElement:
					content.getAllParticipants()

	def collectParticipants(self):
		result = dict()
		if self.statusActive:
			for value in self.logList:
				if type(value) == str:
					pass
				elif type(value) == SeqDiagramElement:
					origin = value.getOrigin()
					target = value.getTarget()
					
					nameOrigin, nameTarget = "main", "Main"
					if origin != None:
						if origin in self.participant:
							nameOrigin = self.participant[origin]
						elif origin in self.top().participant:
							nameOrigin = self.top().participant[origin]
						result[origin] = nameOrigin
					if target != None:
						if target in self.participant:
							nameTarget = self.participant[target]
						elif target in self.top().participant:
							nameTarget = self.top().participant[target]
						result[target] = nameTarget
				else:
					resultC = value.collectParticipants()
					for key, value in resultC.items():
						result[key] = value
		return result

	def out(self):
		# get all participant
		if self.statusActive:
			if self.parent == None:
				# self.hideOut()
				self.getAllParticipants()
			# sort the participant
			# participant = self.top().participant
			participant = self.collectParticipants()
			pk = list(participant.keys())
			pk.sort(key=lambda x:(participant[x] not in self.top().participantOrder, self.top().participantOrder.get(participant[x])))
			textField = self.top().textField
			if textField == None:
				if self.getParent() == None:
					print ("\n*****************************\n")
					print ("participant main as \"Main\"")
					for key, value in participant.items():
						print ("participant " + key + " as \"" + value + "\"")
					print ()
				for value in self.logList:
					print ("type(value)", type(value))
					if type(value) == str:
						print (str(id(self)), value)
					elif type(value) == SeqDiagramElement:
						print (str(id(self)), value.out())
					else:
						value.out()
			else:
				lastBox=None
				if self.parent == None:
					for tag in textField.tag_names():
						textField.tag_delete(tag)
					textField.tag_config("part", foreground="blue")
					textField.delete("1.0", "end")
					# textField.insert("end", "participant main as \"Main\"\n", "part")
					for key in pk:
						if participant.get(key) != lastBox:
							if lastBox != None:
								textField.insert("end", "end box\n", "part")
							lastBox = participant.get(key)
							textField.insert("end", "box \"" + lastBox + "\" #ccc\n", "part")
						textField.insert("end", "participant " + key + " as \"" + participant.get(key) + "\"" + "\n", "part")
				if lastBox != None:
					textField.insert("end", "end box\n", "part")
				textField.insert("end", "\n")
				for value in self.logList:
					if type(value) == str:
						# print ("out+:", value)
						textField.insert("end", str(value) + "\n")
					elif type(value) == SeqDiagramElement:
						# print ("out!:", value.out())
						textField.insert("end", str(value.out()) + "\n")
					else:
						# print ("out>:", value)
						value.out()
		else:
			# textField.insert("end", "hnote over value: idle" + "\n")
			# print ("*************** out status passive *******************")
			pass
		return self

	def hideElements(self, elements):
		self.top().hide = list(set(self.top().hide + elements))
		
	def activate(self, activateElements = []):
		'''
			deactivate all elements except those, which are in the list, and their groups
		'''
		self.statusActive = True
		if 0 < len(activateElements) and self.getParent() != None:
			self.statusActive = False
		result = False
		for value in self.logList:
			if type(value) == str:
				pass
			elif type(value) == SeqDiagramElement:
				origin = value.getOrigin()
				target = value.getTarget()
				if origin != None and origin in activateElements:
					result = True
					self.statusActive = True
				if target != None and target in activateElements:
					result = True
					self.statusActive = True
			else:
				result = value.activate(activateElements)
				if result:
					self.statusActive = True
		return result

	def hideOut(self):
		'''
			deactivate all groups
			only keeps the topElements
		'''
		self.statusActive = True
		for value in self.logList:
			if type(value) == str:
				if re.search(r"group", value):
					self.statusActive = False
					print ("#*** deactivated", value)
			elif type(value) == SeqDiagramElement:
				pass
			else:
				value.hideOut()
		return self.statusActive

	def reset(self):
		for content in self.logList:
			if type(content) != str and type(content) != SeqDiagramElement:
				content.reset()
		self.participant = dict()
		self.logList = list()
		self.hide = list()
		SeqDiagram.actualGroup = None

	def setTextField(self, field):
		self.top().textField = field
		
	def addParticipantOrder(self, name, value):
		self.top().participantOrder[name] = value

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
				if _id1 in self.top().participant:
					_name1 = self.top().participant[_id1]
				self.participant[_id1] = _name1
				# print("participant " + _id1 + " as \"" + _name1 + "\"")
			_name1 = self.participant[_id1]
		if args2 and args2[0] == 'self':  # typical for instance methods
			selfObject2=locals2_.get('self')
			_id2 = '_' + str(id(locals2_.get('self')))
			if _id2 not in self.participant:
				if _id2 in self.top().participant:
					_name2 = self.participant[_id2]
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
		self.log(_id2 + " -> " + _id1 + _func + args, _id2, _id1)
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
		'''
			the group is an instance in the log
		'''
		frame = inspect.currentframe()
		outer = inspect.getouterframes(frame)
		args, _a, _b, locals_ = inspect.getargvalues(outer[1].frame)
		
		_id = "main"
		_name = "main"
		_func = ""
		if args and args[0] == 'self':  # typical for instance methods
			selfObject=locals_.get('self')
			_name = type(selfObject).__name__
			_id = '_' + str(id(selfObject))
			if _id not in self.participant:
				if _id in self.top().participant:
					_name = self.top().participant[_id]
				self.participant[_id] = _name
			_name = self.participant[_id]
		if outer[1].function != None:
			if outer[2].function != None:
				# _func = " : " + outer[2].function + " " + str(outer[2].lineno) + " -> " + outer[1].function + " " + str(outer[1].lineno)
				_func = " : " + str(outer[2].lineno) + " " + outer[2].function + " ->\\n" + str(outer[1].lineno)  + " " + outer[1].function
			else:
				# _func = " : " + outer[1].function + " " + str(outer[1].lineno)
				_func = " : " + str(outer[1].lineno) + " " + outer[1].function
		group = SeqDiagram()
		self.log(group)
		group.setParent(self)
		group.setParentGroup(SeqDiagram.actualGroup)
		SeqDiagram.actualGroup = group
		# SeqDiagram.actualGroup.setParent(self)
		if seqDiagramVerbose:
			print ("!!! group start", id(SeqDiagram.actualGroup), name, _id, _name)
		elem = SeqDiagram.actualGroup.log("group" + color + " " + color + " " + name, _id)
		elem.setGroupName(name)

	def groupEnd(self, comment=""):
		if seqDiagramVerbose:
			print ("!!! group end", id(SeqDiagram.actualGroup), comment)
		SeqDiagram.actualGroup.log("end")
		if SeqDiagram.actualGroup.getParentGroup() != None:
			SeqDiagram.actualGroup = SeqDiagram.actualGroup.getParentGroup()
		
	def setGroupName(self, name):
		print ("setGroupName logList", str(self.logList))
		pass
		
	def setParent(self, parent):
		self.parent = parent

	def getParent(self):
		return self.parent
	
	def setParentGroup(self, parentGroup):
		self.parentGroup = parentGroup

	def getParentGroup(self):
		return self.parentGroup

	def top(self):
		result = self
		while result.getParent() != None:
			result = result.getParent()
		return result

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
	
	def displayStructure(self, tab = 0):
		'''
			iterates recursively through the logs and collects all items
			result is length, the logitems and groupnames
		'''
		# result = {"groups": {}}
		result = SeqDiagramResult(self)
		if seqDiagramVerbose:
			if tab == 0:
				print ("*******************************")
			if self.statusActive:
				print ("\t" * 2 * tab, "*** active")
			else:
				print ("\t" * 2 * tab, "*** passiv")
		for elem in self.logList:
			# print ("\t" * tab, elem)
			if type(elem) == str:
				# pure string
				if seqDiagramVerbose:
					print ("\t" * (2 * tab + 1), "s:", elem)
				result += 1
				if self.statusActive:
					result.addActive(1)
			elif type(elem) == SeqDiagramElement:
				# special-element
				groupName  = elem.getGroupName()
				if seqDiagramVerbose:
					print ("\t" * (2 * tab + 1), "d:", elem.out(), str(elem), str(groupName))
				if groupName != None:
					result.addGroup(groupName,elem)
				if elem.getTarget() != None:
					result.addElem(elem.getTarget())
				result += 1
				if self.statusActive:
					result.addActive(1)
			else:
				resultSub = elem.displayStructure(tab + 1)
				result += resultSub
				if self.statusActive:
					result.addActive(resultSub.getValueActive())
				# if self.statusActive:
				#	result.addActive(resultSub)
		if seqDiagramVerbose:
			print ("\t" * 2 * tab, "*** length", str(result))
		
		return result
	
	def __len__(self):
		result = 0
		for elem in self.logList:
			# print ("type(value)", type(elem))
			if type(elem) == str:
				result += 1
			elif type(elem) == SeqDiagramElement:
				result += 1
			else:
				result += len(elem)
		return result


