import os
import sys

app_path = str(os.path.dirname(os.path.abspath(sys.argv[0])))

tftpd_path = os.path.join(app_path, "tftpd")

tftpd_svc_name = 'tftpd64_svc.exe'

tftpd_svc_path = os.path.join(tftpd_path, tftpd_svc_name)

tftpd_cfg_path = os.path.join(tftpd_path, 'tftpd32.ini')

#default_cfg_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Configs')
default_cfg_path = os.path.join(app_path, 'configs')

tftpd_strg_path = ''

tftpd_imprint_sha1 = 'a2c2c0912f9632024245007083b0f75c4d520afe'


def config_device(port):
    return {
        "device_type": "cisco_ios_serial",
        "serial_settings": {"port": port.device},
        "username": "admin",
        "password": "",
        'global_delay_factor': 3,
        "secret": ''
    }


dev_type = ''
connect = ''