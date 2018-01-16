#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import signal
import serial
import struct
import argparse
import subprocess
from . import sbb_rs485


def unpack(data):
    return struct.unpack( "=B", data )[0]

def pack(data):
    return struct.pack( "=B", data )


parser = argparse.ArgumentParser(description="Mock an sbb panel")
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

args = parser.parse_args()
panel = sbb_rs485.PanelAlphanumControl([0,1])
plen = args.end - args.start + 1
curr_data  =  [' ']*plen

# create virtual serial device
cmd = "socat -d -d pty,raw,echo=0 pty,raw,echo=0"
proc_socat = subprocess.Popen(
    cmd,
    preexec_fn=os.setsid,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
time.sleep(1)
pty1 = str(proc_socat.stderr.readline()).split("is ")[1].strip()[:-3]
pty2 = str(proc_socat.stderr.readline()).split("is ")[1].strip()[:-3]

# init cursor
sdev = serial.Serial( pty2 )

print(chr(27) + "[2J")
print("\033[1;1HVirtual device: {0}".format( pty1 ) )
print("\033[3;1H{0}".format( ' '*plen ) )


# mainloop
msg_start = False
msg_type  = False
addr      = False

while True:
    try:
        data = sdev.read()
    except KeyboardInterrupt:
        os.killpg(os.getpgid(proc_socat.pid), signal.SIGTERM)
        sys.exit()

    if data == b'\xFF':
        msg_start = True
    if msg_start:
        if not msg_type:
            if data == b'\xc0':
                msg_type = 'set'
            if data == b'\xd0':
                msg_type = 'get'

        elif msg_type and not addr:
            addr = data

        elif msg_type=='set' and addr:
            char = panel.pos_to_str( [ unpack(data) ] )
            paddr = unpack(addr) - (args.start)
            curr_data[paddr] = char
            print("\033[3;{0}H{1}".format(paddr+1,str(char)))
            msg_start = False
            msg_type  = False
            addr      = False

        if msg_type=='get' and addr:
            paddr = unpack(addr) - args.start
            sdev.write( panel.str_to_pos(curr_data[paddr]) )
            msg_start = False
            msg_type  = False
            addr      = False

    pass
