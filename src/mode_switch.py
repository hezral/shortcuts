# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GObject, Gdk

class ModeSwitch(Gtk.Grid):
    '''Gtk only basic port of https://github.com/elementary/granite/blob/master/lib/Widgets/ModeSwitch.vala'''

    __gtype_name__ = "ModeSwitch"

    CSS = """
    .modeswitch slider {min-height: 16px; min-width: 16px;}
    .modeswitch:checked {background-clip: border-box; background-color: rgba(0,0,0,0.1); background-image: none;}
    """
    
    def __init__(self, primary_widget, secondary_widget, primary_widget_callback, secondary_widget_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set CSS provider for display
        provider = Gtk.CssProvider()
        provider.load_from_data(self.CSS.encode())
        Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.primary_widget = primary_widget
        self.secondary_widget = secondary_widget

        self.primary_widget_callback = primary_widget_callback
        self.secondary_widget_callback = secondary_widget_callback
        
        if self.primary_widget is not None:
            click = Gtk.GestureClick()
            click.connect("released", lambda *_: self.switch.set_active(False))
            self.primary_widget.add_controller(click)
            self.primary_widget.props.valign = Gtk.Align.CENTER
            self.primary_widget.props.halign = Gtk.Align.END
            self.attach(self.primary_widget, 0, 0, 1, 1)

        if self.secondary_widget is not None:
            click = Gtk.GestureClick()
            click.connect("released", lambda *_: self.switch.set_active(True))
            self.secondary_widget.add_controller(click)
            self.secondary_widget.props.valign = Gtk.Align.CENTER
            self.secondary_widget.props.halign = Gtk.Align.START
            self.attach(self.secondary_widget, 2, 0, 1, 1)
    
        self.switch = Gtk.Switch()
        self.switch.add_css_class("modeswitch")
        self.switch.props.can_focus = False
        self.switch.props.valign = Gtk.Align.CENTER
        self.switch.props.margin_top = 1
        self.switch.set_size_request(32, -1)
        self.attach(self.switch, 1, 0, 1, 1)

        self.switch.connect("notify::active", self.on_switch_active_changed)

        self.props.column_spacing = 6
        self.props.margin_top = 6
        self.props.margin_end = 6

    def on_switch_active_changed(self, switch, pspec):
        if switch.get_active():
            if self.secondary_widget_callback is not None:
                self.secondary_widget_callback()
        else:
            if self.primary_widget_callback is not None:
                self.primary_widget_callback()
