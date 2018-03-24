#def fizzbuzz(number):
#	return str()
#def fizzbuzz(number):
#	return str(number)

"""
def fizzbuzz(number):
	if number % 15 == 0: #15 davam jako prvni, aby to nejdriv zkontrolovalo 
		return 'fizzbuzz'
	if number % 3 == 0:
		return 'fizz'
	if number % 5 == 0:
		return 'buzz'
	return str(number)
"""

# lepsi zpusob s prazdnymm rezetcem
def fizzbuzz(number):
	ret = ''
	if number % 3 == 0:
		ret+= 'fizz'
	if number % 5 == 0:
		ret+= 'buzz'
	return ret or str(number)