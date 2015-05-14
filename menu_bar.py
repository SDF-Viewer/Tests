from tkinter import*


class GMenu(Menu):
    def __init__(self, root, **kwargs):
        Menu.__init__(self, root, **kwargs)
        # self.FileMenu = Menu(self)
        # self.add_cascade(label='Файл', menu=self.FileMenu)
        self.ParentWindow = root
        self.set_commands()

    def set_commands(self):
        """ Отдельно вынесенный метод для простановки кнопок/каскадов горизонтального меню программы
        """

        self.add_command(label='Открыть файл', command=self.open_file)
        self.add_command(label='Выбор полей', command=self.call_field_chooser)
        self.add_command(label='Спрака', command=self.call_manual)
        # self.add_command(label='Фильтр молекул', command=self.call_mol_filter)
        # self.add_command(label='Переоткрыть исходник', command=self.call_reopen)

    def open_file(self):
        """ Вызывает диалоговое окошко askopenfilename с доступом к файлам .sdf типа,
            затем вызывает open_file главного окошка программы AppWindow.

            В случае нажатия кнопки 'Отмена' произойдет вызов от пустой строки - AppWindow.open_file('')
        """

        import tkinter.filedialog
        # добавить, чтоб только SDF видел
        open_file_name = tkinter.filedialog.askopenfilename(filetypes=(('SDF тип', '*.sdf *.SDF'),))
        # print("-------->", open_file_name)
        self.ParentWindow.open_file(open_file_name)

    def call_field_chooser(self):
        import field_chooser
        field_chooser_menu = field_chooser.FieldChooser(root=self.ParentWindow)

    def call_mol_filter(self):
        import mol_filter
        MolFilter = mol_filter.MoleculesFilter(root=self.ParentWindow)

    def call_reopen(self):
        if self.ParentWindow.WorkingFrame.MoleculesList is not None:
            self.ParentWindow.open_file(self.ParentWindow.WorkingFrame.MoleculesList.source_file_name)
        else:
            import tkinter.messagebox
            tkinter.messagebox.showerror(title='Сообщение', message='Ни один файл не был открыт')

    def call_manual(self):
        import manual
        ManualWindow = manual.Manual(root=self.ParentWindow)