#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import time
import serial
import struct
import datetime

from pprint import pprint


class PanelControl:

    CMD_GOTO         = b'\xC0'
    CMD_ZERO         = b'\xC5'
    CMD_STEP         = b'\xC6'
    CMD_PULSE        = b'\xC7'
    CMD_READ_POS     = b'\xD0'
    CMD_READ_SERIAL  = b'\xDF'
    CMD_CHANGE_ADDR  = b'\xCE'


    def __init__( self, port="/dev/ttyUSB0" ):
        self.port = port
        self.break_time = 0.05


    def connect( self ):
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=19200
            )
        except:
            print("ERROR: Opening serial port failed")
            self.serial = False
            return


    def pack_msg( self, cmd, addr, value=False ):
        msg =  b"\xFF"
        msg += cmd
        msg += struct.pack( "=B", addr )
        if value is not False:
            msg += struct.pack( "=B", value )
        return msg


    def pack_msg_goto( self, addr, pos ):
        return self.pack_msg(
            self.CMD_GOTO,
            addr,
            pos
        )


    def set_break(self):
        self.serial.break_condition = True
        time.sleep(self.break_time)
        self.serial.break_condition = False


    def send_msg( self, msg ):
        if not self.serial:
            return
        self.set_break()
        self.serial.write( msg )


    def send_multiple( self, msgs, sleep_between=False):
        if not self.serial:
            return
        for msg in msgs:
            self.set_break()
            self.serial.write( msg )
            if sleep_between:
                time.sleep(0.003)


    def send_and_read( self, msg, ret_len ):
        self.send_msg( msg )
        data = self.serial.read( ret_len )
        return data


    def get_serial_number( self, addr ):
        msg = self.pack_msg(
            self.CMD_READ_SERIAL,
            addr
        )
        return self.send_and_read( msg, 4 )


    def get_position( self, addr ):
        msg = self.pack_msg(
            self.CMD_READ_POS,
            addr
        )
        try:
            pos_raw = self.send_and_read( msg, 1 )
            pos = struct.unpack( "=B", pos_raw )
            return pos[0]
        except struct.error:
            return -1


    def set_position(self, addr, pos):
        self.send_msg(
            self.pack_msg_goto(
                addr,
                pos
            )
        )


    def fill_list( self, lst, n, fill):
        return lst + [fill] * (n - len(lst))





class PanelAlphanumControl( PanelControl ):

    ALPHANUM_MAPPING = "abcdefghijklmnopqrstuvwxyz/-1234567890. "
    POS_BLANK        = 39

    def __init__(self, addresses, port="/dev/ttyUSB0" ):
        super().__init__(port)
        self.break_time=0.001
        self.addrs = addresses
        self.length = len(addresses)


    def str_to_pos(self, string):
        ret = []
        for c in string:
            pos = self.ALPHANUM_MAPPING.find(c.lower())
            if pos > -1:
                ret.append(pos)
        return ret


    def pos_to_str(self, pos):
        ret = ""
        for p in pos:
            ret += self.ALPHANUM_MAPPING[p]
        return ret


    def get_text(self):
        pos = []
        for addr in self.addrs:
            pos.append(
                self.get_position( addr )
            )
            self.serial.flushInput()
        return self.pos_to_str(pos)


    def pos_to_msg(self, pos):
        msg  = []
        addr_pos = 0
        for char in pos:
            msg.append(
                self.pack_msg_goto(
                    self.addrs[addr_pos],
                    char
                )
            )
            addr_pos+=1
        return msg


    def set_zero(self):
        pos = self.fill_list(
            [],
            self.length,
            self.POS_BLANK
        )
        msg = self.pos_to_msg(pos)
        self.send_multiple(msg)


    def set_text(self, text, fill=True):

        pos  = self.str_to_pos(text)
        pos = pos[:self.length]
        if fill:
            pos = self.fill_list(
                pos,
                self.length,
                self.POS_BLANK
            )

        msg = self.pos_to_msg(pos)
        self.send_multiple(msg)





class PanelClockControl( PanelControl ):

    def __init__(self, port="/dev/ttyUSB0", addr_hour=82, addr_min=29):
        super().__init__(port)
        self.addr_hour = addr_hour
        self.addr_min  = addr_min


    def calc_min_pos( self, pos ):
        if pos<31:
            pos = pos+30
        else:
            pos = pos-31
        return pos


    def calc_min_pos_rev( self, pos ):
        if pos>30:
            ret = pos-30
        else:
            ret = pos+31
        return ret


    def get_minute( self ):
        pos_raw = self.get_position( self.addr_min )
        return self.calc_min_pos_rev( pos_raw )


    def get_hour( self ):
        return self.get_position( self.addr_hour )


    def get_time( self ):
        hour   = self.get_hour()
        minute = self.get_minute()
        return hour,minute


    def set_zero( self ):
        msg = [
            self.build_set_hour_msg( 0 ),
            self.build_set_minute_msg( 0 )
        ]
        self.send_multiple( msg )


    def set_minute( self, minute ):
        if minute>60:
            return
        self.set_position(
            self.addr_min,
            self.calc_min_pos( minute )
        )


    def set_hour( self, hour ):
        if hour>23:
            return
        self.set_position(
            self.addr_hour,
            hour
        )


    def set_time( self, hour, minute ):
        self.set_hour(hour)
        self.set_minute(minute)


    def set_time_now( self ):
        now = datetime.datetime.now()
        self.set_time(now.hour, now.minute)
