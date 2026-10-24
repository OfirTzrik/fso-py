"""pytest searches for a file called conftest.py where all test setup
is stored and all test files share, this makes it so this is the first
file that gets loaded so there is no risk of working with the real
database"""

import os

from dotenv import load_dotenv

# Loads both DATABASE_URL and TEST_DATABASE_URL
load_dotenv()

# Replace the Neon URL with the test database URL
# load_dotenv() in database.py can't change it back to the original
# DATABASE_URL which uses the real database URL because it doesn't
# replace a variable that's already set.
#
# If TEST_DATABASE_URL is missing we get a KeyError which means tests
# can't fall back to using Neon.
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
