from collections import Counter


def dummy(blogs: list[dict]) -> int:
	return 1


def total_likes(blogs: list[dict]) -> int:
	return sum([blog["likes"] for blog in blogs], 0)


def favorite_blog(blogs: list[dict]) -> dict | None:
	if len(blogs) == 0:
		return None
	return max(blogs, key=lambda blog: blog["likes"])


def most_blogs(blogs: list[dict]) -> dict | None:
	if len(blogs) == 0:
		return None

	counts = Counter(blog["author"] for blog in blogs)
	author, count = counts.most_common(1)[0]
	return {"author": author, "blogs": count}


def most_likes(blogs: list[dict]) -> dict | None:
	if len(blogs) == 0:
		return None

	counts = Counter()
	for blog in blogs:
		counts[blog["author"]] += blog["likes"]

	author, likes = counts.most_common(1)[0]
	return {"author": author, "likes": likes}
