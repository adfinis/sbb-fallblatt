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
        msg =  b"\xFF"
        msg += cmd
        msg += struct.pack("=B", addr)
        if value is not False:
            msg += struct.pack("=B", value)
        return msg


    def send_msg(self, msg):
        if not self.serial:
            return
        self.serial.send_break()
        self.serial.write(msg)


    def send_and_read(self, msg, ret_len):
        self.send_msg(msg)
        data = self.serial.read(ret_len)
        return data


    def get_serial_number(self, addr):
        msg = self.pack_msg(
            self.CMD_READ_SERIAL,
            addr
        )
        return self.send_and_read(msg, 4)


    def get_position(self, addr):
        msg = self.pack_msg(
            self.CMD_READ_POS,
            addr
        )
        pos_raw = self.send_and_read(msg, 1)
        pos = struct.unpack("=B", pos_raw)
        return pos[0]



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


    def calc_min_pos_rev(self, pos):
        if pos>30:
            ret = pos-30
        else:
            ret = pos+31
        return ret


    def get_minutes(self):
        pos_raw = self.get_position(self.addr_min)
        return self.calc_min_pos_rev(pos_raw)


    def get_hours(self):
        return self.get_position(self.addr_hour)


    def get_time(self):
        hh = self.get_hours()
        mm = self.get_minutes()
        return hh,mm


    def zero_minute(self):
        self.send_msg(
            self.pack_msg(
                self.CMD_ZERO,
                self.addr_min
            )
        )


    def zero_hour(self):
        self.send_msg(
            self.pack_msg(
                self.CMD_ZERO,
                self.addr_hour
            )
        )


    def goto_min(self, minutes):
        if minutes>60:
            return
        msg = self.pack_msg(
            self.CMD_GOTO,
            self.addr_min,
            self.calc_min_pos(
                minutes
            )
        )
        self.send_msg( msg )


    def goto_hour(self, hour):
        self.send_msg(
            self.pack_msg(
                self.CMD_GOTO,
                self.addr_hour,
                hour
            )
        )


    def goto_current_time(self):
        now = datetime.datetime.now()
        self.goto_hour(now.hour)
        self.goto_min(now.minute)


    def goto_time(self, hour, minute):
        self.goto_hour(hour)
        self.goto_min(minute)
