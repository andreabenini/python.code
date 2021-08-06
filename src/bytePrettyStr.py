# bytes to pretty format string
def bytePrettyStr(num):
    for unit in ['','Kb','Mb','Gb','Tb','Pb','Eb','Zb']:
        if abs(num) < 1024.0:
            return "{:3.1f} {}".format(num, unit)
        num /= 1024.0
    return "{:.1f} {}".format(num, 'Yb')
