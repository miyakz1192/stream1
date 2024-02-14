set -x

cd /etc/systemd/system 
sudo rm video-index-server.service
sudo rm video-server.service
sudo ln -s /home/miyakz/stream1/video_server/etc/video-index-server.service video-index-server.service 
sudo ln -s /home/miyakz/stream1/video_server/etc/video-server.service video-server.service 

sudo systemctl enable video-index-server.service
sudo systemctl enable video-server.service

