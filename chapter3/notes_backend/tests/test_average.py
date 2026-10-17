from utils.for_testing import average


class TestAverage:
	def test_of_one_value_is_the_value_itself(self):
		assert average([1]) == 1

	def test_of_many_is_calculated_right(self):
		assert average([1, 2, 3, 4, 5, 6]) == 3.5

	def test_of_empty_list_is_zero(self):
		assert average([]) == 0
