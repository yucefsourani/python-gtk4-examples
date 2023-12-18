# Gtk.ListView

```python

import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio,GObject,Gdk,GLib

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(800, 600)
        
        sw = Gtk.ScrolledWindow.new()
        self.set_child(sw)
        
        headerbar = Gtk.HeaderBar.new()
        headerbar.set_title_widget(Gtk.Label.new("Simple ListView Example"))
        self.set_titlebar(headerbar)
        
        append_button = Gtk.Button.new_from_icon_name("list-add-symbolic")
        append_button.connect("clicked",self.on_add_button_clicked)
        headerbar.pack_start(append_button)
        
        # GtkStringList is a list model that wraps an array of strings.
        # The objects in the model are of type [class`Gtk`.StringObject
        # and have a “string” property that can be used inside expressions.
        self.stringlist = Gtk.StringList.new(None) 
        
        # allows marking each item in a model as either selected or not selected
        # by wrapping a model with one of the GTK models provided for this purposes,
        # such as GtkNoSelection or GtkSingleSelection.
        self.single_selection_list_store = Gtk.SingleSelection.new(self.stringlist)
        
        # A GtkListItemFactory creates widgets for the items taken from a GListModel.
        # The GtkListItemFactory is tasked with creating widgets for items taken from the model when the views need
        # them and updating them as the items displayed by the view change.
        self.signal_factory = Gtk.SignalListItemFactory.new()


        # setup signal Emitted when a new listitem has been created and needs to be setup for use.
        self.signal_factory.connect("setup",self.on_setup)
        
        # bind signal emitted  when  [property`Gtk`.ListItem:item] has been set on a listitem and should be bound for use.
        self.signal_factory.connect("bind",self.on_object_bound_to_use) 
        
        
        # https://docs.gtk.org/gtk4/section-list-widget.html
        self.listview = Gtk.ListView.new(self.single_selection_list_store,self.signal_factory)
        sw.set_child(self.listview)
        
            
        for i in range(100):
            self.stringlist.append(str(i))

        # when 'selected' property changed
        self.single_selection_list_store.connect("notify::selected",self.on_item_list_selected)
        
    def on_setup(self,signal_factory, list_item):
        print("Setup--> Prepering Widgets Start")
        # GtkListItem is used by list widgets to represent items in a [iface`Gio`.ListModel]
        # GtkListItem objects are managed by the list widget (with its factory) and cannot be created by applications,
        # but they need to be populated by application code. This is done by calling [method`Gtk`.ListItem.set_child].
        print(list_item)
        print(list_item.props.item) # item == None
        
        label = Gtk.Label.new()
        label.set_halign(Gtk.Align.START)
        list_item.set_child(label)
        print("Setup--> Prepering Widgets End\n")
        
    def on_object_bound_to_use(self,signal_factory, list_item):
        print("Bind--> modified Widgets Start") 
        item  = list_item.props.item # item == Gtk.StringObject (Gtk.StringObject wrapping str in Gtk.StringList)
        label = list_item.get_child()# label
        label.props.label = item.props.string #https://lazka.github.io/pgi-docs/index.html#Gtk-4.0/classes/StringObject.html#Gtk.StringObject.props.string
        print("Bind--> modified Widgets End\n") 
        

    def on_item_list_selected(self,single_selection_list_store,props):
        selected_item = single_selection_list_store.props.selected_item # Gtk.StringObject
        string_value  = selected_item.props.string
        position      = single_selection_list_store.get_selected()
        print(f"Selected String   = {string_value}")
        print(f"Selected Position = {position}")

        
    def on_add_button_clicked(self,button):
        self.stringlist.append("New")
        context = GLib.MainContext().default()
        while context.pending():
            context.iteration(True)
        self.listview.scroll_to(self.stringlist.get_n_items()-1,Gtk.ListScrollFlags.FOCUS | Gtk.ListScrollFlags.SELECT  ,None)
        
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/simple_list_view_example/Screenshot.png "Screenshot")

[Gtk.ListView](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/ListView.html)

[Gtk.StringList](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/StringList.html)
