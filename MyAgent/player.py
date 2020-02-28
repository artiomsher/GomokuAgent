import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent


class Player(GomokuAgent):
    
    def move(self, board):

        while True:
            
            print("NOW IS PLAYER ", self.ID, " MOVE!!!\n")
            print(getHeuristics(self, board))
            moveLoc = determineMove(self, board)#COMBINATION OF RANDOM AND NOT RANDOM MOVES
            #if moveLoc == (-1,-1):
                #print("random move")
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            #else:
                #print("NOT RANDOM MOVE")
                
            if legalMove(board, moveLoc):
                #print("NEW FIGURE ADDED:::::::::", moveLoc)
                return moveLoc
                
    # Python3 program to demonstrate  
# working of Alpha-Beta Pruning  
  
# Initial values of Aplha and Beta  
MAX, MIN = 1000, -1000 
numberOfChildren = 2
# Returns optimal value for current player  
#(Initially called for root and maximizer)  
def minimax(depth, nodeIndex, id,  
            values, alpha, beta, numberOfChildren):  
    
    # Terminating condition. i.e  
    # leaf node is reached  
    if depth == 3:  
        return values[nodeIndex]  
  
    if id == 1:  
       
        best = MIN 
  
        # Recur for left and right children  
        for i in range(0, numberOfChildren):  
            print(numberOfChildren)
            val = minimax(depth + 1, nodeIndex * 2 + i,  
                          -1, values, alpha, beta, numberOfChildren - 1)  
            best = max(best, val)  
            alpha = max(alpha, best)  
            
            # Alpha Beta Pruning  
            if beta <= alpha:  
                break 
           
        return best  
       
    else: 
        best = MAX 
  
        # Recur for left and  
        # right children  
        for i in range(0, numberOfChildren):  
            print(numberOfChildren)
            val = minimax(depth + 1, nodeIndex * 2 + i,  
                            1, values, alpha, beta, numberOfChildren - 1)  
            best = min(best, val)  
            beta = min(beta, best)  
  
            # Alpha Beta Pruning  
            if beta <= alpha:  
                break 
           
        return best  
       
# Driver Code  
if __name__ == "__main__":  
   
    values = [3, 5, 6, 9, 1, 2, 0, -1]   
    print("The optimal value is :", minimax(0, 0, True, values, MIN, MAX, numberOfChildren - 1))  
      
# This code is contributed by Rituraj Jain 

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
    numOfChildren = 0
    values = [3, 5, 6, 9, 1, 2, 0, -1] 
    nextMoveCoords = minimax(0, 0, self.ID, values, MIN, MAX, numOfChildren)

    
    
    
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

def getHeuristics(self, board):
    figs2VH, figs3VH, figs4VH = boardValRow(self, board, self.ID)#GET figures of specified player horizonta and vertical
    figs2Diag, figs3Diag, figs4Diag = boardValDiag(self, board, self.ID)#DIagonal
    figs2VHEnemy, figs3VHEnemy, figs4VHEnemy = boardValRow(self, board, -self.ID)#GET figures of specified player horizonta and vertical
    figs2DiagEnemy, figs3DiagEnemy, figs4DiagEnemy = boardValDiag(self, board, -self.ID)#DIagonal
    
    figures2 = figs2VH+figs2Diag#combination of vert and horizontal fig, separated by its length
    figures3 = figs3VH+figs3Diag
    figures4 = figs4VH+figs4Diag
    figures2Enemy = figs2VHEnemy+figs2DiagEnemy#combination of vert and horizontal fig, separated by its length
    figures3Enemy = figs3VHEnemy+figs3DiagEnemy
    figures4Enemy = figs4VHEnemy+figs4DiagEnemy

    priorityValid2, normalValid2 = isPotentialWin(board, figures2, 2, self.ID)
    priorityValid3, normalValid3 = isPotentialWin(board, figures3, 3, self.ID)
    priorityValid4, normalValid4 = isPotentialWin(board, figures4, 4, self.ID)
    priorityValid2Enemy, normalValid2Enemy = isPotentialWin(board, figures2, 2, -self.ID)
    priorityValid3Enemy, normalValid3Enemy = isPotentialWin(board, figures3, 3, -self.ID)
    priorityValid4Enemy, normalValid4Enemy = isPotentialWin(board, figures4, 4, -self.ID)

    #priorityValid = priorityValid4 + priorityValid3 + priorityValid2
    #normalValid = normalValid4 + normalValid3 + normalValid2
    fig4Value = 0 
    fig4ValueEnemy = 0
    fig3ValueP = 0 
    fig3ValuePEnemy = 0
    fig3ValueN = 0 
    fig3ValueNEnemy = 0
    fig2ValueP = 0 
    fig2ValuePEnemy = 0
    fig2ValueN = 0 
    fig2ValueNEnemy = 0
    borderValue = 0 
    borderValueEnemy = 0
    finalValue = 0 
    finalValueEnemy = 0
    
    if (priorityValid4 or priorityValid3 or priorityValid2):

        VALUE_4 = 100
        VALUE_3_P = 100
        VALUE_3_N = 25
        VALUE_2_P = 100
        VALUE_2_N = 10
    else:
        VALUE_4 = 100
        VALUE_3_P = 100
        VALUE_3_N = 30
        VALUE_2_P = 100
        VALUE_2_N = 5
    
    for fig in priorityValid4:
        fig4Value = fig4Value + VALUE_4
        fig4ValueEnemy = fig4ValueEnemy + VALUE_4
    for fig in priorityValid3:
        fig3ValueP = fig3ValueP + VALUE_3_P 
        fig3ValuePEnemy = fig3ValuePEnemy + VALUE_3_P 
    for fig in normalValid3:
        fig3ValueN = fig3ValueN + VALUE_3_N
        fig3ValueNEnemy = fig3ValueNEnemy + VALUE_3_N
    for fig in priorityValid2:
        fig2ValueP = fig2ValueP + VALUE_2_P
        fig2ValuePEnemy = fig2ValuePEnemy + VALUE_2_P
    for fig in normalValid2:
        fig2ValueN = fig2ValueN + VALUE_2_N 
        fig2ValueNEnemy = fig2ValueNEnemy + VALUE_2_N 

    finalValueFig = fig4Value + fig3ValueP + fig3ValueN + fig2ValueP + fig2ValueN
    finalValueFigEnemy = fig4ValueEnemy + fig3ValuePEnemy + fig3ValueNEnemy + fig2ValuePEnemy + fig2ValueNEnemy
    finalValueFig = finalValueFig + borderValue
    finalValueFigEnemy = finalValueFigEnemy + borderValueEnemy
    border(board)
    return finalValueFig

def border(board):
    counter = 0
    # (3,3) - (3,7)
    for i in range (3,8):
        for j in range (3,8):
            if(board[i,j] != 1 and board[i,j] != -1):
                counter += 1
    return counter
