from collections import deque
from random import randint

class AI():
    def __init__(self, difficulty):
        self.difficuly = difficulty
        self.target = self.GetTarget()
    
    
    def GetTarget(self):
        n = 5
        target = []
        for x in range(5): 
                for y in range(5):
                    if y <= n:
                        target.append((x,y))
                n -= 1
        return target

    def GetMove(self, game, toMove=None):
        board = game.GetBoard()
        if self.difficuly == 1:
            if toMove == None:
                canMove = []
                for row in range(16):
                    for col in range(16):
                        if board[col][row] == 2:
                            canMove.append((col,row))
                pickPiece = randint(0,len(canMove)-1)
                while len(game.GetMoves(canMove[pickPiece][0],canMove[pickPiece][1],False)) == 0:
                    pickPiece = randint(0,len(canMove)-1)
                moves = game.GetMoves(canMove[pickPiece][0],canMove[pickPiece][1],False)
                pickMove = randint(0,len(moves)-1)
                return canMove[pickPiece],moves[pickMove]
            else:
                moves = game.GetMoves(toMove[0],toMove[1],True)
                pickMove = randint(0,len(moves)-1)
                return toMove,moves[pickMove]

        elif self.difficuly == 2:
            canMove = []
            if toMove == None:
                for row in range(16):
                    for col in range(16):
                        if board[col][row] == 2:
                            canMove.append((col,row))
                jump = False
            else:
                jump = True
                canMove.append(toMove)

            self.deepSearch(game, board, canMove, jump, 3)

        elif self.difficuly == 3:
            ...

    def deepSearch(self, game, board, canMove, jump, itterations):
        search = self.search(game, board, canMove, jump)
        for key in search:
            for move in search[key]:
                board = game.GetBoard()
                self.simulateMove(board, key, move[1])
                if jump != True:
                    dx = key[0] - move[1][0]
                    dy = key[1] - move[1][1]
                    if dx in game.GetJumpCheck() or dy in game.GetJumpCheck():
                        jump = True
                    else:
                        jump = False
                deepReturn = self.deepSearch(game, board, canMove, jump, itterations-1)
                weight = 0
                for key in deepReturn:
                    weight += deepReturn[key][0]

    def search(self, game, board, canMove, jump=False):
        pieceMove = {}
        for piece in canMove:
            moveWeights = []
            moves = game.GetMoves(piece[0],piece[1],jump)
            for move in moves:
                weight = self.getWeight(board, piece, move)
                moveWeights.append((weight,move))
            moveWeights = deque(sorted(moveWeights))
            for _ in range(len(moveWeights//2)):
                moveWeights.popleft()
            pieceMove[piece] = moveWeights
        return pieceMove

    def getWeight(self, board, piece, move):
        # longer the distance the better
        # prioritise the center squares
        # try and minimise trailing pieces
        ...

    def simulateMove(self, board, toMove, moveTo):
        board[toMove[1]][toMove[0]] = 0
        board[moveTo[1]][moveTo[0]] = 2
        return board

    

class Player():
    def __init__(self, name):
        self.name = name