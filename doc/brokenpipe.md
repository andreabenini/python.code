# BrokenPipeError management
When you deal with a huge scripts managing a lot of output it's quite common, usually you start adding pipes `|` to it in order to filter (grep), substitute (sed) or carefully see output later (less|more).  
Things like:
```sh
yourHugeOutputScript.py | less
```
But it's also common to receive errors back when the pipe is ababruptly terminated (type `q` to end less for example),
and usually python interpreter generates some weird error like:
```txt
...
  File "/home/ben/your.program.py", line 62, in yourFunction
    print(line)
...
BrokenPipeError: [Errno 32] Broken pipe
```
and a **BrokenPipeError** is raised. This can be solved in different ways:

- ### Properly dealing with system Signals  
    This snipped might solve that:
    ```python
    # Avoid: '[Errno 32] Broken pipe' error when appending stream to something else (example: '| less')
    from signal import signal, SIGPIPE, SIG_DFL   
    signal(SIGPIPE, SIG_DFL) 
    ```
    It's quite generic and less intrusive, basically it let uses the signal default handler **(SIG_DFL)**
    when needed. That's because Python does not deal with it directly unless told so.
- ### Dealing pipe errors in the code itself
    This is tailored to a specific chunk of code when you already know you're generating a lot of output.  
    This handles pipe errors exactly where the huge output generation is. **EPIPE** errors might be handled there
    ```python
    import sys 
    import errno 

    try: 
        for i in range(10000):
            print(i)
    except IOError as e:
        if e.errno == errno.EPIPE:
            pass        # Handling of the error
    ```
