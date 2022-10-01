# Gtk.Stack

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

        self.headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(self.headerbar)
        add_random_label_button = Gtk.Button.new_from_icon_name("list-add-symbolic")
        add_random_label_button.connect("clicked",self.on_add_random_label_button_clicked)
        add_random_label_button.set_tooltip_text("Add Random Label")
        self.headerbar.pack_start(add_random_label_button)
                                                 
        self.main_box = Gtk.Box.new( Gtk.Orientation.HORIZONTAL,0) #(orientation VERTICAL|HORIZONTAL  , spacing in pixels)
        self.set_child(self.main_box)

        
        self.stack = Gtk.Stack.new()
        self.stack.props.hexpand = True
        self.stack.props.vexpand = True
        categories = ("Internet","Graphics")

        for category in categories:
            sw  = Gtk.ScrolledWindow.new()
            box = Gtk.Box.new( Gtk.Orientation.VERTICAL,0)
            sw.set_child(box)
            self.stack.add_titled(sw,category,category) # Widget,name,title to show in Gtk.StackSidebar
            
        stack_switcher_sidebar =  Gtk.StackSidebar.new()
        stack_switcher_sidebar.props.hexpand = False
        stack_switcher_sidebar.props.vexpand = False
        stack_switcher_sidebar.set_stack(self.stack)
        
        self.main_box.append(stack_switcher_sidebar)
        self.main_box.append(self.stack)

    def on_add_random_label_button_clicked(self,button):
        visible_box        = self.stack.get_visible_child().get_child().get_child() # Gtk.ScrolledWindow ===> get_child ====> Gtk.Viewport ===> get_child ====> Gtk.Box
        visible_child_name = self.stack.get_visible_child_name() # name look at self.stack.add_titled
        print(visible_box)
        print(visible_child_name)
        
        visible_box.append(Gtk.Label.new(visible_child_name))
        
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/stack/Screenshot.png "Screenshot")

[Gtk.Stack](https://amolenaar.github.io/pgi-docgen/index.html#Gtk-4.0/classes/Stack.html)
