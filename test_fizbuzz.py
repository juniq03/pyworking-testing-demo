from fb import fizzbuzz

def test_fizbuzz_returns_str():
	assert isinstance (fizzbuzz(1), str)

#dalsi test
def test_fizbuzz_1_returns_1():
	assert fizzbuzz(1) == '1'