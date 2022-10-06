"""Test :class:`PanelAlphanumControl`"""

import time
from datetime import datetime
from threading import Thread
import pytest
from sbb_fallblatt import panel_mock
from sbb_fallblatt import sbb_rs485

class TestPanelAlphanumControl:
    """This class is used to test all functions from sbb_fallblatt.sbb_rs485.PanelAlphanumControl"""

    panel_mock = panel_mock.MockPanel(start_address=10, end_address=15)
    mock_thread = Thread(target=panel_mock.run, daemon=True)
    mock_thread.start()

    panel_addresses = list(range(10, 16))
    panel = sbb_rs485.PanelAlphanumControl(addresses=panel_addresses,
      port=panel_mock.get_serial_port()
    )
    panel.connect()

    def test_initialization(self):
        """Test that the panel is an instance of sbb_rs485.PanelAlphanumControl"""
        assert isinstance(self.panel, sbb_rs485.PanelAlphanumControl)

    def test_str_to_pos(self):
        """Test that the sbb_rs485.PanelAlphanumControl.str_to_pos function
        returns a list of positions of the character positions"""

        pos = self.panel.str_to_pos("test01")

        assert [19, 4, 18, 19, 37, 28] == pos

    def test_pos_to_str(self):
        """Test that the sbb_rs485.PanelAlphanumControl.pos_to_str function
        returns the string from a list character positions"""

        string = self.panel.pos_to_str([19, 4, 18, 19, 37, 28])
        assert "test01" == string

    def test_pos_to_msg(self):
        """Test that the sbb_rs485.PanelAlphanumControl.pos_to_msg function
        returns a list from the sent positions
        """
        msg = self.panel.pos_to_msg([19, 4, 18, 19, 37, 28])
        assert [b'\xff\xc0\n\x13', b'\xff\xc0\x0b\x04', b'\xff\xc0\x0c\x12',
                b'\xff\xc0\r\x13', b'\xff\xc0\x0e%', b'\xff\xc0\x0f\x1c'] == msg

    def test_set_zero(self):
        """Test if the panel correctly sets the zero value"""
        self.panel.set_zero()
        time.sleep(0.2)
        assert "      " == "".join(self.panel_mock.panel_data)

    def test_unconnected(self):
        """Test if the unconnected method fails if serial is not connected"""

    def test_get_set_text(self):
        """Test if the panel mock received the text correctly and replies with the correct text"""
        self.panel.set_text("test01")
        time.sleep(0.2)
        assert "test01" == "".join(self.panel_mock.panel_data)
        assert "test01" == self.panel.get_text()

class TestPanelControl:
    """This class is used to test all functions from sbb_fallblatt.sbb_rs485.PanelControl"""

    panel_mock = panel_mock.MockPanel(start_address=10, end_address=15)
    mock_thread = Thread(target=panel_mock.run, daemon=True)
    mock_thread.start()

    panel_addresses = list(range(10, 16))
    panel = sbb_rs485.PanelControl(port=panel_mock.get_serial_port())
    panel.connect()

    def test_no_serial_connection(self):
        """Test if the functions fail if serial is not connnected"""
        unconnected_panel = sbb_rs485.PanelAlphanumControl(addresses=self.panel_addresses,
          port=self.panel_mock.get_serial_port()
        )
        with pytest.raises(AttributeError,
                match=r"'PanelAlphanumControl' object has no attribute 'serial'"):
            unconnected_panel.set_zero()

    def test_panel_connect(self, capfd):
        """Failing test with an invalid serial port"""
        unconnected_panel = sbb_rs485.PanelControl("/dev/pts/nope"
        )
        unconnected_panel.connect()
        out, _err = capfd.readouterr()
        assert out == "ERROR: Opening serial port failed\n"
        assert unconnected_panel.serial is False

    def test_send_msg(self):
        """Test if the function returns if serial is not connected"""

        self.panel_mock.panel_data = [" " for i in self.panel_mock.panel_data]

        unconnected_panel = sbb_rs485.PanelControl("/dev/pts/nope"
        )
        unconnected_panel.connect()

        # The unconnected panel will return without sending data to the panel
        assert unconnected_panel.send_msg(b"\xff\xc0\x0a\x13") is None

        # The connected panel will send the data to the panel_mock where we can validate it
        assert self.panel.send_msg(b"\xff\xc0\x0a\x12") is None
        time.sleep(0.2)
        assert "".join(self.panel_mock.panel_data) == "s     "

    def test_send_multiple(self):
        """Test if the function returns if serial is not connected"""

        self.panel_mock.panel_data = [" " for i in self.panel_mock.panel_data]

        unconnected_panel = sbb_rs485.PanelControl("/dev/pts/nope"
        )
        unconnected_panel.connect()

        # The unconnected panel will return without sending data to the panel
        assert unconnected_panel.send_multiple([b"\xff\xc0\x0a\x13", b"\xff\xc0\x0b\x04"]) is None

        # The connected panel will send the data to the panel_mock where we can validate it
        assert self.panel.send_multiple([b"\xff\xc0\x0a\x13", b"\xff\xc0\x0b\x04"],
                sleep_between=True) is None
        time.sleep(0.2)
        assert "".join(self.panel_mock.panel_data) == "te    "

    def test_get_serial_number(self):
        """Test if the serial number is returned from the mock panel"""
        ret = self.panel.get_serial_number(10)

        assert ret == b"\x01\x88\x3f\x00"

    def test_get_position(self):
        """Test if the get_position function is working correctly"""
        self.panel_mock.panel_data = [" " for i in self.panel_mock.panel_data]

        ret_valid = self.panel.get_position(10)
        assert ret_valid == 39

    def test_set_position(self):
        """Test if the set_position is working correctly"""
        self.panel_mock.panel_data = [" " for i in self.panel_mock.panel_data]
        self.panel.set_position(11, 12)
        time.sleep(0.2)

        assert "".join(self.panel_mock.panel_data) == " m    "

class TestPanelClockControl:
    """This class is used to test all functions from sbb_fallblatt.sbb_rs485.PanelClockControl"""

    panel_mock = panel_mock.MockPanel(start_address=10, end_address=12)
    mock_thread = Thread(target=panel_mock.run, daemon=True)
    mock_thread.start()

    panel = sbb_rs485.PanelClockControl(addr_hour=10, addr_min=11, port=panel_mock.get_serial_port())
    panel.connect()

    """
    Something is really strange here. From time to time, the set_time() function is hanging:
      Traceback (most recent call last):
    File "/usr/lib/python3.10/threading.py", line 1016, in _bootstrap_inner
      self.run()
    File "/usr/lib/python3.10/threading.py", line 953, in run
      self._target(*self._args, **self._kwargs)
    File "/home/fuj/repos/github.com/adfinis/sbb-fallblatt/sbb_fallblatt/panel_mock.py", line 65, in run
      char = self.panel.pos_to_str( [ self.unpack(data) ] )
    File "/home/fuj/repos/github.com/adfinis/sbb-fallblatt/sbb_fallblatt/sbb_rs485.py", line 149, in pos_to_str
      ret += self.ALPHANUM_MAPPING[p]
    IndexError: string index out of range

    This might be a bug in panel_mock.
    """


    #def test_set_time_now(self):
    #    """Test if the time is set correctly from datetime.now()"""
    #    dt_now = datetime.now()
    #    self.panel.set_time_now()

    #    assert self.panel.get_hour() == dt_now.hour
    #    assert self.panel.get_minute() == dt_now.minute

    #def test_set_zero(self):
    #    """Test setting both modules to zero.
    #    TODO
    #    This test needs rework. Currently, the build_set_hour_msg and build_set_minute_msg
    #    are not even implemented. But this can easily be done with set_time() anyways..
    #    """
    #    #self.panel.set_zero()
    #    self.panel.set_time(0,0)
    #    assert self.panel.get_time() == (0, 0)
