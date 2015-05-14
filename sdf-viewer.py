""" SDF-Viewer
"""


from tkinter import*
from working_panel import*
from menu_bar import*


class AppWindow(Tk):
    def __init__(self, **kwargs):
        ### GUI ###
        Tk.__init__(self, **kwargs)
        self.wm_title('SDF-Viewer')
        self.WorkingFrame = WorkingPanel(root=self)
        self.AppMenu = GMenu(root=self)
        self.config(menu=self.AppMenu)

        self.WorkingFrame.grid(row=0, column=0, sticky='nwes')

        self.resizable(0, 0)

        ### DATA ###
        self.open_file_name = None
        self.MoleculesListDB = []

    def open_file(self, file_name):
        self.open_file_name = file_name
        if file_name != '':
            file = open(file_name, 'tr')
            OpenMoleculeslist = extract_molecules_list_from_sdf(file, 'Source')
            if OpenMoleculeslist is not None:
                OpenMoleculeslist.source_file_name = file_name
                self.MoleculesListDB.append(OpenMoleculeslist)
                self.WorkingFrame.change_molecules_list(OpenMoleculeslist)
            else:
                import tkinter.messagebox
                tkinter.messagebox.showerror(title='Сообщение', message='Похоже, файл некорректен или не содержит '
                                                                        'молекул. Проверьте простановку "$$$$"')
            file.close()
        else:
            pass

    def update_after_using_editor(self):
        self.WorkingFrame.update_after_using_editor()


def main(argv=None):
    if argv is None:
        pass
    try:
        MainWindow = AppWindow()
        MainWindow.mainloop()
    except:
        pass


if __name__ == "__main__":
    sys.exit(main())