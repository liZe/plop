#!/usr/bin/env python

import configparser
import feedparser
import os
import sys
import webbrowser
from gi.repository import Gtk, GLib


class Feed(Gtk.TreeView):
    def __init__(self, name, url):
        super().__init__()
        self.set_headers_visible(False)

        store = Gtk.ListStore(str, str)
        self.set_model(store)
        pane_cell = Gtk.CellRendererText()
        pane_column = Gtk.TreeViewColumn('Articles', pane_cell, text=0)
        self.append_column(pane_column)

        self.connect('row-activated', self.activated)

        for entry in feedparser.parse(url).entries:
            store.append((entry.title, entry.link))

    def activated(self, treeview, path, view):
        webbrowser.open(treeview.props.model[path][1])


class Window(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application)
        self.set_title('Plop')
        self.set_icon_name('edit-find')
        self.set_hide_titlebar_when_maximized(True)

        hbox = Gtk.HBox()
        self.feed_list = Gtk.StackSidebar()
        self.feed_list.set_stack(Gtk.Stack())
        self.feed_list.props.stack.set_transition_type(
            Gtk.StackTransitionType.CROSSFADE)

        hbox.pack_start(self.feed_list, False, False, 0)
        hbox.pack_start(self.feed_list.props.stack, True, True, 0)
        self.add(hbox)

        self.config = configparser.SafeConfigParser()
        self.config.read(os.path.expanduser('~/.config/plop'))

    def update(self):
        for child in self.feed_list.props.stack.get_children():
            self.feed_list.props.stack.remove(child)
        for section in self.config.sections():
            scroll = Gtk.ScrolledWindow()
            scroll.add(Feed(section, self.config[section]['url']))
            self.feed_list.props.stack.add_titled(scroll, section, section)
        self.show_all()


class Plop(Gtk.Application):
    def do_activate(self):
        self.window = Window(self)
        self.window.connect('destroy', lambda window: sys.exit())
        self.window.update()
        GLib.timeout_add_seconds(30, lambda: self.window.update() or True)


if __name__ == '__main__':
    Plop().run(sys.argv)
