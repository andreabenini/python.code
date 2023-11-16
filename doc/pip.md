# pip3 installation on RHEL or CentOS OSes
Install python setup tools first
```
/ # rpm -qa |grep setuptools
python34-setuptools-19.2-3.el7.noarch
```
Now install pip with setup tools:
```
/ # easy_install-3.4 pip
Searching for pip
Best match: pip 10.0.1
Processing pip-10.0.1-py3.4.egg
pip 10.0.1 is already the active version in easy-install.pth
Installing pip3 script to /usr/bin
Installing pip3.4 script to /usr/bin
Installing pip script to /usr/bin

Using /usr/lib/python3.4/site-packages/pip-10.0.1-py3.4.egg
Processing dependencies for pip
Finished processing dependencies for pip
```

**NOTE:**

EPEL Repository must be enabled for these operations

# pip3 install cryptography
To use and install cryptography module you must have these installed
```
openssl
libffi | ffi
libffi-devel (if any)
```
When you're still having problems inside your virtual env you might use this hack:
```
source bin/activate
pip install --upgrade pip
pip install wheel
pip install cffi
pip install cryptography
```
Tested on Linux Arch (arm on RPi)

# pip install packages from other sources
github or similar git repo (https)
```sh
#   cmd     git |---        Repository base URL         ---| branch
pip install git+https://github.com/jay-g-mehta/pydhcpdparser@master
```
Local drive install
```
pip install ~/my/path/to/project/
```

# pip clear environment
**NOTE:** Don't do this unless you know what you are doing.  
To clear/uninstall all pip packages in a VirtualEnvironment you can basically use the freeze+xargs magic combo, like:
```sh
pip freeze | xargs pip uninstall -y
```


---


# Troubleshooting
## `ModuleNotFoundError: No module named 'pip'` error
The Python _"ModuleNotFoundError: No module named 'pip'"_ occurs when pip is not 
installed in our Python environment. You can surely install it through your
favorite package manager, `python-pip` is what you are looking for.  

But if you still see a message like this one:
```
$ pip
Traceback (most recent call last):
  File "./env/bin/pip", line 5, in <module>
    from pip._internal.cli.main import main
ModuleNotFoundError: No module named 'pip'
```
and `python-pip` is installed the error might be related to an upgrade or a
virtual environment massive change, you can surely fix wrongly referred python
modules with this command:
```
$ python -m ensurepip --upgrade
Looking in links: /tmp/tmpbwved7yk
Processing /tmp/tmpbwved7yk/setuptools-xx.x.x-pyx-none-any.whl
Processing /tmp/tmpbwved7yk/pip-xx.x.x-pyx-none-any.whl
Installing collected packages: setuptools, pip
Successfully installed pip-xx.x.x setuptools-xx.x.x
```
now pip list finally works:
```
$ pip list
Package    Version
---------- -------
pip        xx.x.x
setuptools xx.x.x
```

---
