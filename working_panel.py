from tkinter import *
from molecules_list import *
import module_ref


class WorkingPanel(Frame):
    """ Рабочая панель, объединяющая 3 фрейма для работы со списком молекул
    """

    def __init__(self, root, MoleculesList=None, **kwargs):
        """ Наследует свойства родителя, также закрепляет за собой MoleculeList,
            инициализирует 3 фрейма: рисунок молекулы, панель навигации и таблицу полей
        """
        Frame.__init__(self, root, **kwargs)

        self.active_page = 0
        self.pages_sum = 0
        self.showed_fields_list = None
        # self.ParentWindow = root
        # self.showed_mol_list = None
        # исключение
        if MoleculesList is not None:
            try:
                # self.CurrMolecule = MoleculesList.mol_list[0]
                self.change_molecules_list(MoleculesList)
            except:
                self.send_error_message()
        else:
            self.MoleculesList = None

        self.CanvasFrame = CanvasFrame(root=self)
        self.NavigationFrame = NavigationFrame(root=self)
        self.FieldsFrame = FieldsFrame(root=self)
        self.TitleFrame = TitleFrame(root=self)
        self.create_scaffold()

    def create_scaffold(self):
        """ Размещает составляющие на WorkingPanel друг под другом
        """

        self.TitleFrame.grid(row=0, column=0, sticky='wen')
        self.CanvasFrame.grid(row=1, column=0)
        self.NavigationFrame.grid(row=2, column=0, sticky='we')
        self.FieldsFrame.grid(row=3, column=0)

        self.TitleFrame.rowconfigure(0, weight=5)
        self.CanvasFrame.rowconfigure(1, weight=38)
        self.NavigationFrame.rowconfigure(2, weight=18)
        self.FieldsFrame.rowconfigure(3, weight=10)

        self.TitleFrame.fill()

    def turn_page(self, page_code):
        """ Смена отображаемого элемента списка молекул

            page_code: -1 -- next page, -2 -- previous page, 0, <-2 -- ignore, >0 -- goto page
        """
        try:
            if self.MoleculesList is not None:
                # определяем страницу, на которую нужно переключиться, исключая невозможные варианты
                if 0 < page_code <= self.pages_sum:
                    self.active_page = page_code
                    self.change_status(Molecule=self.MoleculesList.mol_list[self.active_page - 1])
                elif (page_code == -2) and (self.active_page > 1):
                    self.active_page -= 1
                    self.change_status(Molecule=self.MoleculesList.mol_list[self.active_page - 1])
                elif (page_code == -1) and (self.active_page < self.pages_sum):
                    self.active_page += 1
                    self.change_status(Molecule=self.MoleculesList.mol_list[self.active_page - 1])
                else:
                    pass
        except:
            print('Smth wrong')

    def change_status(self, Molecule=None, set_empty_status=False):
        """ Наполняет составляющие содержимым, подгружает новую молекулу
        """
        if set_empty_status is False:
            self.NavigationFrame.change_status()
            self.FieldsFrame.fill(Molecule=Molecule)
            self.CanvasFrame.scale = 1
            self.CanvasFrame.fill(Molecule=Molecule)
        else:
            self.active_page = 0
            self.pages_sum = 0
            self.MoleculesList = None
            self.NavigationFrame.change_status()
            self.TitleFrame.fill()

    def change_molecules_list(self, MoleculesList):
        """ Вызывается при смене отображаемого на панели MoleculesList
        """
        import copy
        # self.MoleculesList = MoleculesList
        self.MoleculesList = copy.deepcopy(MoleculesList)
        self.MoleculesList.mol_list = copy.deepcopy(MoleculesList.mol_list)

        self.showed_fields_list = list(self.MoleculesList.get_union_fields_set())
        self.showed_fields_list.sort()
        # self.showed_mol_list =

        self.active_page = 1
        self.pages_sum = len(MoleculesList.mol_list)
        self.NavigationFrame.fill_molecules_box()
        self.TitleFrame.fill()
        self.change_status(Molecule=self.MoleculesList.mol_list[self.active_page - 1])

    def update_after_using_editor(self):
        self.change_status(Molecule=self.MoleculesList.mol_list[self.active_page - 1])
        # self.FieldsFrame.fill(Molecule=self.MoleculesList.mol_list[self.active_page - 1])

    def send_error_message(self):
        import tkinter.messagebox
        tkinter.messagebox.showerror(title='Сообщение', message='Файл битый')


class TitleFrame(Frame):
    def __init__(self, root, **kwargs):
        Frame.__init__(self, root, **kwargs)
        self.ParentWorkingFrame = root
        self.TitleLabel = Label(self, anchor='center')
        self.fill()

        self.TitleLabel.grid(row=0, column=0, sticky='we')

    def fill(self):
        if self.ParentWorkingFrame.MoleculesList is not None:
            molecules_list_name = self.ParentWorkingFrame.MoleculesList.name # + \
                                  # self.ParentWorkingFrame.MoleculesList.source_file_name
        else:
            molecules_list_name = 'Файл не выбран'
        self.TitleLabel.configure(text=molecules_list_name)


class CanvasFrame(Frame):
    """ Фрейм, содержащий рисунок молекулы и ползунки для навигации по рисунку
    """

    def __init__(self, root, **kwargs):
        Frame.__init__(self, root, **kwargs)

        self.Canvas = Canvas(self, bg="lightyellow")
        self.scale = 1
        self.Molecule = None

        self.YScrollBar = Scrollbar(self, orient=VERTICAL)
        self.YScrollBar.config(command=self.Canvas.yview)
        self.Canvas.config(yscrollcommand=self.YScrollBar.set)

        self.XScrollBar = Scrollbar(self, orient=HORIZONTAL)
        self.XScrollBar.config(command=self.Canvas.xview)
        self.Canvas.config(xscrollcommand=self.XScrollBar.set)

        self.YScrollBar.grid(row=0, column=0, sticky='ns')
        self.XScrollBar.grid(row=1, column=1, sticky='we')
        self.Canvas.grid(row=0, column=1, sticky='we' )
        self.Canvas.config(scrollregion=(0, 0, self.Canvas.winfo_reqwidth(), self.Canvas.winfo_reqheight()))
        # self.CanvasCenter = (self.Canvas.canvasx, self.Canvas.canvasy)
        # print(self.CanvasCenter)
        self.Canvas.bind("<ButtonPress-1>", lambda event: self.Canvas.scan_mark(event.x, event.y))
        self.Canvas.bind("<B1-Motion>", lambda event: self.Canvas.scan_dragto(event.x, event.y, gain=1))
        self.Canvas.bind("<MouseWheel>", self.change_scale)

    def fill(self, Molecule=None, scale=1):
        """ Подгрузка Canvas другой молекулой / масштаббирование
        """

        if Molecule is not None:
            import copy
            MoleculeCopy = copy.deepcopy(Molecule)
            MoleculeCopy.bond_block = copy.deepcopy(Molecule.bond_block)
            MoleculeCopy.atom_block = copy.deepcopy(Molecule.atom_block)
            """ вроде бы потеряла актуальнсть: отцентровать холст! при перелистовании"""
            self.Molecule = MoleculeCopy
            self.Canvas.delete("all")
            module_ref.draw_mol(mol=MoleculeCopy, canv0=self.Canvas, scale=self.scale)
            self.Canvas.scan_mark(0, 0)

    def change_scale(self, event):
        """ Масштабирование молекулы
        """

        if event.delta == 120 and self.scale <= 15:
            self.scale += 0.5
            self.fill(Molecule=self.Molecule, scale=self.scale)
        elif event.delta == -120 and self.scale > 1:
            self.scale -= 0.5
            self.fill(Molecule=self.Molecule, scale=self.scale)


class NavigationFrame(Frame):
    """ Панель навигации
    """
    def __init__(self, root, **kwargs):
        Frame.__init__(self, root, **kwargs)

        self.ParentWorkingPanel = root
        self.PreviousPageButton = Button(self, text='<')
        self.PreviousPageButton.grid(row=0, column=0, sticky='e')

        self.NextPageButton = Button(self, text='>')
        self.NextPageButton.grid(row=0, column=1, sticky='w')

        self.PositionLabel = Label(self, text='0/0')
        self.PositionLabel.grid(row=0, column=2)

        self.GoToPageButton = Button(self, text='Перейти')
        self.GoToPageButton.grid(row=0, column=3)

        self.GoToPageEntry = Entry(self, width=5)
        self.GoToPageEntry.grid(row=0, column=4)

        # self.CallListButton = Button(self, text='Список молекул')
        # self.CallListButton.grid(row=0, column=5)
        import tkinter.ttk
        self.MoleculesBox = tkinter.ttk.Combobox(self, height=10, state='readonly')
        self.MoleculesBox.grid(row=0, column=5)

        self.columnconfigure(0, weight=8)
        self.columnconfigure(1, weight=8)
        self.columnconfigure(2, weight=8)
        self.columnconfigure(3, weight=8)
        self.columnconfigure(4, weight=4)
        self.columnconfigure(5, weight=20)

        self.set_binding()

    def change_status(self):
        """ Обработчик события 'смена страницы' для Navigation Panel

            Обновляет информацию Navigation Panel для пользователя
        """
        position_label = str(self.ParentWorkingPanel.active_page) + '/' + \
                         str(self.ParentWorkingPanel.pages_sum)
        self.PositionLabel.config(text=position_label)
        self.MoleculesBox.current(self.ParentWorkingPanel.active_page-1)

    def fill_molecules_box(self):
        curr_mol_list = self.ParentWorkingPanel.MoleculesList.mol_list
        molecules_names = [mol.header_list[0] for mol in curr_mol_list]
        self.MoleculesBox.config(values=molecules_names)

    def set_binding(self):
        """ Простановка обработчиков событий
        """
        self.NextPageButton.bind("<Button-1>", self.next_page_click)
        self.PreviousPageButton.bind("<Button-1>", self.previous_page_click)
        self.GoToPageButton.bind("<Button-1>", self.go_to_page_click)
        self.GoToPageEntry.bind("<Return>", self.go_to_page_click)
        self.MoleculesBox.bind("<<ComboboxSelected>>", self.select_from_box)

    def next_page_click(self, event):
        self.ParentWorkingPanel.turn_page(page_code=-1)

    def previous_page_click(self, event):
        self.ParentWorkingPanel.turn_page(page_code=-2)

    def go_to_page_click(self, event):
        """ Обработчик нажатия на кнопку 'Перейти'. Исключение -- ввод символов.
        """
        try:
            page = int(self.GoToPageEntry.get())
            if 0 < page <= self.ParentWorkingPanel.pages_sum:
                self.ParentWorkingPanel.turn_page(page_code=page)
        except:
            pass
        self.GoToPageEntry.delete(first=0, last='end')

    def select_from_box(self, event):
        new_page = event.widget.current() + 1
        self.ParentWorkingPanel.turn_page(new_page)
        event.widget.selection_clear()


class FieldsFrame(Frame):
    """ Таблица с информаций о содержании полей молекулы
    """
    def __init__(self, root, **kwargs):
        Frame.__init__(self, root, **kwargs)
        self.parent_working_panel = root
        import tkinter.ttk

        self.Table = tkinter.ttk.Treeview(self)
        self.Table['columns'] = ('FieldValue')
        self.Table.heading('#0', text='Название поля')
        self.Table.heading('FieldValue', text='Значение поля')
        ''' сделать что-либо, чтобы табличка не уезжала при изменении размеров'''
        self.Table.column('#0', stretch=True)
        self.Table.column('FieldValue', stretch=True)

        self.YScrollBar = Scrollbar(self)
        self.YScrollBar.config(command=self.Table.yview)
        self.Table.configure(yscrollcommand=self.YScrollBar.set)

        self.Table.grid(row=0, column=0, sticky=(N, S, E, W))
        self.YScrollBar.grid(row=0, column=1, sticky=(N, S))

    def fill(self, Molecule):
        self.Table.delete(*self.Table.get_children())
        undefault_order_list = self.parent_working_panel.showed_fields_list

        if undefault_order_list is None:
            order_list = Molecule.fill_default_field_order_list()
        else:
            order_list = undefault_order_list

        for field_name in order_list:
            try:
                # возможен key error
                field_value = Molecule.fields_dict[field_name]
                self.Table.insert('', 'end', text=field_name,
                                  values=(field_value,))
            except:
                continue