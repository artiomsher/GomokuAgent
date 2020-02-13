import numpy as np

from misc import legalMove
from gomokuAgent import GomokuAgent

class Player(GomokuAgent):
    def move(self, board):
        while True:
            moveLoc = tuple(np.random.randint(self.BOARD_SIZE, size=2))
            
            print("Player " + str(self.ID))
            print("Horizontally: ")
            boardValRow(self, board, False)
            print("Horizontally End.")
            print("Vertically: ")
            boardPrime = np.rot90(board)
            boardValRow(self, boardPrime, True)
            print("Vertically End.")
            
            # BOARD_SIZE = board.shape[0]
            # for r in range(BOARD_SIZE):
            #     for c in range(BOARD_SIZE-self.X_IN_A_LINE+1):
            #         scores = 0
            #         for i in range(self.X_IN_A_LINE):
            #             if board[r,c+i] == self.ID:
            #                 scores+=1
            #                 if scores == 3:
            #                     print ("I have 3 in a row! at " + str(r) + ", " + str(c))
            #                 elif scores == 4:
            #                     print ("I have 4 in a row! at " + str(r) + ", " + str(c))
            #             else:
            #                 break
            if legalMove(board, moveLoc):
                return moveLoc
    
def boardValRow(self, board, isRotated):
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE-self.X_IN_A_LINE + 3):
            scores = 0
            for i in range(self.X_IN_A_LINE-2):
                if board[r,c+i] == self.ID:
                    scores+=1
                    if scores == 4 or scores == 3:
                        if isRotated:
                            row = c
                            col = 10-r
                        else: 
                            row = r
                            col = c
                        print ("I have " + str(scores) + " in a row! at " + str(row) + ", " + str(col))
                else:
                    break

def boardValDiagonal(self, board, isRotated):
    BOARD_SIZE = board.shape[0]
    for r in range(BOARD_SIZE - self.X_IN_A_LINE + 1):
        for c in range(BOARD_SIZE - self.X_IN_A_LINE + 1):
            scores = 0
            for i in range(self.X_IN_A_LINE):
                if board[r+i,c+i] != self.ID:
                    scores+=1
                    break
                    
