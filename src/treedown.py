# -*- coding: UTF-8
#  Treedown utility
#
#  Converts Treedown to bracket notation or Lowfat XML.

import re
import sys
import argparse
import codecs

scanner = re.compile(r'''
    ^(\s+) |                     # left-hand whitespace
    ([\+\:sv]|pc|od|oi) |        # keywords
    ([-]+) |                     # dashes - keywords or punctuation
    (\#.+)  |                    # comments
    (\w+) |                      # words
    ([\.\;\"··\-,]) |            # punctuation - incomplete ".,·;—>·()"
    (\s+) |                      # generic whitespace
    (.)                          # an error!
''', re.DOTALL | re.VERBOSE | re.UNICODE)


class BracketEmitter:
    def labeled_leftbracket(self, label):
        print "["+str(label)

    def leftbracket(self):
        print "["

    def rightbracket(self):
        print "]"

    def word(self, string):
        print string

    def punc(self, string):
        print string

    def whitespace(self, string):
        print string

    def unexpected(self, string):
        print string


class XMLEmitter:
    def labeled_leftbracket(self, label):
        print '<wg role="'+str(label)+'">'

    def leftbracket(self):
        print "<wg>"

    def rightbracket(self):
        print "</wg>"

    def word(self, string):
        print "<w>" + string + "</w>"

    def punc(self, string):
        print "<pc>" + string + "</pc>"

    def whitespace(self, string):
        return

    def unexpected(self, string):
        print "<error>" + string + "</error>"


class LineParser:
    level = 0      # 0 = not in sentence, 1 = top level in sentence, etc.
    emitter = None

    def __init__(self, emitter):   # type = 'brackets', 'xml', or 'normalize'
        self.emitter = emitter

    def milestone(self, tokens):
        return False

    def comment_line(self, tokens):
        if len(tokens) == 1 and tokens[0][3] != "":
            return True
        elif len(tokens) == 2 and tokens[1][3] != "":
            return True
        else:
            return False

    def blank_line(self, tokens):
        if tokens is None:
            return False
        elif tokens == [] or len(tokens) == 1 and tokens[0][0] != "":
            return True
        else:
            return False

    def indentation(self, tokens):
        if self.blank_line(tokens):
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

    def process(self, line):
        tokens = scanner.findall(line)

        if self.milestone(tokens):
            return
        if self.comment_line(tokens):
            return
        if self.blank_line(tokens):
            return

        newlevel = self.indentation(tokens)

        if newlevel > 0 and self.level == 0:  # beginning of sentence
            self.emitter.labeled_leftbracket("S")
            lbracks = range(self.level + 1, newlevel)
        else:
            lbracks = range(self.level, newlevel)
        for i in lbracks:
            self.emitter.leftbracket()

        for i in range(newlevel, self.level):
            self.emitter.rightbracket()

        self.line_content(tokens)

        self.level = newlevel

    def line_content(self, tokens):
        label = False
        for t in tokens:
            if t[0] != "":    # indentation
                continue
            elif t[1] != "":  # label
                self.emitter.labeled_leftbracket(t[1])
                label = True
            elif t[2] != "":  # dash ... TODO
                continue
            elif t[3] != "":  # TD comment
                continue
            elif t[4] != "":  # word
                self.emitter.word(t[4])
            elif t[5] != "":  # punctuation
                self.emitter.punc(t[5])
            elif t[6] != "":  # whitespace
                self.emitter.whitespace(t[6])
            elif t[7] != "":  # unexpected
                self.emitter.unexpected(t[7])

        if label is True:
            self.emitter.rightbracket()

    def cleanup(self):
        for i in range(0, self.level):
            self.emitter.rightbracket()


argparser = argparse.ArgumentParser(description='Treedown utility')
argparser.add_argument('input', metavar='infile', type=str, help='input file (in Treedown format)')
argparser.add_argument("-b", "--brackets", help="produce bracket notation instead of XML", action="store_true")
args = argparser.parse_args()

f = codecs.open(args.input, encoding='utf-8', mode='r')
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

if args.brackets:
    lp = LineParser(BracketEmitter())
else:
    lp = LineParser(XMLEmitter())
for line in f:
    lp.process(line)
lp.cleanup()

# Full parsing of line
# Complete XML structure
# Add pattern for annotations
# Add pattern for milestones
# Don't rely on indentation for comments / milestones / annotations
