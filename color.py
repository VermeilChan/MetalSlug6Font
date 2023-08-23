from colorama import Fore
from itertools import combinations

# Available color codes excluding black
COLORS = [color_code for color_name, color_code in vars(Fore).items() if color_name != 'BLACK']

# Generate distinct color combinations
DISTINCT_COLOR_COMBINATIONS = list(combinations(COLORS, 2))
