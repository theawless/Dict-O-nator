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

from gi.repository import GObject, Gtk, Gedit, PeasGtk

from .configurablesettings import ConfigurableDialogBox
from .pluginactions import DictonatorPluginActions
from .setlog import logger

GEDIT_PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))
BOTTOM_WIDGET_UI_PATH = GEDIT_PLUGIN_PATH + "/bottomwidgetui.glade"


class DictonatorUI(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    """Handle UI, define when plugin runs."""
    __gtype_name__ = "Dictonator"
    window = GObject.property(type=Gedit.Window)

    # Defining the UI string that is to be added
    ui_str = '''
                <ui>
                  <menubar name="MenuBar">
                    <menu name="ToolsMenu" action="Tools">
                      <placeholder name="ToolsOps_2">
                        <menu name="Dictonator" action="Dictonator">
                          <menuitem name="Listen" action="Listen"/>
                          <menuitem name="Stop" action="Stop"/>
                          <menuitem name="Setup Dictator" action="Setup Dictator"/>
                          <menuitem name="Logit" action="Logit"/>
                        </menu>
                      </placeholder>
                    </menu>
                  </menubar>
                </ui>
            '''

    def __init__(self):
        """Constructor for UI handler."""
        GObject.Object.__init__(self)
        self._action_group = Gtk.ActionGroup("DictonatorPluginActions")
        self.bottom_widget = Gtk.Builder()
        self.bottom_widget.add_from_file(BOTTOM_WIDGET_UI_PATH)
        # Get the plugin manager
        self.plugin_manager = DictonatorPluginActions(self.bottom_bar_text_changer, self.bottom_bar_handler)
        logger.debug('UI INIT')

    def do_update_state(self):
        self.plugin_manager.window = self.window
        self._action_group.set_sensitive(self.window.get_active_document() is not None)

    def do_activate(self):
        """Activate plugin, insert UI."""
        # Insert menu and bottom panel into gui
        self._insert_menu()
        self._insert_bottom_panel()
        # Very important window updated for manager class
        self.plugin_manager.window = self.window

    def _insert_menu(self):
        # Define actions and merge into UImanager
        actions = [
            ('Dictonator', None, 'Dictonator'),
            ("Listen", None, "Start Listening", '<Control><Alt>2', "Start Listening",
             self.plugin_manager.on_listen_activate),
            ("Stop", None, "Stop Listening", '<Control><Alt>3', "Stop Listening",
             self.plugin_manager.on_stop_activate),
            ("Setup Dictator", None, "Setup Dictator", '<Control><Alt>4', "Setup Dicatator",
             self.plugin_manager.on_setup_activate),
            ("Logit", None, "Logit", '<Control><Alt>5', "Logit",
             self.plugin_manager.on_logit_activate),
        ]

        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()
        self._action_group.add_actions(actions)
        manager.insert_action_group(self._action_group)
        # Merge the UI
        self._ui_id = manager.add_ui_from_string(self.ui_str)

    @staticmethod
    def get_icon(size: Gtk.IconSize):
        """Return scaled dictonator icon from disk."""
        icon = Gtk.Image.new_from_icon_name("dictonator", size)
        return icon

    def _insert_bottom_panel(self):
        # Implement the plugin into bottom bar
        icon = self.get_icon(Gtk.IconSize.SMALL_TOOLBAR)
        panel = self.window.get_bottom_panel()
        panel.add_item(self.bottom_widget.get_object("full_box"), "Dictonator", "Dict'O'nator", icon)
        panel.activate_item(self.bottom_widget.get_object("full_box"))
        panel.show()

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
        self._remove_menu()
        self._remove_bottom_panel()
        self._action_group = None
        self.stop()

    def _remove_menu(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_id)
        manager.remove_action_group(self._action_group)
        # Make sure the manager updates
        manager.ensure_update()

    def _remove_bottom_panel(self):
        panel = self.window.get_bottom_panel()
        panel.remove_item(self.bottom_widget.get_object("full_box"))
        # logger.debug("Removed bottom bar")

    def do_create_configure_widget(self):
        """Implement the configuration box in plugin preferences"""
        return ConfigurableDialogBox().get_configure_box

    def stop(self):
        """Stop the plugin. """
        self.plugin_manager.stop()
        del self.plugin_manager
        del self.bottom_widget

    def __del__(self):
        logger.debug("UI DEL")
