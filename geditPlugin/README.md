# Dict'O'nator: A Dictation Plugin for Gedit
### Features
* Dictate text into Gedit  
* Choose one from many recognisation services  
* A comprehensive bottom bar

### Requirements
* [Gedit (Version 3.8)](https://wiki.gnome.org/Apps/Gedit)
* [Zhang, A.(2016) Speech Recognition](https://github.com/Uberi/speech_recognition#readme)
* [CMU Sphinx (Version 4 and higher)](http://cmusphinx.sourceforge.net/)
* [PocketSphinx Python Wrappers](https://github.com/cmusphinx/pocketsphinx)

### Installation
* Install with script
  * Open terminal and execute `sudo ./plugininstall.sh`
* Manual Install
  * Copy all contents of **geditplugin** to path `~/.local/share/gedit/plugins/`
  * Copy **dictonator.svg** to path `/usr/share/icons/hicolor/scalable/apps/`
  * Install **python3** and **pip3** by `sudo apt-get install python3-all-dev python3-pip`
  * Install **portaudio** and **swig** by `sudo apt-get install swig portaudio19-dev`
  * Install **SpeechRecognition** and **pocketsphinx** by `pip3 install SpeechRecognition pocketsphinx`

### License
Dict'O'nator - A dictation plugin for gedit.  
Copyright (C) <2016>  <Abhinav Singh>  

Dict'O'nator is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.  

Dict'O'nator is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
GNU General Public License for more details.  

You should have received a copy of the GNU General Public License  
along with Dict'O'nator.  If not, see <http://www.gnu.org/licenses/>.  
