# pyscanbc.py
#
# Copyright 2023 youssef sourani
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
# Requires packages gstreamer1-plugins-bad-free-zbar    gstreamer1-plugin-gtk4 (in fedora 39 repos)

import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gst,Gtk,Gio,Adw,GObject,Gdk
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import os
import sys


DBusGMainLoop(set_as_default=True)
  
Gst.init(None)

request_iface = 'org.freedesktop.portal.Request'
session_iface = 'org.freedesktop.portal.Session'

class CProxy():
    def __init__(self,name,object_path,interface_name):
        self.__name            = name
        self.__object_path     = object_path
        self.__interface_name  = interface_name
        self.bus               = dbus.SessionBus()
        
        self.__main_object     = self.bus.get_object(self.__name,self.__object_path)
        self.__props_interface = dbus.Interface(self.__main_object,"org.freedesktop.DBus.Properties")
        
        self.__token_temp      = 0
        self.unique_name       = self.bus.get_unique_name().replace(":","").replace(".","_")
        self.create_token()
        
    def create_token(self):
        self.token         = os.path.basename(__file__).replace(":","").replace(".","_")+ str(self.__token_temp)
        self.__token_temp += 1
        return self.token

    def get_method(self,method_name,interface = None):
        if not interface:
            interface = self.__interface_name
        return self.__main_object.get_dbus_method(method_name,interface)

    def get_props(self,props):
        return self.__props_interface.Get(self.__interface_name,props)
        
    def connect_to_request_response(self,path_name,callback):
        return self.bus.add_signal_receiver(handler_function=callback,
            bus_name=self.__name,
            dbus_interface=request_iface,
            signal_name="Response",
            path_keyword=path_name)


class BarCode(Gtk.Widget):
    __gsignals__ = { "barcode"            : (GObject.SignalFlags.RUN_LAST, None, (str,)),
                     "eos"                : (GObject.SignalFlags.RUN_LAST, None, ()),
                     "stopped"            : (GObject.SignalFlags.RUN_LAST, None, ()),
                     "playing"            : (GObject.SignalFlags.RUN_LAST, None, ()),
                     "warning"            : (GObject.SignalFlags.RUN_LAST, None, (str,str)),
                     "error"              : (GObject.SignalFlags.RUN_LAST, None, (str,str)),
                     "permission_camera"  : (GObject.SignalFlags.RUN_LAST, None, (bool,)),
                     "permission_device"  : (GObject.SignalFlags.RUN_LAST, None, (bool,)),
                     "camera_present"     : (GObject.SignalFlags.RUN_LAST, None, (bool,))
    }
    def __init__(self,parent,temp_icon_file="scanner-symbolic",w=0,h=0):
        Gtk.Widget.__init__(self)
        self.props.vexpand    = True
        self.props.hexpand    = True
        self.__parent         = parent
        self.w                = w
        self.h                = h
        self.__temp_icon_file = temp_icon_file
        self.dp = CProxy("org.freedesktop.portal.Desktop","/org/freedesktop/portal/desktop","org.freedesktop.portal.Device")
        self.cp = CProxy("org.freedesktop.portal.Desktop","/org/freedesktop/portal/desktop","org.freedesktop.portal.Camera")

        self.player = Gst.parse_launch("pipewiresrc name=pipewiresrc ! videoconvert ! zbar attach-frame=true ! videoconvert  ! gtk4paintablesink name=gtk4")
        self.pipewiresrc       = self.player.get_by_name('pipewiresrc')
        self.gtk4paintablesink = self.player.get_by_name('gtk4')
        self.gtk4paintables    = self.gtk4paintablesink.props.paintable
        
        if self.__temp_icon_file:
            self.__use_icon = True
            if os.path.isfile(self.__temp_icon_file):
                self.__mediafile = Gtk.MediaFile.new_for_filename(self.__temp_icon_file)
                self.__mediafile.set_loop(True)
                self.__mediafile.play()
            else:
                icon_theme       = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
                icon             = icon_theme.lookup_icon(self.__temp_icon_file,["applications-accessories"],self.w,1, self.__parent.get_direction(), Gtk.IconLookupFlags(1)  )
                self.__mediafile = Gtk.MediaFile.new_for_file(icon.props.file)
                self.__mediafile.set_loop(True)
                self.__mediafile.play()
        else:
            self.__use_icon = False
        self.pipbus = self.player.get_bus()
        self.pipbus.add_signal_watch()
        self.pipbus.connect("message", self.__bus_call)

        self.gtk4paintables.connect("invalidate_contents",lambda *a : self.queue_draw())
        self.gtk4paintables.connect("invalidate_size",lambda *a : self.queue_draw())
        

        
    def init(self):
        if self.cp.get_props("IsCameraPresent"):
            self.emit("camera_present",True)
            self.access_device()
        else:
            self.emit("camera_present",False)

    def access_device(self):
        request = self.dp.get_method("AccessDevice")(os.getpid(),["camera"],{"handle_token": self.dp.create_token()})
        self.dp.last_signal = self.dp.connect_to_request_response(request,self.on_access_device_done)

    def on_access_device_done(self,*aa,**bb):
        self.dp.last_signal.remove()
        if aa[0] == 0:
            self.emit("permission_device",True)
            self.access_camera()
        else:
            self.emit("permission_device",False)
            
    def do_snapshot(self,snapshot):
        if self.w == 0 :
            w = self.__parent.get_width()
        else:
            w = self.w
        if self.h == 0 :
            h = self.__parent.get_height()
        else:
            h = self.h
        if self.__use_icon :
            self.__mediafile.snapshot(snapshot,w,h)
        else:
            self.gtk4paintables.snapshot(snapshot,w,h)

    def play(self):
        self.__use_icon = False
        self.player.set_state(Gst.State.PLAYING)
        self.emit("playing")
        
    def stop(self):
        if self.__temp_icon_file:
            self.__use_icon = True
        self.player.set_state(Gst.State.NULL )
        self.emit("stopped")
        
    def access_camera(self):
        request = self.cp.get_method("AccessCamera")({"handle_token": self.cp.create_token()})
        self.cp.last_signal= self.cp.connect_to_request_response(request,self.on_access_camera_done)

    def on_access_camera_done(self,*aa,**bb):
        self.cp.last_signal.remove()
        if aa[0] == 0:
            self.emit("permission_camera",True)
            fd = self.cp.get_method("OpenPipeWireRemote")(dict())
            fd = fd.take()
            self.pipewiresrc.set_property('fd',fd)
        else:
            self.emit("permission_camera",False)

    def __bus_call(self,bus, message):
        if message.src.get_name() == "zbar0":
            barcode = message.get_structure().get_string("symbol")
            if barcode :
                self.emit("barcode",barcode)
        t = message.type
        if t == Gst.MessageType.EOS:
            self.emit("eos")
        elif t == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            self.emit("warning",str(err),str(debug))
            print("warning",str(err),str(debug))
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            self.emit("error",str(err),str(debug))
            print("error",str(err),str(debug))
        return True

    def do_get_request_mode(self):
        return Gtk.SizeRequestMode.CONSTANT_SIZE
        
    def do_measure(self, orientation, for_size):
        if self.w == 0 :
            w = self.__parent.get_width()
        else:
            w = self.w
        if self.h == 0 :
            h = self.__parent.get_height()
        else:
            h = self.h
        if orientation == Gtk.Orientation.HORIZONTAL:
            return (w, w, -1, -1)
        else:
            return (h, h, -1, -1)
            
class pyscanbcWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'pyscanbcWindow'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maximize()
        
        mainbox = Gtk.Box.new(orientation = Gtk.Orientation.VERTICAL,spacing=0)
        self.set_content(mainbox)
        
        headerbar = Adw.HeaderBar.new()
        headerbar.set_title_widget(Gtk.Label.new("Pyscanbc"))
        mainbox.append(headerbar)
        
        listbox = Gtk.ListBox.new()
        listbox.props.margin_start = 1
        listbox.props.margin_end   = 1
        listbox.props.margin_top    = 1
        listbox.props.margin_bottom    = 1
        mainbox.append(listbox)
        self.result_entry = Adw.EntryRow.new()
        
        copy_button = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
        copy_button.connect("clicked",self.on_copy_button_clicked)
        copy_button.add_css_class("flat")
        copy_button.add_css_class("osd")
        copy_button.add_css_class("circular")
        self.result_entry.add_suffix(copy_button)
        listbox.append(self.result_entry)
        
        self.revealer = Gtk.Revealer.new()
        self.revealer.set_transition_duration(2000)
        mainbox.append(self.revealer)
        
        self.status_label = Gtk.Label.new()
        self.revealer.set_child(self.status_label)
        
        barcode_box = Gtk.Box.new(orientation = Gtk.Orientation.HORIZONTAL,spacing=0)
        mainbox.append(barcode_box)
        self.barcode_widget = BarCode(barcode_box)
        barcode_box.append(self.barcode_widget)
        
        self.play_button = Gtk.ToggleButton.new()
        self.play_button.props.icon_name = "media-playback-start-symbolic"
        self.play_signal_handler = self.play_button.connect("toggled",self.on_toggle_play_button)
        mainbox.append(self.play_button)
        
        self.barcode_widget.connect("camera_present",self.__on_camera_present_check_done)
        self.barcode_widget.connect("permission_camera",self.__on_permission_done,"Camera")
        self.barcode_widget.connect("permission_device",self.__on_permission_done,"Camera Device")
        self.barcode_widget.connect("barcode",self.__on_barcode_detected)
        self.barcode_widget.connect("error",self.__on_stopped)
        self.barcode_widget.connect("eos",self.__on_stopped)
        self.barcode_widget.init()

    def on_copy_button_clicked(self,button):
        text = self.result_entry.get_text()
        if not text.strip():
            return
        clipboard = self.get_clipboard()
        clipboard.set_content(Gdk.ContentProvider.new_for_value(text))
        
    def on_toggle_play_button(self,play_button):
        if not play_button.props.active:
            self.barcode_widget.stop()
            play_button.props.icon_name = "media-playback-start-symbolic"
        else:
            self.barcode_widget.play()
            play_button.props.icon_name = "media-playback-stop-symbolic"
        
    def __on_camera_present_check_done(self,barcode_widget,iscamerapresent):
        if  not iscamerapresent:
            self.status_label.props.label = "Camera Is Not Present"
            self.status_label.add_css_class("error")
            self.revealer.props.reveal_child = True
            self.play_button.set_sensitive(False)
        
    def __on_barcode_detected(self,barcode_widget,barcode_text):
        print(barcode_text)
        self.result_entry.set_text(barcode_text)
        self.play_button.set_active(False)
        
    def __on_stopped(self,barcode_widget,error=None,debug=None):
        self.play_button.set_active(False)
        
    def __on_permission_done(self,barcode_widget,permission,name):
        if not permission:
            self.play_button.set_sensitive(False)
            self.status_label.props.label = "{} Permission Denied".format(name)
            self.status_label.add_css_class("error")
            self.revealer.props.reveal_child = True

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = pyscanbcWindow(application=self)
            self.win.present()

if __name__ == "__main__":
    app = MyApp(application_id="com.github.yucefsourani.pyscanbc",flags= Gio.ApplicationFlags.FLAGS_NONE)
    app.run(sys.argv)
