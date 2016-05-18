__author__ = 'Baoxue1008'


tokens = []

change = {}

delimiter = '+-*/();[]<, '

lexicalInf = ['PROGRAM','PROCEDURE','TYPE','VAR','IF',
	'THEN',	'ELSE',	'FI','WHILE','DO',
	'ENDWH','BEGIN','END','READ','WRITE',
	'ARRAY','OF','RECORD','RETURN',
	'INTEGER','CHAR']

deliName = {'=':'EQ',
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
            ')':'RMIDPAREN'
}

def getChange():
    global change
    change = {}
    text = open('change.txt').readlines()
    for line in text:
        vals = line.strip().split()
        for i in range(len(vals)):
            vals[i] = int(vals[i][1:])
        tmpdir = {}
        for i in range(len(vals)-1):
            tmpdir[i] = vals[i+1]
        change[vals[0]] = tmpdir

def getToken(state,buf,line):
    if state == 1:
        capbuf = buf.upper()
        if capbuf in lexicalInf:
            return (line,capbuf,None)
        else:
            return (line,'ID',buf)

    if state == 2: return (line,'INTC',int(buf))
    if state == 3: return (line,deliName[buf],None)
    if state == 5: return (line,'ASSIGN',None)
    if state == 8: return (line,'DOT',None)
    if state == 9: return (line,'UNDERANGE',None)
    if state == 12: return (line,'CHARC',buf)
    if state == 13: return (line,'ERROR',None)




def getType(ch):
    if ch.isalpha(): return 0
    if ch.isdigit(): return 1
    if ch in delimiter: return 2
    if ch == ':': return 3
    if ch == '=': return 4
    if ch == '{': return 5
    if ch == '}': return 6
    if ch == '.': return 7
    if ch == '\'': return 8
    else : return 9



def main(dir):
    getChange()
    text = open(dir).read()
    curState = 0
    linenum = 1
    buf = []
    text = text + '#'
    for ch in text:
        tch = ch
        if ch in '\t\n': ch = ' '
        chtype = getType(ch)
        nextState = change[curState][chtype]
        if nextState == 0:
            if buf != [' ']:
                curToken = getToken(curState,''.join(buf),linenum)
                tokens.append(curToken)
            curState = change[0][chtype]
            buf = [ch]
        else:
            buf.append(ch)
            curState = nextState
        if tch == '\n': linenum += 1
        if ch == '#':
            tokens.append((linenum,'EOF',None))
    return tokens

t  = main('test.txt')
for i in t:
    print i