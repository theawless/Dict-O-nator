# Dict'O'nator - A dictation plugin for gedit.
# Copyright (C) <2016>  <Abhinav Singh>
#
# This file is part of Dict'O'nator.
#
# Dict'O'nator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dict'O'nator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dict'O'nator.  If not, see <http://www.gnu.org/licenses/>.

import configparser
import copy
import os

from gi.repository import Gtk

from .setlog import logger

GEDIT_PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = GEDIT_PLUGIN_PATH + "/config.ini"
CONFIG_DIALOG_UI_PATH = GEDIT_PLUGIN_PATH + "/configurationboxui.glade"


class PluginSettings:
    """Implements save/load functions of settings."""
    # A static variable in all instances
    settings = dict()

    def __init__(self):
        """Loads the global settings."""
        self.load_settings()

    @classmethod
    def default_settings(cls):
        """Default settings, to define the format of config file.
        :rtype: configparser.ConfigParser
        """
        config = configparser.ConfigParser()
        config['Main'] = {'recogniser': 'WITAI'}
        config['Sphinx'] = {'version': 'pocketsphinx'}
        config['Google'] = {'api_key': ''}
        config['WITAI'] = {'api_key': 'A3OGNVOCVIMZVWBWLHSV2WLNO5ASS43J'}
        config['APIAI'] = {'api_key': '26014dcd873d4c879d9d410aa6a34521'}
        config['Bing'] = {'api_key': 'eea410c705e74b349a26eebe4ca510f7'}
        config['IBM'] = {'username': '', 'password': ''}
        return config

    @classmethod
    def load_settings(cls):
        """Get the configuration from saved file into global settings."""
        config = PluginSettings.default_settings()
        config.read(CONFIG_FILE_PATH)
        cls.settings = cls.config_to_dict(config)

    @classmethod
    def config_to_dict(cls, config: configparser.ConfigParser):
        """ Convert config parser type to dictionary.

        :param config: the configurations.
        :return: a dictionary of settings.
        """
        settings_dictionary = {}
        for sect in config.sections():
            settings_dictionary[sect] = {}
            for opt in config.options(sect):
                settings_dictionary[sect][opt] = config.get(sect, opt)
        return settings_dictionary

    @classmethod
    def save_settings(cls, settings: dict):
        """Saving settings given from the parameter and updating global settings.
        :param settings: the settings in a dictionary format.
        """
        cls.settings = settings
        config = cls.default_settings()
        config['Main'] = {'recogniser': settings['Main']['recogniser']}
        config['Google'] = {'api_key': settings['Google']['api_key']}
        config['WITAI'] = {'api_key': settings['WITAI']['api_key']}
        config['APIAI'] = {'api_key': settings['APIAI']['api_key']}
        config['Bing'] = {'api_key': settings['Bing']['api_key']}
        config['IBM'] = {'username': settings['IBM']['username'], 'password': settings['IBM']['password']}
        # Write new values to the configuration file
        with open(CONFIG_FILE_PATH, 'w+') as configfile:
            config.write(configfile)

            # logger.debug("Saved settings")

    @classmethod
    def stop(cls):
        del cls.settings


class ConfigurableDialogBox:
    """Implements the Configurable file_chooser box."""

    def __init__(self):
        """Get local settings from global settings. Get UI."""
        self.settings = copy.deepcopy(PluginSettings.settings)
        self.ui = Gtk.Builder()
        self.ui.add_from_file(CONFIG_DIALOG_UI_PATH)

    @property
    def get_configure_box(self):
        """Return only the box. Peas configurable handles the file_chooser making.
        :rtype: Gtk.Box
        """
        logger.debug("get configure box")
        self._get_saved_into_text_boxes()
        self._choose_labelled_input_boxes()
        self._connect_everything()
        self._configure_radios()

        return self.ui.get_object("full_box")

    def _get_saved_into_text_boxes(self):
        _settings = self.settings
        self.ui.get_object("google_key_entry").set_text(_settings['Google']['api_key'])
        self.ui.get_object("witai_key_entry").set_text(_settings['WITAI']['api_key'])
        self.ui.get_object("bing_key_entry").set_text(_settings['Bing']['api_key'])
        self.ui.get_object("ibm_username_entry").set_text(_settings['IBM']['username'])
        self.ui.get_object("ibm_password_entry").set_text(_settings['IBM']['password'])
        self.ui.get_object("apiai_key_entry").set_text(_settings['APIAI']['api_key'])

    def _connect_everything(self):
        # Connecting all radios,buttons to the callback function
        self.ui.get_object("sphinx_radio").connect("toggled", self._radio_callback, "Sphinx")
        self.ui.get_object("bing_radio").connect("toggled", self._radio_callback, "Bing")
        self.ui.get_object("google_radio").connect("toggled", self._radio_callback, "Google")
        self.ui.get_object("witai_radio").connect("toggled", self._radio_callback, "WITAI")
        self.ui.get_object("apiai_radio").connect("toggled", self._radio_callback, "APIAI")
        self.ui.get_object("ibm_radio").connect("toggled", self._radio_callback, "IBM")
        self.ui.get_object("save_button").connect("clicked", self._confirm_config)
        self.ui.get_object("default_button").connect("clicked", self._set_default_config)

    def _configure_radios(self):
        # Load the radio buttons with settings
        _settings = self.settings

        if _settings['Main']['recogniser'] == "Sphinx":
            self.ui.get_object("sphinx_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "Google":
            self.ui.get_object("google_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "WITAI":
            self.ui.get_object("witai_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "IBM":
            self.ui.get_object("ibm_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "APIAI":
            self.ui.get_object("apiai_radio").set_active(True)
        elif _settings['Main']['recogniser'] == "Bing":
            self.ui.get_object("bing_radio").set_active(True)

    def _choose_labelled_input_boxes(self):
        # choosing input box
        self.ui.get_object("google_box").set_sensitive(False)
        self.ui.get_object("ibm_box").set_sensitive(False)
        self.ui.get_object("apiai_box").set_sensitive(False)
        self.ui.get_object("witai_box").set_sensitive(False)
        self.ui.get_object("bing_box").set_sensitive(False)
        # Disabled everything"

        data = self.settings['Main']['recogniser']
        if data == 'Google':
            self.ui.get_object("google_box").set_sensitive(True)
        elif data == 'WITAI':
            self.ui.get_object("witai_box").set_sensitive(True)
        elif data == "Bing":
            self.ui.get_object("bing_box").set_sensitive(True)
        elif data == 'APIAI':
            self.ui.get_object("apiai_box").set_sensitive(True)
        elif data == 'IBM':
            self.ui.get_object("ibm_box").set_sensitive(True)

    def _radio_callback(self, radio, data):
        # Define what happens when Radio options are selected
        # logger.debug("%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()]))
        if radio.get_active():
            # All radio_callback are called simultaneously, checking which one went active
            self.settings['Main']['recogniser'] = data
            self._choose_labelled_input_boxes()

    def _set_default_config(self, button):
        # load default settigns and save them by calling PluginSetting
        self.settings = PluginSettings.config_to_dict(PluginSettings.default_settings())
        PluginSettings.save_settings(self.settings)
        self._get_saved_into_text_boxes()
        self._configure_radios()

    def _confirm_config(self, button):
        # save input values to temporary settings
        self.settings['Google']['api_key'] = self.ui.get_object("google_key_entry").get_text()
        self.settings['Bing']['api_key'] = self.ui.get_object("bing_key_entry").get_text()
        self.settings['WITAI']['api_key'] = self.ui.get_object("witai_key_entry").get_text()
        self.settings['IBM']['username'] = self.ui.get_object("ibm_username_entry").get_text()
        self.settings['IBM']['password'] = self.ui.get_object("ibm_password_entry").get_text()
        self.settings['APIAI']['api_key'] = self.ui.get_object("apiai_key_entry").get_text()
        # save to PluginClass
        PluginSettings.save_settings(self.settings)
