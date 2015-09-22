#!/usr/bin/env python

import sys
from gi.repository import Gtk


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


class Plop(Gtk.Application):
    def do_activate(self):
        self.window = Window(self)
        self.window.connect('destroy', lambda window: sys.exit())
        self.window.show_all()


if __name__ == '__main__':
    Plop().run(sys.argv)
