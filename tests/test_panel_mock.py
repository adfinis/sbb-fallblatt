"""This files contains tests for the panel_mock.py script"""

import struct
from sbb_fallblatt.panel_mock import parse_args, MockPanel

def test_args_parser():
    """Test the argument parser"""
    arguments = parse_args(["--start", "10", "--end", "16"])
    assert arguments.start == 10
    assert arguments.end == 16

def test_unpack_data():
    """Test the unpack function of the MockPanel class"""

    mockpanel = MockPanel(10, 16)
    data_struct = struct.pack("=B", 29)
    assert 29 == mockpanel.unpack(data_struct)

def test_pack_data():
    """Test the pack function of the MockPanel class"""
    mockpanel = MockPanel(10, 16)
    data_struct = mockpanel.pack(29)
    assert 29 == mockpanel.unpack(data_struct)
    assert 29 == struct.unpack("=B", data_struct)[0]
