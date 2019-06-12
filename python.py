def format_duration(seconds):
    origin = seconds
    dic = {
        'D': 60 * 60 * 24,
        'Hour': 60 * 60,
        'Min': 60,
        'Sec': 1
    }
    spent = {'D':"0 Day ", 
            'Hour':'00:', 
            'Min':"00:", 
            'Sec':"00"
            }
    ans = ""
    for x in ['D', 'Hour', 'Min', 'Sec']:
        tmp = seconds // dic[x]
        if tmp:
            if x == 'D':
                spent[x] = str(tmp) + " day "
            elif x == 'Hour' or x == 'Min':
                if tmp < 10:
                    spent[x] = "0" + str(tmp) + ":"
                else:
                    spent[x] = str(tmp) + ":"
            else:
                if tmp < 10:
                    spent[x] = "0" + str(tmp)
                else:
                    spent[x] = str(tmp)
        seconds %= dic[x]
        ans += spent[x]
    return  ans