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
                                        print(1)
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

    def boardSetup(self, players):
        pygame.init()
        
        colour = (255,255,255)

        screen = pygame.display.set_mode((1005, 800))
        screen.fill((100,100,100))
        pygame.display.set_caption("Halma")

        for row in range(16):
            for col in range(row % 2,16,2):
                pygame.draw.rect(screen,colour,(row*50, col*50, 50, 50))
        
        pygame.draw.rect(screen,(0,0,0), (800,0,5,800))

        pygame.display.update()        
        return screen


    def NoAiPlay(self, players):
        screen = self.boardSetup(players)
        
        if players == 2:
            ...
        else:
            ...
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    pass

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
    
    
