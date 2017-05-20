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
    CMD_CHANGE_ADDR = b'\xCE'


    def __init__( self, port="/dev/ttyUSB0" ):
        self.port = port


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


    def send_msg( self, msg ):
        if not self.serial:
            return
        self.serial.send_break( 0.05 )
        self.serial.write( msg )


    def send_multiple( self, msgs, sleep_between=True):
        if not self.serial:
            return

        for msg in msgs:
            self.serial.send_break( 0.05 )
            self.serial.write( msg )
            #if sleep_between:
                #time.sleep(0.003)


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


    def build_set_minute_msg( self, minute ):
        return self.pack_msg(
            self.CMD_GOTO,
            self.addr_min,
            self.calc_min_pos(
                minute
            )
        )


    def build_set_hour_msg( self, hour ):
        return self.pack_msg(
            self.CMD_GOTO,
            self.addr_hour,
            hour
        )


    def set_zero( self ):
        msg = [
            self.build_set_hour_msg( 0 ),
            self.build_set_minute_msg( 0 )
        ]
        self.send_multiple( msg )


    def set_minute( self, minute ):
        if minute>60:
            return
        self.send_msg(
            self.build_set_minute_msg(
                minute
            )
        )

    def set_pos_test( self, pos ):
        self.send_msg(
            self.build_set_hour_msg(
                pos
            )
        )
    def set_addr_test( self, addr ):
        self.addr_hour = addr


    def set_hour( self, hour ):
        if hour>23:
            return
        self.send_msg(
            self.build_set_hour_msg(
                hour
            )
        )


    def set_time( self, hour, minute ):
        msg = [
            self.build_set_hour_msg( hour ),
            self.build_set_minute_msg( minute )
        ]
        self.send_multiple( msg, sleep_between=True )


    def set_time_now( self ):
        now = datetime.datetime.now()
        msg = [
            self.build_set_hour_msg(
                now.hour
            ),
            self.build_set_minute_msg(
                now.minute
            )
        ]
        self.send_multiple( msg )
