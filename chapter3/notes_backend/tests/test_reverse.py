from utils.for_testing import reverse


def test_reverse_of_a():
	assert reverse("a") == "a"


def test_reverse_of_react():
	assert reverse("react") == "tcaer"


def test_reverse_of_saippuakauppias():
	assert reverse("saippuakauppias") == "saippuakauppias"
