from utils.list_helper import most_blogs
from test_list_helper import blogs


class TestMostBlogs:
	def test_most_blogs_empty(self):
		assert most_blogs([]) is None

	def test_most_blogs_one(self):
		assert most_blogs([blogs[0]]) == {"author": "Maren Holt", "blogs": 1}

	def test_most_blogs_all(self):
		assert most_blogs(blogs) == {"author": "Noor Haddad", "blogs": 3}
