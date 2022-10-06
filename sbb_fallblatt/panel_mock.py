"""This class is used to mock an sbb fallblatt panel"""

import os
import sys
import pty
import struct
import argparse
from sbb_fallblatt import sbb_rs485

class MockPanel():
    """This class is used to Mock an SBB Fallblatt Panel"""

    def __init__(self, start_address=10, end_address=64):
        self._stop = False
        self.start_address = start_address
        self.panel_length = len(list(range(self.start_address, end_address+1)))
        self.panel = sbb_rs485.PanelAlphanumControl([0,1])
        self.panel_data = [' ']*self.panel_length

        self.serial_int, self.serial_out = pty.openpty()

    def get_serial_port(self):
        """return the serial port name"""
        return os.ttyname(self.serial_out)

    def unpack(self, data):
        """Function to unpack content from a data struct"""
        return struct.unpack( "=B", data )[0]

    def pack(self, data):
        """Function to pack content into a data struct"""
        return struct.pack( "=B", data )

    def stop(self):
        """Stop the execution of the run loop"""
        self._stop = True

    def run(self):
        """Main mock loop"""

        # mainloop
        msg_start = False
        msg_type  = False
        addr      = False

        while not self._stop:

            data = os.read(self.serial_int, 1)

            if data == b'\xFF':
                msg_start = True
            if msg_start:
                if not msg_type:
                    if data == b'\xc0':
                        msg_type = 'set'
                    if data == b'\xd0':
                        msg_type = 'get'
                    if data == b'\xdf':
                        msg_type = 'serial'

                elif msg_type and not addr:
                    addr = data

                elif msg_type=='set' and addr:
                    char = self.panel.pos_to_str( [ self.unpack(data) ] )
                    paddr = self.unpack(addr) - (self.start_address)
                    self.panel_data[paddr] = char
                    msg_start = False
                    msg_type  = False
                    addr      = False

                if msg_type=='get' and addr:
                    paddr = self.unpack(addr) - self.start_address
                    if paddr <= len(self.panel_data):
                        os.write(self.serial_int,
                                bytes(self.panel.str_to_pos(self.panel_data[paddr])))
                    msg_start = False
                    msg_type  = False
                    addr      = False

                if msg_type=='serial' and addr:
                    paddr = self.unpack(addr) - self.start_address
                    os.write(self.serial_int, b"\x01\x88\x3f\x00")
                    msg_start = False
                    msg_type  = False
                    addr      = False

def parse_args(arguments):
    """Parse the CLI Arguments"""
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

    return parser.parse_args(arguments)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    mock_panel = MockPanel(args.start, args.end)
    print(mock_panel.get_serial_port)
    mock_panel.run()
