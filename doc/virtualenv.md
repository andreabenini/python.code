# virtualenv installation
Virtualenv is a tool to create isolated Python environments. Virtualenv creates a folder which contains
all the necessary executables to use the packages that a Python project would need.
### Installation
```
pip3 install virtualenv
# pip install virtualenv
```
### Test
```
virtualenv --version
```
### Creation
Create a virtual environment for a project
```
virtualenv projectFolder
# Basically the same of:
#    - mkdir projectFolder
#    - cd projectFolder
#    - virtualenv .
```
**python3 creation (from official doc)**, that's the suggested creation command for python3
```
python3 -m venv projectFolder
```
You can also use the Python interpreter of your choice (like python2.7)
```
virtualenv -p /usr/bin/python2.7 projectFolder
```
### Activation
To begin using the virtual environment, it needs to be activated
```
source projectFolder/bin/activate
```
### Deactivation
```
deactivate
```

### Upgrade
```sh
python -m venv --upgrade [virtualEnvDirectory]
```

### Execute an python script in a virtualenv
You basically need to activate the environment, execute the script and deactivate the environment at the end.
There're these options available:
- Create an alias to specified dir and execute that interactively:  
  `alias activate=". projectFolder/bin/activate"`
- Create a script (_sampleScript.sh_) with `source ./projectFolder/bin/activate` and place your python execution there
```sh
#!/usr/bin/env bash
# sampleScript.sh
source ./projectFolder/bin/activate
./projectFolder/yourPythonScriptHere.py
```
- Execute your _activate_ script from shell but with some env export, just like:
```sh
. ./projectFolder/script.sh
```
the leading `.` **is important**.


# Troubleshooting
## No module named 'pip'
When you upgrade system wide python environment you may have troubles inside your virtualenv installation, you can still enter it but sometimes
you may face something like:
```sh
(myvirtualenv) ~ $ pip
Traceback (most recent call last):
  File "/my/env/home/bin/pip3", line 5, in <module>
    from pip._internal.cli.main import main
ModuleNotFoundError: No module named 'pip'
```
and even classic upgrade won't solve it
```sh
(myvirtualenv) ~ $ python -m pip install --upgrade pip
/my/env/home/bin/python: No module named pip
```
### **Solution [1]**:
- `deactivate` virtual env
- remove (_or rename_) pyvenv.cfg file inside your virtual env, if any
- `source <yourenv>/bin/activate` to enter it again
- `python -m pip install --upgrade pip` again to solve the venv environment
...now it's time to upgrade remaining packages in your VirtualEnv
### **Solution [2]**:
`python3 -m venv --upgrade <venvDir>`
This _might_ wipe your installed packages or internal environment do **NOT**
use it unless you're sure of what you're doing
### **Solution [3]**:
- `python -m venvDir --no-setuptools`
- activate virtualenv `source ... activate`
- download and run `get-pip.py` to manually install pip & setuptools in
this virtualenv
    - `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
    - `python3 get-pip.py --force-reinstall`
- continue as normal
