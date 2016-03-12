#!/usr/bin/python3

import sys
import configparser
from gi.repository import GObject, Gtk, Gedit, PeasGtk, GdkPixbuf

gedit_plugin_path = '.local/share/gedit/plugins/'
sys.path.append(gedit_plugin_path)
import setlog
import recogSpeech
import threading

import statesMod

# Getting the states
states = statesMod.states
# Setting up logger
logger = setlog.logger
logger.debug('Start Plugin')

# Defining the UI string that is to be added
ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menu name="DicNator" action="DicNator">
          <menuitem name="Clear" action="Clear"/>
          <menuitem name="Listen" action="Listen"/>
          <menuitem name="Stop" action="Stop"/>
          <menuitem name="Setup Dictator" action="Setup Dictator"/>
        </menu>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""


class BackgroundThread(threading.Thread):
    def __init__(self, instance):
        threading.Thread.__init__(self)
        self.pluginClass = instance

    def run(self):
        logger.debug(self.name + " run thread")
        self.pluginClass.bgcallhandler()

    def stop(self):
        logger.debug(self.name + " stop thread")


class DicNatorPlugin(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "DicNator"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        # Constructor
        GObject.Object.__init__(self)
        self.thread_is_running = False
        self._action_group = Gtk.ActionGroup("DicNatorPluginActions")
        self.thread = BackgroundThread(self)
        self.settings = self.get_config()
        self._bottom_widget = None
        self.s_recogniser = recogSpeech.SpeechRecogniser()
        self.s_recogniser.fix_ambient_noise()
        logger.debug('Init end')

    def do_activate(self):
        self._insert_menu()
        self._insert_bottom_panel()
        # Insert menu to gui

        logger.debug("Finished inserting menu")

    def do_deactivate(self):
        # Remove any installed menu items
        self._remove_menu()
        self._action_group = None
        logger.debug("Finished removing menu")

    def _insert_bottom_panel(self):
        icon = self._get_icon(20, 20)
        self._bottom_widget = Gtk.Label("Welcome to DicNator!  Start by speaking \"Start Dictation\"")
        panel = self.window.get_bottom_panel()
        panel.add_item(self._bottom_widget, "DicNator", "DicNator", icon)
        panel.activate_item(self._bottom_widget)

    def _get_icon(self, size_x, size_y):
        icon = Gtk.Image()
        buf = GdkPixbuf.Pixbuf.new_from_file(gedit_plugin_path + 'DicNator_Icon.png')
        scaled_ico = buf.scale_simple(size_x, size_y, GdkPixbuf.InterpType.BILINEAR)
        icon.set_from_pixbuf(scaled_ico)

        return icon

    def _insert_menu(self):
        actions = [
            ('DicNator', None, 'DicNator'),
            ("Clear", None, "Clear Document", '<Control><Alt>1', "Clear the document", self.on_clear_document_activate),
            ("Listen", None, "Start Listening", '<Control><Alt>2', "Start Listening", self.on_listen_activate),
            ("Stop", None, "Stop Listening", '<Control><Alt>3', "Stop Listening", self.on_stop_activate),
            ("Setup Dictator", None, "Setup Dictator", '<Control><Alt>4', "Setup Dicatator", self.on_setup_activate)

        ]

        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        # Create a new action group
        self._action_group.add_actions(actions)
        # Insert the action group
        manager.insert_action_group(self._action_group)
        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        # Remove the ui
        manager.remove_ui(self._ui_id)
        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def do_create_configure_widget(self):
        widget_vbox = Gtk.VBox()
        widget_vbox.set_border_width(6)
        widget_vbox.set_spacing(20)
        box = Gtk.HBox()
        label = Gtk.Label("Select Speech Recogniser")
        box.pack_start(label, False, False, 6)
        logger.debug("Added label")

        box2 = self.get_configured_radio_buttons()

        widget_vbox.pack_start(box, False, True, 0)
        widget_vbox.pack_start(box2, False, True, 0)
        icon = self._get_icon(50, 50)
        widget_vbox.pack_start(icon, False, True, 0)
        return widget_vbox

    def get_configured_radio_buttons(self):
        box = Gtk.HBox()
        _settings = self.settings

        radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=None, label="Google")
        radio.connect("toggled", self.radio_callback, "Google")
        if _settings == "Google":
            radio.set_active(True)
        box.pack_start(radio, False, False, 6)

        radio2 = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=radio, label="Sphinx")
        if _settings == "Sphinx":
            radio2.set_active(True)
        radio2.connect("toggled", self.radio_callback, "Sphinx")

        box.pack_start(radio2, False, False, 6)
        return box

    def get_config(self):
        config = configparser.ConfigParser()
        # Default recogniser is Sphinx
        config['main'] = {'recogniser': 'Sphinx'}
        config.read(gedit_plugin_path + 'DicNator_Settings.ini')
        select = config.get('main', 'recogniser')
        return select

    def radio_callback(self, widget, data=None):
        logger.debug("%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()]))
        if widget.get_active():
            self.settings = data
            config = configparser.ConfigParser()
            config['main'] = {'recogniser': data}
            with open(gedit_plugin_path + 'DicNator_Settings.ini', 'w') as configfile:
                config.write(configfile)

    def do_update_state(self):
        self._action_group.set_sensitive(self.window.get_active_document() is not None)

    def on_clear_document_activate(self, action):
        # Clears the document
        logger.debug("cleared the doc")
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.set_text('')

    def on_setup_activate(self, action):
        pass

    def on_listen_activate(self, action):
        # For debugging purposes we will start dictator on call only
        logger.debug('Thread Started')
        # Calling the background handler in a different thread
        self.thread_is_running = True
        self.thread.start()

    def on_stop_activate(self, action):
        # For debugging purposes we will stop dictator on call only
        logger.debug('Thread Stopping')
        # Stopping the background handler
        self.thread_is_running = False
        self.thread.stop()
        self.thread = BackgroundThread(self)
        logger.debug('Stopped')

    def change_bottom_text(self, txt="Welcome to DicNator!  Start by speaking \"Start Dictation\""):
        self._bottom_widget.set_text(txt)

    def inserttext(self, text="Default insertText"):
        # Inserts the text in the document
        doc = self.window.get_active_document()
        doc.begin_user_action()
        doc.insert_at_cursor(text)
        doc.end_user_action()

    def _callrecog(self):
        # Calls recognizer and gets the text output
        _textout = self.s_recogniser.recog(self.settings)
        _state = statesMod.decide_state(_textout)
        return _textout, _state

    def bgcallhandler(self):
        # Based on output by the callRecog we proceed further
        logger.debug("Inside bgcallhandler")
        if not self.thread_is_running:
            logger.debug("Thread not running")
            return
        self.change_bottom_text("Start Speaking")
        (text, currstate) = self._callrecog()
        if currstate == states[0]:
            self.inserttext(text)
            self.bgcallhandler()
        else:
            logger.debug("End Background Call Handler")
            return
