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

import os
import time

from gi.repository import GObject, Gtk, Gedit, PeasGtk, Gio

from dictonator.actionhandler import DictonatorActionHandler
from dictonator.setlog import logger
from dictonator.settings import ConfigurationDialogBox

GEDIT_PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))
BOTTOM_WIDGET_UI_PATH = GEDIT_PLUGIN_PATH + "/widget.glade"


class DictonatorAppActivatable(GObject.Object, Gedit.AppActivatable):
    app = GObject.property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)
        self.menu_ext = None

    def do_activate(self):
        self.menu_ext = self.extend_menu("tools-section")
        menu = Gio.Menu()
        item1 = Gio.MenuItem.new("Start Dict'O'nator", 'win.dictonator_start')
        item2 = Gio.MenuItem.new("Stop Dict'O'nator", 'win.dictonator_stop')
        item3 = Gio.MenuItem.new("Setup Dict'O'nator", 'win.dictonator_setup')
        item4 = Gio.MenuItem.new("Logit Dict'O'nator", 'win.dictonator_logit')
        menu.append_item(item1)
        menu.append_item(item2)
        menu.append_item(item3)
        menu.append_item(item4)
        menu_item = Gio.MenuItem.new_submenu("Dict'O'nator", menu)
        self.menu_ext.append_menu_item(menu_item)
        self.app.set_accels_for_action("win.dictonator_start", ("<Primary><Alt>2", None))
        self.app.set_accels_for_action("win.dictonator_stop", ("<Primary><Alt>3", None))
        self.app.set_accels_for_action("win.dictonator_setup", ("<Primary><Alt>4", None))
        self.app.set_accels_for_action("win.dictonator_logit", ("<Primary><Alt>5", None))

    def do_deactivate(self):
        self.app.set_accels_for_action("win.dictonator_start", ())
        self.app.set_accels_for_action("win.dictonator_stop", ())
        self.app.set_accels_for_action("win.dictonator_setup", ())
        self.app.set_accels_for_action("win.dictonator_logit", ())
        self.menu_ext = None


class DictonatorWindowActivatable(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    """Handle UI, define when plugin runs."""
    __gtype_name__ = "dictonator"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        """Constructor for UI handler."""
        GObject.Object.__init__(self)
        self.bottom_widget = Gtk.Builder()
        self.bottom_widget.add_from_file(BOTTOM_WIDGET_UI_PATH)
        # Get the plugin manager
        self.plugin_manager = DictonatorActionHandler(self.bottom_bar_text_changer, self.bottom_bar_handler)
        logger.debug('UI INIT')

    def do_update_state(self):
        self._update_state()
        active = False
        if self.window.get_active_view() is not None:
            active = True
        self.window.lookup_action('dictonator_start').set_enabled(active)
        self.window.lookup_action('dictonator_stop').set_enabled(active)
        self.window.lookup_action('dictonator_setup').set_enabled(active)
        self.window.lookup_action('dictonator_logit').set_enabled(active)

    def _update_state(self):
        # every time the state is updated, we need to update it in plugin manager class too
        window = self.window
        self.plugin_manager.window = window
        self.plugin_manager.document = window.get_active_document()
        self.plugin_manager.view = window.get_active_view()
        self.plugin_manager.tab = window.get_active_tab()

    def do_activate(self):
        """Activate plugin, insert UI."""
        self._update_state()
        # Insert menu and bottom panel into gui
        action1 = Gio.SimpleAction(name='dictonator_start')
        action1.connect('activate', self.do_action_cb, "start")
        action2 = Gio.SimpleAction(name='dictonator_stop')
        action2.connect('activate', self.do_action_cb, "stop")
        action3 = Gio.SimpleAction(name='dictonator_setup')
        action3.connect('activate', self.do_action_cb, "setup")
        action4 = Gio.SimpleAction(name='dictonator_logit')
        action4.connect('activate', self.do_action_cb, "logit")

        self.window.add_action(action1)
        self.window.add_action(action2)
        self.window.add_action(action3)
        self.window.add_action(action4)
        self._insert_bottom_panel()

    def do_action_cb(self, action, uuser_data, user_data):
        if user_data == 'start':
            self.plugin_manager.on_listen_activate(None)
        if user_data == 'stop':
            self.plugin_manager.on_stop_activate(None)
        if user_data == 'setup':
            self.plugin_manager.on_setup_activate(None)
        if user_data == 'logit':
            self.plugin_manager.on_logit_activate(None)

    @staticmethod
    def get_icon(size: Gtk.IconSize):
        """Return scaled dictonator icon from disk."""
        icon = Gtk.Image.new_from_icon_name("dictonator", size)
        return icon

    def _insert_bottom_panel(self):
        # Implement the plugin into bottom bar
        wid = self.bottom_widget.get_object("full_box")
        panel = self.window.get_bottom_panel()
        panel.add_titled(wid, 'dictonator', "Dict'O'nator")
        panel.show()
        wid.show_all()
        panel.set_visible_child(wid)

    def bottom_bar_handler(self, tim: time, text: str, action: str):
        """Add actions to the eventlist in the bottom bar.

        :param tim: Time of action.
        :param text: Recognized text.
        :param action: Action performed.
        """
        row = Gtk.ListBoxRow()
        box = Gtk.HBox()
        box.set_homogeneous(True)
        text_label = Gtk.Label(text)
        text_label.set_line_wrap(True)
        box.pack_start(Gtk.Label(tim), False, False, 0)
        box.pack_start(text_label, True, True, 0)
        box.pack_start(Gtk.Label(action), False, False, 0)
        row.add(box)
        # Remove old entries
        if self.bottom_widget.get_object("event_list").get_row_at_index(40):
            self.bottom_widget.get_object("event_list").get_row_at_index(40).destroy()
        row.show_all()
        self.bottom_widget.get_object("event_list").prepend(row)

    def bottom_bar_text_changer(self, text: str):
        """Change main bottom bar text.

        :param text: New bottom bar main text.
        """
        self.bottom_widget.get_object("head_label").set_text(text)

    def do_deactivate(self):
        """Plugin close. Remove menu items and bottom bar."""
        logger.debug("DEACTIVATING")
        self._remove_bottom_panel()
        self.stop()

    def _remove_bottom_panel(self):
        panel = self.window.get_bottom_panel()
        panel.remove(self.bottom_widget.get_object("full_box"))
        # logger.debug("Removed bottom bar")

    def do_create_configure_widget(self):
        """Implement the configuration box in plugin preferences"""
        return ConfigurationDialogBox().get_configure_box

    def stop(self):
        """Stop the plugin. """
        self.plugin_manager.stop()
        del self.plugin_manager
        del self.bottom_widget
