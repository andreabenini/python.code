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
