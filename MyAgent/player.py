import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    
    def move(self, board):
        while True:
            #print(isBeneficial(self, board, (5,5)))
            print("NOW IS PLAYER ", self.ID, " MOVE!!!\n")
            moveLoc = determineMove(self, board)#COMBINATION OF RANDOM AND NOT RANDOM MOVES
            if moveLoc == (-1,-1):
                print("random move")
                moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            else:
                print("NOT RANDOM MOVE")
                
            if legalMove(board, moveLoc):
                print("NEW FIGURE ADDED:::::::::", moveLoc)
                return moveLoc

def readBoard(self, board, ID):
    BOARD_SIZE = board.shape[0]
    
    figs2VH, figs3VH, figs4VH = boardValRow(self, board, ID)#GET figures of specified player horizonta and vertical
    figs2Diag, figs3Diag, figs4Diag = boardValDiag(self, board, ID)#DIagonal
    
    figures2 = figs2VH+figs2Diag#combination of vert and horizontal fig, separated by its length
    figures3 = figs3VH+figs3Diag
    figures4 = figs4VH+figs4Diag

    #print("Figures2: ", figures2)
    #print("Figures3: ", figures3)
    #print("Figures4: ", figures4)
    return figures2, figures3, figures4

def boardValRow(self, board, ID):
    figures2 = []
    figures3 = []
    figures4 = []
    isRotated = False
    BOARD_SIZE = board.shape[0]
    for times in range (2):
        
        for r in range(BOARD_SIZE):
            jumpVal = 0#value to jump through desk if last figure was found
            for c in range(BOARD_SIZE - self.X_IN_A_LINE + 4):#last "starting point" is 8, to detet 3 in a row
                
                scores = 0
                figure = ((-1,-1), (-1,-1))
                for i in range(self.X_IN_A_LINE - 1):# -1 for detecting up to 4 
                    #print(r,c,i, "SSS",r,c+i)
                    if c + i + jumpVal < BOARD_SIZE: #protects against out of bounds if last positions in the row
                        
                        if board[r,c + i + jumpVal] == ID:

                            scores+=1

                            #print(r,c+i)
                            if scores == 4 or scores == 3 or scores == 2:
                                if isRotated:#VERTICAL
                                    row = c + jumpVal
                                    col = 10-r
                                    figure = ((row,col), (row + scores - 1,col))

                                else: #HORIZONTAL

                                    row = r
                                    col = c + jumpVal

                                    figure = ((row,col), (row,col + scores - 1))

                                
                                #FIGURA MOZET BITJ ODNA V DRUGOJ
                        else:
                            break
                

                if scores == 4: 
                    figures4.append(figure)
                elif scores == 3:
                    figures3.append(figure)
                elif scores == 2:
                    figures2.append(figure)
                
                if scores > 1:
                    jumpVal = jumpVal + scores - 1
                 
                       
        if not isRotated:
            board = np.rot90(board)
            isRotated = True
        else:
            board = np.rot90(board,3)
            isRotated = False
            
    return figures2, figures3, figures4  
                    
def boardValDiag(self, board, ID):
    figures2 = []
    figures3 = []
    figures4 = []
    
    isRotated = False
    BOARD_SIZE = board.shape[0]
    for times in range (2):
        blackList = [] #to avoid repeated figures, contains the cells which we dont eed to visit
        for r in range(BOARD_SIZE - self.X_IN_A_LINE + 3):
            for c in range(BOARD_SIZE - self.X_IN_A_LINE + 3):
                if not (r,c) in blackList: #if the point is not part of the figure
                    figure = (-1,-1)
                    scores = 0
                    for i in range(self.X_IN_A_LINE - 1):
                        if c+i < BOARD_SIZE and r+i < BOARD_SIZE:
                            
                            if board[r + i,c + i] == ID:
                                scores+=1
                                if scores == 4 or scores == 3 or scores == 2:
                                    if isRotated:#VERTICAL
                                        row = c
                                        col = 10-r
                                        figure = ((row,col), (row + scores - 1, col - scores + 1))

                                    else: #HORIZONTAL

                                        row = r
                                        col = c

                                        figure = ((row,col), (row + scores - 1,col + scores - 1))

                                    
                            else:
                                break

                    if scores == 4:
                        figures4.append(figure)
                        blackList.append((r+1, c+1))
                        blackList.append((r+2, c+2))
                        blackList.append((r+3, c+3))
                    elif scores == 3:
                        figures3.append(figure)
                        blackList.append((r+1, c+1))
                        blackList.append((r+2, c+2))
                    elif scores == 2:
                        figures2.append(figure)
                        blackList.append((r+1, c+1))        
        if not isRotated:
            board = np.rot90(board)
            isRotated = True
        else:
            board = np.rot90(board,3)
            isRotated = False
            
    return figures2,figures3, figures4   

def determineMove(self, board):
    nextMoveCoords = (-1,-1)
    suggestedMoves = []
    ally2, ally3, ally4 = readBoard(self, board, self.ID)
    enemy2, enemy3, enemy4 = readBoard(self, board, -self.ID)
    print("Ally:",ally2, ally3, ally4)
    print("Enemy:",enemy2, enemy3, enemy4)
    
    if ally4:#DETERMINE LAST MOVE TO WIN IF POSSIBLE
        nextMoveCoords = check4InLine(board, ally4)
    if enemy4 and not isDecidedMove(nextMoveCoords):# if the move is not decided yet and enemy can potentially win next move, need to prevent
        nextMoveCoords = check4InLine(board, enemy4)    
        #print("Prevented", nextMoveCoords)
    if ally3 and not isDecidedMove(nextMoveCoords):

        suggestedMoves = checkFigs3(board, ally3)   

    return nextMoveCoords
       

def check4InLine(board, fig4):
    nextMoveCoords = (-1,-1)
    for shape in fig4:
            
            possibleLocs = getMovesOnEdgesForFig(board, shape, 1, 0)
                         
            if possibleLocs:
                nextMoveCoords = possibleLocs[0]
    return nextMoveCoords   

def getMovesOnEdgesForFig(board, figure, dist, id):
    possibleLocs = []
    y,x = figure[0]
    y1, x1 = figure[1]
    if x == x1:#if vertical
        if isBeneficial(board,(y-dist, x), id):
            possibleLocs.append((y - dist, x))
        if isBeneficial(board,(y1+dist, x), id):
            possibleLocs.append((y1 + dist, x))
                    
                    
    elif y == y1:#if horizontal
        if isBeneficial(board,(y, x-dist), id):
            possibleLocs.append((y, x - dist))
        if isBeneficial(board,(y1, x1+dist), id):
            possibleLocs.append((y1, x1 + dist))
                    
    elif abs(x1-x) == abs(y1-y):#IF DIAGONAL
        if x<x1 and y<y1:#left up to down bot
            if isBeneficial(board,(y - dist, x - dist), id):
                possibleLocs.append((y - dist, x - dist))
            if isBeneficial(board,(y1 + dist, x1 + dist), id):
                possibleLocs.append((y1 + dist, x1 + dist))
        else:#right up to left bot
            if isBeneficial(board,(y - dist, x + dist), id):
                possibleLocs.append((y - dist, x + dist))
            if isBeneficial(board,(y1 + dist, x1 - dist), id):
                possibleLocs.append((y1 + dist, x1 - dist))
    return possibleLocs                    

def checkFigs3(board, fig3):
    suggestedMoves = []
    allPossibleLocs = []
    for fig in fig3:
        newPossibleLocs = getMovesOnEdgesForFig(board, fig, 1, 0)
        if newPossibleLocs:
            allPossibleLocs.append(getMovesOnEdgesForFig(board, fig, 1, 0))

    print("POSSIBLE MOVES",allPossibleLocs)                    
    if suggestedMoves:
        return suggestedMoves
    else:
        return (-1,-1)    


def isDecidedMove(coords):
    if coords == (-1,-1):
        return False
    else:
        return True    

def isBeneficial(board, moveLoc, id):
    BOARD_SIZE = board.shape[0]
    if moveLoc[0] < 0 or moveLoc[0] >= BOARD_SIZE or \
       moveLoc[1] < 0 or moveLoc[1] >= BOARD_SIZE: 
        return False

    if board[moveLoc] == id:
        return True
    return False
