    def __dialog(self, text='', title=None, inputField=False):
        dialog = Gtk.MessageDialog(
                modal=True, destroy_with_parent=True, flags=0,
                text=text, title=title, message_type=Gtk.MessageType.INFO,
                parent = self.builder.get_object("formMain"),
                buttons = Gtk.ButtonsType.OK_CANCEL if inputField else Gtk.ButtonsType.OK
        )
        if inputField:
            dialogbox = dialog.get_content_area()
            entry = Gtk.Entry()
            entry.set_visibility(True)
            entry.set_size_request(50,0)
            dialogbox.pack_end(entry, False, False, 0)
        dialog.show_all()
        response = dialog.run()
        text = None if not inputField else entry.get_text()
        dialog.destroy()
        if inputField:
            if (response == Gtk.ResponseType.OK) and (text != ''):
                return text
        return None

    def test(self):
        # input()
        username = self.__dialog(text='Enter username', title='Username ?', inputField=True)
        # about msgbox
        self.__dialog(text="This is a MessageDialog", title='Information')
