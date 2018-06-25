# Create/Edit a service file
For example something named `/etc/systemd/system/uwsgi.service` where you can write a content like this one:
```
[Unit]
Description=uWSGI instance to serve myapp
After=syslog.target

[Service]
ExecStart=/root/uwsgi/uwsgi --ini /etc/uwsgi/emperor.ini
# VirtualEnv stuff, when needed
# ExecStartPre=-/usr/bin/bash -c 'mkdir -p /run/uwsgi; chown user:nginx /run/uwsgi'
# ExecStart=/usr/bin/bash -c 'cd /home/user/myapp; source myappenv/bin/activate; uwsgi --ini myapp.ini'

# These options require systemd version 211 or newer
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
Edit or adapt your script accordingly

# Restart/Reload
Reload your new configuration with `systemctl daemon-reload` and start/restart it with `systemctl start uwsgi`
