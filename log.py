from colorama import init
init()

class text_colors:
    HEADER = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    RESET = "\033[0m"
    UNDERLINE = "\033[4m"

def info(*arg):
    print(text_colors.CYAN,join_args(arg),text_colors.RESET, sep="")

def error(*arg):
    print(text_colors.FAIL,join_args(arg),text_colors.RESET, sep="")

def warn(*arg):
    print(text_colors.WARNING,join_args(arg),text_colors.RESET, sep="")

def success(*arg):
    print(text_colors.GREEN,join_args(arg),text_colors.RESET, sep="")

def join_args(*arg,sep:str=" "):
    arg = arg[0]
    if len(arg) == 0:
        return ""
    if len(arg) == 1:
        return str(arg[0])
    i = 0
    s = ""
    while i < len(arg):
        s += str(arg[i])
        if i != len(arg) - 1:
            s += sep
        i+=1
    return s