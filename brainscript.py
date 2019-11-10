"""
BrainScript by h34
Copyright (C) h34ting4ppliance 2019
Licensed under GNU GPL version 3 because yes.
}

You can even eval normal brainfuck code :
eval(++[>+++<-])
"""

import sys, getch # Will need it for later

############################## Command Parsing

def parseCommand(line):
	if not(line.count("(") == line.count(")") == 1):
		return ["!SYNTAX_ERROR1"]

	objName = line[:line.find("(")]
	if objName == "":
		return ["!SYNTAX_ERROR2"]

	args = line[line.find("(") + 1:line.find(")")]

	if args == "":
		Aargs = []
	else:
		Aargs = args.replace(" ", "").split(",")

		if line[line.find(")")+1:] != "":
			print(line[line.find(")"):])
			return ["!SYNTAX_ERROR3"]

	output = [objName]
	for x in Aargs:
		output.append(x)

	return output

def indexFunctions(code):
	tempIndex, indexDict, funcTypes = None, {}, {}
	if not(code.count("{") == code.count("}")):
		return None
	if code.count("{") == 0:
		return {}

	Ccode = code.replace("\t", "").replace("\n", "").split(";")

	for x in range(len(Ccode)):
		Ccode[x] = Ccode[x].strip()

	for x, y in enumerate(Ccode):
		if y.endswith("{"):
			t = y[:-1].strip().split(":")
			if len(t) != 2:
				print(t)
				return 0
			if tempIndex != None:
				return 1
			if t[0] != "relative" and t[0] != "absolute":
				return 2
			if t[1] in indexDict:
				return 3

			tempIndex = x

		if y == "}":
			if tempIndex == None:
				return 4

			n = Ccode[tempIndex][:-1].strip().split(":")
			indexDict[n[1]] = tempIndex
			funcTypes[n[1]] = n[0]
			tempIndex = None

	return (indexDict, funcTypes)

def indexBraces(code):
	bmap = {}
	tempMap = []
	Ccode = code.replace("\t", "").replace("\n", "").split(";")

	for y, x in enumerate(Ccode):
		if x.strip() == "!": tempMap.append(y)
		if x.strip() == "?":
			start = tempMap.pop()
			bmap[start] = y
			bmap[y] = start

	return bmap

############################## BrainScript

class BrainScript:
	def __init__(self, code):
		if not(code.count("(") == code.count(")") and code.count("{") == code.count("}") and code.count("!") == code.count("?")):
			raise SyntaxError("Brackets syntax error.")

		self.code = code.replace("\t", "").replace("\n", "").split(";")
		for x in range(len(self.code)):
			self.code[x] = self.code[x].strip()


		self.data = [0]
		# print(indexFunctions(code))
		self.funcIndex = indexFunctions(code)[0]
		self.funcTypes = indexFunctions(code)[1]
		# print((self.funcIndex, self.funcTypes))
		self.loopIndex = indexBraces(code)
		# print(self.loopIndex)
		if type(self.funcIndex) is int or self.funcIndex == None:
			raise SyntaxError("Function Definition Error : " + str(funcIndex))
		if "main" not in self.funcIndex:
			raise SyntaxError("Main function not found")
		if self.funcTypes["main"] != "absolute":
			raise TypeError("Main function must be absolute")

	def execute(self):
		dpStack = [0]
		subroutineStack = []
		instPtr = self.funcIndex["main"]
		dataptr = 0

		while (instPtr < len(self.code)):
			instPtr += 1
			# print(str(instPtr) + "\t" + str(dataptr) + "\t" + str(subroutineStack))
			curcode = self.code[instPtr]
			if self.code[instPtr] != "!" and self.code[instPtr] != "?" and self.code[instPtr] != "}":
				code = parseCommand(self.code[instPtr])
				if code[0].startswith("!"):
					print("parseCommand- " + code[0])
					return 1
			else:
				code = [self.code[instPtr]]

			repeat = 1 if len(code) == 1 else int(code[1])
			instruction = code[0]

			if instruction == "right":
				for x in range(repeat):
					dataptr += 1
					if dataptr == len(self.data):
						self.data.append(0);
			elif instruction == "left":
				for x in range(repeat):
					dataptr = dataptr - 1 if dataptr > 0 else 0
			elif instruction == "add":
				# memory[dataPtr] = memory[dataPtr] + 1 if memory[dataPtr] < 255 else 0
				for x in range(repeat):
					self.data[dataptr] = self.data[dataptr] + 1 if self.data[dataptr] < 255 else 0
			elif instruction == "sub":
				for x in range(repeat):
					self.data[dataptr] = self.data[dataptr] - 1 if self.data[dataptr] > 0 else 255
			elif instruction == "print":
				for x in range(repeat):
					print(chr(self.data[dataptr]), end='')
			elif instruction == "input":
				self.data[dataptr] = ord(getch.getch())
				# print(self.data[dataptr])
			elif instruction == "!":
				if self.data[dataptr] == 0:
					instPtr = self.loopIndex[instPtr]
			elif instruction == "?":
				if self.data[dataptr] != 0:
					instPtr = self.loopIndex[instPtr]
			elif instruction in self.funcIndex:
				if self.funcTypes[instruction] == "relative":
					# print(instruction + " is a relative function")
					dpStack.append(dataptr)
				if self.funcTypes[instruction] == "absolute":
					# print("wtf.")
					dpStack.append(dataptr)
					dataptr = 0

				subroutineStack.append(instPtr)
				instPtr = self.funcIndex[instruction]
			elif instruction == "}":
				dataptr = dpStack.pop()
				if subroutineStack == []:
					return 0
				else:
					instPtr = subroutineStack.pop()
			else:
				print("Syntax Error at line " + str(instPtr))
				return 1

##############################

