from tkinter import *


class Manual(Toplevel):
    def __init__(self, root, **kwargs):
        Toplevel.__init__(self, master=root, **kwargs)
        self.title("Справка")
        self.resizable(0, 0)
        file = open('manual.txt', 'tr', encoding='utf-8')
        self.file_as_string = file.read()
        file.close()

        self.TextBox = Text(self, width=100, height=35)
        self.TextBox.grid(row=0, column=0)
        self.TextBox.insert('end', self.file_as_string)
        self.TextBox.config(state=DISABLED)

        self.YScrollBar = Scrollbar(self, orient=VERTICAL)
        self.YScrollBar.grid(row=0, column=1, sticky='ns')

        self.YScrollBar.configure(command=self.TextBox.yview)
        self.TextBox.configure(yscrollcommand=self.YScrollBar.set)
