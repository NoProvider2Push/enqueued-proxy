# NoProvider2Push Enqueued Proxy

This is a proxy designed for [NoProvider2Push](https://github.com/NoProvider2Push/android).

Push messages that can't reach your phone will be saved in a database until the phone is reachable again.

## Installation

### Dependencies

Dependencies are in requirements.txt.

```
mkdir venv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Initiate database

```
source venv/bin/activate
flask db migrate
```

### Nginx

A configuration like the following should work.

```
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name relay.example.tld;


    ssl_certificate /opt/certs/relay.example.tld/crt.pem;
    ssl_certificate_key /opt/certs/relay.example.tld/key.pem;

    
    more_set_headers "Strict-Transport-Security : max-age=63072000; includeSubDomains; preload";

    location / {
			proxy_pass http://127.0.0.1:5001/;
      proxy_buffering  off;
      client_max_body_size  5M;
    }

    access_log /var/log/nginx/relay.example.tld-access.log;
    error_log /var/log/nginx/relay.example.tld-error.log;
}
```

### Systemd service

Edit np2p-proxy.service and replace User, WorkingDirectory and ExecStart to match your configuration, then copy to in `/etc/systemd/system/np2p-proxy.service` .

Finally, start the service and check its status:

```
systemctl daemon-reload
systemctl start np2p-proxy
systemctl status np2p-proxy
```

