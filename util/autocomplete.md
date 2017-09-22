# Python Shell Autocomplete Feature
Here are few basic steps to get bash like tab expansion into your python shell

#### Create a `~/.pythonrc` file
```bash
# ~/.pythonrc
# enable syntax completion
try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")
```

### Shell setup
Export startup file in a variable:

`export PYTHONSTARTUP=~/.pythonrc`

and put it into your `.bashrc` file or wherever you prefer to set your environment.
Now you have a working Python shell with a nice tab based syntax expansion
