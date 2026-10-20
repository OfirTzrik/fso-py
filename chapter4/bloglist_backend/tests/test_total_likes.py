from utils.list_helper import total_likes
from test_list_helper import blogs


class TestTotalLikes:
	def test_total_empty(self):
		assert total_likes([]) == 0

	def test_total_one(self):
		assert total_likes([blogs[2]]) == 12

	def test_total_all(self):
		assert total_likes(blogs) == 36
