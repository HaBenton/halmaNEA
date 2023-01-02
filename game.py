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
        cornerList = [(0,0),(15,15),(15,0),(0,15)]
        if self._numPlayers == 2:
            width = 5
            n = 5
        elif self._numPlayers == 4:
            width = 4
            n = 4
        for player in range(self._numPlayers):
            for x in range(width): 
                for y in range(width):
                    if y <= n - x:
                        self._board[(abs(cornerList[player][1]-y))][(abs(cornerList[player][0]-x))] = player + 1
                    

    def GetBoard(self):
        return self._board
    
    def GetTurn(self):
        return self._turn

    def GetMovement(self):
        return self._movement

    def GetPlayers(self):
        return self._numPlayers

    def GetJumpCheck(self):
        return self._jump_check

    def LoadGame(self, file):
        with open(file, "r") as f:
            row = 0
            for line in f:
                if row < 16:
                    for col in range(len(line)-1):
                        self._board[row][col] = int(line[col])
                elif row == 16: self._turn = int(line)
                row += 1

    def SaveGame(self, file):
        with open(file, "w") as f:
            for row in self._board:
                for piece in row:
                    f.write(str(piece))
                f.write("\n")
            f.write(str(self._turn))
                    
            
    
    def EndTurn(self):
        winner = False
        if self.WinCheck():
            winner = True
        self._turn += 1
        if self._turn > self._numPlayers:
            self._turn = 1
        return winner
    
    def CornerCheck(self, xCheck, yCheck, player):
        cornerList = [(15,15),(0,0),(0,15),(15,0)]
        if self._numPlayers == 2:
            width = 5
            n = 5
        elif self._numPlayers == 4:
            width = 4
            n = 4
        for x in range(width): 
            for y in range(width):
                if y <= n - x:
                    if (abs(cornerList[player][0]-x)) == xCheck and (abs(cornerList[player][1]-y)) == yCheck:
                        return True
        return False

    
    def GetMoves(self, x, y, jump, board=False):
        if not board:
            board = self.GetBoard()
        moves = []
        if not jump:
            for xMove in self.GetMovement():
                for yMove in self.GetMovement():
                    xFinal,yFinal = (x+xMove),(y+yMove)
                    if xFinal >= 0 and yFinal >= 0 and xFinal <= 15 and yFinal <= 15:
                        if board[y+yMove][x+xMove] == 0:
                            if (not self.CornerCheck(x,y,self._turn-1)) or (self.CornerCheck(x,y,self._turn-1) and self.CornerCheck(x+xMove,y+yMove,self._turn-1)):
                                moves.append((xFinal,yFinal))
        for move in self.GetJumpCheck():
            xFinal,yFinal = (x+move[0]),(y+move[1])
            if xFinal >= 0 and yFinal >= 0 and xFinal <= 15 and yFinal <= 15:
                if board[y+move[1]][x+move[0]] == 0:
                    if board[y+(move[1]//2)][x+(move[0]//2)] != 0:
                        if (not self.CornerCheck(x,y,self._turn-1)) or (self.CornerCheck(x,y,self._turn-1) and self.CornerCheck(x+move[0],y+move[1],self._turn-1)):
                            moves.append((xFinal,yFinal))
        return moves

    def Move(self, start, end): #start and end are tuples of coords
        dy = end[1] - start[1]
        dx = end[0] - start[0]
        if (not self.CornerCheck(start[0], start[1],self._turn-1)) or (self.CornerCheck(start[0], start[1],self._turn-1) and self.CornerCheck(end[0], end[1],self._turn-1)):
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
            else:
                print("not valid piece to move")
        return False

    def aiMove(self, move):
        self._board[move.start.y][move.start.x] = 0
        self._board[move.end.y][move.end.x] = self.GetTurn()
        
    
    def WinCheck(self):
        cornerList = [(15,15),(0,0),(0,15),(15,0)]
        if self._numPlayers == 2:
            width = 5
            n = 5
        elif self._numPlayers == 4:
            width = 4
            n = 4
        for x in range(width): 
            for y in range(width):
                if y <= n - x:
                    if self._board[(abs(cornerList[self._turn-1][1]-y))][(abs(cornerList[self._turn-1][0]-x))] != self._turn:
                        return False
        return True
        