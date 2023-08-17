from colorama import Fore, Style

# Color codes
COLORS = [
    Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA,
    Fore.CYAN, Fore.WHITE, Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX,
    Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX,
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX
]

# Text formatting options
BOLD = Style.BRIGHT
RESET = Style.RESET_ALL

def generate_unique_color_combinations(colors):
    combinations = [(color1, color2) for i, color1 in enumerate(colors) for j, color2 in enumerate(colors) if i != j]
    return combinations

DISTINCT_COLOR_COMBINATIONS = generate_unique_color_combinations(COLORS)
