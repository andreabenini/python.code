import readline

# Print shell command line history
def History():
    for i in range(readline.get_current_history_length()):
        print("%3d %s" % (i+1, readline.get_history_item(i + 1)))
