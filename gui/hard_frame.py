import tkinter as tk
import gui.ui_resources as ui
import func


hard_stat = func.get_hard_status()
hard_stat_var = tk.StringVar()
hard_stat_var.set('...')

hard_name = func.get_hard_name()
hard_name_var = tk.StringVar()
hard_name_var.set('...')

hard_type = ''
hard_type_var = tk.StringVar()
hard_type_var.set('определение...')


hrd_frame = tk.LabelFrame(text="Оборудование", font=ui.head_font)
hrd_frame.pack(anchor=tk.NE, padx=10, pady=5, fill=tk.X, side=tk.TOP)


hrd_row_1 = tk.Frame(hrd_frame)
hrd_row_1.pack(anchor=tk.NW, padx=5)

hrd_cnct_h_lbl = tk.Label(hrd_row_1, text='Подключение:', font=ui.main_font)
hrd_cnct_h_lbl.pack(anchor=tk.E, pady=1, side=tk.LEFT)

hrd_cnct_stat_lbl = tk.Label(hrd_row_1, textvariable=hard_stat_var, font=ui.main_font)
hrd_cnct_stat_lbl.pack(anchor=tk.NW, padx=5)


hrd_row_2 = tk.Frame(hrd_frame)
hrd_row_2.pack(anchor=tk.NW, padx=5)

hrd_port_h_lbl = tk.Label(hrd_row_2, text='Порт:', font=ui.main_font)
hrd_port_h_lbl.pack(anchor=tk.E, pady=1, side=tk.LEFT)

hrd_port_val_lbl = tk.Label(hrd_row_2, textvariable=hard_name_var, font=ui.main_font)
hrd_port_val_lbl.pack(anchor=tk.NW, padx=5)


hrd_row_3 = tk.Frame(hrd_frame)
hrd_row_3.pack(anchor=tk.NW, padx=5)

hrd_type_h_lbl = tk.Label(hrd_row_3, text='Тип устройства:', font=ui.main_font)
hrd_type_h_lbl.pack(anchor=tk.E, pady=1, side=tk.LEFT)

hrd_type_val_lbl = tk.Label(hrd_row_3, textvariable=hard_type_var, font=ui.main_font)
hrd_type_val_lbl.pack(anchor=tk.NW, padx=5)