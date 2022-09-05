## Compile
- [PSYCO Compiler](http://psyco.sourceforge.net/introduction.html)
- [Convert python code to ANSI C and compile (cpython)](https://medium.com/@xpl/protecting-python-sources-using-cython-dcd940bb188e)

## Multiprocessing / Multithreading
- [Multithreading and Multiprocessing Tutorial](https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python)

## TCP, Sockets, Select
- [multiple sockets with select()](https://steelkiwi.com/blog/working-tcp-sockets/)

## Exceptions
- https://docs.python.org/3/library/exceptions.html#exception-hierarchy  
  Builtin exception names and hierarchy

## Modules Handling
- `help("modules")` Show installed modules

## Various

- Separate functions of class into multiple files  
  https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files

- Getting list of parameter names inside python function  
  https://stackoverflow.com/questions/582056/getting-list-of-parameter-names-inside-python-function

- Writing and unit testing a Python application to query the RPM database  
  https://www.redhat.com/sysadmin/query-rpm-database-python  
    - Command line handling with _ArgumentParser_
    - Test unit with _unittest_

- Quick and short tips  
  [http://sahandsaba.com/thirty-python-language-features-and-tricks-you-may-not-know.html](http://sahandsaba.com/thirty-python-language-features-and-tricks-you-may-not-know.html)


## `python`, command not found
You obviously need to install it before (...) but if you've already did it it might be a nice idea to RTFM
```sh
man unversioned-python
# as you can see from there it might be nice to issue something like:
alternatives --set python /usr/bin/python3
# your mileage might vary
```
