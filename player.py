from random import randint

class AI():
    def __init__(self, difficulty):
        self.difficuly = difficulty

    def GetMove(self, game, toMove=None):
        board = game.GetBoard()
        if self.difficuly == 1:
            if toMove == None:
                canMove = []
                for row in range(16):
                    for col in range(16):
                        if board[col][row] == 2:
                            canMove.append((col,row))
                while True:
                    pickPiece = randint(0,len(canMove)-1)
                    if game.GetMoves(canMove[pickPiece][0],canMove[pickPiece][1],False) != []:
                        break
                moves = game.GetMoves(canMove[pickPiece][0],canMove[pickPiece][1],False)
                while True:
                    pickMove = randint(0,len(moves)-1)
                    if moves[pickMove][0] < 8:
                        if randint(0,3) != 0:
                            return canMove[pickPiece],moves[pickMove]
                    else:
                        return canMove[pickPiece],moves[pickMove]
            else:
                moves = game.GetMoves(toMove[0],toMove[1],True)
                pickMove = randint(0,len(moves)-1)
                return toMove,moves[pickMove]

        elif self.difficuly == 2:
            ##################
            # Minimax 3 deep #
            ##################
            ...
        elif self.difficuly == 3:
            ##################
            # Minimax 7 deep #
            ##################
            ...





class Player():
    def __init__(self, name):
        self.name = name