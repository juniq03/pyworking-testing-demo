from fb import fizzbuzz
import pytest

def test_fizzbuzz_returns_str():
	assert isinstance (fizzbuzz(1), str)

#dalsi test
@pytest.mark.parametrize('num',[1, 2, 4, 7, 8, 11, 13, 14])
def test_fizzbuzz_regular_returns_self(num):
	assert fizzbuzz(num) == str(num)

@pytest.mark.parametrize('num',[3,6,9, 12])
def test_fizzbuzz_3div_returns_fizz(num):
	assert fizzbuzz(num) == 'fizz'

@pytest.mark.parametrize('num',[5, 10, 8885])
def test_fizzbuzz_5div_returns_buzz(num):
	assert fizzbuzz(num) == 'buzz'

@pytest.mark.parametrize('num',[15, 15000015])
def test_fizzbuzz_5div_returns_buzz(num):
	assert fizzbuzz(num) == 'fizzbuzz'