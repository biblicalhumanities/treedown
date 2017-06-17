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
# [ ] tokenizes (emit with some delimiter)
# [ ] tokenizer more accurately reflects Treedown language
# [ ] brackets
# [ ] XML


# TODO: extend for Greek punc
# TODO: add extensions:  ( scope=constituent, status=new )

SCANNER = re.compile(r'''
  (\s+) |                      # whitespace
  (\#)[^\n]* |                 # comments
  (\d+) |                      # integer literals
  ([][(){}<>=,;:*+-/]) |       # punctuation
  ([A-Za-z_][A-Za-z0-9_]*) |   # identifiers
  """(.*?)""" |                # multi-line string literal
  "((?:[^"\n\\]|\\.)*)" |      # regular string literal
  (.)                          # an error!
''', re.DOTALL | re.VERBOSE)


#  Return 5-tuples as in Python scanner	
#  Consider line continuation

f = open(args.input)
for line in f:
  print line,