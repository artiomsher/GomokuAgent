# Authors: Artiom Serstobitov,
# Oskars Dervinis
import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent
from misc import winningTest

class Player(GomokuAgent):
    
    def move(self, board):

        while True:
            print("H now: ",getHeuristics(self, board))
            print("NOW IS PLAYER ", self.ID, " MOVE!!!\n")

            moveLoc = determineMove(self, board)#COMBINATION OF RANDOM AND NOT RANDOM MOVES                
            if legalMove(board, moveLoc):
                return moveLoc
                
def getMoveCoords(self, board1, board2):
    for i in range(self.BOARD_SIZE):
        for j in range(self.BOARD_SIZE):
            if board1[i][j] != board2[i][j]:
                return (i,j)

MAX, MIN = 1000000, -1000000 
def minimax(node, depth, maximizingPlayer,  
            alpha, beta, self):  
   

    if depth == 1:  
        heuristics = getHeuristics(self, node.board)
        return heuristics, node 
  
    if maximizingPlayer:  
        nodeToReturn = node
        best = MIN 
        children = getAllChildren(node, self.ID)
        for child in children: 
            val, processedNode = minimax(child, depth + 1, False, alpha, beta, self)  
            oldBest = best    
            best = max(best, val)  
            alpha = max(alpha, best) 

            if oldBest != best:#if the child changes values, return it
                nodeToReturn = processedNode 
            if beta <= alpha:  
                break 

        return best, nodeToReturn
       
    else: 
        nodeToReturn = node
        best = MAX 
  
        children = getAllChildren(node, -self.ID)
        for child in children:   
            val, processedNode = minimax(child, depth + 1, True, alpha, beta, self)  
            oldBest = best    
            best = min(best, val)  
            beta = min(beta, best)  

            if oldBest != best:#if the child changes values, return it
                nodeToReturn = processedNode
            if beta <= alpha:  
                break 
                
        return best, nodeToReturn

def getAllChildren(node, id):#gets all children for a node
    children = []
    for i in range(11):
        for j in range(11):
            if node.board[i][j] == 0:
                newBoard = np.copy(node.board)
                newBoard[i][j] = id
                newNode = Node(newBoard, node)
                children.append(newNode)
    return children

def boardValRow(self, board, ID):
    figures2 = []
    figures3 = []
    figures4 = []
    isRotated = False
    BOARD_SIZE = board.shape[0]
    for times in range (2):
        
        for r in range(BOARD_SIZE):
            jumpVal = 0#value to jump through desk if last figure was found
            for c in range(BOARD_SIZE - 1):
                
                scores = 0
                figure = ((-1,-1), (-1,-1))
                for i in range(self.X_IN_A_LINE - 1):# -1 for detecting up to 4 
                    if c + i + jumpVal < BOARD_SIZE: #protects against out of bounds if last positions in the row
                        
                        if board[r,c + i + jumpVal] == ID:
                            scores+=1
                            if scores == 4 or scores == 3 or scores == 2:
                                if isRotated:#VERTICAL
                                    row = c + jumpVal
                                    col = 10-r
                                    figure = ((row,col), (row + scores - 1,col))
                                else: #HORIZONTAL
                                    row = r
                                    col = c + jumpVal
                                    figure = ((row,col), (row,col + scores - 1)) 
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
        for r in range(BOARD_SIZE - 1):
            for c in range(BOARD_SIZE - 1):
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
    node = Node(board, None)
    heuristic, node = minimax(node, 0, True, MIN, MAX, self)
    nextMoveCoords = getMoveCoords(self, board, node.board)#finds the difference between current and next state boards
    return nextMoveCoords
       

class Node:
    def __init__(self, board, ancestor):
        self.board = board
        self.ancestor = ancestor

#returns the coords of possible location depending from the id and dist
def getMovesOnEdgesForFig(board, figure, dist, id):
    possibleLocsLeft = []
    possibleLocsRight = []
    newYL = 0
    newXL = 0
    newYR = 0
    newXR = 0
    y,x = figure[0]
    y1, x1 = figure[1]

    if x == x1:#if vertical
        newYL = y-dist
        newXL = x
        newYR = y1+dist
        newXR = x
    elif y == y1:#if horizontal
        newYL = y
        newXL = x-dist
        newYR = y
        newXR = x1 + dist
    elif abs(x1-x) == abs(y1-y):#if diagonal
        if x<x1 and y<y1:#if left to right
            newYL = y - dist
            newXL = x - dist
            newYR = y1 + dist
            newXR = x1 + dist
        else:#if right to left
            newYL = y - dist
            newXL = x + dist
            newYR = y1 + dist
            newXR = x1 - dist

    if isBeneficial(board,(newYL, newXL), id):
        possibleLocsLeft.append((newYL, newXL))
    if isBeneficial(board,(newYR, newXR), id):
        possibleLocsRight.append((newYR, newXR))
                          
    return possibleLocsLeft, possibleLocsRight                  

#improved version of legalMove
def isBeneficial(board, moveLoc, id):
    BOARD_SIZE = board.shape[0]
    if moveLoc[0] < 0 or moveLoc[0] >= BOARD_SIZE or moveLoc[1] < 0 or moveLoc[1] >= BOARD_SIZE: 
        return False

    if board[moveLoc] == id:
        return True
    return False

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

    priorityValid2, normalValid2 = isPotentialWin(board, figs2VH+figs2Diag, 2, self.ID)
    priorityValid3, normalValid3 = isPotentialWin(board, figs3VH+figs3Diag, 3, self.ID)
    priorityValid4, normalValid4 = isPotentialWin(board, figs4VH+figs4Diag, 4, self.ID)
    priorityValid2Enemy, normalValid2Enemy = isPotentialWin(board, figs2VHEnemy+figs2DiagEnemy, 2, -self.ID)
    priorityValid3Enemy, normalValid3Enemy = isPotentialWin(board, figs3VHEnemy+figs3DiagEnemy, 3, -self.ID)
    priorityValid4Enemy, normalValid4Enemy = isPotentialWin(board, figs4VHEnemy+figs4DiagEnemy, 4, -self.ID)

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
        VALUE_5 = 9999
        VALUE_4 = 4000
        VALUE_3_P = 1000
        VALUE_3_N = 100
        VALUE_2_P = 1000
        VALUE_2_N = 20
    else:
        VALUE_5 = 9999
        VALUE_4 = 4000
        VALUE_3_P = 1000
        VALUE_3_N = 100
        VALUE_2_P = 1000
        VALUE_2_N = 20
    
    for fig in priorityValid4:
        fig4Value = fig4Value + VALUE_4
    for fig in priorityValid3:
        fig3ValueP = fig3ValueP + VALUE_3_P 
    for fig in normalValid3:
        fig3ValueN = fig3ValueN + VALUE_3_N
    for fig in priorityValid2:
        fig2ValueP = fig2ValueP + VALUE_2_P
    for fig in normalValid2:
        fig2ValueN = fig2ValueN + VALUE_2_N 

    for fig in priorityValid4Enemy:
        fig4ValueEnemy = fig4ValueEnemy + VALUE_4
    for fig in priorityValid3Enemy:
        fig3ValuePEnemy = fig3ValuePEnemy + VALUE_3_P 
    for fig in normalValid3Enemy:
        fig3ValueNEnemy = fig3ValueNEnemy + VALUE_3_N
    for fig in priorityValid2Enemy:
        fig2ValuePEnemy = fig2ValuePEnemy + VALUE_2_P
    for fig in normalValid2Enemy:
        fig2ValueNEnemy = fig2ValueNEnemy + VALUE_2_N     

    

    borderValue = getBorderValue(board, self.ID)
    borderValueEnemy = getBorderValue(board, -self.ID)
    finalValueFig = fig4Value + fig3ValueP + fig3ValueN + fig2ValueP + fig2ValueN
    finalValueFigEnemy = fig4ValueEnemy + fig3ValuePEnemy + fig3ValueNEnemy + fig2ValuePEnemy + fig2ValueNEnemy
    finalValue = finalValueFig + borderValue
    finalValueEnemy = finalValueFigEnemy + borderValueEnemy#SHOULD BE BORDERVALUE, but maybe not??
    
    if winningTest(self.ID, board, self.X_IN_A_LINE):
        finalValue += VALUE_5
    if winningTest(-self.ID, board, self.X_IN_A_LINE):
        finalValueEnemy += VALUE_5

    returnValue = finalValue - finalValueEnemy
    return returnValue

def getBorderValue(board, id):#gives values for staying closer to the center - more options to move
    counter = 0
    # (3,3) - (3,7)
    for i in range (3,8):
        for j in range (3,8):
            if(board[i,j] == id):
                if(j == 3 or i == 3 or j == 7 or i == 7):
                    counter += 1
    for i in range (4, 7):
        for j in range (4, 7):
            if(board[i,j] == id):
                if(j == 4 or i == 4 or j == 6 or i == 6):
                    counter += 2
    if(j == 5 and i == 5):
        counter += 3
    return counter
