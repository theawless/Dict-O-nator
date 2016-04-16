import os

from gi.repository import Gtk, Gio, Gedit


class FileSaver:
    """Implements the File save as dialog."""

    def __init__(self, window: Gtk.Window):

        """Constructor.

        :param window: current window to set as parent.
        """
        self.dialog = Gtk.FileChooserDialog("Save file", None, Gtk.FileChooserAction.SAVE, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        self.can_save = False
        self._handle_file_dialog(self.dialog, window)

    def _handle_file_dialog(self, dialog: Gtk.Dialog, window: Gtk.Window):
        """Handles the flow of dialog. Shows warnings for overwrite.

        :param dialog: filechooser dialog.
        :param window: current window wo set as parent.
        """
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # OK button was pressed or existing file was double clicked
            self.can_save = False
            if os.path.exists(dialog.get_filename()):
                # does file already exists?
                dialog2 = DialogSaveFile(window, dialog.get_filename())
                # ask to confirm overwrite
                response = dialog2.run()
                if response == Gtk.ResponseType.OK:
                    self.can_save = True
                    dialog2.destroy()
                else:
                    dialog2.destroy()
                    # We need to re-run the file dialog to detect the buttons
                    self._handle_file_dialog(dialog, window)
                    return
            else:
                self.can_save = True
            if self.can_save:
                doc = window.get_active_document()
                # save the document with Gedit's save as function
                gfile_path = Gio.File.new_for_path(dialog.get_filename())
                doc.save_as(gfile_path, doc.get_encoding(), doc.get_newline_type(), doc.get_compression_type(),
                            Gedit.DocumentSaveFlags(15))
                dialog.destroy()
                del self.can_save
            else:
                pass
        else:
            dialog.destroy()


class DialogSaveFile(Gtk.Dialog):
    """Implement warning dialog to overwrite."""

    def __init__(self, parent: Gtk.Widget, db: str):
        """Constructor.

        :param parent: widget to be set as parent.
        :param db: filename that is getting overwritten.
        """
        Gtk.Dialog.__init__(self, "Confirm overwrite", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.box = self.get_content_area()
        self.label = Gtk.Label("The file `" + db + "` already exists!\nDo you want it to be overwritten?")
        self.box.add(self.label)
        self.show_all()
