
## For..loop backwards on a dictionary
```
mydict = {'40': 350, '50': 500, '70': 700}
for key, value in sorted(list(mydict.items()), key=lambda x:x[0].lower(), reverse=True):
    print("{} = {}".format(key, value))
```
