from utils.list_helper import dummy

blogs = [
	{
		"title": "Patterns for state",
		"author": "Maren Holt",
		"url": "https://example.com/state",
		"likes": 7,
	},
	{
		"title": "Why GOTO hurts",
		"author": "Idris Okafor",
		"url": "https://example.com/goto",
		"likes": 5,
	},
	{
		"title": "Shrinking strings",
		"author": "Idris Okafor",
		"url": "https://example.com/strings",
		"likes": 12,
	},
	{
		"title": "First-class tests",
		"author": "Noor Haddad",
		"url": "https://example.com/tests",
		"likes": 10,
	},
	{
		"title": "Does TDD hurt design?",
		"author": "Noor Haddad",
		"url": "https://example.com/tdd",
		"likes": 0,
	},
	{"title": "Type wars", "author": "Noor Haddad", "url": "https://example.com/types", "likes": 2},
]


def test_dummy_returns_one():
	blogs = []
	assert dummy(blogs) == 1
