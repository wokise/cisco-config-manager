import threading
from time import sleep

import config as cfg
from gui import hard_frame, prgrs_frame
from gui.cfg_frame import cfg_lst
import tkinter as tk
import func
import gui.tftp_frame as tftp_frame
import gui.ui_resources as ui


def update_server_status():
    server_status = func.find_proc_by_name(cfg.tftpd_svc_name)
    if server_status:
        tftp_frame.tftp_tgl_btn.configure(image=ui.stop_img, command=func.tftpd_stop)
        tftp_frame.tftp_strg_edt_btn.configure(state=tk.DISABLED)
        tftp_frame.tftp_stat_var.set('активен')
    else:
        tftp_frame.tftp_tgl_btn.configure(image=ui.start_img, command=func.tftpd_run)
        tftp_frame.tftp_strg_edt_btn.configure(state=tk.ACTIVE)
        tftp_frame.tftp_stat_var.set('выключен')


def update_config_list():
    config_files = func.get_config_files()
    listbox_files = list(cfg_lst.get(0, tk.END))
    if listbox_files != config_files:
        cfg_lst.delete(0, tk.END)
        for filename in config_files:
            cfg_lst.insert(tk.END, filename)


def update_hard_frame():
    com = func.search_port('Prolific')
    if com:
        cfg.connect = func.connect_serial(com)
        cfg.dev_type = func.identify_device(cfg.connect)

        hard_frame.hard_stat_var.set('активно')
        hard_frame.hard_name_var.set(com)
        hard_frame.hard_type_var.set(cfg.dev_type)
        prgrs_frame.prgrs_bar['value'] = 100

    else:
        hard_frame.hard_stat_var.set('отсутствует')
        hard_frame.hard_name_var.set('не определен')
        hard_frame.hard_type_var.set('неизвестно')
        prgrs_frame.prgrs_bar['value'] = 0


def update_ui():
    while True:
        update_server_status()
        update_config_list()
        sleep(0.1)


def update_uiloop():
    threading.Thread(target=update_ui).start()
    threading.Thread(target=update_hard_frame).start()