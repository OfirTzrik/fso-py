from utils.list_helper import favorite_blog
from test_list_helper import blogs


class TestFavoriteBlog:
	def test_favorite_empty(self):
		assert favorite_blog([]) is None

	def test_favorite_one(self):
		assert favorite_blog([blogs[0]]) == blogs[0]

	def test_favorite_all(self):
		assert favorite_blog(blogs) == blogs[2]
