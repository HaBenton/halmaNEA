from game import Game
import tkinter as tk
from tkinter import N, S, E, W, ttk
import sys
import pygame

class Ui():
    def __init__(self):
        self._tile_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self._allowed_lengths = [3, 4, 5]
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

    def run(self):
        raise NotImplementedError


class Terminal(Ui):
    def __init__(self):
        super().__init__()
        
    
    def PrintBoard(self, game):
        print("")
        print(" #  |  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16")
        print("----+-------------------------------------------------")
        for i in range(len(game.GetBoard())):
            if i < 9:
                print(f" {i+1}  | {game.GetBoard()[i]}")
            else:
                print(f" {i+1} | {game.GetBoard()[i]}")
        print("")


    def Winner(self, game):
        if game.Winner():
            replay = ""
            print(f"the winner is {game.GetTurn()}")
            while replay != "y" and replay != "n":
                replay = input("would you like to play again (y/n)? ")
            if replay == "y":
                self.run()
            elif replay == "n":
                sys.exit()
    

    def GetJumpSpots(self, game, end):
        jump_spots = []
        board = game.GetBoard()
        for place in self._jump_check:
            try:
                if board[end[1] + place[1]][end[0] + place[0]] == 0:
                    if board[end[1] + (place[1]//2)][end[0] + (place[0]//2)] != 0:
                        if 0 > (end[1] + place[1]) > 15 or 0 > (end[0] + place[0]) > 15:
                            pass
                        else:
                            jump_spots.append([end[1] + place[1], end[0] + place[0]])
            except:
                pass
        return jump_spots
                    

    def run(self):
        while True:
            players = input("how many players (2 or 4): ")
            if players == "2" or players == "4":
                break
        game = Game(int(players))
        while True:
            print("")
            print(f"it is player {game.GetTurn()}s turn")
            self.PrintBoard(game)
            while True:
                selected_tile = "-1"
                end_tile = "-1"
                while (len(selected_tile) not in self._allowed_lengths) and (len(end_tile) not in self._allowed_lengths):
                    valid_input = False
                    selected_tile = input("which piece would you like to move? ")
                    end_tile = input("where would you like to move it to? ")
                    print("")
                try:
                    start = selected_tile.split(" ")
                    end = end_tile.split(" ")
                    valid_input = True
                except:
                    pass
                if valid_input:
                    try:
                        for item in range(len(start)):
                            start[item] = int(start[item])-1
                        for item in range(len(end)):
                            end[item] = int(end[item])-1
                        valid = True
                    except:
                        valid = False
                    for item in start:
                        if item+1 not in self._tile_nums:
                            valid = False
                    for item in end:
                        if item+1 not in self._tile_nums:
                            valid = False
                    if valid:
                        valid_move = game.Move(start, end)
                        if valid_move == "hop":
                            jump_choice = ""
                            jump_spots = self.GetJumpSpots(game, end)
                            end_of_turn = False
                            while not end_of_turn:
                                self.PrintBoard(game)
                                print("you can still jump")
                                while True:
                                    jump_choice = input(f"either input end to end your turn or a square make the piece at {end[0]+1} {end[1]+1}: ")
                                    if jump_choice == "end":
                                        end_of_turn = True
                                        break
                                    else:
                                        try:
                                            jump = jump_choice.split(" ")
                                            temp = []
                                            for item in range(len(jump)):
                                                jump[item] = int(jump[item])-1
                                                temp.append(jump[item])
                                            jump[0] = temp[1]
                                            jump[1] = temp[0]
                                            if jump in jump_spots:
                                                temp[0] = jump[1]
                                                temp[1] = jump[0]
                                                jump[0] = temp[0]
                                                jump[1] = temp[1]
                                                valid_move = game.Move(end, jump)
                                                end = jump
                                                jump_spots = self.GetJumpSpots(game, end)
                                                break
                                        except:
                                            pass              
                            if game.WinCheck():
                                print(f"")
                            game.EndTurn()
                            break
                        elif valid_move == "end":
                            game.WinCheck()
                            game.EndTurn()
                            break
            



class Gui(Ui):

    def __init__(self):
        super().__init__()
        self.MenuRoot = tk.Tk()
        self.MenuRoot.title("play game")

    
    def PlayGame(self):
        PlayerSelect = ttk.Frame(self.MenuRoot, padding="5 5 12 12")
        PlayerSelect.grid(column=0, row=0, sticky=(N, E, S, W))
        SinglePlayer = tk.Label(PlayerSelect, text="Single Player").grid(column=0, row=0, sticky=(N,E,S,W))
        MultiPlayer = tk.Label(PlayerSelect, text="Multiplayer").grid(column=1, row=0, sticky=(N,E,S,W))
        EasyAIPlay = tk.Button(PlayerSelect, text="Easy", width=20, height=3).grid(column=0, row=1, sticky=(N,E,S,W))
        MediumAIPlay = tk.Button(PlayerSelect, text="Medium", width=20, height=3).grid(column=0, row=2, sticky=(N,E,S,W))
        HardAIPlay = tk.Button(PlayerSelect, text="Hard", width=20, height=3).grid(column=0, row=3, sticky=(N,E,S,W))
        TwoPlayersPlay = tk.Button(PlayerSelect, text="Two Players", width=20, height=3, command=lambda:self.NoAiPlay(2)).grid(column=1, row=1, sticky=(N,E,S,W))
        FourPlayersPlay = tk.Button(PlayerSelect, text="Four Players", width=20, height=3, command=lambda:self.NoAiPlay(4)).grid(column=1, row=2, sticky=(N,E,S,W))
        Quit = tk.Button(PlayerSelect, text="Quit", width=20, height=3, command=self.MenuRoot.destroy).grid(column=1, row=3, sticky=(N,E,S,W))
        PlayerSelect.mainloop()

    def boardSetup(self, players, game):
        screen = pygame.display.set_mode((1005, 800))
        screen.fill((100,100,100))
        pygame.display.set_caption("Halma")
        pygame.display.update()
        self.boardUpdate(screen, game, False)
        return screen

    def MoveCheckandMove(self, mouse, game, screen, moves, toMove, jump):
        board = game.GetBoard()
        if mouse[0] <= 800 and mouse[1] <= 800:
            xposition = mouse[0]//50
            yposition = mouse[1]//50
            if board[yposition][xposition] == game.GetTurn() and not jump:
                moves = self.GetMoves(game, xposition, yposition, screen, False)
                return moves, (xposition, yposition), False
            elif (xposition, yposition) in moves:
                moveReturn = game.Move(toMove, (xposition, yposition))
                self.boardUpdate(screen, game, False)
                if moveReturn == "end":
                    game.EndTurn()
                    self.boardUpdate(screen, game, False)
                    return [], (), False
                elif moveReturn == "hop":
                    moves = self.GetMoves(game, xposition, yposition, screen, True)
                    return moves, (xposition, yposition), True
                elif moveReturn == False and jump:
                    moves = self.GetMoves(game, toMove[0], toMove[1], screen, True)
                    return moves, toMove, jump
                return [], (), False
            else:
                return moves, toMove, jump
        else:
            if 970 >= mouse[0] >= 820 and 110 >= mouse[1] >= 70 and jump:
                game.EndTurn()
                self.boardUpdate(screen, game, False)
                return [], (), False
            else:
                return moves, toMove, jump


    def GetMoves(self, game, x, y, screen, jump):
        board = game.GetBoard()
        self.boardUpdate(screen, game, (x,y))
        moves = []
        if not jump:
            for xMove in game.GetMovement():
                for yMove in game.GetMovement():
                    try:
                        if board[y+yMove][x+xMove] == 0:
                            xFinal,yFinal = (x+xMove),(y+yMove)
                            if xFinal >= 0 and yFinal >= 0:
                                moves.append((xFinal,yFinal))
                                pygame.draw.circle(screen,(0,0,0),(((x+xMove)*50+25), ((y+yMove)*50+25)), 15)
                    except IndexError:
                        pass
        for move in self._jump_check:
            try:
                if board[y+move[1]][x+move[0]] == 0:
                    if board[y+(move[1]//2)][x+(move[0]//2)] != 0:
                        xFinal,yFinal = (x+move[0]),(y+move[1])
                        if xFinal >= 0 and yFinal >= 0:
                            moves.append((xFinal,yFinal))
                            pygame.draw.circle(screen,(0,0,0),(((x+move[0])*50+25), ((y+move[1])*50+25)), 15)
            except IndexError:
                pass
        pygame.display.update()
        return moves


    def boardUpdate(self, screen, game, selected):
        colour = (255,255,255)
        board = game.GetBoard()
        pygame.draw.rect(screen,(100,100,100),(0,0,800,800))
        for row in range(16):
            for col in range(row % 2,16,2):
                pygame.draw.rect(screen,colour,(row*50, col*50, 50, 50))
        pygame.draw.rect(screen,(0,0,0), (800,0,5,800))
        for row in range(16):
            for col in range(16):
                if board[col][row] != 0:
                    if board[col][row] == 1:
                        pygame.draw.circle(screen,(0,0,255),((row*50+25), (col*50)+25), 15)
                    elif board[col][row] == 2:
                        pygame.draw.circle(screen,(255,0,0),((row*50+25), (col*50)+25), 15)
                    elif board[col][row] == 3:
                        pygame.draw.circle(screen,(0,255,0),((row*50+25), (col*50)+25), 15)
                    elif board[col][row] == 4:
                        pygame.draw.circle(screen,(255,0,255),((row*50+25), (col*50)+25), 15)
        if selected:
            pygame.draw.circle(screen,(52,235,225),((selected[0]*50+25), (selected[1]*50)+25), 15)

        self.Sidebar(game,screen)
        
        pygame.display.update()

    def Sidebar(self, game, screen):
        FONT = pygame.font.Font(None, 25)
        TurnText = FONT.render(f"It is player {game.GetTurn()}'s turn", True, "BLACK")
        Turn = pygame.draw.rect(screen,(100,100,100), (820, 20, 150, 40))
        screen.blit(TurnText, TurnText.get_rect(center = Turn.center))
        EndTurnText = FONT.render("End Turn", True, "BLACK")
        EndTurn = pygame.draw.rect(screen,(255,255,255), (820, 70, 150, 40))
        screen.blit(EndTurnText, EndTurnText.get_rect(center = EndTurn.center))

        if game.GetPlayers() == 2:
            pygame.draw.rect(screen,(0,0,0),(248,0,4,102))
            pygame.draw.rect(screen,(0,0,0),(198,98,54,4))
            pygame.draw.rect(screen,(0,0,0),(198,98,4,52))
            pygame.draw.rect(screen,(0,0,0),(148,148,54,4))
            pygame.draw.rect(screen,(0,0,0),(148,148,4,52))
            pygame.draw.rect(screen,(0,0,0),(98,198,54,4))
            pygame.draw.rect(screen,(0,0,0),(98,198,4,52))
            pygame.draw.rect(screen,(0,0,0),(0,248,102,4))

            pygame.draw.rect(screen,(0,0,0),(548,698,4,102))
            pygame.draw.rect(screen,(0,0,0),(548,698,54,4))
            pygame.draw.rect(screen,(0,0,0),(598,648,4,52))
            pygame.draw.rect(screen,(0,0,0),(598,648,54,4))
            pygame.draw.rect(screen,(0,0,0),(648,598,4,52))
            pygame.draw.rect(screen,(0,0,0),(648,598,54,4))
            pygame.draw.rect(screen,(0,0,0),(698,548,4,52))
            pygame.draw.rect(screen,(0,0,0),(698,548,102,4))
        else:
            pygame.draw.rect(screen,(0,0,0),(198,0,4,102))
            pygame.draw.rect(screen,(0,0,0),(148,98,54,4))
            pygame.draw.rect(screen,(0,0,0),(148,98,4,52))
            pygame.draw.rect(screen,(0,0,0),(98,148,54,4))
            pygame.draw.rect(screen,(0,0,0),(98,148,4,52))
            pygame.draw.rect(screen,(0,0,0),(0,198,102,4))

            pygame.draw.rect(screen,(0,0,0),(598,698,4,102))
            pygame.draw.rect(screen,(0,0,0),(598,698,54,4))
            pygame.draw.rect(screen,(0,0,0),(648,648,4,52))
            pygame.draw.rect(screen,(0,0,0),(648,648,54,4))
            pygame.draw.rect(screen,(0,0,0),(698,598,4,52))
            pygame.draw.rect(screen,(0,0,0),(698,598,102,4))
            
            pygame.draw.rect(screen,(0,0,0),(598,0,4,102))
            pygame.draw.rect(screen,(0,0,0),(598,98,54,4))
            pygame.draw.rect(screen,(0,0,0),(648,98,4,52))
            pygame.draw.rect(screen,(0,0,0),(648,148,54,4))
            pygame.draw.rect(screen,(0,0,0),(698,148,4,52))
            pygame.draw.rect(screen,(0,0,0),(698,198,102,4))

            pygame.draw.rect(screen,(0,0,0),(198,698,4,102))
            pygame.draw.rect(screen,(0,0,0),(148,698,54,4))
            pygame.draw.rect(screen,(0,0,0),(148,648,4,52))
            pygame.draw.rect(screen,(0,0,0),(98,648,54,4))
            pygame.draw.rect(screen,(0,0,0),(98,598,4,52))
            pygame.draw.rect(screen,(0,0,0),(0,598,102,4))

    def NoAiPlay(self, players):
        
        game = Game(int(players))
        pygame.init()
        FONT = pygame.font.Font(None, 25)
        screen = self.boardSetup(players, game)
        
        running = True
        moves = []
        toMove = ()
        jump = False
        while running:
            self.Sidebar(game,screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.MenuRoot.destroy()
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if not jump:
                        moves, toMove, jump = self.MoveCheckandMove(mouse, game, screen, moves, toMove, False)
                    else:
                        moves, toMove, jump = self.MoveCheckandMove(mouse, game, screen, moves, toMove, True)
                        

        pygame.quit()


    def DisplayRules(self):
        RulesVar = """
            The objective:\n
            The objective of the game is to get all of your pieces into the opponents corner\n
            \n
            How to play:\n
            You can select a single one of your pieces to move\n
            You then select a square to move into\n
            this is either one of the 9 adjacent places or\n
            you can jump over a piece in one of the 9 adjacent places\n
            if you jump over a piece then you can continue jumping as much as you want\n
            however you can only jump once you have jumped once on that turn and only with that piece\n
            """
        RulesRoot = tk.Tk()
        RulesRoot.title("Rules")
        Rules = ttk.Frame(RulesRoot, padding="5 5 12 12")
        Rules.grid(column=0, row=0, sticky=(N, E, S, W))
        RulesText = tk.Label(Rules, text=RulesVar).grid(column=0, row=0, sticky=(N,E,S,W))
        Close = tk.Button(Rules, text="Close", command=RulesRoot.destroy, width=10, height=2).grid(column=0, row=1, sticky=(N,S))
        Rules.mainloop()

    def run(self):
        Menu = ttk.Frame(self.MenuRoot, padding="5 5 12 12")
        Menu.grid(column=0, row=0, sticky=(N, E, S, W))
        PlayGame = tk.Button(Menu, text="Play Game", width= 30, height=4, command=(self.PlayGame)).grid(column=0, row=0, sticky=(N,E,S,W))
        Rules = tk.Button(Menu, text="Rules", width=30, height=4, command=self.DisplayRules).grid(column=0, row=1, sticky=(N,E,S,W))
        Quit = tk.Button(Menu, text="Quit", width=30, height=4, command=self.MenuRoot.destroy).grid(column=0, row=2, sticky=(N,E,S,W))
        Menu.mainloop()
    
    
