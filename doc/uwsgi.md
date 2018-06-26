# uwsgi installation on CentOS/RHEL machines
Do not use repos for it, install uwsgi from pip, easy as that:
```
/ # yum install gcc python-devel
...
/ # pip3.4 install uwsgi
Collecting uwsgi
  Downloading https://files.pythonhosted.org/packages/98/b2/19b34b20d22/uwsgi-2.0.17.tar.gz (798kB)
    100% |████████████████████████████████| 798kB 3.4MB/s 
Installing collected packages: uwsgi
  Running setup.py install for uwsgi ... done
Successfully installed uwsgi-2.0.17
/ # uwsgi --version
2.0.17
```
Program versions and URLs might be slightly different, installation steps are basically the same.<br>
CentOS/RHEL packages are outdated and uwsgi needs the bleeding edge stable, use `pip` to get it
