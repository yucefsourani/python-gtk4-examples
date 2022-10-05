# Gtk.AppChooserButton

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        self.set_default_size(400, 200)
                                                 
        self.main_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,0) #(orientation VERTICAL|HORIZONTAL  , spacing in pixels)
        self.set_child(self.main_box)

        app_chooser_button = Gtk.AppChooserButton.new("application/pdf")
        app_chooser_button.set_heading("PDF FILE")
        app_chooser_button.set_modal(True)
        app_chooser_button.set_show_default_item(True) # default program for application/pdf
        app_chooser_button.set_show_dialog_item(True) # enable Other application button
        app_chooser_button.append_separator()
        app_chooser_button.append_custom_item("CUSTOM","Custom",Gio.ThemedIcon.new("x-office-address-book-symbolic"))# name label icon
        app_chooser_button.connect("custom-item-activated",self.on_custom_item_activate)
        app_chooser_button.connect("changed",self.on_item_changed)
        self.main_box.append(app_chooser_button)
        
        print_selected_app_name_button = Gtk.Button.new()
        print_selected_app_name_button.props.label = "Print Selected App"
        print_selected_app_name_button.connect("clicked",self.on_print_selected_app_name_button_clicked,app_chooser_button)
        self.main_box.append(print_selected_app_name_button)

        launch_selected_app_button = Gtk.Button.new()
        launch_selected_app_button.props.label = "Launch Selected App"
        launch_selected_app_button.connect("clicked",self.on_launch_selected_app_button_clicked,app_chooser_button)
        self.main_box.append(launch_selected_app_button)
        
    def on_custom_item_activate(self,app_chooser_button,item_name):
        print(item_name) #CUSTOM

    def on_item_changed(self,app_chooser_button):
        #https://amolenaar.github.io/pgi-docgen/Gio-2.0/classes/AppInfo.html#Gio.AppInfo
        appinfo = app_chooser_button.get_app_info()
        if appinfo:
            print(appinfo.get_executable())
            print(appinfo.get_icon())
            print(appinfo.get_id())
            print(appinfo.get_name())
            print(appinfo.get_supported_types())
            print(appinfo.get_description())
            print(appinfo.get_display_name())
        
    def on_print_selected_app_name_button_clicked(self,print_selected_app_name_button,app_chooser_button):
        #https://amolenaar.github.io/pgi-docgen/Gio-2.0/classes/AppInfo.html#Gio.AppInfo
        appinfo = app_chooser_button.get_app_info()
        if appinfo:
            print(appinfo.get_executable())
            print(appinfo.get_icon())
            print(appinfo.get_id())
            print(appinfo.get_name())
            print(appinfo.get_supported_types())
            print(appinfo.get_description())
            print(appinfo.get_display_name())
            
    def on_launch_selected_app_button_clicked(self,launch_selected_app_button,app_chooser_button):
        #https://amolenaar.github.io/pgi-docgen/Gio-2.0/classes/AppInfo.html#Gio.AppInfo
        appinfo = app_chooser_button.get_app_info()
        if appinfo:
            launch_selected_app_button.set_sensitive(False)#disable button
            appinfo.launch_uris_async(None,None,None,self.on_launch_finish,launch_selected_app_button)
            #https://amolenaar.github.io/pgi-docgen/Gio-2.0/classes/AppInfo.html#Gio.AppInfo.launch_uris_async

    def on_launch_finish(self,appinfo, result,launch_selected_app_button):
        #https://amolenaar.github.io/pgi-docgen/Gio-2.0/callbacks.html#Gio.AsyncReadyCallback
        #https://amolenaar.github.io/pgi-docgen/Gio-2.0/classes/AppInfo.html#Gio.AppInfo.launch_uris_finish
        try:
            status = appinfo.launch_uris_finish(result)
            print(status)
        except Exception as e:
            print(e)
        launch_selected_app_button.set_sensitive(True)#enable button
        
class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.win = MainWindow(application=self)
            self.win.present()

app = MyApp(application_id="com.github.yucefsourani.myapplicationexample",flags= Gio.ApplicationFlags.FLAGS_NONE)
app.run(sys.argv)
```

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/appchooserbutton/Screenshot.png "Screenshot")

[Gtk.AppChooserButton](https://amolenaar.github.io/pgi-docgen/#Gtk-4.0/classes/AppChooserButton.html)
