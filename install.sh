#!/usr/bin/env bash

apt-get install -y python3-pip
pip3 install -r requirements.txt

#create cert/key files
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes

echo "[Unit]
Description=LDAP Webfrontend at 0.0.0.0:8095
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory="$PWD"
ExecStart= "$PWD"/run.sh

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/ldap_webfrontend.service

systemctl enable ldap_webfrontend.service
systemctl start ldap_webfrontend.service

echo "installation finished"
