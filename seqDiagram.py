#!/usr/bin/env python3

import os, traceback, inspect

fontCanvas=("Ubuntu Mono", 12, "normal")

class SeqDiagramElement:
	def __init__(self, value = None):
		if type(value) != str:
			raise Exception("should be string")
		self.value = value
		self.origin = None
		self.target = None

	def setOrigin(self, origin):
		self.origin = origin
		return self

	def setTarget(self, target):
		# print ("####", self.target)
		self.target = target
		return self

	def out(self):
		return self.value
		
	def __str__(self):
		return "<<SeqDiagramElement [" + str(self.origin) + "]->[" + str(self.target) + "] :" + str(self.value) + ">>"

class SeqDiagram:
	actualGroup = None
	def __init__(self):
		self.statusActive = True
		self.parent = None
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
		return self

	def getAllParticipants(self):
		# print ("***:\tgetAllParticipants")
		if self.statusActive:
			for key, value in self.participant.items():
				if key not in self.top().participant:
					# print ("***:\tadd getAllParticipants")
					self.top().participant[key] = value
			for content in self.logList:
				if type(content) != str and type(content) != SeqDiagramElement:
					content.getAllParticipants()

	def out(self):
		# get all participant
		if self.statusActive or True:
			if self.parent == None:
				self.hideOut()
				self.getAllParticipants()
			# sort the participant
			participant = self.top().participant
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
					textField.insert("end", "participant main as \"Main\"\n", "part")
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
			pass
		return self

	def hideElements(self, elements):
		self.top().hide = list(set(self.top().hide + elements))
		
	def hideOut(self):
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
			_name1 = self.participant[_id]
		if outer[1].function != None:
			if outer[2].function != None:
				# _func = " : " + outer[2].function + " " + str(outer[2].lineno) + " -> " + outer[1].function + " " + str(outer[1].lineno)
				_func = " : " + str(outer[2].lineno) + " " + outer[2].function + " ->\\n" + str(outer[1].lineno)  + " " + outer[1].function
			else:
				# _func = " : " + outer[1].function + " " + str(outer[1].lineno)
				_func = " : " + str(outer[1].lineno) + " " + outer[1].function

		group = SeqDiagram()
		self.log(group)
		SeqDiagram.actualGroup = group
		SeqDiagram.actualGroup.setParent(self)
		SeqDiagram.actualGroup.log("group" + color + " " + color + " " + name)

	def groupEnd(self):
		SeqDiagram.actualGroup.log("end")
		if SeqDiagram.actualGroup.getParent() != None:
			print ("!!! goto Parent")
			SeqDiagram.actualGroup = SeqDiagram.actualGroup.getParent()
		
	def setParent(self, parent):
		self.parent = parent

	def getParent(self):
		return self.parent
		
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
		if self.statusActive:
			print ("\t" * 2 * tab, "*** active")
		else:
			print ("\t" * 2 * tab, "*** passiv")
		result = 0
		for elem in self.logList:
			# print ("\t" * tab, elem)
			if type(elem) == str:
				# pure string
				print ("\t" * (2 * tab + 1), "s:", elem)
				result += 1
			elif type(elem) == SeqDiagramElement:
				# special-element
				print ("\t" * (2 * tab + 1), "d:", elem.out(), str(elem))
				result += 1
			else:
				result += elem.displayStructure(tab + 1)
		print ("\t" * 2 * tab, "*** length", result)
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


