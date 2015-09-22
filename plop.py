#!/usr/bin/env python

import feedparser
import sys
import webbrowser
from gi.repository import Gtk


class Feed(Gtk.TreeView):
    def __init__(self, name, url):
        super().__init__()

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

        hbox = Gtk.HBox()
        feed_list = Gtk.StackSidebar()
        feed_list.set_stack(Gtk.Stack())

        hbox.pack_start(feed_list, False, False, 0)
        hbox.pack_start(feed_list.props.stack, True, True, 0)
        self.add(hbox)

        feed_list.props.stack.add_titled(
            Feed('LinuxFR', 'https://linuxfr.org/news.atom'),
            'linuxfr', 'LinuxFR')
        feed_list.props.stack.add_titled(
            Feed('L’équipe', 'http://www.lequipe.fr/rss/actu_rss.xml'),
            'lequipe', 'L’équipe')


class Plop(Gtk.Application):
    def do_activate(self):
        self.window = Window(self)
        self.window.connect('destroy', lambda window: sys.exit())
        self.window.show_all()


if __name__ == '__main__':
    Plop().run(sys.argv)
