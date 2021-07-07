import os
import tkinter as tk
from tkinter import filedialog

import func
import gui.ui_resources as ui
import config as cfg


pc_loc_ip = func.get_my_ip()
tftp_ip_var = tk.StringVar()
tftp_ip_var.set(pc_loc_ip)

serv_stat = func.get_serv_status()
tftp_stat_var = tk.StringVar()
tftp_stat_var.set(serv_stat)

tftp_strg_var = tk.StringVar()
tftp_strg_var.set(cfg.tftpd_strg_path)


def open_folder_event():
    os.startfile(cfg.tftpd_strg_path)


def edit_folder_event():
    slct_dir = filedialog.askdirectory()
    if not slct_dir:
        return
    cfg.tftpd_strg_path = slct_dir
    tftp_strg_var.set(cfg.tftpd_strg_path)
    func.update_config()


tftp_frame = tk.LabelFrame(text="TFTP-сервер", font=ui.head_font)
tftp_frame.pack(anchor=tk.NW, fill=tk.X, padx=10, pady=5)


tftp_row_1 = tk.Frame(tftp_frame)
tftp_row_1.pack(anchor=tk.NW, fill=tk.X, padx=5)

tftp_ip_h_lbl = tk.Label(tftp_row_1, text=f'IPv4:', font=ui.main_font)
tftp_ip_h_lbl.pack(anchor=tk.NE, side=tk.LEFT)

tftp_ip_val_lbl = tk.Label(tftp_row_1, textvariable=tftp_ip_var, font=ui.main_font)
tftp_ip_val_lbl.pack(anchor=tk.NE, side=tk.LEFT)

tftp_tgl_btn = tk.Button(tftp_row_1, width=22, height=22, image=ui.start_img)
tftp_tgl_btn.pack(anchor=tk.NE, padx=5, side=tk.RIGHT)


tftp_row_2 = tk.Frame(tftp_frame)
tftp_row_2.pack(anchor=tk.NW, fill=tk.X, padx=5)

tftp_stat_h_lbl = tk.Label(tftp_row_2, text='Статус:', font=ui.main_font)
tftp_stat_h_lbl.pack(anchor=tk.NE, side=tk.LEFT)

tftp_stat_val_lbl = tk.Label(tftp_row_2, textvariable=tftp_stat_var, font=ui.main_font)
tftp_stat_val_lbl.pack(anchor=tk.NW, side=tk.LEFT, padx=5)


tftp_row_3 = tk.Frame(tftp_frame)
tftp_row_3.pack(anchor=tk.NW, fill=tk.X, padx=5, pady=5)

tftp_strg_h_lbl = tk.Label(tftp_row_3, text='Хранилище:', font=ui.main_font)
tftp_strg_h_lbl.pack(anchor=tk.NW, side=tk.LEFT, pady=1)

tftp_strg_inp = tk.Entry(
    tftp_row_3, width=40, font=ui.main_font, state="readonly", 
    readonlybackground='#fff', textvariable=tftp_strg_var)
tftp_strg_inp.pack(anchor=tk.NW, padx=13, pady=4, side=tk.LEFT)

tftp_strg_edt_btn = tk.Button(
    tftp_row_3, width=22, height=22, image=ui.pencil_img,
    font=ui.main_font, command=edit_folder_event)
tftp_strg_edt_btn.pack(anchor=tk.NW, padx=8, side=tk.LEFT)

tftp_strg_opn_btn = tk.Button(tftp_row_3, width=22, height=22, image=ui.folder_img,
                              font=ui.main_font, command=open_folder_event)
tftp_strg_opn_btn.pack(anchor=tk.NW, padx=4)
