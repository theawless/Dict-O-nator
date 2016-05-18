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

from dictonator.settings import DictonatorSettings


class TestDictonatorSettings(TestCase):
    def setUp(self):
        DictonatorSettings()
        self.config = configparser.ConfigParser()
        self.config['Main'] = {'recogniser': 'WITAI', 'dynamic_noise_suppression': 'False'}
        self.config['Sphinx'] = {'version': 'pocketsphinx'}
        self.config['Google'] = {'api_key': ''}
        self.config['WITAI'] = {'api_key': ''}
        self.config['IBM'] = {'username': '', 'password': ''}
        self.config['Bing'] = {'api_key': ''}
        self.config['APIAI'] = {'api_key': ''}
        return True

    def run(self, result=None):
        conf = self.test_default_settings()
        dic = self.test_config_to_dict(conf)
        self.test_save_settings(dic)
        self.test_load_settings()

    def test_default_settings(self):
        _config = DictonatorSettings.default_settings()
        self.assertEqual(_config, self.config, "Default settings not equal")
        print("Default settings tested")
        return _config

    def test_config_to_dict(self, conf):
        dic = DictonatorSettings.config_to_dict(conf)
        _dic = {'Sphinx': {'version': 'pocketsphinx'},
                'WITAI': {'api_key': ''},
                'Google': {'api_key': ''},
                'Main': {'recogniser': 'WITAI', 'dynamic_noise_suppression': 'False'},
                'IBM': {'password': '', 'username': ''},
                'APIAI': {'api_key': ''},
                'Bing': {'api_key': ''}
                }

        self.assertEqual(_dic, dic, "Conversion from configparser to dictionary failed")
        print("settings convert to dictionary tested")
        return dic

    def test_save_settings(self, dic):
        DictonatorSettings.save_settings(dic)

    def test_load_settings(self):
        DictonatorSettings.load_settings()
        self.assertEqual(DictonatorSettings.settings, DictonatorSettings.config_to_dict(self.config),
                         "Incorrect load or save")
        print("Load and save settings tested")
