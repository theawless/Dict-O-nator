from gi.repository import Gtk
import configparser
import DicNator.setlog as setlog

gedit_plugin_path = '.local/share/gedit/plugins'
# Setting up logger
logger = setlog.logger


class ConfigurableWidgetSettings:
    settings = dict()

    def __init__(self):
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
        # initialising all radio buttons
        self.sphinx_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=None, label="Sphinx")
        self.google_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=self.sphinx_radio,
                                                                       label="Google")
        self.wit_ai_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=self.sphinx_radio,
                                                                       label="WIT AI")
        self.att_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=self.sphinx_radio, label="ATT&T")
        self.ibm_radio = Gtk.RadioButton.new_with_label_from_widget(radio_group_member=self.sphinx_radio, label="IBM")

        logger.debug("Settings INIT")

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
        _settings = ConfigurableWidgetSettings.settings
        self.google_api_key.set_text(_settings['Google']['api_key'])
        self.witai_api_key.set_text(_settings['WITAI']['api_key'])
        self.ibm_username.set_text(_settings['IBM']['username'])
        self.ibm_password.set_text(_settings['IBM']['password'])
        self.att_app_key.set_text(_settings['ATT']['app_key'])
        self.att_app_secret.set_text(_settings['ATT']['app_secret'])
        # logger.debug("Got save text boxes")

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
        # logger.debug("Loading settings")
        for section in config.sections():
            dictionary[section] = {}
            for option in config.options(section):
                dictionary[section][option] = config.get(section, option)
        # logger.debug("loaded settings")
        return dictionary

    def save_settings(self):
        # Saving settings
        # logger.debug("Saving settings")
        config = self._default_settings()
        _settings = ConfigurableWidgetSettings.settings
        config['Main'] = {'recogniser': _settings['Main']['recogniser']}
        config['Google'] = {'api_key': _settings['Google']['api_key']}
        config['WITAI'] = {'api_key': _settings['WITAI']['api_key']}
        config['IBM'] = {'username': _settings['IBM']['username'], 'password': _settings['IBM']['password']}
        config['ATT'] = {'app_key': _settings['ATT']['app_key'], 'app_secret': _settings['ATT']['app_secret']}
        # Write new values to the configuration file
        with open(gedit_plugin_path + '/DicNator/DicNator_Settings.ini', 'w+') as configfile:
            config.write(configfile)
            # logger.debug("Saved settings")

    def _get_radio_buttons(self):
        # Connecting all buttons to the callback function
        self.sphinx_radio.connect("toggled", self._radio_callback, "Sphinx")
        self.google_radio.connect("toggled", self._radio_callback, "Google")
        self.wit_ai_radio.connect("toggled", self._radio_callback, "WITAI")
        self.att_radio.connect("toggled", self._radio_callback, "ATT")
        self.ibm_radio.connect("toggled", self._radio_callback, "IBM")
        self.configure_radios()
        # packing all radios
        self.radio_box.pack_start(self.sphinx_radio, True, False, 6)
        self.radio_box.pack_start(self.google_radio, True, False, 6)
        self.radio_box.pack_start(self.wit_ai_radio, True, False, 6)
        self.radio_box.pack_start(self.att_radio, True, False, 6)
        self.radio_box.pack_start(self.ibm_radio, True, False, 6)
        # logger.debug("Finished packing radioboxes")

    def configure_radios(self):
        # Load the radio buttons with settings
        _settings = ConfigurableWidgetSettings.settings

        if _settings['Main']['recogniser'] == "Sphinx":
            self.sphinx_radio.set_active(True)
        elif _settings['Main']['recogniser'] == "Google":
            self.google_radio.set_active(True)
        elif _settings['Main']['recogniser'] == "WITAI":
            self.wit_ai_radio.set_active(True)
        elif _settings['Main']['recogniser'] == "IBM":
            self.ibm_radio.set_active(True)
        elif _settings['Main']['recogniser'] == "ATT":
            self.att_radio.set_active(True)

    def _radio_callback(self, widget, data):
        # Define what happens when Radio options are selected
        # logger.debug("%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()]))
        # All radio_callback are called simultaneously, checking which one went active
        if widget.get_active():
            ConfigurableWidgetSettings.settings['Main']['recogniser'] = data
            self._choose_labelled_input_boxes()
            self.save_settings()

    def _choose_labelled_input_boxes(self):
        # choosing input box
        self.google_box.set_sensitive(False)
        self.ibm_box.set_sensitive(False)
        self.att_box.set_sensitive(False)
        self.witai_box.set_sensitive(False)
        # logger.debug("Hidden everything")
        data = ConfigurableWidgetSettings.settings['Main']['recogniser']
        # logger.debug(data)
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
        default_api_button = Gtk.Button.new_with_label("Load Default Values")
        default_api_button.connect("clicked", self._default_configuration)
        self.input_box.pack_start(default_api_button, False, False, 6)

    def _default_configuration(self, button):
        ConfigurableWidgetSettings.settings = self._default_settings()
        self.save_settings()
        self._get_input_saved_text_boxes()
        self.configure_radios()

    def _confirm_configuration(self, button):
        ConfigurableWidgetSettings.settings['Google']['api_key'] = self.google_api_key.get_text()
        ConfigurableWidgetSettings.settings['WITAI']['api_key'] = self.witai_api_key.get_text()
        ConfigurableWidgetSettings.settings['IBM']['username'] = self.ibm_username.get_text()
        ConfigurableWidgetSettings.settings['IBM']['password'] = self.ibm_password.get_text()
        ConfigurableWidgetSettings.settings['ATT']['app_key'] = self.att_app_key.get_text()
        ConfigurableWidgetSettings.settings['ATT']['app_secret'] = self.att_app_secret.get_text()
        self.save_settings()

    def get_configure_box(self):
        # logger.debug("Got in get_configure_box")
        ConfigurableWidgetSettings.settings = self.load_settings()
        self._get_labeled_boxes()
        self._get_radio_buttons()
        self._get_input_saved_text_boxes()
        self._pack_in_input_box()
        self._setup_confirm_button()
        self._choose_labelled_input_boxes()
        self.full_box.pack_start(self.radio_box, True, False, 6)
        self.full_box.pack_start(self.input_box, False, False, 6)
        return self.full_box

    def stop(self):
        del self.full_box
        del self.radio_box
        del self.input_box
        del self.google_box
        del self.witai_box
        del self.ibm_box
        del self.att_box
        del self.att_app_key_box
        del self.att_app_secret_box
        del self.ibm_username_box
        del self.ibm_password_box
        del self.google_api_key
        del self.witai_api_key
        del self.att_app_key
        del self.att_app_secret
        del self.ibm_username
        del self.ibm_password
        del self.google_api_key_label
        del self.witai_api_key_label
        del self.att_app_key_label
        del self.att_app_secret_label
        del self.ibm_username_label
        del self.ibm_password_label
        del self.sphinx_radio
        del self.google_radio
        del self.wit_ai_radio
        del self.att_radio
        del self.ibm_radio

    def __del__(self):
        logger.debug("Settings DEL")
