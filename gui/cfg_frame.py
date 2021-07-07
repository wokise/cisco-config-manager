import getpass
import tkinter as tk

import func
import gui.ui_resources as ui
from tkinter import messagebox as msg_box
import config as cfg

""""""
def save_cfg_event():
    pc_loc_ip = func.get_my_ip()
    curr_date = func.get_current_date('%d-%m-%Y_%H-%M')
    curr_user = func.latina_to_cyrillic(getpass.getuser())
    filename = '_'.join([cfg.dev_type, curr_user, curr_date, '.cfg']).replace('_.', '.')
    func.save_config(cfg.connect, pc_loc_ip, filename)
    msg_box.showinfo("Сохранить", "Конфигурация успешно сохранена")


def load_cfg_event():
    pc_loc_ip = func.get_my_ip()
    func.load_config(cfg.connect, pc_loc_ip)
    msg_box.showinfo("Сохранить", "Конфигурация успешно загружена")


cfg_frame = tk.LabelFrame(text="Конфигурации", font=ui.head_font)
cfg_frame.pack(padx=10, pady=5, ipady=7, fill=tk.X, side=tk.LEFT, anchor=tk.NE)


cfg_lst = tk.Listbox(cfg_frame, width=40, height=5)
cfg_lst.pack(padx=5, pady=5)


cfg_save_btn = tk.Button(cfg_frame, text='Сохранить', width=8, height=1, font=ui.main_font, command=save_cfg_event)
cfg_save_btn.pack(padx=6, side=tk.LEFT)

cfg_load_btn = tk.Button(cfg_frame, text='Загрузить', width=8, height=1, font=ui.main_font, command=load_cfg_event)
cfg_load_btn.pack(padx=6, side=tk.RIGHT)