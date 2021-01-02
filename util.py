''' utility functions '''

def q_split (s):
    ''' split a string at spaces, ignoring quoted sections '''
    split = []
    keyword = ''
    quote_ = escape_ = False

    c = 0
    while c < len(s):
        if s[c] == '\\':
            if not escape_:
                escape_ = True
                c += 1
                continue

        elif (s[c] == '"' or s[c] == "'") and (not escape_):
            if quote_:
                quote_ = False
            else:
                quote_ = True

        elif s[c] == ' ' and (not quote_) and (not escape_):
            split += [keyword]
            keyword = ''
            c += 1
            continue

        elif escape_:
            keyword += '\\'

        keyword += s[c]
        c += 1
        if escape_:
            escape_ = False

    if len(keyword):
        split += [keyword]

    return split

