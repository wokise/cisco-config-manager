import configparser
import hashlib
import os
import socket
import subprocess
from datetime import datetime

import netmiko

import psutil
import config as cfg
from dropper import dropper
from dropper.tftpd_cfg_b64 import tftpd_cfg_base64
from dropper.tftpd_svc_b64 import tftpd_svc_base64

import cserial
import serial
import sys

alph = {
    ' ': '-',
    ',': '',
    '.': '-',
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'yo',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': 'y',
    'ы': 'y',
    'ь': "'",
    'э': 'e',
    'ю': 'yu',
    'я': 'ya'
}


def latina_to_cyrillic(keyword):
    res = ''
    for symbol in keyword:
        symbol = symbol.lower()
        if symbol in alph:
            symbol = alph.get(symbol)
        res += symbol
    return res


def get_my_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return str(local_ip)


def find_proc_by_name(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            return proc.as_dict(attrs=['pid', 'name'])
    return False


def get_serv_status():
    server_status = find_proc_by_name(cfg.tftpd_svc_name)
    return {
        True: 'запущен',
        False: 'выключен'
    }.get(server_status)


def get_config_files():
    config_files = []
    for addr, dirs, dir_files in os.walk(cfg.tftpd_strg_path):
        config_files = [file for file in dir_files if file.endswith('.cfg')]
    return config_files


def update_config():
    tftpd_conf = configparser.ConfigParser()
    tftpd_conf.read(cfg.tftpd_cfg_path)

    pc_loc_ip = get_my_ip()

    tftpd_conf['TFTPD32']['localip'] = pc_loc_ip
    tftpd_conf['TFTPD32']['basedirectory'] = cfg.tftpd_strg_path

    with open(cfg.tftpd_cfg_path, 'w') as configfile:
        tftpd_conf.write(configfile)


def tftpd_run():
    update_config()
    sha1 = get_file_sha1(cfg.tftpd_svc_path)
    if sha1 != cfg.tftpd_imprint_sha1:
        return
    SW_MINIMIZE = 6
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_MINIMIZE
    subprocess.Popen(cfg.tftpd_svc_path + ' -debug', startupinfo=info)


def get_file_sha1(file):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def tftpd_stop():
    server_status = find_proc_by_name(cfg.tftpd_svc_name)
    psutil.Process(server_status['pid']).terminate()


def search_port(name):
    pac = ''
    ports = serial.tools.list_ports.comports()
    for port in ports:
        desc = port.description
        if name in desc:
            pac = port
            break
    if pac:
        return pac.name
    else:
        return pac


def get_hard_status():
    com_port = search_port('Prolific')
    if com_port:
        return 'активно'
    else:
        return 'отсутствует'


def device_connect(config):
    conn = netmiko.ConnectHandler(**config)
    conn.enable()
    return conn


def connect_serial(com):
    console = serial.Serial(
        port=com,
        baudrate=9600,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=cserial.READ_TIMEOUT
    )
    if not console.isOpen():
        sys.exit()
    cserial.login(console)
    return console


def get_hard_type(conn):
    device = ''
    ident_list = {
        'access-expression': 'router',
        'beep': 'switch'
    }
    config = conn.send_command('show ?')
    for tech in ident_list:
        if tech in config:
            device = ident_list[tech]
            break
    return device


def identify_device(console):
    device = ''
    ident_list = {
        'accounting': 'router',
        'caaa': 'switch'
    }
    config = str(cserial.send_command(console, cmd='show ?'))
    for tech in ident_list:
        if tech in config:
            device = ident_list[tech]
            break
    return device


def get_hard_name():
    return ''


def save_config(console, pc_ip, filename):
    cserial.login(console)
    cserial.send_command(console, cmd='enable')
    cserial.send_command(console, cmd=f'copy nvram:startup-config tftp://{pc_ip}/{filename}')
    cserial.send_command(console, cmd='\r\n')


def load_config(console, pc_ip):
    from gui import cfg_frame
    cserial.login(console)
    filename = cfg_frame.cfg_lst.get(cfg_frame.cfg_lst.curselection())
    cserial.send_command(console, cmd=f'configure replace tftp://{pc_ip}/{filename}\rY')


def get_current_date(format):
    today = datetime.now()
    return today.strftime(format)


def tftpd_create_if_not_exists():
    # Проверка наличия папки tftpd
    if not os.path.exists(cfg.tftpd_path):
        os.makedirs(cfg.tftpd_path)

    # Проверка наличия сервера tftpd
    if not os.path.exists(cfg.tftpd_svc_path):
        dropper.drop_file(cfg.tftpd_svc_path, tftpd_svc_base64)

    # Проверка наличия конфига tftpd
    if not os.path.exists(cfg.tftpd_cfg_path):
        dropper.drop_file(cfg.tftpd_cfg_path, tftpd_cfg_base64)

    tftpd_conf = configparser.ConfigParser()
    tftpd_conf.read(cfg.tftpd_cfg_path)

    cfg.tftpd_strg_path = os.path.normpath(tftpd_conf['TFTPD32']['basedirectory'])
    if not os.path.exists(cfg.tftpd_strg_path):
        cfg.tftpd_strg_path = cfg.default_cfg_path
        os.makedirs(cfg.tftpd_strg_path)
        tftpd_conf['TFTPD32']['basedirectory'] = cfg.tftpd_strg_path
        with open(cfg.tftpd_cfg_path, 'w') as configfile:
            tftpd_conf.write(configfile)
    else:
        cfg.tftpd_strg_path = os.path.normpath(tftpd_conf['TFTPD32']['basedirectory'])