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
                #print("random move")
                moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            #else:
                #print("NOT RANDOM MOVE")
                
            if legalMove(board, moveLoc):
                #print("NEW FIGURE ADDED:::::::::", moveLoc)
                return moveLoc

def readBoard(self, board, ID):
    BOARD_SIZE = board.shape[0]
    
    figs2VH, figs3VH, figs4VH = boardValRow(self, board, ID)#GET figures of specified player horizonta and vertical
    figs2Diag, figs3Diag, figs4Diag = boardValDiag(self, board, ID)#DIagonal
    
    figures2 = figs2VH+figs2Diag#combination of vert and horizontal fig, separated by its length
    figures3 = figs3VH+figs3Diag
    figures4 = figs4VH+figs4Diag

    priorityValid2, normalValid2 = isPotentialWin(board, figures2, 2, ID)
    priorityValid3, normalValid3 = isPotentialWin(board, figures3, 3, ID)
    priorityValid4, normalValid4 = isPotentialWin(board, figures4, 4, ID)

    priorityValid = priorityValid4 + priorityValid3 + priorityValid2
    normalValid = normalValid4 + normalValid3 + normalValid2

    print("PRIORITY:  ", priorityValid)
    print("NORMAL:  ", normalValid)
    #print("AVAILABLE FOR WIN3: ", isPotentialWin(board, figures3, 3, ID))
    #print("AVAILABLE FOR WIN2: ", isPotentialWin(board, figures2, 2, ID))
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
    #print("Ally:",ally2, ally3, ally4)
    #print("Enemy:",enemy2, enemy3, enemy4)
    
    if ally4:#DETERMINE LAST MOVE TO WIN IF POSSIBLE
        nextMoveCoords = check4InLine(board, ally4)
    if enemy4 and not isDecidedMove(nextMoveCoords):# if the move is not decided yet and enemy can potentially win next move, need to prevent
        nextMoveCoords = check4InLine(board, enemy4)    
        #print("Prevented", nextMoveCoords)
    if ally3 and not isDecidedMove(nextMoveCoords):

        #suggested = checkFigs3(board, ally3)[0]
        #if isDecidedMove(suggested):
            #suggestedMoves.append(suggested)   
        nextMoveCoords = checkFigs3(board, ally3)    
    
    #if not isDecidedMove(nextMoveCoords) and suggestedMoves:
        #nextMoveCoords = suggestedMoves[0]
    return nextMoveCoords
       

def check4InLine(board, fig4):
    nextMoveCoords = (-1,-1)
    for shape in fig4:
            
            possibleLocsL, possibleLocsR = getMovesOnEdgesForFig(board, shape, 1, 0)
            possibleLocs = possibleLocsL + possibleLocsR             
            if possibleLocs:
                nextMoveCoords = possibleLocs[0]
    return nextMoveCoords   

def getMovesOnEdgesForFig(board, figure, dist, id):
    possibleLocsLeft = []
    possibleLocsRight = []
    y,x = figure[0]
    y1, x1 = figure[1]
    if x == x1:#if vertical
        if isBeneficial(board,(y-dist, x), id):
            possibleLocsLeft.append((y - dist, x))
        if isBeneficial(board,(y1+dist, x), id):
            possibleLocsRight.append((y1 + dist, x))
                    
                    
    elif y == y1:#if horizontal
        if isBeneficial(board,(y, x-dist), id):
            possibleLocsLeft.append((y, x - dist))
        if isBeneficial(board,(y1, x1+dist), id):
            possibleLocsRight.append((y1, x1 + dist))
                    
    elif abs(x1-x) == abs(y1-y):#IF DIAGONAL
        if x<x1 and y<y1:#left up to down bot
            if isBeneficial(board,(y - dist, x - dist), id):
                possibleLocsLeft.append((y - dist, x - dist))
            if isBeneficial(board,(y1 + dist, x1 + dist), id):
                possibleLocsRight.append((y1 + dist, x1 + dist))
        else:#right up to left bot
            if isBeneficial(board,(y - dist, x + dist), id):
                possibleLocsLeft.append((y - dist, x + dist))
            if isBeneficial(board,(y1 + dist, x1 - dist), id):
                possibleLocsRight.append((y1 + dist, x1 - dist))
    return possibleLocsLeft, possibleLocsRight                  

def checkFigs3(board, fig3):
    suggestedMoves = (-1,-1)

    allPossibleLocs3To4 = []

    for fig in fig3:
        toCombineSplitted = checkSplitted(board, fig, 1)
        if isDecidedMove(toCombineSplitted):
            suggestedMoves = toCombineSplitted
        
        newPossibleLocsL, newPossibleLocsR = getMovesOnEdgesForFig(board, fig, 1, 0)
        newPossibleLocs = newPossibleLocsL + newPossibleLocsR
        if newPossibleLocs:
            allPossibleLocs3To4.append(newPossibleLocs)

    #print("POSSIBLE MOVES 3 to 4",allPossibleLocs3To4)                    
    if suggestedMoves:
        return suggestedMoves
        #print("SPLITTED COMBINED")
    else:
        return (-1,-1) 


def isDecidedMove(coords):
    if coords == (-1,-1) or coords == []:
        return False
    else:
        return True    

def isBeneficial(board, moveLoc, id):
    BOARD_SIZE = board.shape[0]
    if moveLoc[0] < 0 or moveLoc[0] >= BOARD_SIZE or moveLoc[1] < 0 or moveLoc[1] >= BOARD_SIZE: 
        return False

    if board[moveLoc] == id:
        return True
    return False

def checkSplitted(board, figure, id):
    coordsToCombine = (-1, -1)
    y,x = figure[0]
    y1,x1 = figure[1]
    afterGapL, afterGapR = getMovesOnEdgesForFig(board, figure, 2, id)
    afterGap = afterGapL+afterGapR
    if afterGap:
        gapL, gapR = getMovesOnEdgesForFig(board, figure, 1, 0)
        gap = gapL + gapR
        if gap and afterGap:
            coordsToCombine = gap[0]
            #print("after 1 is:", coordsToCombine)    

    return coordsToCombine

def isPotentialWin(board, figures, len, id):
    toReturnNormal = []
    toReturnPriority = []
    
    for fig in figures:
        #if fi is 4
        if len==4:
            moveForFig5L, moveForFig5R = getMovesOnEdgesForFig(board, fig, 1, 0)
            moveForFig5 = moveForFig5L + moveForFig5R
            if moveForFig5 != []:
                toReturnPriority.append(fig)
        if len == 3:    
            moveForFig4L, moveForFig4R = getMovesOnEdgesForFig(board, fig, 1, 0)
            moveForFig5L, moveForFig5R = getMovesOnEdgesForFig(board, fig, 2, 0)
            moveForFig5LSelf, moveForFig5RSelf = getMovesOnEdgesForFig(board, fig, 2, id)
            
            if (
                (moveForFig4R and moveForFig5RSelf) or                  # 1 1 1 0 1
                (moveForFig4L and moveForFig5LSelf) or                  # 1 0 1 1 1 

                (moveForFig4L and moveForFig5L and moveForFig4R) or     # 0 0 1 1 1 0 
                (moveForFig4L and moveForFig4R and moveForFig5R)):      # 0 1 1 1 0 0
                    toReturnPriority.append(fig)
            
            elif (
                (moveForFig4L and moveForFig5L) or                      # 0 0 1 1 1
                (moveForFig4R and moveForFig5R) or                      # 1 1 1 0 0 
            
                (moveForFig4L and moveForFig4R)):                       # 0 1 1 1 0
                toReturnNormal.append(fig)

        if len == 2:
            moveForFig3L, moveForFig3R = getMovesOnEdgesForFig(board, fig, 1, 0)#3rd empty
            moveForFig4L, moveForFig4R = getMovesOnEdgesForFig(board, fig, 2, 0)#4th empty
            moveForFig4LSelf, moveForFig4RSelf = getMovesOnEdgesForFig(board, fig, 2, id)#4th ally
            moveForFig5L, moveForFig5R = getMovesOnEdgesForFig(board, fig, 3, 0)#5th empty
            moveForFig5LSelf, moveForFig5RSelf = getMovesOnEdgesForFig(board, fig, 3, id)#5th ally

            if ((moveForFig3L and moveForFig4LSelf and moveForFig5LSelf) or #1 1 0 1 1 
                (moveForFig3R and moveForFig4RSelf and moveForFig5RSelf)):   #1 1 0 1 1 
                 toReturnPriority.append(fig)

            if ((moveForFig3L and moveForFig4L and moveForFig5L) or # 0 0 0 1 1 
            (moveForFig3L and moveForFig4L and moveForFig5LSelf) or # 1 0 0 1 1 
            (moveForFig3L and moveForFig4LSelf and moveForFig5L) or # 0 1 0 1 1 
            

            (moveForFig3R and moveForFig4R and moveForFig5R) or #1 1 0 0 0 
            (moveForFig3R and moveForFig4R and moveForFig5RSelf) or #1 1 0 0 1 
            (moveForFig3R and moveForFig4RSelf and moveForFig5R) or#1 1 0 1 0 
            

            (moveForFig3L and moveForFig3R and moveForFig4R) or#0 1 1 0 0 
            (moveForFig3L and moveForFig4L and moveForFig3R)):#0 0 1 1 0
                toReturnNormal.append(fig)
        
        
        
        
    return toReturnPriority, toReturnNormal     
#         if len(fig) == 4:
#             x,y = fig[0]#start
#             x1,y1 = fig[1]#end
#             if x==x1:
#                 if board[x,y-1] == 0 or board[x,y1+1]==0:
#                     toReturn.append(fig)
#                     print("HERE")
#             elif y==y1:
#                 if board[x-1,y] == 0 or board[x1+1,y]==0:
#                     toReturn.append(fig)
#                     print("HERE")
#             elif abs(x1-x) == abs(y1-y):#IF DIAGONAL
#                 if x<x1 and y<y1:#left up to down bot
#                     if board[x-1, y-1] == 0 or board[x1+1,y1+1]==0:
#                         toReturn.append(fig)
#                 else:#right up to left bot
#                     if board[x-1, y+1] == 0 or board[x1+1,y1-1]==0:
#                         toReturn.append(fig)
#     return toReturn


