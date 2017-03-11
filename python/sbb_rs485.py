#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import time
import serial
import struct
import datetime

from pprint import pprint


class PanelControl:

    CMD_GOTO        = b'\xC0'
    CMD_ZERO        = b'\xC5'
    CMD_STEP        = b'\xC6'
    CMD_PULSE       = b'\xC7'
    CMD_READ_POS    = b'\xD0'
    CMD_READ_SERIAL = b'\xDF'

    def __init__(self, port="/dev/ttyUSB0"):
        self.port = port

    def connect(self):
        try:
            self.serial = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=19200
            )
        except:
            print("ERROR: Opening serial port failed")
            self.serial = False
            return

    def pack_msg(self, cmd, addr, value=False):
        msg = b"\xFF"
        msg+=cmd
        msg+=struct.pack("=B", addr)
        if value:
            msg+=struct.pack("=B", value)
        return msg


    def send_msg(self, msg):
        if not self.serial:
            return
        self.serial.send_break()
        self.serial.write(msg)



class PanelClockControl(PanelControl):
    def __init__(self, port="/dev/ttyUSB0", addr_hour=82, addr_min=29):
        super().__init__(port)
        self.addr_hour = addr_hour
        self.addr_min = addr_min

    def calc_min_pos(self, pos):
        if pos<31:
            pos=pos+30
        else:
            pos=pos-31
        return pos

    def zero_minute(self):
        msg = self.pack_msg( self.CMD_ZERO, self.addr_min )
        self.send_msg( msg )

    def zero_hour(self):
        msg = self.pack_msg( self.CMD_ZERO, self.addr_hour )
        self.send_msg( msg )

    def goto_min(self, minutes):
        if minutes>60:
            return
        val = self.calc_min_pos(minutes)
        msg = self.pack_msg(self.CMD_GOTO, self.addr_min, val)
        self.send_msg( msg )

    def goto_hour(self, hour):
        msg = self.pack_msg(self.CMD_GOTO, self.addr_hour, hour)
        self.send_msg( msg )

    def goto_current_time(self):
        now = datetime.datetime.now()
        self.goto_hour(now.hour)
        self.goto_min(now.minute)

    def goto_time(self, hour, minute):
        self.goto_hour(hour)
        self.goto_min(minute)
