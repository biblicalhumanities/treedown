# -*- coding: UTF-8
#  Treedown utility
#
#  Converts Treedown to bracket notation or Lowfat XML, 
#  might also support HTML for literate programming.

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


  def emit(self, line):
    tokens = scanner.findall(line) 
    if blank_line(tokens):
      return

    newlevel = indent(tokens)

    if newlevel > 0 and self.level == 0: # beginning of sentence
        print "[S "  # 0 -> 1
        lbracks = range(self.level + 1, newlevel)
    else:
        lbracks = range(self.level, newlevel)
    for i in lbracks:
        print "[ " 

    for i in range(newlevel, self.level):
      print "]"

    print "["+line.strip()+"]"


    self.level = newlevel   


  def cleanup(self):
    for i in range(0, self.level):
      print "]"

f = codecs.open(args.input, encoding='utf-8', mode='r')
e = Emitter('brackets')
for line in f:
    e.emit(line)
e.cleanup()