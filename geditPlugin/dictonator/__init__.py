#!/usr/bin/python3

from gi.repository import GObject, Gtk, Gedit, PeasGtk, GLib
from .setlog import logger
from .configurablesettings import ConfigurableDialogBox, PluginSettings
import threading
from .recogspeechbg import SpeechRecogniser
from .saveasdialog import FileSaver
from .setlog import logger
from .statesmod import states
import time

GEDIT_PLUGIN_PATH = '.local/share/gedit/plugins'


class DictonatorPluginActions:
    """Contains recogniser, threader and actions.

         Active window updated from the UI class.
         Handles all actions.
    """

    def __init__(self, f_bottom_bar_changer: callable, f_bottom_bar_adder: callable):
        """ Constructor.

        :param f_bottom_bar_changer: change the bottom bar main text.
        :param f_bottom_bar_adder: add to the actions list in bottom bar.
        """
        self.window = None
        # A manager to handle settings
        self.settings = PluginSettings().settings
        # Using like a global function
        self.bottom_bar_text_set = f_bottom_bar_changer
        self.bottom_bar_add = f_bottom_bar_adder
        GLib.threads_init()
        self.recogniser = SpeechRecogniser(f_bottom_bar_changer, self.action_handler)
        self.threader = threading.Thread(target=self.recogniser.start_recognising)
        self.threader.daemon = True
        logger.debug("Actions INIT")

    def on_setup_activate(self, action):
        """Demands noise fix from recogniser."""
        logger.debug("Demand noise variable set to True")
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "setup_dictation")
        self.recogniser.demand_fix_ambient_noise = True

    def on_listen_activate(self, action):
        """Start recogniser thread."""
        if not self.threader.isAlive():
            self.threader.start()
            logger.debug('Thread Started')
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "start_dictation")
        self.recogniser.wants_to_run = True
        logger.debug("wants to run is true")

    def on_stop_activate(self, action):
        """Stop recogniser thread."""
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "None", "stop_dicatation")
        self.recogniser.wants_to_run = False
        logger.debug("wants to run is false")

    def inserttext(self, text: str):
        """Inserts the text in the document at cursor position."""
        doc = self.window.get_active_document()
        doc.begin_user_action()
        ei = self.get_cursor_position(doc)
        if not ei.ends_sentence():
            logger.debug("********************************")
            text = text.capitalize()
        doc.insert_at_cursor(text)
        doc.end_user_action()
        # logger.debug("Inserted Text")

    @staticmethod
    def get_cursor_position(doc: Gedit.Document):
        """Gets the current cursor position from the doc given, Gtk+ 2.1 has this inbuilt as property."""
        c_mark = doc.get_insert()
        i = doc.get_iter_at_mark(c_mark)
        return i

    def on_logit_activate(self, action):
        """A test function."""
        ei = self.get_cursor_position(self.window.get_active_document())
        # ;ogger.debug(str(ei.starts_sentence()) + str(ei.inside_sentence()) + str(ei.ends_sentence()))
        # self.inserttext("i am abhinav")
        self.bottom_bar_add(time.strftime("%H:%M:%S"), "", "log_it")
        # a fuction to test other functions

    def action_handler(self, text: str):
        """Based on output by the decide_state we choose action."""
        currstate = statesmod.decide_state(text)
        self.bottom_bar_add(time.strftime("%H:%M:%S"), text, currstate)
        if currstate == "continue_dictation":
            self.inserttext(text)
        elif currstate == "start_dictation":
            self.on_listen_activate(None)
        elif currstate == "stop_dictation":
            self.on_stop_activate(None)
        elif currstate == "hold_dictation":
            pass
        elif currstate == "scroll_to_cursor":
            vi = self.window.get_active_view()
            vi.scroll_to_cursor()
        elif currstate == "goto_line":
            pass
        elif currstate == "undo":
            doc = self.window.get_active_document()
            if doc.can_undo():
                doc.begin_user_action()
                doc.undo()
                doc.end_user_action()
        elif currstate == "redo":
            doc = self.window.get_active_document()
            if doc.can_redo():
                doc.begin_user_action()
                doc.redo()
                doc.end_user_action()
        elif currstate == "cut_clipboard":
            vi = self.window.get_active_view()
            vi.cut_clipboard()
        elif currstate == "copy_clipboard":
            vi = self.window.get_active_view()
            vi.copy_clipboard()
        elif currstate == "paste_clipboard":
            vi = self.window.get_active_view()
            vi.paste_clipboard()
        elif currstate == "delete_selection":
            vi = self.window.get_active_view()
            vi.delete_selection()
        elif currstate == "select_all":
            vi = self.window.get_active_view()
            vi.select_all()
        elif currstate == "spacebar_input":
            self.inserttext(' ')
        elif currstate == "sentence_end":
            self.inserttext('. ')
        elif currstate == "delete_line":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self.get_cursor_position(doc)
            si = self.get_cursor_position(doc)
            si.set_line(ei.get_line())
            ei.forward_to_line_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "delete_sentence":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self.get_cursor_position(doc)
            si = self.get_cursor_position(doc)
            if not si.starts_sentence():
                si.backward_sentence_start()
            si.backward_char()
            ei.forward_sentence_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "delete_word":
            doc = self.window.get_active_document()
            doc.begin_user_action()
            ei = self.get_cursor_position(doc)
            si = self.get_cursor_position(doc)
            si.backward_word_start()
            si.backward_char()
            ei.forward_word_end()
            doc.delete(si, ei)
            doc.end_user_action()
        elif currstate == "clear_document":
            doc = self.window.get_active_document()
            if not doc:
                return
            doc.begin_user_action()
            doc.set_text('')
            doc.end_user_action()
        elif currstate == "new_document":
            self.window.create_tab(True)
        elif currstate == "save_document":
            doc = self.window.get_active_document()
            # checking if the document is a new document
            if doc.is_untitled():
                self.bottom_bar_text_set("First save should be Save As...")
                FileSaver(self.window)
            else:
                doc.save(Gedit.DocumentSaveFlags(15))
        elif currstate == "save_as_document":
            FileSaver(self.window)
        elif currstate == "close_document":
            if self.window.get_active_document.is_untouched():
                self.window.close_tab(self.window.get_active_tab())
            else:
                # to prevent data loss
                self.bottom_bar_text_set("You might wanna save the document before quitting.")
        elif currstate == "force_close_document":
            self.window.close_tab(self.window.get_active_tab())
        elif currstate == "error_state":
            logger.debug("Some Error ######")
        else:
            self.bottom_bar_text_set("Turned OFF")
        return

    def stop(self):
        """Stop Actions class."""
        del self.window
        del self.settings
        del self.bottom_bar_text_set

    def __del__(self):
        logger.debug("Actions DEL")


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
        self.bottom_widget.add_from_file(GEDIT_PLUGIN_PATH + "/dictonator/bottomwidgetui.glade")
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
        """Add actions to the eventlist int bottom bar.

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
