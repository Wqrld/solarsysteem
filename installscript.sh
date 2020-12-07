apt install -y git
cd /srv
git clone https://github.com/Wqrld/solarsysteem.git
cd solarsysteem

cat > /etc/systemd/system/solar.service <<- 'EOF'

[Unit]
Description=Solar

[Service]
User=root
WorkingDirectory=/srv/solarsysteem
LimitNOFILE=4096
ExecStart=while(true); do python3 serplot.py; sleep 30; done
Restart=on-failure
StartLimitInterval=600

[Install]
WantedBy=multi-user.target
EOF

systemctl enable --now solar
