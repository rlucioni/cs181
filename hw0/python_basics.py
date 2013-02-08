print 'Hello World'

# More details can be found at:
# http://docs.python.org/library/index.html

# Boolean.  True and False are used to specifiy boolean values
print '----Boolean values'
a = True
b = False
print a == b
print a != b

# Create a string using printf like formatting
mystr = '%s %s %d' % ('part 1', 'part 2', 1)
assert mystr == 'part 1 part 2 1'
# Also can be used with print
print '%s %s %d' % ('part 1', 'part 2', 1)

# Strings
# For more information, see:
# http://docs.python.org/library/stdtypes.html#string-methods
print '\n----Strings'
# Can specify strings using either " or ' quotes
a = 'Hello World!'
b = "Hello World 2!"
# print of variables separated by a comma inserts a space between the two
# variables
print a, b
# Returns the index of 'World' in b
assert b.find('World') == 6

print 'Basic python data structures'
# Data structures
# For more information, see:
# http://docs.python.org/tutorial/datastructures.html

# Lists
print '\n----Lists'
lst = []
lst.append(1)
lst.append(2)
lst.append(10)
print lst
# Sublists.  Syntax is [start:end].  If either is not specified, then this means
# to start at the first element or end at the last element.  Negative indexing
# can be used.  -1 means to end at the second to last element.
print lst[1:]
print lst[:-1]

print 'Iterate over a list'
for element in lst:
  print element

# Dictionaries
print '\n----Dictonaries'
# Dictionaries are maps from keys to values.
classes_to_number = {}
classes_to_number["computer science classes"] = 2
classes_to_number["math classes"] = 1
print classes_to_number
print classes_to_number.values()
for key in classes_to_number:
  print classes_to_number[key]
# Testing whether or not a key is in a dictionary using the 'in' keyword and
# 'not' keywords
assert 'computer science classes' in classes_to_number
assert not 'english classes' in classes_to_number

# File Operations
print '\n----File Operations'
infile = open('points.txt', 'r')
# Read the lines in infile and print them out
for line in infile:
  print line.strip()
