from func import tftpd_create_if_not_exists


if __name__ == '__main__':
    tftpd_create_if_not_exists()
    from gui.main_frame import root
    from gui.ui_dynamic import update_uiloop
    update_uiloop()
    root.mainloop()