def reverse(text: str) -> str:
	return text[::-1]


def average(numbers: list[float]) -> float:
	if len(numbers) == 0:
		return 0
	return sum(numbers) / len(numbers)
