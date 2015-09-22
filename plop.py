#!/usr/bin/env python

import sys
from gi.repository import Gtk


class Plop(Gtk.Application):
    def do_activate(self):
        self.window = Gtk.Window(application=self)
        self.window.connect('destroy', lambda window: sys.exit())
        self.window.show_all()


if __name__ == '__main__':
    Plop().run(sys.argv)
