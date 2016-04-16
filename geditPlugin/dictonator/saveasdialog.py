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

from gi.repository import Gtk, Gio, Gedit


class FileSaveAsDialog:
    """Implements the File save as file_chooser."""

    def __init__(self, window: Gtk.Window):

        """Constructor.

        :param window: current window to set as parent.
        """
        self.file_chooser = Gtk.FileChooserDialog("Save file", None, Gtk.FileChooserAction.SAVE, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        # Sets whether we get the overwrite confirmation
        self.file_chooser.set_do_overwrite_confirmation(True)
        self.save_possible = False
        self._file_dialog_handler(self.file_chooser, window)

    def _file_dialog_handler(self, saver_dialog: Gtk.Dialog, window: Gtk.Window):
        response = saver_dialog.run()
        if response == Gtk.ResponseType.OK:
            doc = window.get_active_document()
            # save the document with Gedit's save as function
            gfile_path = Gio.File.new_for_path(saver_dialog.get_filename())
            doc.save_as(gfile_path, doc.get_encoding(), doc.get_newline_type(), doc.get_compression_type(),
                        Gedit.DocumentSaveFlags(15))
            saver_dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            saver_dialog.destroy()
