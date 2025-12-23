# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject

from .mode_switch import ModeSwitch

class shortcutsWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'shortcutsWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = self.get_application()

        light = Gtk.Image.new_from_icon_name("display-brightness-symbolic")
        dark = Gtk.Image.new_from_icon_name("weather-clear-night-symbolic")
        
        # Primary is light (False), secondary is dark (True)
        modeswitch = ModeSwitch(light, dark, 
                               lambda: self.app.gtk_settings.set_property("gtk-application-prefer-dark-theme", False), 
                               lambda: self.app.gtk_settings.set_property("gtk-application-prefer-dark-theme", True))

        # Sync switch state with GtkSettings
        def on_theme_changed(*args):
            is_dark = self.app.gtk_settings.get_property("gtk-application-prefer-dark-theme")
            # Block signals to avoid feedback loop
            modeswitch.switch.handler_block_by_func(modeswitch.on_switch_active_changed)
            modeswitch.switch.set_active(is_dark)
            modeswitch.switch.handler_unblock_by_func(modeswitch.on_switch_active_changed)
            
        self.app.gtk_settings.connect("notify::gtk-application-prefer-dark-theme", on_theme_changed)
        on_theme_changed()

        header = Gtk.HeaderBar()
        header.set_show_title_buttons(True)
        header.pack_end(modeswitch)
        
        # Set the Custom HeaderBar as the official titlebar
        self.set_titlebar(header)

        label = Gtk.Label(label="Shortcuts World")
        label.set_hexpand(True)
        label.set_vexpand(True)
        label.set_valign(Gtk.Align.CENTER)
        label.set_halign(Gtk.Align.CENTER)

        self.set_child(label)
        self.set_default_size(480, 320)
