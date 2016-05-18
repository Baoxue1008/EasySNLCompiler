__author__ = 'baoli1100'
import copy

tokens = []
curpos = 0
curToken = None
curLine = 0


class node():
    nodekind = 0
    child = []
    line = 0
    def __init__(self,type = 'unknown'):
        self.nodekind = type
        self.child = []
        self.linenum = 0

def getNextToken():
    global curPos
    global tokens
    global curToken
    curpos += 1
    curToken = tokens[curPos]


def syntaxError():
    print 'error'

def match(nextToken):
    if curToken[1] == nextToken:
        getNextToken()
        curLine = curToken[0]
    else:
        syntaxError()
        getNextToken()

def program():
    t = programHead()
    q = declarePart()
    s = programBody()
    root = node('ProK')

    root.linenum = 0
    root.child.append(t)
    root.child.append(q)
    root.child.append(s)
    match('DOT')
    return root

def programHead():
    t = node('PheadK')
    match('PROGRAM')
    if curToken[1] == 'ID':
        t.linenum = 0
        t.name = curToken[2]
    match('ID')
    return t

def declarePart():
    typeP = node('TypeK')
    pp = typeP
