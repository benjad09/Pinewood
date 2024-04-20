

def resToStr(value):
    return("*" if value is None else str(value))

def strToRes(value):
    return(None if value == "*" else int(value))

def remove0index(value):
    if type(value) == str:
        return "*" if value == "*" else str(int(value)+1)
    else:
        return value + 1
    
def add0index(value):
    if value is None:
        return None
    if type(value) == str:
        return str(int(value)-1)
    else:
        return value-1