

testCode = """
[cateringType:OptionGroup r]
[reason:TextField r]
[startDate:PopupDateField r] [startTime:PopupDateField]  [stopDate:PopupDateField r] [stopTime:PopupDateField]
[location:TextField r]
[assignmentType:OptionGroup r] [assignmentObject:TextField r]
[requester:TextField r]
"""

from .parsec import *
from pprint import *

from .common import *
import os

class Component(object):
	
	def __init__(self, arg):
		super(Component, self).__init__()
		self.name = arg[0]
		self.type = arg[1]
		self.props = arg[2]

class Property(object):
	
	def __init__(self, arg):
		super(Property, self).__init__()
		self.name = arg[0]
		self.args = arg[1]
		self.arg = self.args[0] if self.args else None
		


name = ident
jType = ident
sep = comma
arglist = lparen >> sepBy1(ident, sep) << rparen
myProperty = (ident + optional(arglist, [])).parsecmap(Property)
properties = sepBy(myProperty, sep)
component = joint(lbracket >> name << colon, jType, properties, rbracket).parsecmap(Component)
line = many(component) << le
definition = many(line)

#print Parser(ident).parse('dd  ')
#print Parser(arglist).parse('(dd,ff,gg)')
#print Parser(myProperty).parse('asdf(dd,ff,gg)')
#print Parser(myProperty).parse('asdf')
#print Parser(component).parse('[assignmentObject:TextField]')
#print Parser(line).parse('[assignmentObject:TextField][olol:OptionGroup]\n')
#lines = Parser(definition).parse(testCode)

def components(lines):
	for components in lines:
		for component in components:
			yield component

def generateFields(lines):
	return os.linesep.join(map("private final {0.type} {0.name};".format, components(lines)))

def generateInits(lines):
	return os.linesep.join(map(generateInit, components(lines)))

def generateInit(component):
	result = ""
	result += "{0.name} = new {0.type}();".format(component)
	result += "".join([os.linesep+'{c.name}.setCaption(translate("{p.arg}"));'.format(c=component, p=p) for p in component.props if p.name=='caption'])
	return result

def generateLayout(lines):
	return join([generateHorLayout(x) for x in lines if x],
		','+os.linesep,
		"new VerticalLayout("+os.linesep,
		os.linesep+")")

def generateHorLayout(components):
	if len(components) > 1:
		return join(map(lambda x: '        '+generateComponent(x), components),
			','+os.linesep,
			'    new HorizontalLayout('+os.linesep,
			os.linesep+'    )')
	elif len(components) == 1:
		return '    '+generateComponent(components[0])

def generateComponent(component):
	return component.name

def transform(text):
	lines = Parser(definition).parse(text)
	return join((generateFields(lines), generateInits(lines), generateLayout(lines)), 2*os.linesep)
