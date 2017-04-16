import copy
import random
import os
import time

##### CONSTANTS #####
BOARD_SIZE = 10		#Currently only supports 10 :(
####################

#Splash screen to greet user and quickly explain rules
def splash_screen():
	with open("splash_screen.txt") as text:
		print text.read()

#Prompt user to place their ships + give orientation.
def user_place_ships(game_board, ships_to_place):
	for ship in ships_to_place:
		#Clear screen so the terminal window doesn't get obnoxious
		os.system('cls' if os.name == 'nt' else 'clear')
		#Prompt user for coordinates
		valid = False
		while(not valid):
			print_board("player", game_board)
			print "Currently placing the " + ship.name + ", size = " + str(ship.size) + " units"
			x, y = get_coordinates()
			orientation = get_orientation()
			valid = validate(game_board, ship, x, y, orientation)
			if not valid:
				print "\n\nINVALID LOCATION (off the board or coliding with another ship)\nPlease try again.\n\n"

		#Place the ship
		game_board = place_ship(game_board, ship, ship.short_name, orientation, x, y)

	raw_input("All ships placed. Press ENTER to start the game!")
	return game_board

#Computer places random ships at the start
def computer_place_ships(game_board, ships_to_place):
	for ship in ships_to_place:
		os.system('cls' if os.name == 'nt' else 'clear')
		valid = False
		while(not valid):
			x = random.randint(1,BOARD_SIZE-1)
			y = random.randint(1,BOARD_SIZE-1)
			if random.randint(0,1) == 0:
				orientation = "v"
			else:
				orientation = "h"
			valid = validate(game_board, ship, x, y, orientation)

		#Place the ship
		game_board = place_ship(game_board, ship, ship.short_name, orientation, x, y)


	return game_board

#Place a ship. Location has laready been validated at this point
def place_ship(game_board, ship, short_name, orientation, x, y):
	print short_name
	if orientation == "v":
		for i in range(ship.size):
			game_board[x + i][y] = short_name
			ship.loc.append({x+i, y})
	elif orientation == "h":
		for i in range(ship.size):
			game_board[x][y + i] = short_name
			ship.loc.append({x, y+i})

	return game_board

#Validate if the ship placement location is valid
def validate(game_board, ship, x, y, orientation):
	if orientation == "v" and ship.size + x > 10:
		return False
	elif orientation == "h" and ship.size + y > 10:
		return False
	else:
		if orientation == "v":
			for i in range(ship.size):
				if game_board[x + i][y] != -1:
					return False
		elif orientation == "h":
			for i in range(ship.size):
				if game_board[x][y + i] != -1:
					return False

	return True

#Prompt user for input for ship orientation
def get_orientation():
	while(True):
		user_input = raw_input('Place ship vertically ("v") or horizontally ("h")')
		if user_input == "v" or user_input == "h":
			return user_input
		else:
			print "Invalid input. Please only enter v or h"

#Prompt user for input for ship/gun coordinates
def get_coordinates():
	while (True):
		user_input = raw_input("Enter your coordinates (row, col): ")

		try:
			#Sanitize input before validating
			user_input.strip()
			coord = user_input.split(",")
			coord[1] = coord[1].replace(" ", "")

			if len(coord) != 2:
				raise Exception("Invalid entry, too few/many coordinates.");

			#Convert letter coordinate into int for ease of use
			coord[1] = coord[1].upper()
			coord[1] = ord(coord[1]) - 64

			#Check that 2 values are integers
			coord[0] = int(coord[0])-1
			coord[1] = int(coord[1])-1

			#Check that integers are within bounds
			if coord[0] < 0 or coord[0] > 9 or coord[1] < 0 or coord[1] > 9:
				raise Exception("Coordinates need to be between 1-10/A-J")

			return coord
		#Catch any input exceptions
		except ValueError:
			print "Invalid entry. Please enter only numeric values for coordinates"
		except Exception as e:
			print e

#Process the players move
def user_move(game_board):
	while(True):
		x, y = get_coordinates()
		move = make_move(game_board, x, y)
		if move == "hit":
			print str(x + 1) + "," + chr(64 + y + 1) + " is a HIT!"
			check_hit(game_board, x, y)
			game_board[x][y] = 'X'
			if check_win(game_board):
				return "WIN"
		elif move == "miss":
			print str(x + 1) + "," + chr(64 + y + 1) + " is a miss"
			game_board[x][y] = "*"
		elif move == "try again":
			print "Sorry, that coordinate was already hit. Please try again"

		if move != "try again":
			return game_board

#Process the computers move
def computer_move(game_board):
	print "Computer is thinking..."
	time.sleep(2)	#The future of A.I.

	while(True):
		x = random.randint(1,10)-1
		y = random.randint(1,10)-1
		move = make_move(game_board, x, y)
		if move == "hit":
			print str(x + 1) + "," + chr(64 + y + 1) + " is a HIT!"
			check_hit(game_board, x, y)
			game_board[x][y] = 'X'
			if check_win(game_board):
				return "WIN"
		elif move == "miss":
			print str(x + 1) + "," + chr(64 + y + 1) + " is a miss"
			game_board[x][y] = "*"

		if move != "try again":
			return game_board

#Make a move
def make_move(game_board, x, y):
	if game_board[x][y] == -1:
		return "miss"
	elif game_board[x][y] == '*' or game_board[x][y] == '$':
		return "try again"
	else:
		return "hit"

#Iterate over entire game board and check if any tile is left
def check_win(game_board):
	for i in range(10):
		for j in range(10):
			if game_board[i][j] != -1 and game_board[i][j] != '*' and game_board[i][j] != '$':
				return False
	return True

#Print game board to the screen
def print_board(current_player, game_board):
	if current_player == "player":
		print "Your board\n"
	else:
		print "Opponent board\n"

	print " ",
	for i in range(BOARD_SIZE):
		print "  " + chr(64 + i + 1) + "  ",
	print "\n"

	for i in range(BOARD_SIZE):
		if i == 0:
			print "   " + "-" * 58
		if i != BOARD_SIZE-1:
			print str(i + 1) + "  ",
		else:
			print str(i + 1) + " ",

		for j in range(BOARD_SIZE):
			if game_board[i][j] == -1:
				print ' ',
			elif current_player == "player":
				print game_board[i][j],
			else:
				if game_board[i][j] == "*" or game_board[i][j] == "$":
					print game_board[i][j],
				else:
					print " ",

			if j != BOARD_SIZE-1:
				print " | ",
		print " "
		print "   " + "-" * 58

#Create a list of ships for the user/computer to place
def ship_generator():
	CV = Carrier()
	BB = Battleship()
	SS = Submarine()
	DD = Destroyer()
	PT = PTBoat()

	return [CV, BB, SS, DD, PT]

def main():
	splash_screen()
	raw_input("\n\nPress ENTER to start!")

	#Generate ships for each player
	player_ships = ship_generator()
	opp_ships = ship_generator()

	#Initialize game board
	game_board = [[-1 for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

	#Perform a deep copy to cleanly recreate the game boards for each player
	player_board = copy.deepcopy(game_board)
	opp_board = copy.deepcopy(game_board)

	#Enter place ships phase
	player_board = user_place_ships(player_board, player_ships)
	opp_board = computer_place_ships(opp_board, opp_ships)

	#Main game loop
	while(True):
		#Clear the window at the start of each turn
		os.system('cls' if os.name == 'nt' else 'clear')

		print_board("c",opp_board)
		opp_board = user_move(opp_board)

		#Check win condition if there are no allive oppoent ships
		win_flag = True
		for ship in opp_ships:
			if ship.alive:
				win_flag = False

		if win_flag:
			print "You won!"
			quit()

		#Check loss condition if you have no alive ships left
		loss_flag = True
		for ship in player_ships:
			if ship.alive:
				loss_flag = False

		if loss_flag:
			print "You lost!"
			quit()

		print_board("c",opp_board)

		player_board = computer_move(player_board)

		if player_board == "WIN":
			print "You lost"
			quit()

		print_board("u",player_board)
		raw_input("To end turn, hit ENTER")

#Parent class for all ships
class Ship():
	name = "Ship"
	size = 0	#PT Boat = 2, Destroyer = 3, Submarine = 3, Battleship = 4, Carrier = 5
	short_name = ""
	hits = []
	loc = []
	alive = True

class PTBoat(Ship):
    def __init__(self):
        self.name="PT Boat"
        self.short_name = "P"
        self.size=2
        self.hits=[0,0]

class Destroyer(Ship):
    def __init__(self):
    	self.name="Destroyer"
        self.short_name = "D"
        self.size=3
        self.hits=[0,0,0]

class Submarine(Ship):
    def __init__(self):
        self.name="Submarine"
        self.short_name = "S"
        self.size=3
        self.hits=[0,0,0]

class Battleship(Ship):
    def __init__(self):
        self.name="Battleship"
        self.short_name = "B"
        self.size=4
        self.hits=[0,0,0,0]

class Carrier(Ship):
    def __init__(self):
        self.name="Aircraft Carrier"
        self.short_name = "C"
        self.size=5
        self.hits=[0,0,0,0,0]

if __name__=="__main__":
	main()
