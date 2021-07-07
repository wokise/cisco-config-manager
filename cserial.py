import time


READ_TIMEOUT = 8


def read_serial(console):
    data_bytes = console.inWaiting()
    if data_bytes:
        return console.read(data_bytes)
    else:
        return ""


def check_logged_in(console):
    console.write(b"\r\n\r\n")
    time.sleep(1)
    prompt = str(read_serial(console))
    if '>' in prompt or '#' in prompt:
        return True
    else:
        return False


def login(console):
    login_status = check_logged_in(console)
    if login_status:
        #print("Already logged in")
        return None

    #print("Logging into router")
    while True:
        console.write(b"\r\n")
        time.sleep(1)
        input_data = read_serial(console)
        if not 'Username' in input_data:
            continue
        console.write("\r\n".encode('utf-8'))
        time.sleep(1)

        input_data = read_serial(console)
        if not 'Password' in input_data:
            continue
        console.write("\r\n".encode('utf-8'))
        time.sleep(1)

        login_status = check_logged_in(console)
        if login_status:
            #print("We are logged in\n")
            break


def logout(console):
    #print("Logging out from router")
    while check_logged_in(console):
        console.write("exit\r\n".encode('utf-8'))
        time.sleep(.5)

    print("Successfully logged out from router")


def send_command(console, cmd=''):
    if not check_logged_in(console):
        login(console)
    console.write((cmd + '\r\n').encode('utf-8'))
    time.sleep(1)
    return str(read_serial(console))