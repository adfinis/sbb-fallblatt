#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import sbb_rs485
import time
from datetime import datetime

DELAY_TIME = 4

POS_A = 0
POS_E = 4
POS_Z = 25
POS_5 = 32

LOG_OK = 1
LOG_FAIL = 4

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
    ss=str(hex(ser[0]))[2:].upper() + str(hex(ser[1]))[2:].upper() + str(hex(ser[2]))[2:].upper() + str(hex(ser[3]))[2:].upper()
    return ss

def main():
    cc = sbb_rs485.PanelControl()
    cc.connect()
    cc.serial.timeout = 2
    exit = False
    while not exit:
        addr = input("Module address: {0}".format(bcolors.BOLD))
        print(bcolors.ENDC, end="")
        addr_int = int(addr)

        serial = cc.get_serial_number(addr_int)
        if len(serial)==4:
            log(LOG_OK, "reading serial ({0})".format(fmt_ser(serial)))
        else:
            log(LOG_FAIL, "reading serial")

        cc.serial.flushInput()
        cc.set_position(addr_int, POS_E)
        time.sleep(DELAY_TIME)
        cc.serial.flushInput()
        pos = cc.get_position(addr_int)
        if pos == POS_E:
            log(LOG_OK, "position E")
        else:
            log(LOG_FAIL, "position E")

        cc.serial.flushInput()
        cc.set_position(addr_int, POS_Z)
        time.sleep(DELAY_TIME)
        cc.serial.flushInput()
        pos = cc.get_position(addr_int)
        if pos == POS_Z:
            log(LOG_OK, "position Z")
        else:
            log(LOG_FAIL, "position Z")

        cc.serial.flushInput()
        cc.set_position(addr_int, POS_5)
        time.sleep(DELAY_TIME)
        cc.serial.flushInput()
        pos = cc.get_position(addr_int)
        if pos == POS_5:
            log(LOG_OK, "position 5")
        else:
            log(LOG_FAIL, "position 5")

        cc.set_position(addr_int, 0)

        print("")
        inp = input("Test another module (Y/n): ")
        if inp.lower()=="n":
            exit = True
        else:
            print("")



if __name__ == '__main__':
    main()
