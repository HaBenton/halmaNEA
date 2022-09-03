from sys import argv
from game import Game
from ui import Gui, Terminal

def usage():   
    print(f"""
Usage: {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal""")
    quit()

if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    elif argv[1] == "g":
        ui = Gui()
        ui.run()
    elif argv[1] == "t":
        ui = Terminal()
        ui.run()
    else:
        usage()