from random import randint
from game import Game
from player import Human, EasyAI, MediumAI, HardAI
import tkinter as tk
from tkinter import N, S, E, W, ttk, END
import sys
import pygame

class Ui():
    def __init__(self):
        self._tile_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self._allowed_lengths = [3, 4, 5]

    def run(self):
        raise NotImplementedError


class Terminal(Ui):
    def __init__(self):
        super().__init__()
        
    
    def __PrintBoard(self, game):
        print("")
        print(" #  |  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16")
        print("----+-------------------------------------------------")
        for i in range(len(game.GetBoard())):
            if i < 9:
                print(f" {i+1}  | {game.GetBoard()[i]}")
            else:
                print(f" {i+1} | {game.GetBoard()[i]}")
        print("")


    def __Winner(self, game):
        replay = ""
        print(f"the winner is {game.GetTurn()-1//game.GetPlayers()}")
        while replay != "y" and replay != "n":
            replay = input("would you like to play again (y/n)? ")
        if replay == "y":
            self.run()
        elif replay == "n":
            sys.exit()
    

    def __GetJumpSpots(self, game, end):
        jump_spots = []
        board = game.GetBoard()
        for place in game.GetJumpCheck():
            if 0 <= (end[1] + place[1]) <= 15 or 0 <= (end[0] + place[0]) <= 15:
                if board[end[1] + place[1]][end[0] + place[0]] == 0:
                    if board[end[1] + (place[1]//2)][end[0] + (place[0]//2)] != 0:
                        jump_spots.append([end[1] + place[1], end[0] + place[0]])
        return jump_spots
                    

    def run(self):
        players = ""
        while players != "2" and players != "4":
            players = input("how many players (2 or 4): ")
        game = Game(int(players))
        while True:
            print("")
            print(f"it is player {game.GetTurn()}s turn")
            self.__PrintBoard(game)
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
                            jump_spots = self.__GetJumpSpots(game, end)
                            end_of_turn = False
                            while not end_of_turn:
                                self.__PrintBoard(game)
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
                                                jump_spots = self.__GetJumpSpots(game, end)
                                                break
                                        except:
                                            pass              
                            if game.EndTurn():
                                self.__Winner(game)
                            break
                        elif valid_move == "end":
                            if game.EndTurn():
                                self.__Winner(game)
                            break
            



class Gui(Ui):

    def __init__(self):
        super().__init__()
        self.__MenuRoot = tk.Tk()
        self.__MenuRoot.title("play game")
        self.__activeNames = [None, None, None, None]
        self.__names = {}
        #####################################################################################
        # CATAGORY B: dictionaries                                                          #
        # used a dictionary to make a pair of the name of a player with their player object #
        #####################################################################################
        self.__rawNames = []
        ###############################################
        # CATAGORY B: reading from a file             #
        # used to import the player stats from a file #
        ###############################################
        with open ("stats.txt", "r") as f:
            for line in f:
                name = line.split(":")
                winLoss = name[1].split("/")
                self.__names.update({name[0]:Human(name[0],int(winLoss[0]),int(winLoss[1]))})
                self.__rawNames.append(name[0])



    def run(self):
        Menu = ttk.Frame(self.__MenuRoot, padding="5 5 12 12")
        Menu.grid(column=0, row=0, sticky=(N, E, S, W))
        PlayGame = tk.Button(Menu, text="Play Game", width= 30, height=4, command=(self.__PlayGame)).grid(column=0, row=0, sticky=(N,E,S,W))
        Rules = tk.Button(Menu, text="Rules", width=30, height=4, command=self.__DisplayRules).grid(column=0, row=1, sticky=(N,E,S,W))
        Quit = tk.Button(Menu, text="Quit", width=30, height=4, command=self.__MenuRoot.destroy).grid(column=0, row=2, sticky=(N,E,S,W))
        Menu.mainloop()
    
    def __PlayGame(self):
        PlayerSelect = ttk.Frame(self.__MenuRoot, padding="5 5 12 12")
        PlayerSelect.grid(column=0, row=0, sticky=(N, E, S, W))
        SinglePlayer = tk.Label(PlayerSelect, text="Single Player").grid(column=0, row=0, sticky=(N,E,S,W))
        MultiPlayer = tk.Label(PlayerSelect, text="Multiplayer").grid(column=1, row=0, sticky=(N,E,S,W))
        EasyAIPlay = tk.Button(PlayerSelect, text="Easy", width=20, height=3, command=lambda:self.__PlayerNames(1,2)).grid(column=0, row=1, sticky=(N,E,S,W))
        MediumAIPlay = tk.Button(PlayerSelect, text="Medium", width=20, height=3, command=lambda:self.__PlayerNames(2,2)).grid(column=0, row=2, sticky=(N,E,S,W))
        HardAIPlay = tk.Button(PlayerSelect, text="Hard", width=20, height=3, command=lambda:self.__PlayerNames(3,2)).grid(column=0, row=3, sticky=(N,E,S,W))
        TwoPlayersPlay = tk.Button(PlayerSelect, text="Two Players", width=20, height=3, command=lambda:self.__PlayerNames(0,2)).grid(column=1, row=1, sticky=(N,E,S,W))
        FourPlayersPlay = tk.Button(PlayerSelect, text="Four Players", width=20, height=3, command=lambda:self.__PlayerNames(0,4)).grid(column=1, row=2, sticky=(N,E,S,W))
        Quit = tk.Button(PlayerSelect, text="Quit", width=20, height=3, command=self.__MenuRoot.destroy).grid(column=1, row=3, sticky=(N,E,S,W))
        PlayerSelect.mainloop()

    def __PlayerNames(self, ai, players):
        PlayerNames = ttk.Frame(self.__MenuRoot, padding="5 5 12 12")
        PlayerNames.grid(column=0, row=0, sticky=(N, E, S, W))
        AddName = tk.Label(PlayerNames, text="Add Name:", width=20, height=2).grid(column=0, row=0, sticky=(N,E,S,W))
        NameToAdd = tk.Entry(PlayerNames, width=20)
        NameToAdd.grid(column=0, row=1, sticky=(N,E,S,W))
        AddButton = tk.Button(PlayerNames, text="Add", width=20, height=2, command=lambda:[self.__AddName(NameToAdd.get()),NameToAdd.delete(0, END)]).grid(column=0, row=2, sticky=(N,E,S,W))
        
        if ai != 0:

            PlayerNameOneLabel = tk.Label(PlayerNames, text="Name:", width=20, height=2).grid(column=0, row=3, sticky=(N,E,S,W))
            PlayerNameOne = tk.StringVar()
            PlayerNameOneBox = ttk.Combobox(PlayerNames, textvariable=PlayerNameOne, width=20, height=2, postcommand=lambda:self.__nameListUpdate(PlayerNameOneBox))
            PlayerNameOneBox.grid(column=0, row=4, sticky=(N,E,S,W))
            PlayerNameOneBox['values'] = self.__rawNames
            PlayerNameOneBox['state'] = 'readonly'
            PlayerNameOneBox.bind('<<ComboboxSelected>>', lambda event:self.__nameHandler(0,PlayerNameOne.get()))

        elif players == 2:

            PlayerNameOneLabel = tk.Label(PlayerNames, text="Name:", width=20, height=2).grid(column=0, row=3, sticky=(N,E,S,W))
            PlayerNameOne = tk.StringVar()
            PlayerNameOneBox = ttk.Combobox(PlayerNames, textvariable=PlayerNameOne, width=20, height=2, postcommand=lambda:self.__nameListUpdate(PlayerNameOneBox))
            PlayerNameOneBox.grid(column=0, row=4, sticky=(N,E,S,W))
            PlayerNameOneBox['values'] = self.__rawNames
            PlayerNameOneBox['state'] = 'readonly'
            PlayerNameOneBox.bind('<<ComboboxSelected>>', lambda event:self.__nameHandler(0,PlayerNameOne.get()))
            
            PlayerNameTwoLabel =tk.Label(PlayerNames, text="Name:", width=20, height=2).grid(column=0, row=5, sticky=(N,E,S,W))
            PlayerNameTwo = tk.StringVar()
            PlayerNameTwoBox = ttk.Combobox(PlayerNames, textvariable=PlayerNameTwo, width=20, height=2, postcommand=lambda:self.__nameListUpdate(PlayerNameTwoBox))
            PlayerNameTwoBox.grid(column=0, row=6, sticky=(N,E,S,W))
            PlayerNameTwoBox['values'] = self.__rawNames
            PlayerNameTwoBox['state'] = 'readonly'
            PlayerNameTwoBox.bind('<<ComboboxSelected>>', lambda event:self.__nameHandler(1,PlayerNameTwo.get()))

        elif players == 4:

            PlayerNameOneLabel = tk.Label(PlayerNames, text="Name:", width=20, height=2).grid(column=0, row=3, sticky=(N,E,S,W))
            PlayerNameOne = tk.StringVar()
            PlayerNameOneBox = ttk.Combobox(PlayerNames, textvariable=PlayerNameOne, width=20, height=2, postcommand=lambda:self.__nameListUpdate(PlayerNameOneBox))
            PlayerNameOneBox.grid(column=0, row=4, sticky=(N,E,S,W))
            PlayerNameOneBox['values'] = self.__rawNames
            PlayerNameOneBox['state'] = 'readonly'
            PlayerNameOneBox.bind('<<ComboboxSelected>>', lambda event:self.__nameHandler(0,PlayerNameOne.get()))

            PlayerNameTwoLabel =tk.Label(PlayerNames, text="Name:", width=20, height=2).grid(column=0, row=5, sticky=(N,E,S,W))
            PlayerNameTwo = tk.StringVar()
            PlayerNameTwoBox = ttk.Combobox(PlayerNames, textvariable=PlayerNameTwo, width=20, height=2, postcommand=lambda:self.__nameListUpdate(PlayerNameTwoBox))
            PlayerNameTwoBox.grid(column=0, row=6, sticky=(N,E,S,W))
            PlayerNameTwoBox['values'] = self.__rawNames
            PlayerNameTwoBox['state'] = 'readonly'
            PlayerNameTwoBox.bind('<<ComboboxSelected>>', lambda event:self.__nameHandler(1,PlayerNameTwo.get()))

            PlayerNameThreeLabel =tk.Label(PlayerNames, text="Name:", width=20, height=2).grid(column=0, row=7, sticky=(N,E,S,W))
            PlayerNameThree = tk.StringVar()
            PlayerNameThreeBox = ttk.Combobox(PlayerNames, textvariable=PlayerNameThree, width=20, height=2, postcommand=lambda:self.__nameListUpdate(PlayerNameThreeBox))
            PlayerNameThreeBox.grid(column=0, row=8, sticky=(N,E,S,W))
            PlayerNameThreeBox['values'] = self.__rawNames
            PlayerNameThreeBox['state'] = 'readonly'
            PlayerNameThreeBox.bind('<<ComboboxSelected>>', lambda event:self.__nameHandler(2,PlayerNameThree.get()))

            PlayerNameFourLabel =tk.Label(PlayerNames, text="Name:", width=20, height=2).grid(column=0, row=9, sticky=(N,E,S,W))
            PlayerNameFour = tk.StringVar()
            PlayerNameFourBox = ttk.Combobox(PlayerNames, textvariable=PlayerNameFour, width=20, height=2, postcommand=lambda:self.__nameListUpdate(PlayerNameFourBox))
            PlayerNameFourBox.grid(column=0, row=10, sticky=(N,E,S,W))
            PlayerNameFourBox['values'] = self.__rawNames
            PlayerNameFourBox['state'] = 'readonly'
            PlayerNameFourBox.bind('<<ComboboxSelected>>', lambda event:self.__nameHandler(3,PlayerNameFour.get()))
            
        PlayButton = tk.Button(PlayerNames, text="Play", width=20, height=2, command=lambda:[self.__MenuRoot.destroy(),self.__gamemodeHandler(ai, players)]).grid(column=1, row=0, sticky=(N,E,S,W))        
        Quit = tk.Button(PlayerNames, text="Quit", width=20, height=2, command=self.__MenuRoot.destroy).grid(column=1, row=1, sticky=(N,E,S,W))
        PlayerNames.mainloop()

    def __AddName(self, name):
        if name not in self.__names:
            if name != "":
                self.__names.update({name:Human(name,0,0)})
                self.__rawNames.append(name)

    def __nameHandler(self, index, name):
        self.__activeNames[index] = name

    def __nameListUpdate(self, box):
        box['values'] = self.__rawNames

    def __gamemodeHandler(self, ai, players):
        if ai != 0: self.__AiPlay(ai)
        else: self.__NoAiPlay(players)

    def __boardSetup(self, players, game):
        screen = pygame.display.set_mode((1005, 800))
        screen.fill((100,100,100))
        pygame.display.set_caption("Halma")
        pygame.display.update()
        self.__boardUpdate(screen, game, False)
        return screen

    def __MoveCheckandMove(self, mouse, game, screen, moves, toMove, jump, diff=0):
        board = game.GetBoard()
        if mouse[0] <= 800 and mouse[1] <= 800:
            xposition = mouse[0]//50
            yposition = mouse[1]//50
            if board[yposition][xposition] == game.GetTurn() and not jump:
                moves = self.__GetMoves(game, xposition, yposition, screen, False)
                return moves, (xposition, yposition), False
            elif (xposition, yposition) in moves:
                moveReturn = game.Move(toMove, (xposition, yposition))
                self.__boardUpdate(screen, game, False)
                if moveReturn == "end":
                    if game.EndTurn():
                        if diff != 0: self.__Winner(game,game.GetPlayers())
                        else: self.__Winner(game,0,diff)
                    self.__boardUpdate(screen, game, False)
                    return [], (), False
                elif moveReturn == "hop":
                    moves = self.__GetMoves(game, xposition, yposition, screen, True)
                    return moves, (xposition, yposition), True
                elif moveReturn == False and jump:
                    moves = self.__GetMoves(game, toMove[0], toMove[1], screen, True)
                    return moves, toMove, jump
                return [], (), False
            else:
                return moves, toMove, jump
        else:
            if 970 >= mouse[0] >= 820 and 110 >= mouse[1] >= 70 and jump:
                if game.EndTurn():
                    if diff != 0: self.__Winner(game,game.GetPlayers())
                    else: self.__Winner(game,0,diff)
                self.__boardUpdate(screen, game, False)
                return [], (), False
            else:
                return moves, toMove, jump


    def __GetMoves(self, game, x, y, screen, jump):
        board = game.GetBoard()
        self.__boardUpdate(screen, game, (x,y))
        moves = game.GetMoves(x, y, jump)
        for move in moves:
            pygame.draw.circle(screen,(0,0,0),(((move[0])*50+25), ((move[1])*50+25)), 15)
        pygame.display.update()
        return moves


    def __boardUpdate(self, screen, game, selected):
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

        self.__Sidebar(game,screen)
        
        pygame.display.update()

    def __Sidebar(self, game, screen):
        pygame.font.init()
        FONT = pygame.font.Font(None, 25)
        TurnText = FONT.render(f"It is player {game.GetTurn()}'s turn", True, "BLACK")
        Turn = pygame.draw.rect(screen,(100,100,100), (820, 20, 150, 40))
        screen.blit(TurnText, TurnText.get_rect(center = Turn.center))
        EndTurnText = FONT.render("End Turn", True, "BLACK")
        EndTurn = pygame.draw.rect(screen,(255,255,255), (820, 70, 150, 40))
        screen.blit(EndTurnText, EndTurnText.get_rect(center = EndTurn.center))
        RestartText = FONT.render("Restart", True, "BLACK")
        Restart = pygame.draw.rect(screen, (255,255,255), (820, 130, 150, 40))
        screen.blit(RestartText, RestartText.get_rect(center = Restart.center))
        RulesText = FONT.render("Rules", True, "BLACK")
        Rules = pygame.draw.rect(screen,(255,255,255), (820, 690, 150, 40))
        screen.blit(RulesText, RulesText.get_rect(center = Rules.center))
        QuitText = FONT.render("Quit", True, "BLACK")
        Quit = pygame.draw.rect(screen,(255,255,255), (820, 740, 150, 40))
        screen.blit(QuitText, QuitText.get_rect(center = Quit.center))
        LoadSaveText = FONT.render("Load/Save", True, "BLACK")
        LoadSave = pygame.draw.rect(screen, (255,255,255), (820, 650, 150, 30))
        screen.blit(LoadSaveText, LoadSaveText.get_rect(center = LoadSave.center))

        if game.GetPlayers() == 2:

            pygame.draw.rect(screen,(255,255,255),(820,190,150,100))
            pygame.draw.circle(screen,(0,0,255),(850,220),15)
            pygame.draw.circle(screen,(255,0,0),(850,260),15)
            one = FONT.render("player 1", True, "BLACK")
            two = FONT.render("player 2", True, "BLACK")
            screen.blit(one,(870,210))
            screen.blit(two,(870,250))

            pygame.draw.rect(screen,(0,0,0),(248,0,4,102))
            pygame.draw.rect(screen,(0,0,0),(0,248,102,4))
            pygame.draw.rect(screen,(0,0,0),(548,698,4,102))
            pygame.draw.rect(screen,(0,0,0),(698,548,102,4))
            
            pos = [198,148,98,598,648,548,698]
            pos2 = [98,148,198,648,598,698,548]
            for item in range(len(pos)):
                pygame.draw.rect(screen,(0,0,0),(pos[item],pos2[item],54,4))
                pygame.draw.rect(screen,(0,0,0),(pos[item],pos2[item],4,52)) 

            stats = FONT.render("Stats:", True, "BLACK")
            screen.blit(stats,(875,310))

            PlayerOne = FONT.render(f"1: {self.__activeNames[0]}", True, "BLACK")
            screen.blit(PlayerOne,(845,340))
            P1CurrStats = FONT.render(f"W: {self.__names[self.__activeNames[0]].currWins} // L: {self.__names[self.__activeNames[0]].currLoss}", True, "BLACK")
            P1CurrRatio = FONT.render(f"WLR: {self.__names[self.__activeNames[0]].currRatio}", True, "BLACK")
            P1AllStats = FONT.render(f"W: {self.__names[self.__activeNames[0]].Wins} // L: {self.__names[self.__activeNames[0]].Loss}", True, "BLACK")
            P1Ratio = FONT.render(f"WLR: {self.__names[self.__activeNames[0]].Ratio}", True, "BLACK")
            screen.blit(P1CurrStats,(810,360))
            screen.blit(P1CurrRatio,(810,380))
            screen.blit(P1AllStats,(810,400))
            screen.blit(P1Ratio,(810,420))

            if self.__activeNames[1] != None:
                PlayerTwo = FONT.render(f"2: {self.__activeNames[1]}", True, "BLACK")
                screen.blit(PlayerTwo,(845,445))
                P2CurrStats = FONT.render(f"W: {self.__names[self.__activeNames[1]].currWins} // L: {self.__names[self.__activeNames[1]].currLoss}", True, "BLACK")
                P2CurrRatio = FONT.render(f"WLR: {self.__names[self.__activeNames[1]].currRatio}", True, "BLACK")
                P2AllStats = FONT.render(f"W: {self.__names[self.__activeNames[1]].Wins} // L: {self.__names[self.__activeNames[1]].Loss}", True, "BLACK")
                P2Ratio = FONT.render(f"WLR: {self.__names[self.__activeNames[1]].Ratio}", True, "BLACK")
                screen.blit(P2CurrStats,(810,465))
                screen.blit(P2CurrRatio,(810,485))
                screen.blit(P2AllStats,(810,505))
                screen.blit(P2Ratio,(810,525))
        
        else:

            pygame.draw.rect(screen,(255,255,255),(820,190,150,190))
            pygame.draw.circle(screen,(0,0,255),(850,220),15)
            pygame.draw.circle(screen,(255,0,0),(850,260),15)
            pygame.draw.circle(screen,(0,255,0),(850,300),15)
            pygame.draw.circle(screen,(255,0,255),(850,340),15)
            one = FONT.render("player 1", True, "BLACK")
            two = FONT.render("player 2", True, "BLACK")
            three = FONT.render("player 3", True, "BLACK")
            four = FONT.render("player 4", True, "BLACK")
            screen.blit(one,(870,210))
            screen.blit(two,(870,250))
            screen.blit(three,(870,290))
            screen.blit(four,(870,330))

            pos = [198,598,598,198]
            pos2 = [0,698,0,698]
            for item in range(len(pos)):
                pygame.draw.rect(screen,(0,0,0),(pos[item],pos2[item],4,102))
                pygame.draw.rect(screen,(0,0,0),(pos2[item],pos[item],102,4)) 

            pos = [148,98,648,598,698]
            pos2 = [98,148,648,698,598]
            for item in range(len(pos)):
                pygame.draw.rect(screen,(0,0,0),(pos[item],pos2[item],54,4))
                pygame.draw.rect(screen,(0,0,0),(pos[item],pos2[item],4,52))     
            
            pos = [598,98,648,148]
            pos2 = [98,648,148,698]
            for item in range(len(pos)):
                pygame.draw.rect(screen,(0,0,0),(pos[item],pos2[item],54,4))
                pygame.draw.rect(screen,(0,0,0),(pos2[item],pos[item],4,52))  

            stats = FONT.render("Stats:", True, "BLACK")
            screen.blit(stats,(875,390))

            PlayerOne = FONT.render(f"1: {self.__activeNames[0]}", True, "BLACK")
            screen.blit(PlayerOne,(845,410))
            P1CurrStats = FONT.render(f"W: {self.__names[self.__activeNames[0]].currWins} // L: {self.__names[self.__activeNames[0]].currLoss}", True, "BLACK")
            P1AllStats = FONT.render(f"W: {self.__names[self.__activeNames[0]].Wins} // L: {self.__names[self.__activeNames[0]].Loss}", True, "BLACK")
            screen.blit(P1CurrStats,(810,430))
            screen.blit(P1AllStats,(810,450))

            PlayerTwo = FONT.render(f"2: {self.__activeNames[1]}", True, "BLACK")
            screen.blit(PlayerTwo,(845,470))
            P2CurrStats = FONT.render(f"W: {self.__names[self.__activeNames[1]].currWins} // L: {self.__names[self.__activeNames[1]].currLoss}", True, "BLACK")
            P2AllStats = FONT.render(f"W: {self.__names[self.__activeNames[1]].Wins} // L: {self.__names[self.__activeNames[1]].Loss}", True, "BLACK")
            screen.blit(P2CurrStats,(810,490))
            screen.blit(P2AllStats,(810,510))

            PlayerThree = FONT.render(f"3: {self.__activeNames[2]}", True, "BLACK")
            screen.blit(PlayerThree,(845,530))
            P3CurrStats = FONT.render(f"W: {self.__names[self.__activeNames[2]].currWins} // L: {self.__names[self.__activeNames[2]].currLoss}", True, "BLACK")
            P3AllStats = FONT.render(f"W: {self.__names[self.__activeNames[2]].Wins} // L: {self.__names[self.__activeNames[2]].Loss}", True, "BLACK")
            screen.blit(P3CurrStats,(810,550))
            screen.blit(P3AllStats,(810,570))

            PlayerFour = FONT.render(f"4: {self.__activeNames[3]}", True, "BLACK")
            screen.blit(PlayerFour,(845,590))
            P4CurrStats = FONT.render(f"W: {self.__names[self.__activeNames[3]].currWins} // L: {self.__names[self.__activeNames[3]].currLoss}", True, "BLACK")
            P4AllStats = FONT.render(f"W: {self.__names[self.__activeNames[3]].Wins} // L: {self.__names[self.__activeNames[3]].Loss}", True, "BLACK")
            screen.blit(P4CurrStats,(810,610))
            screen.blit(P4AllStats,(810,630))


    def __NoAiPlay(self, players, game=False, moves=[], toMove=(), jump=False):
        if not game and players != None:
            game = Game(int(players))
        elif players == None:
            return
        pygame.init()
        pygame.font.init()
        FONT = pygame.font.Font(None, 25)
        screen = self.__boardSetup(players, game)

        if toMove != ():
            self.__GetMoves(game,toMove[0],toMove[1],screen,jump)
        
        running = True
        while running:
            self.__Sidebar(game,screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__MenuRoot.destroy()
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 970 >= mouse[0] >= 820 and 170 >= mouse[1] >= 130:
                        self.__NoAiPlay(players)
                    elif 970 >= mouse[0] >= 820 and 730 >= mouse[1] >= 690:
                        self.__DisplayRules(game,players,moves,toMove,jump)
                    elif 970 >= mouse[0] >= 820 and 780 >= mouse[1] >= 740:
                        running = False
                        pygame.quit()
                    elif 970 >= mouse[0] >= 820 and 680 >= mouse[1] >= 650:
                        self.__LoadOrSave(game)
                        self.__boardUpdate(screen, game, False)
                    else:
                        if not jump:
                            moves, toMove, jump = self.__MoveCheckandMove(mouse, game, screen, moves, toMove, False)
                        else:
                            moves, toMove, jump = self.__MoveCheckandMove(mouse, game, screen, moves, toMove, True)
                        

        pygame.quit()

    def __AiPlay(self, difficulty):
        game = Game(2)
        if difficulty == 1: ai = EasyAI()
        elif difficulty == 2: ai = MediumAI()
        elif difficulty == 3: ai = HardAI()
        pygame.init()
        pygame.font.init()
        FONT = pygame.font.Font(None, 25)
        screen = self.__boardSetup(2, game)
        
        running = True
        moves = []
        toMove = ()
        jump = False
        while running:
            self.__Sidebar(game,screen)

            count = 0
            for row in game.GetBoard():
                count += row.count(2)
            if count > 19:
                raise Exception("Duplicated piece")

            if game.GetTurn() == 2:
                move = ai.GetMove(game)
                if game.GetBoard()[move.start.y][move.start.x] == 0: raise Exception("No selected piece")
                game.aiMove(move)
                if game.EndTurn():
                    self.__Winner(game,0,difficulty)
                self.__boardUpdate(screen, game, False)

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__MenuRoot.destroy()
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 970 >= mouse[0] >= 820 and 170 >= mouse[1] >= 130:
                        self.__AiPlay(difficulty)
                    elif 970 >= mouse[0] >= 820 and 730 >= mouse[1] >= 690:
                        self.__DisplayRules()
                    elif 970 >= mouse[0] >= 820 and 780 >= mouse[1] >= 740:
                        running = False
                        pygame.quit()
                    elif 970 >= mouse[0] >= 820 and 680 >= mouse[1] >= 650:
                        self.__LoadOrSave(game)
                        self.__boardUpdate(screen, game, False)
                    else:
                        if game.GetTurn() == 1:
                            moves, toMove, jump = self.__MoveCheckandMove(mouse, game, screen, moves, toMove, jump, difficulty)
                            
                        
        pygame.quit()

    def __LoadOrSave(self, game):
        LoadOrSaveRoot = tk.Tk()
        LoadOrSaveRoot.title("Save Or Load")
        LoadOrSave = ttk.Frame(LoadOrSaveRoot, padding="5 5 12 12")
        LoadOrSave.grid(column=0, row=0, sticky=(N, E, S, W))

        LoadAndSaveTextEntry = tk.Entry(LoadOrSave, width=20)
        LoadAndSaveTextEntry.grid(column=0, row=2, sticky=(N,E,S,W))
        
        LoadButton = tk.Button(LoadOrSave, text="Load", width=20, height=2, command=lambda:[game.LoadGame(LoadAndSaveTextEntry.get()),LoadOrSaveRoot.destroy()]).grid(column=0, row=1, sticky=(N,E,S,W))
        SaveButton = tk.Button(LoadOrSave, text="Save", width=20, height=2, command=lambda:[game.SaveGame(LoadAndSaveTextEntry.get()),LoadOrSaveRoot.destroy()]).grid(column=0, row=3, sticky=(N,E,S,W))

        LoadOrSave.mainloop()


    
    def __Winner(self, game, replay, diff=0):
        winnerNum = game.GetTurn()-1
        if winnerNum == 0:
            winnerNum = game.GetPlayers()
        winnerName = self.__activeNames[winnerNum]
        
        for name in self.__activeNames:
            if name == None:
                pass
            elif name == winnerName:
                self.__names[name].currWins += 1
                self.__names[name].Wins += 1
            else:
                self.__names[name].currLoss += 1
                self.__names[name].Loss += 1

        first = True
        sorted(self.__names)
        ##################################################
        # CATAGORY B: writing to a file                  #
        # used to store/update the player stats on a win #
        ##################################################
        with open("stats.txt", "w") as f:
            for key in self.__names:
                if not first:
                    f.write("\n")
                else:
                    first = False
                f.write(f"{key}:{self.__names[key].Wins}/{self.__names[key].Loss}")
                


        WinnerTextVar = f"The Winner is player {winnerNum}!"
        EndOfGameRoot = tk.Tk()
        EndOfGameRoot.title("Game Over")
        EndOfGame = ttk.Frame(EndOfGameRoot, padding="5 5 12 12")
        EndOfGame.grid(column=0, row=0, sticky=(N, E, S, W))
        WinnerText = tk.Label(EndOfGame, text=WinnerTextVar).grid(column=0, row=0, sticky=(N,E,S,W))
        Close = tk.Button(EndOfGame, text="Close", command=lambda:[EndOfGameRoot.destroy()], width=20, height=3).grid(column=0, row=1, sticky=(N,S))
        Restart = tk.Button(EndOfGame, text="Play Again", command=lambda:[EndOfGameRoot.destroy(),self.__replayHandler(replay,diff)], width=20, height=3).grid(column=0, row=2, sticky=(N,S))
        EndOfGame.mainloop()

    def __replayHandler(self, replay, diff):
        if replay == 2: self.__NoAiPlay(2)
        elif replay == 4: self.__NoAiPlay(4) 
        elif replay == 0: self.__AiPlay(diff)


    def __DisplayRules(self,game=False,players=None, moves=[], toMove=(), jump=False):
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
        Close = tk.Button(Rules, text="Close", command=lambda:[RulesRoot.destroy(),self.__NoAiPlay(players,game,moves,toMove,jump)], width=10, height=2).grid(column=0, row=1, sticky=(N,S))
        RulesRoot.protocol("WM_DELETE_WINDOW", lambda:self.__NoAiPlay(players,game))
        Rules.mainloop() 

