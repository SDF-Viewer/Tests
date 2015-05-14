from tkinter import *


class MoleculesFilter(Toplevel):
    def __init__(self, root, **kwargs):
        self.ParentWindow = root
        if self.ParentWindow.WorkingFrame.MoleculesList is not None:
            Toplevel.__init__(self, master=root, **kwargs)
            self.ParentWindow = root
            self.title("Меню фильтра")
        else:
            import tkinter.messagebox
            tkinter.messagebox.showerror(title='Сообщение', message='Ни один файл не был открыт')