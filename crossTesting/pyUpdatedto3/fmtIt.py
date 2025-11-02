def fmtIt(nm):
    """
    Formats a string, handling different cases for embedded quotes.
    Assumes `nm` is a string.
    """
    parts = nm.split(' "')
    if len(parts) == 2:
        newnm = f'<i>{parts[0]}</i> "{parts[1]}'
    elif '"' in nm:
        newnm = parts[0]
    else:
        newnm = f"<i>{nm}</i>"
    return newnm
