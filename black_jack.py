# Mike Hickey
# Wentworth Institute of Technology.

# Black Jack Game For AI
# This program will allow the user to play Black Jack.

# Imports
import numpy as np 
import random# The RNG used to pick cards.
from datetime import datetime # Used to seed the RNG
import os

# A card has a value and a name.
class Card:
	# Cards come from a deck, therefore a decks index, corresponds to the card.
	def __init__(self, index, value, name):
		self.index = index
		self.value = value
		self.name = name

	def read_card(self):
		return '{}'.format(self.name)

# The player can hold cards and own a specified number of cash.
class Player:
	def __init__(self, cards, num_cards, cash, bet, action_sequence):
		self.cards = cards
		self.num_cards = num_cards
		self.cash = cash
		self.bet = bet
		self.action_sequence = action_sequence

	# Apparently .append() is a destructive function. 
	# This function allows you to append to the list.
	# However, appending cards into a list doesn't require this...
	def append_action(self, action):
		self.action_sequence.append(action)
		return self.action_sequence

	def append_bet(self, user_input):
		self.bet.append(user_input)
		return self.bet


# The Dealer only can hold cards
class Dealer:
	def __init__(self, cards, num_cards):
		self.cards = cards
		self.num_cards = num_cards


class Deck:
	def __init__(self, cards, num_cards):
		self.cards = cards
		self.num_cards = num_cards



########################################################################
# This function will create a deck of cards.
def make_deck():

	# The deck is made up of cards.
	deck = Deck([], 52) # This is an empty list which will hold cards.

	# Initialize the values of the deck.
	init_card_vals(deck)
	
	# Initialize the names of the deck.
	init_card_names(deck)

	return deck


def init_card_vals(deck):
	card_value = 0
	face_counter = 0
	for i in range(deck.num_cards): 
		
		card_value += 1

		if i%13 == 10:
			# Jack
			card_value = 10
			face_counter += 1
		elif i%13 == 11:
			# Queen
			card_value = 10
			face_counter += 1
		elif i%13 == 12:
			# King
			card_value = 10
			face_counter += 1

		# Index the card, assign it a value, and a temporary name.
		card = Card(i, card_value, "TEMP NAME")
		
		# Put the card in the deck.
		deck.cards.append(card)

		# If you saw 3 face cards, that means an Ace is next.
		if face_counter == 3:
			face_counter = 0
			card_value = 0
		

def init_card_names(deck):
	# Generate a string which Humans will use to read the card.
	suit = ""
	face = ""

	for i in range(52):
		if i >= 0:
			suit = "Diamonds"
		
		if i >= 13:
			suit = "Hearts"
		
		if i >= 26:
			suit = "Spades"
		
		if i >= 39:
			suit = "Clubs"

		
		if i%13 == 0:
			face = "Ace"
		elif i%13 == 10:
			face = "Jack"
		elif i%13 == 11:
			face = "Queen"
		elif i%13 == 12:
			face = "King"
		else:
			face = str(i%13 + 1)
			
		deck.cards[i].name = face + " of " + suit

def deal_card(deck, holder, num_cards_to_deal):
	# Deal out a specified number of cards.
	for i in range(num_cards_to_deal):
		# Randomly choose cards.
		card = deck.cards[ random.randint(0, deck.num_cards-1) ]

		# Remove that card from the deck.
		deck.cards.remove(card)
		deck.num_cards -= 1

		# If there are no cards, its the first hand.
		if (holder.num_cards == None):
			holder.num_cards = 0
	
		# Add the new card to the player or dealer's hand.
		holder.cards.append(card)

	# Keep a running total of how many cards, the holder has.	
	holder.num_cards += num_cards_to_deal

	return 0

def evaluate_current_action(player1, dealer1, action):

	the_game_is_over = False

	if action == "hit" and deck.num_cards == 0:
		the_game_is_over = True

	elif action == "hit" and sum_hand(dealer1) < 17:
		# Deal two cards out.
		deal_card(deck, player1, 1)
		deal_card(deck, dealer1, 1)

	elif action == "hit" and sum_hand(dealer1) >= 17:
		# Deal one card to the player.
		deal_card(deck, player1, 1)

	elif action == "stay" and sum_hand(dealer1) < 17:
		# Deal one card to the dealer. None to the player.
		deal_card(deck, dealer1, 1)

	elif action == "stay" and sum_hand(dealer1) >= 17:
		# show hands
		the_game_is_over = True

	# End the game, and check who won.
	return the_game_is_over

def check_outcome(player1, dealer1):
	# Less specific to more specific.

	# won can be either yes, no, or tie
	outcome = "tie"

	# Did a tie occur?
	if sum_hand(player1) == sum_hand(dealer1):
		outcome = "tie"

	# Is the players hand larger than the dealers hand
	if sum_hand(player1) > sum_hand(dealer1):
		outcome = "yes"

	if sum_hand(player1) > 21 and sum_hand(dealer1) > 21:
		outcome = "tie"

	# Did the dealer have a higher score?
	if sum_hand(player1) < sum_hand(dealer1):
		outcome =  "no"

	# Did the player not bust and the dealer bust?
	if sum_hand(player1) <= 21 and sum_hand(dealer1) > 21:
		outcome = "yes"

	# Did the player bust and the dealer did not bust?
	if sum_hand(player1) > 21 and sum_hand(dealer1) <= 21:
		outcome = "no"

	# Calculate the reward. 
	return outcome

def determine_score(outcome, bet):
	# Either add or subtract the bet from the player's cash stack.
	if outcome == "yes":
		player1.cash += bet
		print("Dealer Lost! Won: " + str(bet) + "\n")

	if outcome == "no":
		player1.cash -= bet
		print("Player Lost! Lost: " + str(bet) + "\n")

	if outcome == "tie":
		# Do not add or subtract any cash from the player.
		print("Tie, no money subtracted or added.")

	return outcome


##################################################################



def print_rules():
	print("//=== Black Jack Rules ===\\\\")
	print("Ace is worth 1.")
	print("Face cards are worth 10.\n")
	print("Enter \"quit\" to quit.")
	print("Enter \"bank\" to get money from the bank.")
	print("Player's Cash: " + str(player1.cash))


def print_deck(deck):
		for i in range(deck.num_cards):
			print(deck.cards[i].name + " : " +str(deck.cards[i].value) )


def print_hand(holder):
	# Print out the names of the card in the holder's hand.
	# holder is of type Player.
	for i in range(holder.num_cards):
		print(holder.cards[i].name)
	
def sum_hand(holder):
	# Returns an integer.
	sum_hand = 0
	for i in range(holder.num_cards):
		sum_hand = sum_hand + holder.cards[i].value
	
	return sum_hand


def print_game_hands(player1, dealer1):
	print("Player's Hand: ")
	print_hand(player1)
	print("Player's Sum: " + str(sum_hand(player1)) + "\n")
	print("Dealer's Hand: ")
	print_hand(dealer1)
	print("Dealer's Sum: " + str(sum_hand(dealer1)) + "\n")

def enter_valid_option():
	print("Please enter in a valid option.\n")


def has_no_cards(holder):
	# holder is of type Player, or Dealer
	cards = False
	# If the holder has no cards, return True.
	if holder.cards == []:
		cards = True
	else:
		cards = False
	return cards


def list_card_values(holder):
	# Return a list of values for every card being held by either player or dealer.
	list_of_card_values = []

	for i in holder.num_cards:
		list_of_card_values = holder.cards[i].values

	return list_card_values


def main_menu(player1):
	# Print the Rules
	print_rules()		

	break_or_continue = ""
	bet = 0

	# Check players cash stack.
	if player1.cash <= 0:
		print("\nYou're Bankrupt. Get money from the bank.\n")

	# Ask the bank for cash, make a bet or quit the game
	player_input = input("Quit, bank, or enter an amount to bet: ")	
	print("\n")

	# If the player wants to quit the game.
	if player_input == "quit":
		print("Exiting Game, you ended with: " + str(player1.cash))
		exit()
	
	# Use this if the player is bankrupt. Add money to the cash stack.
	if player_input == "bank":
		player1.cash += 10
		break_or_continue = "continue"
		player1.append_bet(player_input)

	# If the user entered in garbage text for the prompt, say its invalid
	try:
		# Make a variable bet, so I dont need to cast.
		bet = int(player_input)
		#player1.bet = int(player_input)
		player1.append_bet(player_input)
	except ValueError:
		enter_valid_option()
		break_or_continue = "continue"

	# Check the players input for a valid bet.
	if bet > player1.cash or bet <= 0:
		enter_valid_option()
		break_or_continue = "continue"

	return break_or_continue, bet


def deal_first_2_cards(num_round):
	# For code that needs to happen after a player makes a bet and before they take an action.

	# On the first hand, player gets two cards, dealer gets two cards.
	if num_round == 1:
		# Deal two cards to the dealer.
		deal_card(deck, dealer1, 2)
		# Deal two cards to the player
		deal_card(deck, player1, 2)
		# Go to the next action, hit or stay, since the cards are delt.
		num_round += 1


	return num_round

def get_action():
	while(True):
		action = input("Take an action, type \"hit\" or \"stay\": ")
		# Check if the action is either hit or stay.
		if action == "hit" or action == "stay":
			# Exit the while loop.
			print("Action Chosen: " + action + "\n")	
			# Keep track of all the actions taken. (hit, stay)
			player1.append_action(action)
			break
	return action


def get_state(player1, dealer1, bet, outcome):
	# Used once the hands are shown.


	if outcome == "yes":
		outcome = 1
	if outcome == "no":
		outcome = 2
	if outcome == "tie":
		outcome = 3

	#state = [player1.cash, player1.bet, sum_hand(player1), sum_hand(dealer1), player1.action_sequence, outcome]
	state = [player1.cash, bet, sum_hand(player1), sum_hand(dealer1), outcome]

	print(state)
	return state

def build_dataset(dataset, state):
	dataset.append(state)
	return dataset

def save_dateset(dataset):
	# Save the dataset to a *.csv
	np_dataset = np.asarray(dataset)
	np.savetxt("black_jack_dataset.csv", np_dataset, delimiter = ",")
	return 0

def rng_agent_bet(player1):
	# This is not a real AI.
	# This is a random number generator that will be used to make a data set.
	# Starting player1.cash = 500

	# Place Bet
	player1.bet = random.randint(0, int((player1.cash-1)/1000) )

	print("RNG BET: " + str(player1.bet) )
	return player1.bet

def rng_agent_action(player1):
	# This is not a real AI.
	# This is a random number generator that will be used to make a data set.

	# Chose action
	# 0 = hit, 1 = stay
	if random.randint(0, 1):
		rng_action = "hit"
	else:
		rng_action = "stay"

	print("RNG ACTION : " + str(rng_action) )
	return rng_action


def is_player_human():
	print("Is the player Human or an AI?")
	answer = None
	human_or_ai = input("Type \"human\" or \"ai\": ")
	if human_or_ai == "human":
		answer = True
	if human_or_ai == "ai":
		answer = False
	return answer


# Play the game Black Jack
if __name__ == "__main__":
	try:
		# Clear the screen upon script start
		os.system("cls" if os.name == "nt" else "clear") 

		# Seed the random number generator.
		random.seed(datetime.now())

		# Create the deck of cards.
		deck = make_deck()

		# Make an empty dataset to store all the states.
		dataset = []

		# Instantiate the Player.   
		#def __init__(self, cards, num_cards, cash, bet, action_sequence):
		initial_cash = 50000
		player1 = Player([], None, initial_cash, [], [] )

		# Instantiate the Dealer.
		dealer1 = Dealer([], None)

		a_human_is_playing = is_player_human()

		num_games = 1600
		for k in range(num_games):
			# Main Menu
			if a_human_is_playing:
				# Ask the human if they want to make a bet or bank or quit.
				break_or_continue, bet = main_menu(player1)
				if break_or_continue == "break":
					break
				if break_or_continue == "continue":
					continue
			else:
				# RNG DATASET BUILDER
				bet = rng_agent_bet(player1)


			###################################################################

			# While the game is playing, you want to either hit or stay.
			num_round = 1 # Counter for the first round.
			action = ""
			while True:
				# On the first hand; player gets two cards, dealer gets two cards.
				num_round = deal_first_2_cards(num_round)

				if a_human_is_playing:
					# Print out the current hands held by both players.	For Humans... 				
					print_game_hands(player1, dealer1)
					# Perform an action, Hit or Stay.
					action = get_action()
				else:
					action = rng_agent_action(player1)

				the_game_is_over = evaluate_current_action(player1, dealer1, action)

				if the_game_is_over:
					# Print out the current hands held by both players.	 
					
					if a_human_is_playing:
						print_game_hands(player1, dealer1)
					# Who won? Add cash or subtract cash.
					outcome = determine_score( check_outcome(player1, dealer1), bet )
					# Get the state of the game and send it to the AI.
					state = get_state(player1, dealer1, bet, outcome)
					print(state)
					# Put the state into a dataset.
					dataset = build_dataset(dataset, state)
					# Save the dataset to a *.csv to the local project's directory
					save_dateset(dataset)
					# Since the game is over, collect cards and deal new cards.
					break

			###################################################################

			# Game is over, reset the cards.
			player1.cards = []
			dealer1.cards = []

			player1.num_cards = 0
			dealer1.num_cards = 0

			# Rebuild the deck.
			deck = make_deck()

			# Reset the player's bets and actions
			player1.bet = []
			player1.action_sequence = []

	except KeyboardInterrupt:
		print("\nThanks for playing.")
		exit()



		



	




