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

EPEL Repository must be enabled before these operations
