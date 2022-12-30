from random import randint
from itertools import repeat
from math import sqrt
import copy

class Place():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Move():
    def __init__(self, start, end):
        self.start = start
        self.end = end

class ScoreResult():
    def __init__(self, score, iswin, move=None):
        self.score = score
        self.iswin = iswin
        self.move = move

    def reverse(self):
        self.score = -self.score

class Player():
    def __init__(self):
        pass


class AI(Player):
    def __init__(self, difficulty):
        self.difficuly = difficulty

    def GetPieces(self, board, player=1):
        canMove = []
        for row in range(16):
            for col in range(16):
                if board[col][row] == player + 1:
                    canMove.append((col,row))
        return canMove

    def GetMove(self, game):
        board = copy.deepcopy(game.GetBoard())
        if self.difficuly == 1:
            moves = self.possibleMoves(game, board, game.GetTurn()-1)
            chosen = randint(0, len(moves))
            return moves[chosen]

        elif self.difficuly == 2:
            
            score = self.score(game, game.GetTurn()-1, board, 3, game.GetTurn()-1) #player is stored as player 1 or 2 but needs to be 0 or 1 to be manipulated
            move = score.move
            
            return move


    def score(self, game, player, position, depth, playerToMove, move=None):
        if self.winfor(player, position): return ScoreResult(100,1)
        if self.winfor(1-player, position): return ScoreResult(-100,-1)
        if depth == 0:
            return self.heuristicScore(player, position, playerToMove, move)
        else:
            moves = self.possibleMoves(game, position, playerToMove)
            positions = map(self.simulateMove, repeat(position), moves, repeat(playerToMove))
            scores = map(self.score, repeat(game), repeat(playerToMove), positions, repeat(depth-1), repeat(1-playerToMove), moves)
            
            maxScore = -1000
            scoreObj = None

            for score in scores:
                if score.score > maxScore:
                    maxScore = score.score
                    scoreObj = score

            if player == playerToMove: return scoreObj
            else: 
                scoreObj.reverse()
                return scoreObj


    def winfor(self, player, position):
        cornerList = [(15,15),(0,0)]
        for x in range(5): 
            for y in range(5):
                if y <= 5 - x:
                    if position[(abs(cornerList[player][1]-y))][(abs(cornerList[player][0]-x))] != player + 1:
                        return False
        return True
    
    def heuristicScore(self, player, position, playerToMove, move):
        pieces = self.GetPieces(position, playerToMove)
        if playerToMove == 0: corner = 15
        else: corner = 0
        distance = 0
        for piece in pieces:
            distance += round(sqrt(((corner - piece[0])**2)+((corner - piece[1])**2)))
        distance = round(distance/3)
        if player == playerToMove: return ScoreResult(100-distance, 0, move)
        else: return ScoreResult(distance-100, 0, move)

    def possibleMoves(self, game, position, playerToMove):
        pieces = self.GetPieces(position, playerToMove)
        moves = []
        for piece in pieces:
            x = piece[0]
            y = piece[1]
            for xMove in game.GetMovement():
                for yMove in game.GetMovement():
                    xFinal,yFinal = (x+xMove),(y+yMove)
                    if xFinal >= 0 and yFinal >= 0 and xFinal <= 15 and yFinal <= 15:
                        if position[y+yMove][x+xMove] == 0:
                            if (not game.CornerCheck(x,y)) or (game.CornerCheck(x,y) and game.CornerCheck(x+xMove,y+yMove)):
                                moves.append(Move(Place(x,y),Place(xFinal,yFinal)))
            moves += self.possibleJumpMoves(game, position, x, y)
        return moves
            

    def possibleJumpMoves(self, game, position, x, y, prevX=-1, prevY=-1):
        moves = []
        for move in game.GetJumpCheck():
            xFinal,yFinal = (x+move[0]),(y+move[1])
            if xFinal != prevX and yFinal != prevY:
                if xFinal >= 0 and yFinal >= 0 and xFinal <= 15 and yFinal <= 15:
                    if position[y+move[1]][x+move[0]] == 0:
                        if position[y+(move[1]//2)][x+(move[0]//2)] != 0:
                            if (not game.CornerCheck(x,y)) or (game.CornerCheck(x,y) and game.CornerCheck(x+move[0],y+move[1])):
                                moves.append(Move(Place(x,y),Place(xFinal,yFinal)))
                                chainMoves = self.possibleJumpMoves(game, position, xFinal, yFinal, x, y)
                                moves += chainMoves
        return moves
            

    def simulateMove(self, position, move, playerToMove):
        position[move.start.y][move.start.x] = 0
        position[move.end.y][move.end.x] = playerToMove
        return position


class Human(Player):
    def __init__(self, name, wins, loss):
        self.name = name
        self.wins = wins
        self.loss = loss
        self.ratio = wins
        if loss != 0:
            self.ratio = round(wins/loss, 3)
