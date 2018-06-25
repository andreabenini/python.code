# Create/Edit a service file
For example something named `/etc/systemd/system/uwsgi.service` where you can write a content like this one:
```
[Unit]
Description=uWSGI instance to serve myapp
After=network.target

[Service]
User=nginx
Group=nginx
ExecStart=/usr/bin/uwsgi --ini /etc/uwsgi/emperor.ini --logto /tmp/whatever/fileupload.log
# VirtualEnv stuff, when needed
# ExecStartPre=-/usr/bin/bash -c 'mkdir -p /run/uwsgi; chown user:nginx /run/uwsgi'
# ExecStart=/usr/bin/bash -c 'cd /home/user/myapp; source myappenv/bin/activate; uwsgi --ini myapp.ini'
# ExecStop=/something/to/execute/myservice stop
# ExecReload=/something/to/execute/myservice reload_config
Restart=always
# Restart=on-failure
RestartSec=5s
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
Edit or adapt your script accordingly

# Restart/Reload
Reload your new configuration with `systemctl daemon-reload` and start/restart it with `systemctl start uwsgi`
