
def getOrdinal(N :int) -> str:
    tens = N%100
    if tens in [11,12,13]:
        return "th"
    ones = N%10
    if ones == 1:
        return "st"
    elif ones == 2:
        return "nd"
    elif ones == 3:
        return "rd"
    elif ones == 4:
        return "th"
    else:
        return "th"