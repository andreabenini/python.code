### While interactive on console...
You can import a module to test its functions or classes, if you're modifying it and you wish to evaluate newly
applied code you may simply reload the file,  just like this:

#### Python3
```python
>>> import MyFunctions
>>> ...
>>> import imp
>>> imp.reload(MyFunctions)
>>> ...
```
