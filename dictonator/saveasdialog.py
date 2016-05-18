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

from gi.repository import Gtk, Gio


class FileSaveAsDialog:
    """Implements the File save as file_chooser."""

    def __init__(self, window: Gtk.Window):

        """Constructor.

        :param window: current window to set as parent.
        """
        self.owner = window
        self.file_chooser = Gtk.FileChooserDialog("Save file", window, Gtk.FileChooserAction.SAVE, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        # Sets whether we get the overwrite confirmation
        self.file_chooser.set_do_overwrite_confirmation(True)
        self.save_possible = False

    def file_dialog_handler(self, txt):
        saver_dialog = self.file_chooser
        response = saver_dialog.run()
        if response == Gtk.ResponseType.OK:
            # create an file based on dialog, paste the text and caller will load
            gfile_path = Gio.File.new_for_path(saver_dialog.get_filename())
            file = open(saver_dialog.get_filename(), 'w+')
            file.write(txt)
            file.close()
            saver_dialog.destroy()
            return gfile_path
        else:
            saver_dialog.destroy()
            return None
