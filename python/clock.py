#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sbb_rs485
import time
from datetime import datetime




def main():
    clock = sbb_rs485.PanelClockControl()
    clock.connect()
    while True:
        clock.goto_current_time()
        ts = datetime.utcnow()
        sleeptime = 60 - (ts.second + ts.microsecond/1000000.0)
        time.sleep(sleeptime)
        # less precise
        #sleeptime = 60 - datetime.utcnow().second
        #time.sleep(sleeptime)


if __name__ == '__main__':
    main()
