class Game:
    def __init__(self, players):
        self._movement = [0, 1, -1]
        self._jump = [0, 2, -2]
        self._jump_check = [
            [2, 2],
            [0, 2],
            [-2, 2],
            [2, 0],
            [-2, 0],
            [2, -2],
            [0, -2],
            [-2, -2]
        ]
        self._board = []
        self._numPlayers = players
        self._turn = 1
        self.Setup()
    
    def Setup(self):
        self._board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        if self._numPlayers == 2: #2 player game setup
            n = 5
            for x in range(5): #player 1 pieces in place
                for y in range(5):
                    if y <= n:
                        self._board[x][y] = 1
                n -= 1
            n = 5
            for x in range(5): #player 2 pieces in place
                for y in range(5):
                    if y <= n:
                        self._board[15-x][15-y] = 2
                n -= 1
        if self._numPlayers == 4: #4 player game setup
            n = 4
            for x in range(4): #player 1 pieces in place
                for y in range(4):
                    if y <= n:
                        self._board[x][y] = 1
                n -= 1
            n = 4
            for x in range(4): #player 2 pieces in place
                for y in range(4):
                    if y <= n:
                        self._board[15-x][15-y] = 2
                n -= 1
            n = 4
            for x in range(4): #player 3 pieces in place
                for y in range(4):
                    if y <= n:
                        self._board[15-x][y] = 3
                n -= 1
            n = 4
            for x in range(4): #player 4 pieces in place
                for y in range(4):
                    if y <= n:
                        self._board[x][15-y] = 4
                n -= 1
                    

    def GetBoard(self):
        return self._board
    
    def GetTurn(self):
        return self._turn
    
    def GetJump(self):
        return self._jump

    def GetMovement(self):
        return self._movement

    def GetPlayers(self):
        return self._numPlayers

    def GetJumpCheck(self):
        return self._jump_check
    
    def EndTurn(self):
        winner = False
        if self.WinCheck():
            winner = True
        self._turn += 1
        if self._turn > self._numPlayers:
            self._turn = 1
        return winner
    
    def CornerCheck(self, xCheck, yCheck):
        if self._numPlayers == 2:
            width = 5
            n = 5
        elif self._numPlayers == 4:
            width = 4
            n = 4
        if self._turn == 1:
            for x in range(width): 
                for y in range(width):
                    if y <= n:
                        if (15-x) == xCheck and (15-y) == yCheck:
                            return True
                n -= 1
        elif self._turn == 2:
            for x in range(width): 
                for y in range(width):
                    if y <= n:
                        if x == xCheck and y ==yCheck:
                            return True
                n -= 1
        elif self._turn == 4:
            for x in range(width): 
                    for y in range(width):
                        if y <= n:
                            if x == xCheck and (15-y) == yCheck:
                                return True
                    n -= 1
        elif self._turn == 3:
            for x in range(width): 
                for y in range(width):
                    if y <= n:
                        if (15-x) == xCheck and y == yCheck:
                            return True
                n -= 1
        return False

    
    def GetMoves(self, x, y, jump):
        board = self.GetBoard()
        moves = []
        if not jump:
            for xMove in self.GetMovement():
                for yMove in self.GetMovement():
                    try:
                        if board[y+yMove][x+xMove] == 0:
                            if (not self.CornerCheck(x,y)) or (self.CornerCheck(x,y) and self.CornerCheck(x+xMove,y+yMove)):
                                xFinal,yFinal = (x+xMove),(y+yMove)
                                if xFinal >= 0 and yFinal >= 0:
                                    moves.append((xFinal,yFinal))
                    except IndexError:
                        pass
        for move in self._jump_check:
            try:
                if board[y+move[1]][x+move[0]] == 0:
                    if board[y+(move[1]//2)][x+(move[0]//2)] != 0:
                        if (not self.CornerCheck(x,y)) or (self.CornerCheck(x,y) and self.CornerCheck(x+move[0],y+move[1])):
                            xFinal,yFinal = (x+move[0]),(y+move[1])
                            if xFinal >= 0 and yFinal >= 0:
                                moves.append((xFinal,yFinal))
            except IndexError:
                pass
        return moves

    def Move(self, start, end): #start and end are touples of coords
        dy = end[1] - start[1]
        dx = end[0] - start[0]
        if (not self.CornerCheck(start[0], start[1])) or (self.CornerCheck(start[0], start[1]) and self.CornerCheck(end[0], end[1])):
            if self._board[start[1]][start[0]] == self._turn: #selected piece is owned by active player
                if self._board[end[1]][end[0]] == 0: #end tile is empty
                    if dx in self._movement and dy in self._movement: #within one space
                        self._board[start[1]][start[0]] = 0
                        self._board[end[1]][end[0]] = self._turn
                        return "end"
                    elif dx in self._jump and dy in self._jump: #within two spaces for jump
                        jumpOverY = start[1] + (dy//2)
                        jumpOverX = start[0] + (dx//2)
                        if self._board[jumpOverY][jumpOverX] != 0: #check if there is a piece to be jumped over
                            self._board[start[1]][start[0]] = 0
                            self._board[end[1]][end[0]] = self._turn
                            return "hop"
        return False
    
    def WinCheck(self):
        if self._numPlayers == 2:
            width = 5
            n = 5
        elif self._numPlayers == 4:
            width = 4
            n = 4
        if self._turn == 1:
            for x in range(width): 
                for y in range(width):
                    if y <= n:
                        if self._board[15-y][15-x] != self._turn:
                            return False
                n -= 1
        elif self._turn == 2:
            for x in range(width): 
                for y in range(width):
                    if y <= n:
                        if self._board[y][x] != self._turn:
                            return False
                n -= 1
        elif self._turn == 3:
            for x in range(width): 
                for y in range(width):
                    if y <= n:
                         if self._board[y][15-x] != self._turn:
                            return False
                n -= 1
        elif self._turn == 4:
            for x in range(width): 
                for y in range(width):
                    if y <= n:
                        if self._board[15-y][x] != self._turn:
                            return False
                n -= 1
        return True


