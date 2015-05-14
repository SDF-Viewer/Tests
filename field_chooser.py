""" Полёвщик
"""

from tkinter import *


class FieldChooser(Toplevel):
    def __init__(self, root, **kwargs):
        self.ParentWindow = root
        if self.ParentWindow.WorkingFrame.MoleculesList is not None:
            Toplevel.__init__(self, master=root, **kwargs)
            self.ParentWindow = root
            self.title("Меню выбора полей")
            self.resizable(0, 0)
            import copy
            self.input_order_list = copy.deepcopy(self.ParentWindow.WorkingFrame.showed_fields_list)
            self.union_field_list = list(self.ParentWindow.WorkingFrame.MoleculesList.get_union_fields_set())
            self.union_field_list.sort()
            self.input_working_panel_field_list = self.ParentWindow.WorkingFrame.showed_fields_list

            self.flags_list = []

            self.SetCheckForAllButton = Button(self, text='Отметить все')
            self.SelectNoneCheckButton = Button(self, text='Снять все')

            self.CheckListTable = Text(self, cursor='arrow', bg='lightgrey', width=30, height=17)
            self.TableScrollbar = Scrollbar(self, orient=VERTICAL)
            # добавить игрек скроллбар либо менять что то с гридом/размерами

            self.ApplyButton = Button(self, text='Применить')
            self.CancelButton = Button(self, text='Отмена')

            self.set_started_flags()

            self.create_scaffold()
            self.create_binding()

            self.CheckListTable.config(state=DISABLED)
            self.grab_set()
        else:
            import tkinter.messagebox
            tkinter.messagebox.showerror(title='Сообщение', message='Ни один файл не был открыт')

    def create_scaffold(self):
        self.SetCheckForAllButton.grid(row=0, column=0, sticky='e')
        self.SelectNoneCheckButton.grid(row=0, column=1, sticky='w')
        self.CheckListTable.grid(row=1, column=0, columnspan=3)
        self.TableScrollbar.grid(row=1, column=3, sticky='ns')
        self.ApplyButton.grid(row=2, column=0)
        self.CancelButton.grid(row=2, column=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=3)

        self.create_check_list_table()

    def create_check_list_table(self):
        """ Заполнение TextBox'a строками из CheckButtons, установка Scrollbar'a
        """
        self.TableScrollbar.configure(command=self.CheckListTable.yview)
        self.CheckListTable.configure(yscrollcommand=self.TableScrollbar.set)

        for i in range(len(self.union_field_list)):
            field_name = self.union_field_list[i]
            self.append_row_to_check_list_frame(field_name=field_name, index=i)

    def append_row_to_check_list_frame(self, field_name, index):
        curr_var = self.flags_list[index]
        ChButt = Checkbutton(self.CheckListTable, bg='lightgrey', text=field_name, onvalue=1, offvalue=0, variable=curr_var)
        self.CheckListTable.window_create("end", window=ChButt)
        self.CheckListTable.insert("end", "\n")

    def create_binding(self):
        self.SetCheckForAllButton.bind("<ButtonRelease-1>", self.select_all_checkbuttons)
        self.SelectNoneCheckButton.bind("<ButtonRelease-1>", self.select_none_checkbuttons)

        self.ApplyButton.bind("<ButtonRelease-1>", self.collect_flags_and_build_output_list)
        self.CancelButton.bind("<ButtonRelease-1>", lambda event: self.destroy())

    def set_started_flags(self):
        """ Устанавливает флаги тех полей, что отображались до запуска полевщика
        """
        union_field_list = self.union_field_list
        curr_showed_field_list = self.input_working_panel_field_list
        curr_int_var = IntVar()

        if curr_showed_field_list is not None:
            for i in range(len(union_field_list)):
                curr_int_var = IntVar()
                if union_field_list[i] in curr_showed_field_list:
                    curr_int_var.set(1)
                else:
                    curr_int_var.set(0)
                self.flags_list.append(curr_int_var)
        else:
            for i in range(len(union_field_list)):
                curr_int_var.set(1)
                self.flags_list.append(curr_int_var)

    def select_all_checkbuttons(self, event):
        for IntVar in self.flags_list:
            IntVar.set(1)

    def select_none_checkbuttons(self, event):
        for IntVar in self.flags_list:
            IntVar.set(0)

    def collect_flags_and_build_output_list(self, event):
        output_list = []
        for i in range(len(self.flags_list)):
            if self.flags_list[i].get() > 0:
                output_list.append(self.union_field_list[i])
        import copy
        self.ParentWindow.WorkingFrame.showed_fields_list = copy.deepcopy(output_list)
        self.ParentWindow.update_after_using_editor()
        self.destroy()