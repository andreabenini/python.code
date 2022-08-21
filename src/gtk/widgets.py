import gi                               # pip install [vext|vext.gi]
gi.require_version("Gtk", "3.0")        # Must be specified to avoid warnings
from gi.repository import Gio, Gtk, Gdk


# Getting current builder from form
builder = Gtk.Builder()
builder.add_from_file("dynamic.path.to.my.file.glade")
window = builder.get_object("myFormID")
window.show_all()


# Change widget CSS properties (for example: background color)
inputBox = builder.get_object('textInput')
provider = Gtk.CssProvider()
provider.load_from_data(b"* { background: #BDBDBD; }")
inputBox.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
