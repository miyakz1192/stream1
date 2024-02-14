set -x

cd /etc/systemd/system 
sudo rm token-server.service
sudo ln -s /home/miyakz/stream1/token_server/etc/token-server.service token-server.service 

sudo systemctl enable token-server.service

