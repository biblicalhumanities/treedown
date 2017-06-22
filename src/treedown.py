# -*- coding: UTF-8

#  Treedown utility
#
#  Converts Treedown to bracket notation or Lowfat XML, 
#  might also support HTML for literate programming.
#
#  Pass-through for all material in multi-line quotes?
#
#  Parsing technique:
#  http://effbot.org/zone/simple-top-down-parsing.htm
#
#  Scanning technique:
#  https://deplinenoise.wordpress.com/2012/01/04/python-tip-regex-based-tokenizer/
# 
#  Python Regular Expressions
#  https://docs.python.org/3/library/re.html
#  https://docs.python.org/2/howto/regex.html
# 
#  Python tokenizer:
#  https://github.com/python/cpython/blob/master/Lib/tokenize.py

import re
import sys
import argparse
import codecs

#  Command line:
#
#  treedown input.td - writes to stdout
#  -b  emit bracket notation (default)
#  -xml emit Lowfat XML

argparser = argparse.ArgumentParser(description='Treedown utility')
argparser.add_argument('input', metavar='infile', type=str, help='input file (in Treedown format)')
args = argparser.parse_args()

# Milestones
#
# [x] simple arg parser
# [x] reads lines from a file
# [x] tokenizes (emit with some delimiter)
# [x] tokenizer more accurately reflects Treedown language
# [ ] brackets
# [ ] XML

# Don't rely on blank line at end to finish!  If you have processed
# the last line, see if you have to emit something.

# Put everything that is not part of the text first in the pattern. 
# That makes it a lot easier to "print out the rest".

scanner = re.compile(r'''
  ^(\s+) |                     # left-hand whitespace
  ([\+\:sv]|pc|od|oi) |        # keywords - needs refinement for latin char languages
  ([-]+) |                     # dashes - may be keywords or punctuation in text
  (\#.+)  |                    # comments
  (\w+) |                      # words
  ([\.\;\"··]) |               # punctuation - incomplete ".,·;—>·()"
  (\s+) |                      # generic whitespace
  (.)                          # an error!
''', re.DOTALL | re.VERBOSE | re.UNICODE)

#  TODO: Consider line continuation

def blank_line(tokens):
  if tokens is None:
    return False
  elif tokens==[] or len(tokens)==1 and tokens[0][0] != "":
    return True
  else:
    return False

# Don't rely on indentation for comments / milestones / annotations
def indent(tokens):
  if blank_line(tokens):
    level = 0
  elif tokens[0][0] == "":
    level = 1
  else:
    spaces = tokens[0][0].count(' ')
    tabs = tokens[0][0].count('\t')
    if spaces > 0:
      if tabs > 0:
        sys.exit("Don't mix tabs and spaces for indentation")
      if spaces % 4 != 0:
        sys.exit("If indenting with spaces, use 4 spaces per level.")
      else:
        tabs = spaces / 4
    level = tabs + 1
  return level 

class Emitter:
  level = 0      # 0 = not in sentence, 1 = top level in sentence, etc.

  def __init__(self, type):   #  type = 'brackets', 'xml', or 'normalize'
      self.type = type

  def leftbrackets(self, tokens):
    newlevel = indent(tokens)
    if newlevel > 0 and self.level == 0: # beginning of sentence
        print "[S "  # 0 -> 1
    for i in range(1, newlevel):
      print "[ "
    print("left: ",self.level,"=>",newlevel)
    self.level = newlevel   

  def rightbrackets(self, tokens):
    newlevel = indent(tokens)
    if newlevel < self.level:
        for i in range(newlevel, self.level):
          print "]"
    print("right: ",self.level,"=>",newlevel)
    self.level = newlevel

  def text(self, tokens):
    if blank_line(tokens) == False:
      print ""

  def line(self, tokens):
    self.leftbrackets(tokens)
    self.text(tokens) 
    self.rightbrackets(tokens)


f = codecs.open(args.input, encoding='utf-8', mode='r')
e = Emitter('brackets')
for line in f:
    print line
    tokens = scanner.findall(line)
    e.line(tokens)