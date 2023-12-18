# Gtk.InfoBar

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

        infobar = Gtk.InfoBar.new()
        infobar.set_revealed(False) # hide
        infobar.set_show_close_button(True) # When clicked it emits the response Gtk.ResponseType.CLOSE
        infobar.add_button("Yes", Gtk.ResponseType.YES ) # Action button on side.  When clicked it emits the response Gtk.ResponseType.YES
        infobar.add_button("No", Gtk.ResponseType.NO ) # Action button on side. When clicked it emits the response Gtk.ResponseType.NO
        self.main_box.append(infobar)
        
        self.message_to_show_in_infobar = Gtk.Label.new()
        infobar.add_child(self.message_to_show_in_infobar)
        
        infobar.connect("response",self.on_infobar_action_button_clicked)
        
        install_geany_button = Gtk.Button.new()
        install_geany_button.add_css_class("suggested-action") # try add_css_class("destructive-action")
        install_geany_button.props.label = "Install Geany IDE"
        install_geany_button.connect("clicked",self.on_install_geany_button_clicked,infobar,"Yes|No Install Geany ?",["pkexe dnf install geany -y"])
        self.main_box.append(install_geany_button)

    def on_install_geany_button_clicked(self,i_geany_button,infobar,message,commands_to_run):
        self.message_to_show_in_infobar.set_label(message)
        infobar.set_message_type(Gtk.MessageType.QUESTION )
        infobar.set_revealed(True)
        infobar.commands_to_run = commands_to_run
        
    def on_infobar_action_button_clicked(self,infobar,response_id):
        if response_id == Gtk.ResponseType.CLOSE:
            print("Close Clicked")
        elif response_id == Gtk.ResponseType.YES:
            print("Yes Clicked")
            print("Running Commands {}".format(infobar.commands_to_run))
            
        elif response_id == Gtk.ResponseType.NO:
            print("No Clicked")
            print("Running Commands {} Canceled".format(infobar.commands_to_run))
            
        infobar.set_revealed(False) # hide
        
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/infobar/Screenshot.png "Screenshot")

[Gtk.InfoBar](https://lazka.github.io/pgi-docgen/index.html#Gtk-4.0/classes/InfoBar.html)
