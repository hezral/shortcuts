# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import sys
import os

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Granite', '7.0')
from gi.repository import Gtk, Gio, Granite, Gdk, GLib


class Application(Gtk.Application):

    app_id = "com.github.hezral.shortcuts"

    def __init__(self):
        super().__init__(application_id=self.app_id,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.window = None

    def do_activate(self):
        if not self.window:
            from .window import shortcutsWindow
            self.window = shortcutsWindow(application=self)
        self.window.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        
        # Sync GSettings
        self.gio_settings = Gio.Settings(schema_id=self.app_id)
        # Use get_for_display for GTK4
        self.gtk_settings = Gtk.Settings.get_for_display(Gdk.Display.get_default())
        self.granite_settings = Granite.Settings.get_default()

        # Support quiting app using Super+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *_: self.quit())
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])

        # Granite color scheme management
        def update_color_scheme(*args):
            prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
            is_dark = (prefers_color_scheme == Granite.SettingsColorScheme.DARK)
            self.gtk_settings.set_property("gtk-application-prefer-dark-theme", is_dark)

        update_color_scheme()
        self.granite_settings.connect("notify::prefers-color-scheme", update_color_scheme)

        # set CSS provider
        provider = Gtk.CssProvider()
        css_path = os.path.join(os.path.dirname(__file__), "data", "application.css")
        if os.path.exists(css_path):
            provider.load_from_path(css_path)
            Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def main(version):
    app = Application()
    return app.run(sys.argv)
