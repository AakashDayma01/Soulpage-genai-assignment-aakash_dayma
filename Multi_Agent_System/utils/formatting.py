import re

def bold(text): 
    return f"\033[1m{text}\033[0m"
def heading(text): 
    return f"\033[1m\033[95m{text}\033[0m"
def subheading(text): 
    return f"\033[1m\033[94m{text}\033[0m"
def bullet(text): 
    return f"  • {text}"
def numbered(idx, text): 
    return f"  {idx}. {text}"

def human_readable_number(num):
    try:
        num = float(num)
        if num >= 1_000_000_000_000: 
            return f"{num/1_000_000_000_000:.2f}T"
        elif num >= 1_000_000_000: 
            return f"{num/1_000_000_000:.2f}B"
        elif num >= 1_000_000: 
            return f"{num/1_000_000:.2f}M"
        elif num >= 1_000: 
            return f"{num/1_000:.2f}K"
        else: 
            return str(num)
    except: 
        return str(num)

def markdown_to_console_bold(line: str) -> str:
    return re.sub(r"\*\*(.*?)\*\*", lambda m: bold(m.group(1)), line)