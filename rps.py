import pytest
import random

if False:
	human = input ('Rock, paper or scissors?')

	while human not in ['rock','paper','scissors']:
		human = input ('Rock, paper or scissors?')

	computer = random.choice(['rock','paper','scissors'])

	print(computer)

	if human == computer:
		print ('it\'s a tie!')
	elif human+computer in 'rockpaperscissors':
		print('computer wins')
	else:
		print('human wins')



#dalsi kod na testovani
def random_play():
	return random.choice(['rock','paper','scissors'])



#dalsi kod
def determine_game_result(human, computer):
	#Returns str human
	if human == computer:
		return 'tie'
	elif human+computer in 'rockpaperscissors':
		return 'computer'
	else:
		return 'human'

# dalsi kod, stejny jako prvni ale vylepseny
def is_valid_play(play):
	return play in ['rock','paper','scissors']

def main(input=input): #nebo input_func = input
	human = ''
	while not is_valid_play(human):
		human = input ('Rock, paper or scissors?')#nebo misto input input_func(....), protoze prvni input je jen nazev argumentu

	computer = random_play()

	print(computer)

	result = determine_game_result(human,computer)
	if result == 'tie':
		print ('it\'s a tie!')
	else:
		print (result, 'wins')
#spusteni funkce, main card
if __name__ == '__main__':
	main()
