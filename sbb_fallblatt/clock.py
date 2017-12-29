#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import sbb_rs485
import time
from datetime import datetime

SBB_MODULE_ADDR_HOUR = 82
SBB_MODULE_ADDR_MIN  = 29

def main():
    clock = sbb_rs485.PanelClockControl(
        addr_hour = SBB_MODULE_ADDR_HOUR,
        addr_min  = SBB_MODULE_ADDR_MIN
    )
    clock.connect()
    while True:
        clock.set_time_now()
        ts = datetime.utcnow()
        sleeptime = 60 - (ts.second + ts.microsecond/1000000.0)
        time.sleep(sleeptime)
        # less precise
        #sleeptime = 60 - datetime.utcnow().second
        #time.sleep(sleeptime)


if __name__ == '__main__':
    main()
