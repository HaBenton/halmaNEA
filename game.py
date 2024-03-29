class Game:
    def __init__(self, players):
        self.__movement = [0, 1, -1]
        self.__jump = [0, 2, -2]
        self.__jump_check = [
            [2, 2],
            [0, 2],
            [-2, 2],
            [2, 0],
            [-2, 0],
            [2, -2],
            [0, -2],
            [-2, -2]
        ]
        self.__board = []
        self.__numPlayers = players
        self.__turn = 1
        self.__Setup()
    
    def __Setup(self):
        self.__board = [
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
        ##########################################
        # CATAGORY B: Multi-dimensional arrays   #
        # used a 2d array to represent the board #
        ##########################################

        cornerList = [(0,0),(15,15),(15,0),(0,15)]
        if self.__numPlayers == 2:
            width = 5
            n = 5
        elif self.__numPlayers == 4:
            width = 4
            n = 4
        for player in range(self.__numPlayers):
            for x in range(width): 
                for y in range(width):
                    if y <= n - x:
                        self.__board[(abs(cornerList[player][1]-y))][(abs(cornerList[player][0]-x))] = player + 1
                    

    def GetBoard(self):
        return self.__board
    
    def GetTurn(self):
        return self.__turn

    def GetMovement(self):
        return self.__movement

    def GetPlayers(self):
        return self.__numPlayers

    def GetJumpCheck(self):
        return self.__jump_check

    def LoadGame(self, file):
        ###########################################
        # CATAGORY B: reading from a file         #
        # used to import a game state from a file #
        ###########################################
        with open(file, "r") as f:
            row = 0
            for line in f:
                if row < 16:
                    for col in range(len(line)-1):
                        self.__board[row][col] = int(line[col])
                elif row == 16: self.__turn = int(line)
                row += 1

    def SaveGame(self, file):
        #######################################
        # CATAGORY B: writing to a file       #
        # used to save a game state to a file #
        #######################################
        with open(file, "w") as f:
            for row in self.__board:
                for piece in row:
                    f.write(str(piece))
                f.write("\n")
            f.write(str(self.__turn))
                    
            
    
    def EndTurn(self):
        winner = False
        if self.__WinCheck():
            winner = True
        self.__turn += 1
        if self.__turn > self.__numPlayers:
            self.__turn = 1
        return winner
    
    def CornerCheck(self, xCheck, yCheck, player):
        cornerList = [(15,15),(0,0),(0,15),(15,0)]
        if self.__numPlayers == 2:
            width = 5
            n = 5
        elif self.__numPlayers == 4:
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
                            if (not self.CornerCheck(x,y,self.__turn-1)) or (self.CornerCheck(x,y,self.__turn-1) and self.CornerCheck(x+xMove,y+yMove,self.__turn-1)):
                                moves.append((xFinal,yFinal))
        for move in self.GetJumpCheck():
            xFinal,yFinal = (x+move[0]),(y+move[1])
            if xFinal >= 0 and yFinal >= 0 and xFinal <= 15 and yFinal <= 15:
                if board[y+move[1]][x+move[0]] == 0:
                    if board[y+(move[1]//2)][x+(move[0]//2)] != 0:
                        if (not self.CornerCheck(x,y,self.__turn-1)) or (self.CornerCheck(x,y,self.__turn-1) and self.CornerCheck(x+move[0],y+move[1],self.__turn-1)):
                            moves.append((xFinal,yFinal))
        return moves

    def Move(self, start, end): #start and end are tuples of coords
        dy = end[1] - start[1]
        dx = end[0] - start[0]
        if (not self.CornerCheck(start[0], start[1],self.__turn-1)) or (self.CornerCheck(start[0], start[1],self.__turn-1) and self.CornerCheck(end[0], end[1],self.__turn-1)):
            if self.__board[start[1]][start[0]] == self.__turn: #selected piece is owned by active player
                if self.__board[end[1]][end[0]] == 0: #end tile is empty
                    if dx in self.__movement and dy in self.__movement: #within one space
                        self.__board[start[1]][start[0]] = 0
                        self.__board[end[1]][end[0]] = self.__turn
                        return "end"
                    elif dx in self.__jump and dy in self.__jump: #within two spaces for jump
                        jumpOverY = start[1] + (dy//2)
                        jumpOverX = start[0] + (dx//2)
                        if self.__board[jumpOverY][jumpOverX] != 0: #check if there is a piece to be jumped over
                            self.__board[start[1]][start[0]] = 0
                            self.__board[end[1]][end[0]] = self.__turn
                            return "hop"
        return False

    def aiMove(self, move):
        self.__board[move.start.y][move.start.x] = 0
        self.__board[move.end.y][move.end.x] = self.GetTurn()
        
    
    def __WinCheck(self):
        cornerList = [(15,15),(0,0),(0,15),(15,0)]
        if self.__numPlayers == 2:
            width = 5
            n = 5
        elif self.__numPlayers == 4:
            width = 4
            n = 4
        for x in range(width): 
            for y in range(width):
                if y <= n - x:
                    if self.__board[(abs(cornerList[self.__turn-1][1]-y))][(abs(cornerList[self.__turn-1][0]-x))] != self.__turn:
                        return False
        return True
        