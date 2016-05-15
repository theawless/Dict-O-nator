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
  * Copy all contents of **folder that matches your gedit version** to path `~/.local/share/gedit/plugins/`
  * Copy **dictonator.svg** to path `/usr/share/icons/hicolor/scalable/apps/`
  * Install **python3** and **pip3** by `sudo apt-get install python3-all-dev python3-pip`
  * Install **portaudio** and **swig** by `sudo apt-get install swig portaudio19-dev`
  * Install **SpeechRecognition** and **pocketsphinx** by `pip3 install SpeechRecognition pocketsphinx`

### License
Dict'O'nator is released under GNU GPL v3

See LICENSE to read the terms of the GNU General Public License  
If LICENSE is not present, you can visit <http://www.gnu.org/licenses/>.  
