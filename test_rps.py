import rps
import subprocess #umoznuje spoustet podprocesy
import sys #spoustet aktualni python
import pytest


def test_rock_is_valid_play():
	assert rps.is_valid_play('rock') is True

def test_paper_is_valid_play():
	assert rps.is_valid_play('paper') is True

def test_scissors_is_valid_play():
	assert rps.is_valid_play('scissors') is True

def test_lizard_is_invalid_play():
	assert rps.is_valid_play('lizard') is False
#	assert is_valid_play('lizard') == True

#test 2.kodu
def random_play_is_valid():
	play = rps.random_play()
	assert is_valid_play(play)
#stokrat
def random_play_is_valid_100x():
	for _ in range (100):
		play2 = rps.random_play()
		assert is_valid_play(play)

#dalsi kod, 1k random her
def test_random_play_is_fairish():
	# list comprehension; for něco tam append randomplay
	plays = [rps.random_play() for _ in range (1000)]
	# v tisicich hrach, pocitam, ze najdu alespon 100 rock/paper/scissors
	assert plays.count('rock') > 100
	assert plays.count('paper') > 100
	assert plays.count('scissors') > 100

#dalsi kod
def test_paper_beats_rock():
	assert rps.determine_game_result ('paper','rock') == 'human'

#dvojite vraceni, tzv. closure
def input_fake_rock(fake):
	def input_fake_(prompt):
		print (prompt)
		return fake
	return input_fake_


#dekorator, muj play je argument, ktery znamena rock, paper, scissors
@pytest.mark.parametrize ('play', ['rock','paper','scissors'])
#test na celou hru
def test_whole_game(capsys, play):
	#monkeypatch.setattr ('builtins.input', input_fake_rock)
	rps.main(input=input_fake_rock(play))
	out, err = capsys.readouterr()
	print(out)
	assert 'Rock, paper or scissors?' in out
	assert ('computer wins' in out or 
			'human wins' in out or
			'it\'s a tie' in out)

#subprocess
def test_game_asks_again_if_wrong_input():
	cp = subprocess.run([sys.executable,'rps.py'], #sys.executable spousti aktualni jazyk, misto toho by slo 'python'						input='asdf\nrock', #Do rps uzivatel narve bordel (špatnej input), tak se ho to zepta znova a pak da rock , stdout je abzchom si mohli precist vystup
						encoding = 'utf-8',
						stdout=subprocess.PIPE)
	assert cp.stdout.count('Rock, paper or scissors?') == 2