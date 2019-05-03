# Tips
## Error while cythonizing `print("string",end="")` type of statement
Even if you've correctly specified and used a python3 interpreter in order to cythonize your scripts you've 
seen this kind of error. You might get out of it just by adding this line to your python file:
```python
#cython: language_level=3, boundscheck=False
```
This strictly sets the python3 interpreter, seems that cython still uses python2 syntax on `print()` by default.
Add this line at the beginning of your file (as you normally do with linter like directives)
