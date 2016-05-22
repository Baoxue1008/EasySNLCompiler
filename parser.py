__author__ = 'baoli1100'
import latex
import copy
from collections import deque
tokens = []
curpos = 0
curToken = None
curLine = 0
syntaxTree = {}
syntaxTreeNode = {}
ultiSym = []
unultiSym = []
syntaxQueue = []
production = []
predict = []
derive = {}
nodenum = 0
emp = []
haveError = False
curTKErr = False
errorList = []

symName = {'=':'EQ',
            '<':'LT',
            '+':'PLUS',
            '-':'MINUS',
	        '*':'TIMES',
            '/':'OVER',
            '[':'LPAREN',
            ']':'RPAREN',
            '.':'DOT',
            ';':'SEMI',
	        ',':'COMMA',
            '(':'LMIDPAREN',
            ')':'RMIDPAREN',
            ':=':'ASSIGN',
            '..':'UNDERANGE'
}

def getNextToken():
    global curpos, curToken, curTKErr
    curpos += 1
    curToken = tokens[curpos]
    curTKErr = False

def getSym():
    global ultiSym, unultiSym
    ultiSym = open('ultiSym.txt').read().split()
    ultiSym = [sym[:-1] if sym[len(sym)-1] == ',' else sym for sym in ultiSym]

    unultiSym = open('unultiSym.txt').read().split()
    unultiSym = [sym[:-1] if sym[len(sym)-1] == ',' else sym for sym in unultiSym]

def getProduction():
    global production
    production = []
    f = open('production.txt')
    lines = f.readlines()
    lines = [l for l in lines if l != '\n']

    left = ""
    for l in lines:
        l = l.strip()
        if '::=' in l:
            l = l.split('::=')
            left = l[0].strip()
            right = l[1].split()
        else:
            right = l.split('|')[1].split()
        production.append((left,tuple(right)))

def getPredict():
    global predict
    predict = open('predict.txt').readlines()
    predict = [line.strip().split(',') for line in predict]


def getDerive():
    global derive
    for word in unultiSym:
        for token in ultiSym:
            for i in range(len(production)):
                prod = production[i]
                if prod[0] == word and len([t for t in predict[i] if match(t,token) == True]) != 0:
                    derive[(word,token)] = prod[1]

def match(curSym,tokenSym):
    if curSym == tokenSym: return True
    tcurSym = copy.deepcopy(curSym); ttokenSym = copy.deepcopy(tokenSym)
    if tcurSym in symName: tcurSym = symName[curSym]
    if tcurSym == ttokenSym: return True
    if ttokenSym in ultiSym: ttokenSym =tokenSym.lower()
    return True if tcurSym == ttokenSym else False

def addChild(father,son):
    global syntaxTree
    if father not in syntaxTree:
        syntaxTree[father] = []
    syntaxTree[father].append(son)


def init():
    global nodenum,emp
    nodenum = 0
    emp = []
    getSym()
    getProduction()
    getPredict()
    getDerive()


def error(line,expect,found):
    global curTKErr,haveError,errorList
    haveError = True
    if curTKErr : return
    curTKErr = True
    inf = 'Error founded at %d line!\n'%line + 'Expected ' + ' or '.join(expect) + '\n' +'Founded ' + found + '\n'
    errorList.append(inf)


def doParser(father):
    global curToken,nodenum,syntaxTreeNode,syntaxTree,emp
    curSym = syntaxTreeNode[father]
    inf = curToken[1] if curToken[2] == None else curToken[2]
    if (curSym,curToken[1]) not in derive:
        need = [ word for word in ultiSym if (curSym,word) in derive ]
        error(curToken[0],need,inf)
        return
    else:
        rightPart = derive[(curSym,curToken[1])]

    print 'Current Token:',curToken
    print 'Use production:',curSym,'->',rightPart
    print
    empty = True
    for sym in rightPart:
        if sym in [word.lower() for word in ultiSym] + [word for word in ultiSym] or sym in symName:
            inf = curToken[1] if curToken[2] == None else curToken[2]
           # print 'CurUltiSym',sym
            if match(sym,curToken[1]):
                empty = False
                print 'Match ultimate symbol',sym,'to',inf
                print
                nodenum += 1
                syntaxTreeNode[nodenum] = inf
                addChild(father,nodenum)
                #print 'Late Token',curToken
                getNextToken()
               # print 'Next Token',curToken
                #print
            else:
                error(curToken[0],[sym],inf)

        elif sym in unultiSym:
           # print 'CurUnultiSym',sym
            nodenum += 1
            syntaxTreeNode[nodenum] = sym
            addChild(father,nodenum)
            res = doParser(nodenum)
            if res == False: empty = False
    if empty == True:
        emp.append(father)
    return empty


def parser():
    global tokens, curToken, curpos, syntaxTree, syntaxTreeNode,nodenum
    init()
    curpos = -1
    nodenum = 0
    getNextToken()
    syntaxTreeNode[nodenum] = 'Program'
    doParser(0)

def printTree(nodeid,deep):
    if nodeid in emp: return
    print '  '*deep,nodeid,syntaxTreeNode[nodeid]
    if nodeid not in syntaxTree: return
    for child in syntaxTree[nodeid]:
        printTree(child,deep+1)


tokens = latex.getToken(r'test/t2.txt')
print 'Parser start!'
parser()

if haveError == False:
    print 'Print syntax tree!'
    printTree(0,0)
else:
    for err in errorList: print err
