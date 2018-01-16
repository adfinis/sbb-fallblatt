#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import sbb_rs485
import sys
import time
from datetime import datetime
import subprocess

def getch():
    import termios
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log(level, message):
    if (level==1): pf="[{0}{1}{2}] ".format(bcolors.OKGREEN, "OK", bcolors.ENDC)
    if (level==4): pf="[{0}{1}{2}]".format(bcolors.FAIL, "FAIL", bcolors.ENDC)
    print("{0} {1}".format(pf, message))


def fmt_ser(ser):
    ss = str(hex(ser[0]))[2:].upper() + str(hex(ser[1]))[2:].upper() + str(hex(ser[2]))[2:].upper() + str(hex(ser[3]))[2:].upper()
    return ss


def send_msg(msg):
    print("sending: {0}".format(msg))


def print_label(serial, addr):
    cmd = [
        "ptouch-print",
        "--fontsize",
        "15",
        "--text",
        "Address: {0}".format(addr),
        "S/N: {0}".format(serial)
    ]
    subprocess.check_call(cmd)




def change_addr(cc):
    addr = input("Current module address: {0}".format(bcolors.BOLD))
    print(bcolors.ENDC, end="")
    addr = int(addr)
    changed = False
    test_ser = cc.get_serial_number(addr)
    if len(test_ser) !=4:
        print("{0}ERROR:{1} cannot connect to module".format(
            bcolors.FAIL,
            bcolors.ENDC
        ))
        if ask_for_it("Try another module"):
            sys.exit(0)
        change_addr(cc)
        return

    ser_hex = fmt_ser(test_ser)

    new_addr = input("New Module address: {0}".format(bcolors.BOLD))
    print(bcolors.ENDC, end="")
    print("Changing address from {0}{1}{2} to {0}{3}{2} on {0}{4}{2}".format(
        bcolors.BOLD,
        addr,
        bcolors.ENDC,
        new_addr,
        ser_hex
    ))

    change_addr_msg = cc.pack_msg(cc.CMD_CHANGE_ADDR, int(addr), int(new_addr))
    cc.send_msg(change_addr_msg)
    time.sleep(0.5)
    test_ser2 = cc.get_serial_number(int(new_addr))
    if len(test_ser2) == 4:
        print("{0}OK:{1} change address successful".format(
            bcolors.OKGREEN,
            bcolors.ENDC
        ))
    else:
        print("{0}ERROR:{1} cannot verify change".format(
            bcolors.FAIL,
            bcolors.ENDC
        ))

    if not ask_for_it("Print a label"):
        print_label(ser_hex, new_addr)





def ask_for_it(text):
    inp = input("{0} (Y/n): ".format(text))
    if inp.lower()=="n":
        return True
    else:
        return False



def main():
    try:
        ttyport = sys.argv[1]
    except IndexError:
        ttyport = "/dev/ttyUSB3"

    print("Using ttyport: {0}{1}{2}".format(
        bcolors.BOLD,
        ttyport,
        bcolors.ENDC
    ))
    exit = False
    cc = sbb_rs485.PanelControl(ttyport)
    cc.connect()
    cc.serial.timeout = 2


    while not exit:
        change_addr(cc)
        exit = ask_for_it("Change another module")







if __name__ == '__main__':
    main()
