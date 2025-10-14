#!/bin/bash

if ! [[ "14.04 16.04 18.04 20.04 22.04" == *"$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)"* ]];
then
    echo "Ubuntu $(grep VERSION_ID /etc/os-release | cut -d '"' -f 2) is not currently supported.";
    exit;
fi

# Download the package to configure the Microsoft repo
curl -sSL -O https://packages.microsoft.com/config/ubuntu/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2)/packages-microsoft-prod.deb
# Install the package
sudo dpkg -i packages-microsoft-prod.deb
# Delete the file
rm packages-microsoft-prod.deb

sudo apt update
# Add the deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
# Update package lists again after adding PPA
sudo apt update
sudo apt install python3.11 -y
python3.11 --version
echo "Python 3.11 installation complete."
#Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo apt-get install -y unixodbc-dev

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
echo google-chrome --version

echo 'Instalando bibliotecas em requirements.txt'
pip install -r requirements.txt


sudo apt update
sudo apt install -y \
  libnss3 \
  libgconf-2-4 \
  libxi6 \
  libxcursor1 \
  libxcomposite1 \
  libasound2 \
  libxrandr2 \
  libgtk-3-0 \
  libxss1 \
  libxtst6 \
  fonts-liberation \
  xdg-utils \
  unzip \
  wget \
  curl


