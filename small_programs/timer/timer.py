#!/usr/bin/env python3
#
#  
#  Copyright 2023 yucef sourani <yuceff28@fedora>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk,Gio,GLib,Gdk,Adw
import time


# https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/style-classes.html
css = b"""
        #startrecordbutton {
                        padding: 40px;
                        color: @accent_bg_color;
                        background-color: @accent_bg_color;
                        box-shadow: 0px 1px 1px 0px @accent_bg_color, 0px 1px 2px 0px @accent_bg_color, inset 0 0 0 1px @accent_bg_color;
  }
  
        #stoprecordbutton {
                        padding: 40px;
                        color: @destructive_bg_color;
                        background-color: @destructive_bg_color;
                        box-shadow: 0px 1px 1px 0px @destructive_bg_color, 0px 1px 2px 0px @destructive_bg_color, inset 0 0 0 1px @destructive_bg_color;
  }

        """

            
class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.set_default_size(600, 400)
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(Gdk.Display().get_default(),
                                                 style_provider, 
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.mainvbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing = 0)
        self.set_content(self.mainvbox)

        headerbar = Gtk.HeaderBar.new()
        headerbar.set_title_widget(Gtk.Label.new("Timer"))
        self.mainvbox.append(headerbar)
      
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name("open-menu-symbolic")
        headerbar.pack_end(self.menu_button)

        menu = Gio.Menu.new()
        menu.append("About","app.about")
        menu.append("Quit","app.quit")
        self.menu_button.set_menu_model(menu)
            
        clamp = Adw.Clamp.new()
        self.mainvbox.append(clamp)
        clamp.set_halign(Gtk.Align.CENTER)
        clamp.set_valign(Gtk.Align.CENTER)
        clamp.props.hexpand = True
        clamp.props.vexpand = True
        clamp.set_maximum_size(600)
        
        frame = Gtk.Frame.new()
        frame.props.margin_top    = 5
        frame.props.margin_bottom = 5
        frame.props.margin_start  = 5
        frame.props.margin_end    = 5
        clamp.set_child(frame)
        frame.add_css_class("card")
        
        framebox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing = 15)
        frame.set_child(framebox)
        
        self.start_stop_timer_button = Gtk.Button.new()
        self.start_stop_timer_button.set_name("startrecordbutton")
        self.start_stop_timer_button.props.margin_top    = 50
        self.start_stop_timer_button.props.margin_bottom = 10
        self.start_stop_timer_button.set_halign(Gtk.Align.CENTER)
        self.start_stop_timer_button.set_valign(Gtk.Align.CENTER)
        self.start_stop_timer_button.add_css_class("circular")
        self.start_stop_timer_button.add_css_class("flat")
        self.start_stop_timer_button.connect("clicked",self.on_start_stop_button_clicked)
        framebox.append(self.start_stop_timer_button)
        
        self.time_label = Gtk.Label.new()
        self.time_label.add_css_class("title-2")
        self.time_label.props.margin_top    = 30
        self.time_label.props.margin_bottom = 50
        self.time_label.set_halign(Gtk.Align.CENTER)
        self.time_label.set_valign(Gtk.Align.CENTER)
        self.time_label.props.label = "00:00:00"
        framebox.append(self.time_label)
        
    def change_time(self):
        self.time_label.props.label = time.strftime("%H:%M:%S",time.gmtime(time.time() - self.old_time))
        return True # return True to continue false to break timeout_add
        
    def on_start_stop_button_clicked(self,button):
        if button.get_name() == "startrecordbutton":
            button.set_name("stoprecordbutton")
            self.old_time  = time.time()
            self.source_tag = GLib.timeout_add(500,self.change_time)
        else:
            GLib.source_remove(self.source_tag)
            button.set_name("startrecordbutton")

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        
    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application=self)
            self.win.present()
            
    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Timer',
                                application_icon='com.github.yucefsourani.python-gtk4-examples',
                                developer_name='youssef sourani',
                                version='1.0',
                                developers=['youssef sourani'],
                                copyright='© 2023 youssef sourani',
                                comments = "Timer",
                                license_type =  Gtk.License.GPL_3_0 ,
                                website = "https://github.com/yucefsourani/python-gtk4-examples",
                                issue_url = "https://github.com/yucefsourani/python-gtk4-examples/issues")
        about.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

app = MyApp(application_id="com.github.yucefsourani.python-gtk4-examples",flags= Gio.ApplicationFlags.FLAGS_NONE)
app.run(sys.argv)
