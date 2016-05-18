#!/bin/sh

echo "Updating System"
sudo apt-get update
sudo apt-get upgrade

echo "Install Dependencies"
sudo apt-get install python-all-dev python3-all-dev
sudo apt-get install python3-pip
sudo apt-get install swig
sudo apt-get install portaudio19-dev
sudo pip3 install pyaudio
sudo pip3 install SpeechRecognition
sudo pip3 install pocketsphinx

echo "Making Directories"
sudo mkdir ~/.local/share/gedit/plugins/
sudo mkdir ~/.local/share/gedit/plugins/dictonator/

echo "Moving Files"
cp dictonator.plugin ~/.local/share/gedit/plugins/

echo "Moving Python Files"
cp dictonator/__init__.py ~/.local/share/gedit/plugins/dictonator/
cp dictonator/recogspeech.py ~/.local/share/gedit/plugins/dictonator/
cp dictonator/actionhandler.py ~/.local/share/gedit/plugins/dictonator/
cp dictonator/setlog.py ~/.local/share/gedit/plugins/dictonator/
cp dictonator/statesacts.py ~/.local/share/gedit/plugins/dictonator/
cp dictonator/saveasdialog.py ~/.local/share/gedit/plugins/dictonator/
cp dictonator/settings.py ~/.local/share/gedit/plugins/dictonator/
cp dictonator/text2num.py ~/.local/share/gedit/plugins/dictonator/


echo "Moving UI Files"
cp dictonator/widget.glade ~/.local/share/gedit/plugins/dictonator/
cp dictonator/configbox.glade ~/.local/share/gedit/plugins/dictonator/

echo "Moving Icon"
sudo cp dictonator.svg /usr/share/icons/hicolor/scalable/apps/
sudo gtk-update-icon-cache-3.0 /usr/share/icons/hicolor/

echo "Fixing permissions"
sudo chmod -R 777 ~/.local/share/gedit/plugins/
echo "Finished"
