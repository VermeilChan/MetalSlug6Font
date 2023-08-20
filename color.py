from colorama import Fore
from itertools import combinations

# Available color codes
COLORS = list(vars(Fore).values())

# Generate distinct color combinations
DISTINCT_COLOR_COMBINATIONS = list(combinations(COLORS, 2))
