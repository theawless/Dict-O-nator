# Dict'O'nator : A Dictation Plugin for Gedit        <img src="/logo.png" width="60" height="60"/>

### Features
* Dictate text into Gedit  
* Delete sentences/words, perform undo/redo, copy/paste from clipboard, save/clear documents, go to line.
* Repeat commands, insert special characters.
* Choose one from many recognisation services  
* A comprehensive bottom bar

### How to use: [Read HOWTO for complete command list](/HOWTO)
* All commands work from the cursor, including put, deletes. 
* Multiple commands cannot be used together in one sentence
* Only repeatable actions can be repeated
* To input specific characters/digits use "put" command

##### Format of instructions:
* `some non command text` : input directly
* `repeatable command (number) times` : execute command number times
* `non repeatable command` : execute command
* `put (special character)` : input special character
* `put (special character) (number) times` : input special character number times
* `put (number) digit` : input number
* `put (number1) digit (number2) times` : input number1 number2 times

##### Examples:
* `Hello what's up` : non commands will be input directly
* `put underscore` : input _
* `delete sentence` : delete last sentence from pointer 
* `put question mark 4 times` : input question mark 4 times
* `delete 5 lines` : delete 5 lines
* `go to line 5` : moves the cursor to line 5
* `save document` : saves document

### Screenshot: [Go here to see the rest of screenshots](/Screenshots)
<img src="/Screenshots/settings.png" width="910" height="512"/>

### Requirements
* [Gedit](https://wiki.gnome.org/Apps/Gedit)
* [Zhang, A.(2016) Speech Recognition](https://github.com/Uberi/speech_recognition)
* [CMU Sphinx (Version 4 and higher)](http://cmusphinx.sourceforge.net/)
* [PocketSphinx Python Wrappers](https://github.com/cmusphinx/pocketsphinx)

### Installation(For Ubuntu)
* Install with script
  * Open terminal and execute `sudo ./plugininstall.sh`
* Manual Install
  * Copy all contents of **folder that matches your gedit version** to path `~/.local/share/gedit/plugins/`
  * Copy **dictonator.svg** to path `/usr/share/icons/hicolor/scalable/apps/`
  * Install **python3** and **pip3** by `sudo apt-get install python3-all-dev python3-pip`
  * Install **portaudio** and **swig** by `sudo apt-get install swig portaudio19-dev`
  * Install **SpeechRecognition** and **pocketsphinx** by `pip3 install SpeechRecognition pocketsphinx`

### License
Dict'O'nator is released under **GNU GPL v3**

See LICENSE to read the terms of the GNU General Public License  
You can also visit <http://www.gnu.org/licenses/> to read the terms.

### Code Attributes

Basic plugin codes  
License: GPl v2  
[Gedit Wiki](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo)

Speech
License: BSD  
[Uberi Speech Recognition](https://github.com/Uberi/speech_recognition/tree/master/examples)

text2num library  
License: MIT  
[text2num by Greg Hewgill](https://github.com/ghewgill/text2num)
