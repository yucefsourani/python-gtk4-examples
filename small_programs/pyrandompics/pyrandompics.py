#!/usr/bin/env python3
#
#  
#  Copyright 2023 yucef sourani <youssef.m.sourani@gmail.com>
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
gi.require_version('Soup', '3.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk,Gio,GdkPixbuf,GLib,Gdk,Soup,Adw
import dbus
import os

DOWNLOAD_LOCATION = os.path.join(GLib.get_user_special_dir( GLib.UserDirectory.DIRECTORY_PICTURES),"Randomwallpapers")
GLib.mkdir_with_parents(DOWNLOAD_LOCATION,0o777)


class CProxy():
    def __init__(self,name,object_path,interface_name):
        self.__name            = name
        self.__object_path     = object_path
        self.__interface_name  = interface_name
        self.bus               = dbus.SessionBus()
        self.__main_object     = self.bus.get_object(self.__name,self.__object_path)

    def get_method(self,method_name,interface = None):
        if not interface:
            interface = self.__interface_name
        return self.__main_object.get_dbus_method(method_name,interface)

            
class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.set_default_size(800, 600)
        self.proxy = CProxy("org.freedesktop.portal.Desktop",
                            "/org/freedesktop/portal/desktop",
                            "org.freedesktop.portal.Wallpaper")
                                                    
        self.current_pixbuf = None
        
        self.mainvbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing = 5)
        self.set_content(self.mainvbox)

        headerbar = Gtk.HeaderBar.new()
        headerbar.set_title_widget(Gtk.Label.new("Pyrandompics"))
        self.mainvbox.append(headerbar)
        
        self.size_label = Gtk.Label.new()
        self.size_label.add_css_class("success")
        self.size_label.add_css_class("title-4")
        self.size_label.add_css_class("dim-label")
        headerbar.pack_start(self.size_label)
        
        self.get_button = Gtk.Button.new_from_icon_name("media-playlist-shuffle-symbolic")
        self.get_button.connect("clicked",self.on_get_button_clicked)
        headerbar.pack_end(self.get_button)
        
        self.menu_button = Gtk.MenuButton.new()
        self.menu_button.set_icon_name("open-menu-symbolic")
        headerbar.pack_end(self.menu_button)

        setbackground_action = Gio.SimpleAction.new("background")
        setbackground_action.connect("activate",self.on_action_active)
        self.add_action(setbackground_action)
        setlockscreen_action = Gio.SimpleAction.new("lockscreen")
        setlockscreen_action.connect("activate",self.on_action_active)
        self.add_action(setlockscreen_action)
        download_action = Gio.SimpleAction.new("download")
        download_action.connect("activate",self.on_action_active)
        self.add_action(download_action)

        menu = Gio.Menu.new()
        menu.append("Set as Background","win.background")
        menu.append("Set as LockScreen","win.lockscreen")
        menu.append("Download","win.download")
        menu.append("About","app.about")
        menu.append("Quit","app.quit")
        self.menu_button.set_menu_model(menu)
        
        self.__link = "https://source.unsplash.com/random/"
        self.msg     = Soup.Message.new("GET",self.__link)
        self.session = Soup.Session.new()

        listbox = Gtk.ListBox.new()
        listbox.props.margin_start = 1
        listbox.props.margin_end = 1
        self.entry = Adw.EntryRow.new()
        listbox.append(self.entry)
        self.entry.set_title("Enter Keywords...")
        self.entry.set_enable_undo(True)
        self.entry.set_max_width_chars(40)
        self.mainvbox.append(listbox)

        self.toastoverlay = Adw.ToastOverlay.new()
        self.mainvbox.append(self.toastoverlay)
        
        icon_theme     = Gtk.IconTheme.new()
        icon_paintable = icon_theme.lookup_icon("image-missing",["image-x-generic","folder-pictures","preferences-desktop-wallpaper"],512,1,self.get_direction(),Gtk.IconLookupFlags.FORCE_SYMBOLIC )
        self.picture   = Gtk.Picture.new()
        self.picture.set_paintable(icon_paintable )
        
        self.picture.add_css_class("osd")
        self.picture.props.hexpand = True
        self.picture.props.vexpand = True
        self.toastoverlay.set_child(self.picture)
        
    def on_action_active(self,action,p):
        if self.current_pixbuf:
            file_location_to_save = os.path.join(DOWNLOAD_LOCATION,self.current_pixbuf.__file_name)
            if not self.current_pixbuf.savev(file_location_to_save,self.current_pixbuf.__picture_type,None,None):
                self.toastoverlay.add_toast(Adw.Toast(title="Save File Faild",timeout=2))
                return
            action_name = action.get_name()
            if action_name != "download":
                with open(file_location_to_save) as wallpaper_file:
                    self.proxy.get_method("SetWallpaperFile")("",wallpaper_file.fileno(),{"show-preview" : False ,"set-on" : action_name})
            self.toastoverlay.add_toast(Adw.Toast(title="Done",timeout=2))
            
    def on_get_button_clicked(self,get_button):
        get_button.set_sensitive(False)
        keywords = self.entry.get_text().strip()
        if keywords:
            self.__link = "https://source.unsplash.com/random/?{}".format(keywords)
        else:
            self.__link = "https://source.unsplash.com/random/"
        self.msg  = Soup.Message.new("GET",self.__link)
        self.session.send_async(self.msg,GLib.PRIORITY_LOW,None,self.on_connect_finish,None)
        
    def on_connect_finish(self,session, result, data):
        try:
            input_stream = session.send_finish(result)
            self.loader = GdkPixbuf.PixbufLoader.new_with_mime_type(self.msg.props.response_headers.get_content_type()[0])
            self.loader.connect("area_updated",self.on_update)
            self.loader.connect("area-prepared",self.on_prepared)
            input_stream.read_bytes_async(1024*500,GLib.PRIORITY_HIGH_IDLE  ,None,self.on_read_finish)
        except Exception as e:
            self.get_button.set_sensitive(True)
            self.size_label.set_label("")
            self.toastoverlay.add_toast(Adw.Toast(title="Connect Faild",timeout=0)) #If timeout is 0, the toast is displayed indefinitely until manually dismissed
            print(e)
            
    def on_read_finish(self,input_stream, result):
        try:
            chunk = input_stream.read_bytes_finish(result)
            if chunk.get_size()>0:
                self.loader.write_bytes(chunk)
                input_stream.read_bytes_async(1024*500,GLib.PRIORITY_HIGH_IDLE  ,None,self.on_read_finish)
            else:
                self.current_pixbuf = self.loader.get_pixbuf()
                self.current_pixbuf.__picture_type = self.msg.props.response_headers.get_one("Content-Type").split("/")[1]
                self.current_pixbuf.__file_name = self.msg.props.response_headers.get_one("x-imgix-id")+"."+self.current_pixbuf.__picture_type
                self.size_label.set_label("{}X{}".format(self.current_pixbuf.get_width(),self.current_pixbuf.get_height()))
                self.loader.close()
                input_stream.close()
                self.get_button.set_sensitive(True)
        except Exception as e:
            self.get_button.set_sensitive(True)
            self.size_label.set_label("")
            self.toastoverlay.add_toast(Adw.Toast(title="Get File Faild",timeout=0))
            print(e)
            try:
                self.loader.close()
                input_stream.close()
            except Exception as e:
                pass
            print(e)
            
    def on_prepared(self,pixbuf_loader):
        pixbuf = pixbuf_loader.get_pixbuf()
        pixbuf.fill(0xaaaaaaff)
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.picture.set_paintable(texture)
            
    def on_update(self,pixbuf_loader, x, y, width, height):
        pixbuf = pixbuf_loader.get_pixbuf()
        texture = Gdk.Texture.new_for_pixbuf(pixbuf)
        self.picture.set_paintable(texture)
            
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
                                application_name='Pyrandompics',
                                application_icon='com.github.yucefsourani.pyrandompics',
                                developer_name='youssef sourani',
                                version='1.0',
                                developers=['youssef sourani'],
                                copyright='© 2023 youssef sourani',
                                comments = "Get Random Pictures From\n<a href='https://unsplash.com'>https://unsplash.com</a>\n",
                                license_type =  Gtk.License.GPL_3_0 ,
                                website = "https://github.com/yucefsourani/pyrandompics",
                                issue_url = "https://github.com/yucefsourani/pyrandompics/issues")
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

app = MyApp(application_id="com.github.yucefsourani.pyrandompics",flags= Gio.ApplicationFlags.FLAGS_NONE)
app.run(sys.argv)
