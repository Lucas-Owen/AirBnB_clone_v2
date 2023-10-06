#!/usr/bin/env bash
# This bash script configures an ubuntu machine to serve a static webpage
apt-get update
apt install -y nginx
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/
touch /data/web_static/releases/test/index.html
echo -e '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>' > /data/web_static/releases/test/index.html
ln -s -f /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
sed -i '/server_name _;/a\\n\tlocation /hbnb_static \{\n\t\talias /data/web_static/current/;\n\t\}' /etc/nginx/sites-available/default
nginx -s reload
