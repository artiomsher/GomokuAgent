import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    
    def move(self, board):
        while True:
           
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
    
    figs3VH, figs4VH = boardValRow(self, board, ID)
    figs3Diag, figs4Diag = boardValDiag(self, board, ID)
    figures3 = figs3VH+figs3Diag
    figures4 = figs4VH+figs4Diag
    
    #print("Figures3: ", figures3)
    #print("Figures4: ", figures4)
    return figures3, figures4

def boardValRow(self, board, ID):
    figures3 = []
    figures4 = []
    isRotated = False
    BOARD_SIZE = board.shape[0]
    for times in range (2):
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - self.X_IN_A_LINE + 3):#last "starting point" is 8, to detet 3 in a row
                scores = 0
                for i in range(self.X_IN_A_LINE - 1):# -1 for detecting up to 4 
                    #print(r,c,i, "SSS",r,c+i)
                    if c+i < BOARD_SIZE: #protects against out of bounds if last positions in the row
                        
                        if board[r,c+i] == ID:

                            scores+=1
                            #print(r,c+i)
                            if scores == 4 or scores == 3:
                                if isRotated:#VERTICAL
                                    row = c
                                    col = 10-r
                                    fig = ((row,col), (row + scores - 1,col))

                                else: #HORIZONTAL

                                    row = r
                                    col = c

                                    fig = ((row,col), (row,col + scores - 1))

                                if scores == 4: 
                                    figures3.pop()
                                    figures4.append(fig)
                                else:
                                    figures3.append(fig)
                                #FIGURA MOZET BITJ ODNA V DRUGOJ
                        else:
                            break
                        
        if not isRotated:
            board = np.rot90(board)
            isRotated = True
        else:
            board = np.rot90(board,3)
            isRotated = False
            
    return figures3, figures4  
                    
def boardValDiag(self, board, ID):
    figures3 = []
    figures4 = []
    
    isRotated = False
    BOARD_SIZE = board.shape[0]
    for times in range (2):
        
        for r in range(BOARD_SIZE - self.X_IN_A_LINE + 3):
            for c in range(BOARD_SIZE - self.X_IN_A_LINE + 3):
                scores = 0
                for i in range(self.X_IN_A_LINE - 1):
                    if c+i < BOARD_SIZE and r+i < BOARD_SIZE:
                        
                        if board[r + i,c + i] == ID:
                            scores+=1
                            if scores == 4 or scores == 3:
                                if isRotated:#VERTICAL
                                    row = c
                                    col = 10-r
                                    fig = ((row,col), (row + scores - 1, col - scores + 1))

                                else: #HORIZONTAL

                                    row = r
                                    col = c

                                    fig = ((row,col), (row + scores - 1,col + scores - 1))

                                if scores == 4: 
                                    figures3.pop()
                                    figures4.append(fig)
                                else:
                                    figures3.append(fig)#FIGURA MOZET BITJ ODNA V DRUGOJ
                                #print(fig, isRotated)
                        else:
                            break
                        
        if not isRotated:
            board = np.rot90(board)
            isRotated = True
        else:
            board = np.rot90(board,3)
            isRotated = False
            
    return figures3, figures4   

def determineMove(self, board):
    nextMoveCoords = (-1,-1)
    suggestedMoves = []
    ally3, ally4 = readBoard(self, board, self.ID)
    enemy3, enemy4 = readBoard(self, board, -self.ID)
    print("Ally:",ally3, ally4)
    print("Enemy:",enemy3, enemy4)
    
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
            
            possibleLocs = getPossibleMovesForFig(board, shape)
                         
            if possibleLocs:
                nextMoveCoords = possibleLocs[0]
    return nextMoveCoords   

def getPossibleMovesForFig(board, figure):
    possibleLocs = []
    y,x = figure[0]
    y1, x1 = figure[1]
    if x == x1:#if vertical
        if legalMove(board,(y-1, x)):
            possibleLocs.append((y - 1, x))
        elif legalMove(board,(y1+1, x)):
            possibleLocs.append((y1 + 1, x))
                    
                    
    elif y == y1:#if horizontal
        if legalMove(board,(y, x-1)):
            possibleLocs.append((y, x - 1))
        elif legalMove(board,(y1, x1+1)):
            possibleLocs.append((y1, x1 + 1))
                    
    elif abs(x1-x) == abs(y1-y):#IF DIAGONAL
        if x<x1 and y<y1:#left up to down bot
            if legalMove(board,(y - 1, x - 1)):
                possibleLocs.append((y - 1, x - 1))
            elif legalMove(board,(y1 + 1, x1 + 1)):
                possibleLocs.append((y1 + 1, x1 + 1))
        else:#right up to left bot
            if legalMove(board,(y - 1, x + 1)):
                possibleLocs.append((y - 1, x + 1))
            elif legalMove(board,(y1 + 1, x1 - 1)):
                possibleLocs.append((y1 + 1, x1 - 1))
    return possibleLocs                    

def checkFigs3(board, fig3):
    suggestedMoves = []
    allPossibleLocs = []
    for fig in fig3:
        allPossibleLocs.append(getPossibleMovesForFig(board, fig))

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