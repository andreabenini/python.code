import readline

# Print shell command line history
def History():
    for i in range(readline.get_current_history_length()):
        print(readline.get_history_item(i + 1))
