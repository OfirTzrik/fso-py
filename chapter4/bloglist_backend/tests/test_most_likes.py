from utils.list_helper import most_likes
from test_list_helper import blogs


class TestMostLikes:
	def test_most_likes_empty(self):
		assert most_likes([]) is None

	def test_most_likes_one(self):
		assert most_likes([blogs[0]]) == {"author": "Maren Holt", "likes": 7}

	def test_most_likes_all(self):
		assert most_likes(blogs) == {"author": "Idris Okafor", "likes": 17}
