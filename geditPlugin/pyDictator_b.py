#!/usr/bin/python3

import sys
import configparser
from gi.repository import GObject, Gtk, Gedit, PeasGtk, GdkPixbuf

gedit_plugin_path = '.local/share/gedit/plugins/'
sys.path.append(gedit_plugin_path)
status = ""
import setlog
import recogSpeech
import threading
import statesMod

# Getting the states
states = statesMod.states
# Setting up logger
logger = setlog.logger
logger.debug('Start Plugin')


class BackgroundThread(threading.Thread):
    def __init__(self, instance):
        threading.Thread.__init__(self)
        self.plugin_instance = instance

    def run(self):
        logger.debug(self.name + " run thread")
        self.plugin_instance.bgcallhandler()

    def stop(self):
        logger.debug(self.name + " stop thread")


class DicNatorUI:
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

    def __init__(self, instance):
        self.plugin_instance = instance
        self._action_group = Gtk.ActionGroup("DicNatorPluginActions")
        self._bottom_widget = None

    def setup_ui(self):
        # Insert menu to gui
        self._insert_menu()
        self._insert_bottom_panel()
        pass

    def _insert_menu(self):
        actions = [
            ('DicNator', None, 'DicNator'),
            ("Clear", None, "Clear Document", '<Control><Alt>1', "Clear the document",
             self.plugin_instance.on_clear_document_activate),
            ("Listen", None, "Start Listening", '<Control><Alt>2', "Start Listening",
             self.plugin_instance.on_listen_activate),
            ("Stop", None, "Stop Listening", '<Control><Alt>3', "Stop Listening",
             self.plugin_instance.on_stop_activate),
            ("Setup Dictator", None, "Setup Dictator", '<Control><Alt>4', "Setup Dicatator",
             self.plugin_instance.on_setup_activate)
        ]

        # Get the Gtk.UIManager
        manager = self.plugin_instance.window.get_ui_manager()
        # Create a new action group
        self._action_group.add_actions(actions)
        # Insert the action group
        manager.insert_action_group(self._action_group)
        # Merge the UI
        self._ui_id = manager.add_ui_from_string(self.ui_str)

    def _get_icon(self, size_x, size_y):
        icon = Gtk.Image()
        buf = GdkPixbuf.Pixbuf.new_from_file(gedit_plugin_path + 'DicNator_Icon.png')
        scaled_ico = buf.scale_simple(size_x, size_y, GdkPixbuf.InterpType.BILINEAR)
        icon.set_from_pixbuf(scaled_ico)
        return icon

    def _insert_bottom_panel(self):
        icon = self._get_icon(20, 20)
        self._bottom_widget = Gtk.Label("Welcome to DicNator!  Start by speaking \"Start Dictation\"")
        panel = self.plugin_instance.window.get_bottom_panel()
        panel.add_item(self._bottom_widget, "DicNator", "DicNator", icon)
        panel.activate_item(self._bottom_widget)
        panel.show()

    def remove_ui(self):
        # Remove any installed menu items
        self._remove_menu()
        self._remove_bottom_panel()
        self._action_group = None

    def _remove_menu(self):
        # Get the Gtk.UIManager
        manager = self.plugin_instance.window.get_ui_manager()
        # Remove the ui
        manager.remove_ui(self._ui_id)
        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def _remove_bottom_panel(self):
        logger.debug("Removing bottom bar")
        # self._bottom_widget = Gtk.Label("Welcome to DicNator!  Start by speaking \"Start Dictation\"")
        panel = self.plugin_instance.window.get_bottom_panel()
        # panel.add_item(self._bottom_widget, "DicNator", "DicNator", icon)

        panel.remove_item(self._bottom_widget)
        panel.show()
        logger.debug("Removed bottom bar")

    def setup_configure_box(self):
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
        _settings = self.plugin_instance.settings

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

    def radio_callback(self, widget, data=None):
        logger.debug("%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()]))
        if widget.get_active():
            self.plugin_instance.settings = data
            config = configparser.ConfigParser()
            config['main'] = {'recogniser': data}
            with open(gedit_plugin_path + 'DicNator_Settings.ini', 'w') as configfile:
                config.write(configfile)

    def change_bottom_text(self, txt="Welcome to DicNator!  Start by speaking \"Start Dictation\""):
        self._bottom_widget.set_text(txt)


class DicNatorPlugin(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "DicNator"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        # Constructor
        GObject.Object.__init__(self)
        self.plugin_ui_manager = DicNatorUI(self)
        self.settings = self.get_config()
        self.thread = BackgroundThread(self)
        self.thread_is_running = False
        self.demand_fix_ambient_noise = True
        self.s_recogniser = recogSpeech.SpeechRecogniser()
        self.change_bottom_text = self.plugin_ui_manager.change_bottom_text
        logger.debug('Init end')

    def do_activate(self):
        self.plugin_ui_manager.setup_ui()

    def do_deactivate(self):
        self.plugin_ui_manager.remove_ui()

    def do_create_configure_widget(self):
        widget_vbox = self.plugin_ui_manager.setup_configure_box()
        return widget_vbox

    def get_config(self):
        config = configparser.ConfigParser()
        # Default recogniser is Sphinx
        config['main'] = {'recogniser': 'Sphinx'}
        config.read(gedit_plugin_path + 'DicNator_Settings.ini')
        select = config.get('main', 'recogniser')
        return select

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
        logger.debug("Demand noise variable set to True")
        self.on_stop_activate(action)
        self.demand_fix_ambient_noise = True

    def on_listen_activate(self, action):
        # For debugging purposes we will start dictator on call only
        if self.thread_is_running:
            self.on_stop_activate(action)
        logger.debug('Thread Started')
        # Calling the background handler in a different thread
        self.thread_is_running = True
        self.thread.start()

    def on_stop_activate(self, action):
        # For debugging purposes we will stop dictator on call only
        # Stopping the background handler
        if self.thread_is_running:
            logger.debug('Thread Stopping')
            self.thread_is_running = False
            self.thread.stop()
            self.thread.join()
            self.thread = BackgroundThread(self)
            logger.debug('Stopped')

    def inserttext(self, text="Default insertText"):
        # Inserts the text in the document
        logger.debug("Inserting text")
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

        if self.demand_fix_ambient_noise:
            logger.debug("Demanding noise fix")
            self.change_bottom_text("Setting up Dictator, Please wait for 3 seconds")
            self.s_recogniser.fix_ambient_noise()
            self.change_bottom_text("DicNator has been setup")
            self.demand_fix_ambient_noise = False
            logger.debug("Noise Fix Done")

        self.change_bottom_text("Start Speaking")
        (text, currstate) = self._callrecog()
        logger.debug("received text is " + text)

        if not self.thread_is_running:
            logger.debug("Thread not running")
            self.thread.join()
            return

        if currstate == states[0]:
            self.inserttext(text)
            self.bgcallhandler()
        else:
            logger.debug("End Background Call Handler")
            return
