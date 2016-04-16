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
from unittest import TestCase

from ..configurablesettings import PluginSettings


class TestPluginSettings(TestCase):
    def setUp(self):
        PluginSettings()
        self.config = configparser.ConfigParser()
        self.config['Main'] = {'recogniser': 'WITAI'}
        self.config['Sphinx'] = {'version': 'pocketsphinx'}
        self.config['Google'] = {'api_key': ''}
        self.config['WITAI'] = {'api_key': 'A3OGNVOCVIMZVWBWLHSV2WLNO5ASS43J'}
        self.config['IBM'] = {'username': '', 'password': ''}
        self.config['Bing'] = {'api_key': 'eea410c705e74b349a26eebe4ca510f7'}
        self.config['APIAI'] = {'api_key': '26014dcd873d4c879d9d410aa6a34521'}

    def run(self, result=None):
        conf = self.test_default_settings()
        dic = self.test_config_to_dict(conf)
        self.test_save_settings(dic)
        self.test_load_settings()

    def test_default_settings(self):
        _config = PluginSettings.default_settings()
        self.assertEqual(_config, self.config, "Default settings not equal")
        return _config

    def test_config_to_dict(self, conf):
        dic = PluginSettings.config_to_dict(conf)
        _dic = {'Sphinx': {'version': 'pocketsphinx'},
                'WITAI': {'api_key': 'A3OGNVOCVIMZVWBWLHSV2WLNO5ASS43J'},
                'Google': {'api_key': ''},
                'Main': {'recogniser': 'WITAI'},
                'IBM': {'password': '', 'username': ''},
                'APIAI': {'api_key': '26014dcd873d4c879d9d410aa6a34521'},
                'Bing': {'api_key': 'eea410c705e74b349a26eebe4ca510f7'}
                }

        self.assertEqual(_dic, dic, "Conversion from configparser to dictionary failed")
        return dic

    def test_save_settings(self, dic):
        PluginSettings.save_settings(dic)

    def test_load_settings(self):
        PluginSettings.load_settings()
        self.assertEqual(PluginSettings.settings, PluginSettings.config_to_dict(self.config),
                         "Incorrect load or save")
