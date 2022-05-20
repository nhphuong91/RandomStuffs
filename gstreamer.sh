# Some useful gst pipeline

# Open & play video
sudo apt install gstreamer1.0-libav
gst-launch-1.0 filesrc location=<path to>/video.mp4 ! qtdemux ! decodebin ! videoconvert ! videoscale ! autovideosink
