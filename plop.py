#!/usr/bin/env python

import sys
from gi.repository import Gtk


class Feed(Gtk.TreeView):
    def __init__(self, name):
        super().__init__()

        store = Gtk.ListStore(str)
        self.set_model(store)
        pane_cell = Gtk.CellRendererText()
        pane_column = Gtk.TreeViewColumn('Articles', pane_cell, text=0)
        self.append_column(pane_column)

        store.append(('Lien 1 ' + name,))
        store.append(('Lien 2 ' + name,))


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
            Feed('Flux 1'), 'flux1', 'Titre Flux 1')
        feed_list.props.stack.add_titled(
            Feed('Flux 2'), 'flux2', 'Titre Flux 2')


class Plop(Gtk.Application):
    def do_activate(self):
        self.window = Window(self)
        self.window.connect('destroy', lambda window: sys.exit())
        self.window.show_all()


if __name__ == '__main__':
    Plop().run(sys.argv)
