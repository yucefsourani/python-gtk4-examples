# Gtk.ListBox
# Gtk.SearchBar

```python
import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,Gio


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.app_ = self.get_application()
        self.set_default_size(800, 600)
        
        show_searchbar_action =  Gio.SimpleAction.new("show_searchbar")
        show_searchbar_action.connect("activate",self.on_show_searchbar_action_actived)
        
        self.app_.add_action(show_searchbar_action)
        self.app_.set_accels_for_action("app.show_searchbar",["<Ctrl>F"])
        
        self.main_box = Gtk.Box.new( Gtk.Orientation.VERTICAL,0)
        self.set_child(self.main_box)

        self.searchentry = Gtk.SearchEntry.new()
        self.searchentry.connect("search_changed",self.on_search_entry_changed)
        
        self.searchbar = Gtk.SearchBar.new()
        self.searchbar.props.hexpand = True
        self.searchbar.props.vexpand = False
        self.searchbar.connect_entry(self.searchentry)
        self.searchbar.set_child(self.searchentry)
        self.searchbar.set_key_capture_widget(self)
        self.main_box.append(self.searchbar)
        
        self.listbox = Gtk.ListBox.new()
        self.listbox.props.hexpand = True
        self.listbox.props.vexpand = True
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.set_show_separators(True)
        self.main_box.append(self.listbox)

            
        for i in ("Beirut","Saida","Lebanon","Palestine","Tripoli","Syria","Jordan","Iraq","Ksa","kuwait","Egypt","Oman"):
            row_hbox  = Gtk.Box.new( Gtk.Orientation.HORIZONTAL,0)
            row_hbox.MYTEXT = i # to filter later
            self.listbox.append(row_hbox)

            label = Gtk.Label.new(i)
            label.props.margin_start = 5
            label.props.hexpand = True
            label.set_halign(Gtk.Align.START)
            label.set_selectable(True)
            row_hbox.append(label)
            
            image = Gtk.Image.new_from_icon_name("contact-new-symbolic")
            image.props.margin_end = 5
            image.set_halign(Gtk.Align.END)
            row_hbox.append(image)
            
        self.listbox.set_filter_func(self.on_filter_invalidate)

    def on_show_searchbar_action_actived(self,action,parameter):
        self.searchbar.set_search_mode(True) # Ctrl+F To Active show_searchbar and show searchbar
        
    def on_search_entry_changed(self,searchentry):
        """The filter_func will be called for each row after the call, 
        and it will continue to be called each time a row changes (via [method`Gtk`.ListBoxRow.changed]) 
        or when [method`Gtk`.ListBox.invalidate_filter] is called. """
        self.listbox.invalidate_filter() # run filter (run self.on_filter_invalidate look at self.listbox.set_filter_func(self.on_filter_invalidate) )
        
    def on_filter_invalidate(self,row):
        text_to_search = self.searchentry.get_text().strip() # get text from searchentry and remove space from start and end
        if text_to_search.lower() in row.get_child().MYTEXT.lower(): # == row_hbox.MYTEXT (Gtk.ListBoxRow===>get_child()===>row_hbox.MYTEXT)
            return True # if True Show row
        return False 
                
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

![Alt text](https://raw.githubusercontent.com/yucefsourani/python-gtk4-examples/main/listbox_searchbar/Screenshot.png "Screenshot")

[Gtk.ListBox](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/ListBox.html)

[Gtk.SearchBar](https://lazka.github.io/pgi-docs/#Gtk-4.0/classes/SearchBar.html)
