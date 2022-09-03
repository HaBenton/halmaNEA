from game import Game
import sys

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
                    for item in range(len(start)):
                        start[item] = int(start[item])-1
                    for item in range(len(end)):
                        end[item] = int(end[item])-1
                    valid = True
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
        ...
    

    def run(self):
        ...
