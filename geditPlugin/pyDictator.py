#!/usr/bin/python3

import sys
import configparser
from gi.repository import GObject, Gtk, Gedit, PeasGtk, GdkPixbuf

gedit_plugin_path = '.local/share/gedit/plugins'
sys.path.append(gedit_plugin_path)
import DicNator.setlog as setlog
import DicNator.recogSpeech as recogSpeech
import threading
import DicNator.statesMod as statesMod

# Getting the states
states = statesMod.states
# Setting up logger
logger = setlog.logger
logger.debug('Start Plugin')


class BackgroundThread(threading.Thread):
    def __init__(self, instance):
        threading.Thread.__init__(self)
        # getting the plugin instance so we can call its functions
        self.plugin_instance = instance

    def run(self):
        # call the bgcallhandler in this thread
        logger.debug(self.name + " run thread")
        self.plugin_instance.bgcallhandler()

    def stop(self):
        # not implemented
        logger.debug(self.name + " stop thread")
        pass


class ConfigurableWidgetSettings:
    def __init__(self):
        self.settings = dict()
        self.full_box = Gtk.VBox()
        self.radio_box = Gtk.HBox()
        self.input_box = Gtk.VBox()

        self.google_box = Gtk.HBox()
        self.witai_box = Gtk.HBox()
        self.ibm_box = Gtk.VBox()
        self.att_box = Gtk.VBox()
        self.att_app_key_box = Gtk.HBox()
        self.att_app_secret_box = Gtk.HBox()
        self.ibm_username_box = Gtk.HBox()
        self.ibm_password_box = Gtk.HBox()

        self.google_api_key = Gtk.Entry()
        self.witai_api_key = Gtk.Entry()
        self.att_app_key = Gtk.Entry()
        self.att_app_secret = Gtk.Entry()
        self.ibm_username = Gtk.Entry()
        self.ibm_password = Gtk.Entry()
        self.google_api_key_label = Gtk.Label("Google API Key")
        self.witai_api_key_label = Gtk.Label("WITai API Key")
        self.att_app_key_label = Gtk.Label("ATT&T API Key")
        self.att_app_secret_label = Gtk.Label("AT&T app secret")
        self.ibm_username_label = Gtk.Label("IBM Username")
        self.ibm_password_label = Gtk.Label("IBM Password")

        logger.debug("Configurable Widget Init end")

    def _get_labeled_boxes(self):
        self.google_box.pack_start(self.google_api_key_label, True, False, 6)
        self.google_box.pack_start(self.google_api_key, True, True, 6)

        self.witai_box.pack_start(self.witai_api_key_label, True, False, 6)
        self.witai_box.pack_start(self.witai_api_key, True, True, 6)

        self.ibm_username_box.pack_start(self.ibm_username_label, True, False, 6)
        self.ibm_username_box.pack_start(self.ibm_username, True, True, 6)
        self.ibm_password_box.pack_start(self.ibm_password_label, True, False, 6)
        self.ibm_password_box.pack_start(self.ibm_password, True, True, 6)
        self.ibm_box.pack_start(self.ibm_username_box, True, False, 6)
        self.ibm_box.pack_start(self.ibm_password_box, True, True, 6)

        self.att_app_key_box.pack_start(self.att_app_key_label, True, False, 6)
        self.att_app_key_box.pack_start(self.att_app_key, True, True, 6)
        self.att_app_secret_box.pack_start(self.att_app_secret_label, True, False, 6)
        self.att_app_secret_box.pack_start(self.att_app_secret, True, True, 6)
        self.att_box.pack_start(self.att_app_key_box, True, False, 6)
        self.att_box.pack_start(self.att_app_secret_box, True, True, 6)

    def _pack_in_input_box(self):
        self.input_box.pack_start(self.google_box, False, False, 6)
        self.input_box.pack_start(self.witai_box, False, False, 6)
        self.input_box.pack_start(self.ibm_box, False, False, 6)
        self.input_box.pack_start(self.att_box, False, False, 6)

    def _get_input_saved_text_boxes(self):
        _settings = self.settings
        self.google_api_key.set_text(_settings['Google']['api_key'])
        self.witai_api_key.set_text(_settings['WITAI']['api_key'])
        self.ibm_username.set_text(_settings['IBM']['username'])
        self.ibm_password.set_text(_settings['IBM']['password'])
        self.att_app_key.set_text(_settings['ATT']['app_key'])
        self.att_app_secret.set_text(_settings['ATT']['app_secret'])
        logger.debug("Got save text boxes")

    def _default_settings(self):
        # Default settings
        config = configparser.ConfigParser()
        config['Main'] = {'recogniser': 'Sphinx'}
        config['Sphinx'] = {'version': 'pocketsphinx'}
        config['Google'] = {'api_key': ''}
        config['WITAI'] = {'api_key': ''}
        config['IBM'] = {'username': '', 'password': ''}
        config['ATT'] = {'app_key': '', 'app_secret': ''}
        return config

    def load_settings(self):
        # Get the configuration from file
        config = self._default_settings()
        config.read(gedit_plugin_path + '/DicNator/DicNator_Settings.ini')
        dictionary = {}
        logger.debug("Loading settings")
        for section in config.sections():
            dictionary[section] = {}
            for option in config.options(section):
                dictionary[section][option] = config.get(section, option)
        logger.debug("loaded settings")
        return dictionary

    def save_settings(self):
        # Saving settings
        logger.debug("Saving settings")
        config = self._default_settings()
        _settings = self.settings
        config['Main'] = {'recogniser': _settings['Main']['recogniser']}
        config['Google'] = {'api_key': _settings['Google']['api_key']}
        config['WITAI'] = {'api_key': _settings['WITAI']['api_key']}
        config['IBM'] = {'username': _settings['IBM']['username'], 'password': _settings['IBM']['password']}
        config['ATT'] = {'app_key': _settings['ATT']['app_key'], 'app_secret': _settings['ATT']['app_secret']}
        # Write new values to the configuration file
        with open(gedit_plugin_path + '/DicNator/DicNator_Settings.ini', 'w+') as configfile:
            config.write(configfile)
        logger.debug("Saved settings")

    def _get_configured_radio_buttons(self):
        # Load the radio buttons with settings
        _settings = self.settings
        # initialising all radio buttons
        sphinx_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=None, label="Sphinx")
        google_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=sphinx_radio, label="Google")
        wit_ai_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=sphinx_radio, label="WIT AI")
        att_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=sphinx_radio, label="ATT&T")
        ibm_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=sphinx_radio, label="IBM")
        # Connecting all buttons to the callback function
        sphinx_radio.connect("toggled", self._radio_callback, "Sphinx")
        google_radio.connect("toggled", self._radio_callback, "Google")
        wit_ai_radio.connect("toggled", self._radio_callback, "WITAI")
        att_radio.connect("toggled", self._radio_callback, "ATT")
        ibm_radio.connect("toggled", self._radio_callback, "IBM")
        # setting the correct value
        if _settings['Main']['recogniser'] == "Sphinx":
            sphinx_radio.set_active(True)
        elif _settings['Main']['recogniser'] == "Google":
            google_radio.set_active(True)
        elif _settings['Main']['recogniser'] == "WITAI":
            wit_ai_radio.set_active(True)
        elif _settings['Main']['recogniser'] == "IBM":
            ibm_radio.set_active(True)
        elif _settings['Main']['recogniser'] == "ATT":
            att_radio.set_active(True)
        # packing all radios
        self.radio_box.pack_start(sphinx_radio, True, False, 6)
        self.radio_box.pack_start(google_radio, True, False, 6)
        self.radio_box.pack_start(wit_ai_radio, True, False, 6)
        self.radio_box.pack_start(att_radio, True, False, 6)
        self.radio_box.pack_start(ibm_radio, True, False, 6)
        logger.debug("Finished packing radioboxes")

    def _radio_callback(self, widget, data):
        # Define what happens when Radio options are selected
        logger.debug("%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()]))
        # All radio_callback are called simultaneously, checking which one went active

        if widget.get_active():
            self.settings['Main']['recogniser'] = data
            self._choose_labelled_input_boxes()
            self.save_settings()

    def _choose_labelled_input_boxes(self):
        logger.debug("choosing input box")
        # hiding everything
        self.google_box.set_sensitive(False)
        self.ibm_box.set_sensitive(False)
        self.att_box.set_sensitive(False)
        self.witai_box.set_sensitive(False)
        logger.debug("Hidden everything")
        data = self.settings['Main']['recogniser']
        logger.debug(data)
        if data == 'Google':
            self.google_box.set_sensitive(True)
        elif data == 'WITAI':
            self.witai_box.set_sensitive(True)
        elif data == 'ATT':
            self.att_box.set_sensitive(True)
        elif data == 'IBM':
            self.ibm_box.set_sensitive(True)

    def _setup_confirm_button(self):
        confirm_api_button = Gtk.Button.new_with_label("Save these values")
        confirm_api_button.connect("clicked", self._confirm_configuration)
        self.input_box.pack_start(confirm_api_button, False, False, 6)

    def _confirm_configuration(self, button):
        self.settings['Google']['api_key'] = self.google_api_key.get_text()
        self.settings['WITAI']['api_key'] = self.witai_api_key.get_text()
        self.settings['IBM']['username'] = self.ibm_username.get_text()
        self.settings['IBM']['password'] = self.ibm_password.get_text()
        self.settings['ATT']['app_key'] = self.att_app_key.get_text()
        self.settings['ATT']['app_secret'] = self.att_app_secret.get_text()
        self.save_settings()

    def get_configure_box(self):
        logger.debug("Got in get_configure_box")
        self.settings = self.load_settings()
        self._get_labeled_boxes()
        self._get_configured_radio_buttons()
        self._get_input_saved_text_boxes()
        self._pack_in_input_box()
        self._setup_confirm_button()
        self._choose_labelled_input_boxes()
        self.full_box.pack_start(self.radio_box, True, False, 6)
        self.full_box.pack_start(self.input_box, False, False, 6)
        return self.full_box


class DicNatorPlugin:
    def __init__(self, f_bottom_bar_changer):
        # Constructor
        # Will update window from UIClass
        self.window = None
        # A dictionary to hold settings
        self.setting_manager = ConfigurableWidgetSettings()
        # Using like a global function
        self.bottom_bar_text_set = f_bottom_bar_changer
        # each class has its own recogniser thread
        self.thread = BackgroundThread(self)
        self._thread_is_running = False
        self.demand_fix_ambient_noise = True
        self.s_recogniser = recogSpeech.SpeechRecogniser(f_bottom_bar_changer, self.thread_run_get)

    def thread_run_get(self):
        return self._thread_is_running

    def thread_run_set(self, bool_state):
        self._thread_is_running = bool_state

    def on_clear_document_activate(self, action):
        # Clears the document
        doc = self.window.get_active_document()
        if not doc:
            return
        doc.set_text('')
        logger.debug("cleared the doc")

    def on_setup_activate(self, action):
        # Demanding noise fix
        logger.debug("Demand noise variable set to True")
        self.on_stop_activate(action)
        self.demand_fix_ambient_noise = True

    def on_listen_activate(self, action):
        # For debugging purposes start recogniser thread
        if self.thread_run_get():
            self.on_stop_activate(action)
        logger.debug('Thread Started')
        self.thread_run_set(True)
        self.thread.start()

    def on_stop_activate(self, action):
        # For debugging purposes stop recogniser thread
        if self.thread_run_get():
            logger.debug('Thread Stopping')
            self.thread_run_set(False)
            self.thread.stop()
            self.thread.join()
            self.bottom_bar_text_set("Turned OFF")
            self.thread = BackgroundThread(self)
            logger.debug('Stopped')

    def inserttext(self, text="Default insertText"):
        # Inserts the text in the document
        doc = self.window.get_active_document()
        doc.begin_user_action()
        doc.insert_at_cursor(text)
        doc.end_user_action()
        logger.debug("Inserted Text")

    def _callrecog(self):
        # Calls recognizer and gets the text output
        _textout = self.s_recogniser.recog(self.setting_manager.load_settings())
        _state = statesMod.decide_state(_textout)
        return _textout, _state

    def bgcallhandler(self):
        # Based on output by the callRecog we proceed further
        logger.debug("Inside bgcallhandler")
        # Check if ambient noise fix was called for
        if self.demand_fix_ambient_noise:
            logger.debug("Demanding noise fix")
            self.bottom_bar_text_set("Setting up Dictator, Please wait for a few seconds")
            self.s_recogniser.fix_ambient_noise()
            self.bottom_bar_text_set("DicNator has been setup")
            self.demand_fix_ambient_noise = False
            logger.debug("Noise Fix Done")

        self.bottom_bar_text_set("Speak Now!")
        (text, currstate) = self._callrecog()
        logger.debug("received text is " + text)

        if not self.thread_run_get():
            logger.debug("Thread not running")
            self.thread.join()
            self.bottom_bar_text_set("Turned OFF")

            return

        if currstate == states[0]:
            self.inserttext(text)
            self.bgcallhandler()
        elif currstate == states[12]:
            logger.debug("End Background Call Handler")
            return
        else:
            logger.debug("End Background Call Handler")
            self.bottom_bar_text_set("Turned OFF")
            return


class DicNatorUI(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "DicNator"
    window = GObject.property(type=Gedit.Window)

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

    def __init__(self):
        # Main plugin Constructor
        GObject.Object.__init__(self)
        self._action_group = Gtk.ActionGroup("DicNatorPluginActions")
        self._bottom_widget = None
        # Get the plugin manager
        self.plugin_manager = DicNatorPlugin(self.bottom_bar_text_changer)
        logger.debug('Init end')

    def do_update_state(self):
        self._action_group.set_sensitive(self.window.get_active_document() is not None)

    def do_activate(self):
        # Insert menu and bottom panel into gui
        self._insert_menu()
        self._insert_bottom_panel()
        # Very important window updated for manager class
        self.plugin_manager.window = self.window

    def _insert_menu(self):
        # Define actions and merge into UImanager
        actions = [
            ('DicNator', None, 'DicNator'),
            ("Clear", None, "Clear Document", '<Control><Alt>1', "Clear the document",
             self.plugin_manager.on_clear_document_activate),
            ("Listen", None, "Start Listening", '<Control><Alt>2', "Start Listening",
             self.plugin_manager.on_listen_activate),
            ("Stop", None, "Stop Listening", '<Control><Alt>3', "Stop Listening",
             self.plugin_manager.on_stop_activate),
            ("Setup Dictator", None, "Setup Dictator", '<Control><Alt>4', "Setup Dicatator",
             self.plugin_manager.on_setup_activate)
        ]

        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        self._action_group.add_actions(actions)
        manager.insert_action_group(self._action_group)
        # Merge the UI
        self._ui_id = manager.add_ui_from_string(self.ui_str)

    def get_icon(self, size_x, size_y):
        # Get icon from disk and scale it basec on parameters given
        icon = Gtk.Image()
        try:
            buf = GdkPixbuf.Pixbuf.new_from_file(gedit_plugin_path + '/DicNator/DicNator_Icon.png')
            logger.debug("Icon file found")
            scaled_ico = buf.scale_simple(size_x, size_y, GdkPixbuf.InterpType.BILINEAR)
            icon.set_from_pixbuf(scaled_ico)
            return icon
        except:
            # Icon not found on disk, using default
            icon = Gtk.Image.new_from_icon_name("Nothing", 4)
            return icon

    def _insert_bottom_panel(self):
        icon = self.get_icon(20, 20)
        self._bottom_widget = Gtk.Label("Welcome to DicNator!  Start by speaking \"Start Dictation\"")
        panel = self.window.get_bottom_panel()
        panel.add_item(self._bottom_widget, "DicNator", "DicNator", icon)
        panel.activate_item(self._bottom_widget)
        # Make sure that the bottom bar shows up
        panel.show()

    def do_deactivate(self):
        # Remove menu items and bottom bar
        self._remove_menu()
        self._remove_bottom_panel()
        self._action_group = None

    def _remove_menu(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        # Make sure the manager updates
        manager.ensure_update()

    def _remove_bottom_panel(self):
        panel = self.window.get_bottom_panel()
        panel.remove_item(self._bottom_widget)
        logger.debug("Removed bottom bar")

    def do_create_configure_widget(self):
        # Implement the configuration box in plugin preferences
        widget_vbox = Gtk.VBox()
        widget_vbox.set_border_width(6)
        widget_vbox.set_spacing(10)
        label = Gtk.Label("Select Speech Recogniser")
        logger.debug("Inserted label")
        settings_box = self.plugin_manager.setting_manager.get_configure_box()
        # Get icon
        icon = self.get_icon(50, 50)
        # Pack everything
        widget_vbox.pack_start(label, False, True, 0)
        widget_vbox.pack_start(settings_box, False, True, 0)
        widget_vbox.pack_start(icon, False, True, 0)
        return widget_vbox

    def bottom_bar_text_changer(self, txt):
        # A text updater for bottom bar. Kind of a global function
        if self._bottom_widget is not None:
            self._bottom_widget.set_text(txt)
        else:
            logger.debug("Tried to set bottom text after disabling plugin")
