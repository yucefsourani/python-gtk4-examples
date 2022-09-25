# Gtk.HeaderBar + Gtk.MenuButton

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio

MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">win.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">win.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;Q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_ = self.get_application()
        
        self.headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(self.headerbar)
        self.headerbar.set_title_widget(Gtk.Label.new("MyProgram Title")) #can use any widget
        self.headerbar.set_show_title_buttons(True) # Show|Hide Close Minimize Maximize (True by default)

        quit_action = Gio.SimpleAction.new("quit", None) # look at MENU_XML win.quit
        quit_action.connect("activate", self.on_quit_action_actived)
        self.add_action(quit_action) # (self window) == win in MENU_XML
        
        about_action = Gio.SimpleAction.new("about", None) # look at MENU_XML win.about
        about_action.connect("activate", self.on_about_action_actived)
        self.add_action(about_action) # (self window) == win in MENU_XML
        
        self.menu_button = Gtk.MenuButton.new()
        self.headerbar.pack_end(self.menu_button) # or pack_start
        menu = Gtk.Builder.new_from_string(MENU_XML, -1).get_object("app-menu")
        self.menu_button.set_icon_name("open-menu-symbolic") # from Pre-installed standard linux icon names
        #https://specifications.freedesktop.org/icon-naming-spec/latest/ar01s04.html
        self.menu_button.set_menu_model(menu)
    
    def on_about_action_actived(self, action, param=None):
        print("About")
        
    def on_quit_action_actived(self, action, param=None):
        self.app_.quit()

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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/headerbar_and_menubutton/Screenshot.png "Screenshot")



[Gtk.HeaderBar](https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/HeaderBar.html)



[Gtk.MenuButton](https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/MenuButton.html)
