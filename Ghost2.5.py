__author__ = 'Vishal Tandale'
# Vishal Tandale Pd 4 AI //Gabor
import sys, random, time


# This piece of code is to create the keystroke logger
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
getch = _Getch()


#Create Tree from Poswords
def createTree(Poswords):
    root = {}
    Current = root #Current Node
    #Temp = {} #This is just a filler node
    for word in PosWords:
        for char in word:
            if char in Current:
                Current = Current[char]
            else:
                Current[char]={}
                Current = Current[char]
        Current = root
    return root

# This is the actual ghost puzzle c
# This updates the player turn
def nextplayer(current, numplayers):
    if current < numplayers:
        current += 1
    else:
        current = 1
    return current


# Calculates all the possible letters that are possible
def poslet(Posword, currentword, root):
    current = root
    for char in currentword:
        if char in current:
            current = current[char]
        else:
            return set([])
    return set(current.keys())

def getcurrent(root, currentword):
    current = root
    for char in currentword:
        if char in current:
            #*print(str(current))
            current = current[char]
        else:
            return "-"
    return current
def analyze(prefix, playerNum, Poswords, current):
    # returns a tuple of good, bad letters if prefix is a word: return ({prefix}, set())
    if prefix in Poswords and len(prefix)>3:
        return ({1}, set())
    # initialization
    good, bad = set(), set()
    #print(str(current.keys()))
    # recursive part
    #print(prefix[len(prefix)-1])
    for sym in current:
        #print(current[sym].keys())
        tmpGood, tmpBad = analyze(prefix + sym, 1 - playerNum, Poswords, current[sym])
        if len(tmpGood) == 0:
            good.add(sym)
        else:
            bad.add(sym)
    return good, bad
#Computer decides what to play
def computerplay(Poswords,playernum, currentword, current):
    if (currentword in Poswords and len(currentword)>3) or current == '-':
        return '-'
    #Time = time.clock()
    good, bad = analyze(currentword,playernum, PosWords, current)
    #print("Time: "+str(time.clock()-Time))
    if len(good)>0:
        return random.choice(list(good))
    elif len(bad)>0:
        return random.choice(list(bad))
    return '-'


# This method actually plays the game
def playgame(Poswords, players, root, curr):
    currentword = ""  # This is the current string of word
    numplayers = len(players)
    currentplayer = curr  # This is the player whose turn it is
    if players[currentplayer-1]=='c':
        letter=computerplay(PosWords,currentplayer, currentword, root)
    else:
        letter = getch()  # This is the letter inputted rn
    if letter=='*':
        exit()
    while ((letter != '.') and((letter in 'qwertyuiopasdfghjklzxcvbnm') or not(1 <= int(letter) <= numplayers))):
        print(letter,end="",flush=True)
        currentword += letter
        currentplayer = nextplayer(currentplayer, numplayers)
        if players[currentplayer-1]=='c':
            letter=computerplay(PosWords,currentplayer, currentword,getcurrent(root,currentword))
            if letter == '-':
                break
        else:
            letter = getch()  # This is the letter inputted rn
        if letter =='*':
            print()
            exit()
    if letter == '.':
        print()
        print(poslet(PosWords,currentword, root))
        return -1
    elif letter == '-':
        print("\tPlayer"+str(currentplayer)+" Challenges")
        #print(poslet(PosWords,currentword))
        #if len(poslet(PosWords, currentword, root)) > 0:
         #   print(poslet(PosWords,currentword, root))
        if currentplayer == 1:
            return [len(players), currentplayer]
        else:
            return [currentplayer-1, currentplayer]
    else:
        print("\tPlayer"+letter+" Challenges")
        #if currentword in Poswords:
        #    return currentplayer
        if len(poslet(PosWords, currentword, root)) > 0 and not currentword in PosWords:
            return [int(letter), currentplayer]
        else:
            return [currentplayer-1, currentplayer]
    return 0

#Checks if any player has ghost
def checkGhost(Lives):
    for i in range(len(Lives)):
        if Lives[i] == 5:
            return i
    return -1

Temp = 1
Temp = nextplayer(Temp,5)

# Read in ghost.txt
Filename = "ghost.txt"
PosWords = set(open(Filename).read().split())  # This Is a list of all the words that we could use
root = createTree(PosWords)
players = []

# Command Line stuff
if (len(sys.argv) > 1):
    for i in range(1,len(sys.argv)):
        if (sys.argv[i] =='c' or sys.argv[i]=='C'):
            players.append('c')
        else:
            for x in range(int(sys.argv[i])):
                players.append('h')
else:
    players = ['h','h']
Lives = []
for i in range(len(players)):
    Lives.append(0)
curr = 1
while checkGhost(Lives)==-1:
    key = "ghost"
    loser = playgame(PosWords,players, root, curr)
    if loser[0] >0:
        Lives[loser[0]-1]+=1
        print("Player " + str(loser[0]) + " has "+ key[0:Lives[loser[0]-1]])
    curr = loser[1]

print("Player "+ str(checkGhost(Lives)+1) + " Lost the game")
exit()

'''
players = ['c','c']
Lives = []
for i in range(len(players)):
    Lives.append(0)
while checkGhost(Lives)==-1:
    key = "ghost"
    loser = playgame(PosWords, players,root)
    if loser >0:
        Lives[loser-1]+=1
        print("Player " + str(loser) + " has "+ key[0:Lives[loser-1]])
print("Player "+ str(checkGhost(Lives)+1) + " Lost the game")
exit()
'''

