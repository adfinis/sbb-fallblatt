#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import sbb_rs485
import time
from datetime import datetime


def main():
    cc = sbb_rs485.PanelClockControl()
    cc.connect()
    cc.serial.timeout = 2
    exit = False

    input("Press any key")
    msg =  b"\xFF"
    msg += CMD_ZERO
    cc.send_msg(msg)





if __name__ == '__main__':
    main()
