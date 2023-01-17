from random import randint
from itertools import repeat
from math import sqrt
import copy

def addToFS(fs, elt):
    return fs.union(frozenset({elt}))

def removeFromFS(fs, elt):
    return fs.difference(frozenset({elt}))

class Place():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x and self.y != other.y


class Move():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __hash__(self):
        return hash((self.start, self.end))

    def __eq__(self, other):
        return self.start == other.end and self.start == other.end
    
    def __ne__(self, other):
        return self.start != other.end and self.start != other.end

class ScoreResult():
    def __init__(self, score, iswin, move=None):
        self.score = score
        self.iswin = iswin
        self.move = move

    def reverse(self):
        self.score = -self.score

class AI():
    def __init__(self):
        pass

    def _GetPieces(self, board, player):
        canMove = []
        for y in range(16):
            for x in range(16):
                if board[y][x] == player + 1:
                    canMove.append((x,y))
        return canMove

    def _possibleMoves(self, game, position, playerToMove):
        pieces = self._GetPieces(position, playerToMove)
        moves = []
        for piece in pieces:
            x = piece[0]
            y = piece[1]
            for xMove in game.GetMovement():
                for yMove in game.GetMovement():
                    xFinal,yFinal = (x+xMove),(y+yMove)
                    if xFinal >= 0 and yFinal >= 0 and xFinal <= 15 and yFinal <= 15:
                        if position[y+yMove][x+xMove] == 0:
                            if (not game.CornerCheck(x,y,playerToMove)) or (game.CornerCheck(x,y,playerToMove) and game.CornerCheck(x+xMove,y+yMove,playerToMove)):
                                moves.append(Move(Place(x,y),Place(xFinal,yFinal)))
            done = self._jumpLoop(game, playerToMove, frozenset(), addToFS(frozenset(), (tuple(map(tuple, position)),(x,y))))
            for move in done:
                moves.append(Move(Place(x,y),Place(move[1][0],move[1][1])))
        return moves

    def _jumpLoop (self, game, playerToMove, doneBoards, todoBoards):
        if len(todoBoards) == 0: return doneBoards
        else:
            currBoard = list(todoBoards)[0]
            board = currBoard[0]
            x,y = currBoard[1][0],currBoard[1][1]
            if board in doneBoards: return self._jumpLoop(game, playerToMove, doneBoards, removeFromFS(todoBoards, currBoard))
            oneStepBoards = frozenset()
            ################################################################################
            # CATAGORY A: structures of equivalent standard                                #
            # used a frozen set to make sure duplicates do not appear in the list of moves #
            ################################################################################
            for delta in game.GetJumpCheck():
                xFinal,yFinal = (x+delta[0]),(y+delta[1])
                if xFinal >= 0 and yFinal >= 0 and xFinal <= 15 and yFinal <= 15:
                    if board[y+delta[1]][x+delta[0]] == 0:
                        if board[y+(delta[1]//2)][x+(delta[0]//2)] != 0:
                            if (not game.CornerCheck(x,y,playerToMove)) or (game.CornerCheck(x,y,playerToMove) and game.CornerCheck(x+delta[0],y+delta[1],playerToMove)):
                                tempBoard = self._simulateMove(list(map(list, board)),Move(Place(x,y),Place(xFinal,yFinal)),playerToMove)
                                oneStepBoards = addToFS(oneStepBoards, (tuple(map(tuple, tempBoard)),(xFinal,yFinal)))
            return self._jumpLoop(game, playerToMove, addToFS(doneBoards, currBoard), removeFromFS(todoBoards, currBoard).union(oneStepBoards.difference(doneBoards)))

    def _simulateMove(self, position, move, playerToMove):
        board = copy.deepcopy(position)
        board[move.start.y][move.start.x] = 0
        board[move.end.y][move.end.x] = playerToMove + 1
        return board

    def _dumpBoard(self, board):
        for row in board:
            print(row)
        print("")

    def GetMove(self, game):
        raise NotImplementedError


    
class EasyAI(AI):
    ##############################################################################
    # CATAGORY A: Complex user-defined use of OOP (inheritance)                  #
    # used inheritance to give all the versions of the AIs access to key methods #
    ##############################################################################

    def __init__(self):
        ...

    def GetMove(self, game):
        board = copy.deepcopy(game.GetBoard())
        moves = self._possibleMoves(game, board, game.GetTurn()-1)
        chosen = randint(0, len(moves))
        return moves[chosen-1]



class MediumAI(AI):
    def __init__(self):
        ...

    def GetMove(self, game):
        board = copy.deepcopy(game.GetBoard())
        score = self.__score(game, game.GetTurn()-1, board, 2, game.GetTurn()-1) #player is stored as player 1 or 2 but needs to be 0 or 1 to be manipulated
        return score.move


    def __score(self, game, player, position, depth, playerToMove, move=None):
        if self.__winfor(player, position): return ScoreResult(100,1)
        if self.__winfor(1-player, position): return ScoreResult(-100,-1)
        if depth == 0:
            return self.__heuristicScore(player, position, playerToMove, move)
        else:
            moves = self._possibleMoves(game, position, playerToMove)
            #######################################################
            # CATAGORY A: Tree Traversal                          #
            # used tree traversal to seach through possible moves #
            #######################################################
            positions = list(map(self._simulateMove, repeat(position), moves, repeat(playerToMove)))
            ####################################################################
            # CATAGORY A: Recursive algorithms                                 #
            # used a recursive search to check every move that the AI can make #
            ####################################################################
            scores = list(map(self.__score, repeat(game), repeat(playerToMove), positions, repeat(depth-1), repeat(1-playerToMove), moves))
            for sc in range(len(scores)):
                scores[sc].move = moves[sc]
            if moves == []: raise Exception(f"No Moves {moves}")
            elif positions == []: raise Exception(f"No Positions {positions}")
            elif scores == []: raise Exception(f"No Scores {scores}")
            
            maxScore = scores[0].score
            scoreObj = scores[0]

            for score in scores:
                if score.score > maxScore:
                    maxScore = score.score
                    scoreObj = score
            

            if player == playerToMove: return scoreObj
            else: 
                scoreObj.reverse()
                return scoreObj


    def __winfor(self, player, position):
        cornerList = [(15,15),(0,0)]
        for x in range(5): 
            for y in range(5):
                if y <= 5 - x:
                    if position[(abs(cornerList[player][1]-y))][(abs(cornerList[player][0]-x))] != player + 1:
                        return False
        return True
    
    def __heuristicScore(self, player, position, playerToMove, move):
        pieces = self._GetPieces(position, playerToMove)
        if playerToMove == 0: corner = 15
        else: corner = 0
        distance = 0
        for piece in pieces:
            distance += round(sqrt(((corner - piece[0])**2)+((corner - piece[1])**2)))
        distance = round(distance/3)
        #########################################################################################################################
        # CATAGORY A: Dynamic generation of objects                                                                             #
        # used objects to represent the scores that are being generated for a position while keeping the moves together with it #
        #########################################################################################################################
        if player == playerToMove: return ScoreResult(100-distance, 0, move)
        else: return ScoreResult(distance-100, 0, move)



class HardAI(AI):
    ##############################################################################
    # CATAGORY A: Complex user-defined use of OOP (inheritance)                  #
    # used inheritance to give all the versions of the AIs access to key methods #
    ##############################################################################

    def __init__(self):
        ...

    def GetMove(self, game):
        board = copy.deepcopy(game.GetBoard())
        score = self.__score(game, board, 2, game.GetTurn()-1, -200) #player is stored as player 1 or 2 but needs to be 0 or 1 to be manipulated
        return score.move


    def __score(self, game, position, depth, playerToMove, bestForParent):
        if self.__winfor(1-playerToMove, position): return ScoreResult(100,1)
        if self.__winfor(playerToMove, position): return ScoreResult(-100,-1)
        if depth == 0:
            return self.__heuristicScore(position, 1-playerToMove)
        else:
            moves = self._possibleMoves(game, position, playerToMove)
            positions = list(map(self._simulateMove, repeat(position), moves, repeat(playerToMove)))
            ########################################################
            # CATAGORY A: Tree Traversal                           #
            # used tree traversal to search through possible moves #
            ########################################################

            bestForPTM = -200
            for pos,move in zip(positions,moves):
                ####################################################################
                # CATAGORY A: Recursive algorithms                                 #
                # used a recursive search to check every move that the AI can make #
                ####################################################################
                value_of_p = self.__score(game, pos, depth-1, 1-playerToMove, bestForPTM)
                if value_of_p.score > bestForPTM:
                    bestForPTM = value_of_p.score
                    bestMove = move
                if -bestForPTM < bestForParent:
                    #########################################################################################################################
                    # CATAGORY A: Dynamic generation of objects                                                                             #
                    # used objects to represent the scores that are being generated for a position while keeping the moves together with it #
                    #########################################################################################################################

                    return ScoreResult(-bestForPTM, 0, move)
            return ScoreResult(-bestForPTM, 0, bestMove)


    def __winfor(self, player, position):
        cornerList = [(15,15),(0,0)]
        for x in range(5): 
            for y in range(5):
                if y <= 5 - x:
                    if position[(abs(cornerList[player][1]-y))][(abs(cornerList[player][0]-x))] != player + 1:
                        return False
        return True
    
    def __heuristicScore(self, position, playerToMove):
        pieces1 = self._GetPieces(position, playerToMove)
        if playerToMove == 0: corner = 15
        else: corner = 0
        distance = 0
        for piece in pieces1:
            distance += sqrt(((corner - piece[0])**2)+((corner - piece[1])**2))
        playerToMove = 1-playerToMove
        pieces2 = self._GetPieces(position, playerToMove)
        if playerToMove == 0: corner = 15
        else: corner = 0
        for piece in pieces2:
            distance -= sqrt(((corner - piece[0])**2)+((corner - piece[1])**2))
        distance = distance/(len(pieces1)+len(pieces2))
        return ScoreResult(100-distance, 0)



class Human():
    def __init__(self, name, wins, loss):
        self.name = name
        self.currWins = 0
        self.currLoss = 0
        self.currRatio = self.currWins
        if self.currLoss != 0:
            self.currRatio = round(self.currWins/self.currLoss, 2)
        self.Wins = wins
        self.Loss = loss
        self.Ratio = wins
        if self.Loss != 0:
            self.Ratio = round(self.Wins/self.Loss, 2)
