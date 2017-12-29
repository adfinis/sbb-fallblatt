#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import sbb_rs485
import sys
import time
from datetime import datetime
import argparse


def main():

    parser = argparse.ArgumentParser(description="Show text on SBB panels")
    parser.add_argument(
        '--port',
        '-p',
        help="Serial port",
        type=str,
        required=True
    )
    parser.add_argument(
        '--start',
        '-s',
        help="Start address",
        type=int,
        required=True
    )
    parser.add_argument(
        '--end',
        '-e',
        help="End address",
        type=int,
        required=True
    )
    parser.add_argument(
        '--text',
        '-t',
        help="End address",
        type=str,
        required=True
    )
    args = parser.parse_args()

    addrs = list(range(args.start,args.end+1))
    cc = sbb_rs485.PanelAlphanumControl(addresses=addrs, port=args.port )
    cc.connect()
    cc.set_text(args.text)
    cc.serial.close()
    sys.exit(0)







if __name__ == '__main__':
    main()
