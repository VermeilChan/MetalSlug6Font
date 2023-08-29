from colorama import Fore
from itertools import combinations

COLORS = [color_code for color_name, color_code in vars(Fore).items() if color_name != 'BLACK']

DISTINCT_COLOR_COMBINATIONS = list(combinations(COLORS, 2))
