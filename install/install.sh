# This installer will download every needed package to run properly Manga-Alert Notifier

# Update package
sudo apt-get update -y

# Install pip3 package installer
sudo apt-get install python3-pip

# BeautifulSoup4
sudo pip3 install bs4

# Requests
sudo pip3 install requests

# lxml parser
sudo apt-get install python3-lxml -y

# PIL
sudo pip3 install Pillow
sudo apt-get install libopenjp2-7 -y
sudo apt-get install libtiff5 -y
