# How to recover lost Python source code if it's still resident in-memory

I screwed up using rm and deleted the code I had just written... but it was still running. 
Here's how I got it back, using https://pypi.python.org/pypi/pyrasite/ and https://pypi.python.org/pypi/uncompyle6

## Attach a shell to the docker container

## Install GDB (needed by pyrasite)

    apt-get update && apt-get install gdb

## Install pyrasite - this will let you attach a Python shell to the still-running process

    pip install pyrasite

## Install uncompyle6, which will let you get Python source code back from in-memory code objects

    pip install uncompyle6

## Find the PID of the process that is still running

    ps aux | grep python

## Attach an interactive prompt using pyrasite

    pyrasite-shell <PID>

## Now you're in an interactive prompt! Import the code you need to recover

    >>> from my_package import my_module

## Figure out which functions and classes you need to recover

    >>> dir(my_module)
    ['MyClass', 'my_function']

## Decompile the function into source code

    >>> import uncompyle6
    >>> import sys
    >>> uncompyle6.main.uncompyle(
        2.7, my_module.my_function.func_code, sys.stdout
    )
    # uncompyle6 version 2.9.10
    # Python bytecode 2.7
    # Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
    # [GCC 5.4.0 20160609]
    # Embedded file name: /srv/my_package/my_module.py
    function_body = "appears here"

## For the class, you'll need to decompile each method in turn

    >>> uncompyle6.main.uncompyle(
        2.7, my_module.MyClass.my_method.im_func.func_code, sys.stdout
    )
    # uncompyle6 version 2.9.10
    # Python bytecode 2.7
    # Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
    # [GCC 5.4.0 20160609]
    # Embedded file name: /srv/my_package/my_module.py
    class_method_body = "appears here"
    
